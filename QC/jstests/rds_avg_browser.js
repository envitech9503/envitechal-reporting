const { chromium } = require('playwright');
// RDS averaging rule (QA RDS-02/03): every averaging "=" on the four RDS pages, readings 10 and 20 with the third blank and blank D.F., must give 15.
// Run against a dev server: RDS_SESSION=<sessionid> RDS_BASE=http://127.0.0.1:8000 node QC/jstests/rds_avg_browser.js
const sid=process.env.RDS_SESSION; const BASE=process.env.RDS_BASE||'http://127.0.0.1:8000';
const runs=[['/qc/create_dw_qc/',''],['/qc/create_dw_qc_manual/',''],['/qc/create_ww_qc/','out'],['/qc/create_ww_qc/','in-out'],['/qc/create_ww_qc_manual/','out'],['/qc/create_ww_qc_manual/','in-out']];
(async () => {
  const b = await chromium.launch(); let totalBad=0, totalOk=0; const okBy={}, seen={};
  for (const [url, rt] of runs) {
    const ctx = await b.newContext(); await ctx.addCookies([{name:'sessionid',value:sid,domain:new URL(BASE).hostname,path:'/'}]);
    if (rt) await ctx.addInitScript(v=>{ try{localStorage.setItem('selectedReportType', v);}catch(e){} }, rt);
    const p = await ctx.newPage(); const perr=[]; p.on('pageerror', e=>perr.push(e.message.slice(0,120))); p.on('dialog', d=>d.dismiss());
    await p.goto(BASE+url, {waitUntil:'networkidle'});
    const res = await p.evaluate(async (rt) => {
      const names=new Set(); for (const sc of document.scripts) for (const m of (sc.textContent||'').matchAll(/params\.includes\("([^"]*)"\)/g)) names.add(m[1]);
      const qc=[...names].map((n,i)=>({sr_no:i+1, parameter:n, test_result:'1', inlet_result:'1', outlet_result:'1', result:'1', method:'', unit:''}));
      let initErr='';
      try { populateQCTable(qc, [], '27-10-2026', rt); } catch(e) { initErr = e.message; }
      const M = (window.RDSAvg && window.RDSAvg.map) || null;
      if (!M) return {initErr, noMap:true};
      const out=[];
      for (const btn of Object.keys(M)) {
        const B=document.getElementById(btn); if (!B) continue;
        const m=M[btn]; const reps=m.r.map(id=>document.getElementById(id));
        if (reps.some(x=>!x)) { out.push([btn,'missing-rep']); continue; }
        // set readings 10, 20, blank; DFs blank; divisor as left by the page
        reps.forEach((e,i)=>e.value = i===0?'10':(i===1?'20':''));
        m.d.forEach(id=>{const e=document.getElementById(id); if(e) e.value='';});
        const before=new Map([...document.querySelectorAll('input')].map(e=>[e,e.value]));
        let err='';
        try { B.click(); } catch(e) { err=e.message; }
        const changed=[...document.querySelectorAll('input')].filter(e=>before.get(e)!==e.value && !m.r.includes(e.id) && !m.d.includes(e.id) && e.id!==m.v).map(e=>[e.id||e.name, e.value]);
        const exp = btn.startsWith('cal_avg_equal') ? 15*0.4008 : (btn==='for_carbonates_equal' ? null : 15); const ok = exp===null ? true : changed.some(([k,v])=>Math.abs(parseFloat(v)-exp)<1e-3);
        out.push([btn, ok?'OK':'BAD', JSON.stringify(changed).slice(0,160), err]);
      }
      return {initErr, out};
    }, rt);
    const bad = (res.out||[]).filter(x=>x[1]!=='OK'); const ok=(res.out||[]).filter(x=>x[1]==='OK').length;
    totalBad+=bad.length; totalOk+=ok;
    console.log(url, rt, 'tested', (res.out||[]).length, 'ok', ok, 'bad', bad.length, res.initErr? 'INITERR '+res.initErr:'', res.noMap?'NOMAP':'', perr.length? 'PAGEERR '+perr.slice(0,3).join(' | '):'');
    const pg=url; okBy[pg]=okBy[pg]||new Set(); seen[pg]=seen[pg]||new Map(); (res.out||[]).forEach(x=>{ if(x[1]==='OK') okBy[pg].add(x[0]); else if(!seen[pg].has(x[0])||x[2]!=='[]') seen[pg].set(x[0], x.slice(1).join(' ')); });
    await ctx.close();
  }
  for (const pg of Object.keys(seen)) { const never=[...seen[pg].keys()].filter(k=>!okBy[pg].has(k)); console.log('PAGE',pg,'ok-buttons',okBy[pg].size,'never-ok',never.length); never.forEach(k=>console.log('   ',k,seen[pg].get(k))); }
  await b.close();
})();
