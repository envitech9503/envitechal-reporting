
       

$(document).ready(function() {

    new DataTable('#example', { order: [] });
      
    $("#result_type").on("change",function(){
  
      const value_range = $("#result_type").val()
      switch(value_range){
       case "PEQS":
           $(".SEQS,.NEQS").hide()    
           $(".PEQS").show()
       break;
       case "NEQS":
           $(".SEQS,.PEQS").hide()    
           $(".NEQS").show()    
       break;
       case "SEQS":
           $(".PEQS,.NEQS").hide()    
           $(".SEQS").show()    
       break;
      }
   })
  
   $("#result_type_1").on("change",function(){
      const value_range1 = $("#result_type_1").val()
      switch(value_range1){
          case "Residential Night":
              $(".res_day,.commer_day,.commer_night,.indus_day,.indus_night,.silence_day,.silence_night").hide()
              $(".res_night").show()
          break;
          case "Residential Day":
              $(".res_night,.commer_day,.commer_night,.indus_day,.indus_night,.silence_day,.silence_night").hide()
              $(".res_day").show()
          break;
          case "Commercial Day":
              $(".res_night,.res_day,.commer_night,.indus_day,.indus_night,.silence_day,.silence_night").hide()
              $(".commer_day").show()
          break;
          case "Commercial Night":
              $(".res_night,.commer_day,.res_day,.indus_day,.indus_night,.silence_day,.silence_night").hide()
              $(".commer_night").show()
          break;
          case "Industrial Day":
              $(".res_night,.commer_day,.commer_night,.res_day,.indus_night,.silence_day,.silence_night").hide()
              $(".indus_day").show()
          break;
          case "Industrial Night":
              $(".res_night,.commer_day,.commer_night,.indus_day,.res_day,.silence_day,.silence_night").hide()
              $(".indus_night").show()
          break;
          case "Silence Day":
              $(".res_night,.commer_day,.commer_night,.indus_day,.indus_night,.res_day,.silence_night").hide()
              $(".silence_day").show()
          break;
          case "Silence Night":
              $(".res_night,.commer_day,.commer_night,.indus_day,.indus_night,.silence_day,.res_day").hide()
              $(".silence_night").show()
          break;
  
      }
   })

   
      
  });

  $(document).ready(function () {
    $(".sideNavFormBtn").click(function () {
        $(".formMainDiv").toggle(function () {
            if ($(".formMainDiv").is(":visible")) {
                $(".wasteWaterDiv, .luxDiv, .noiseDiv, .ppbagDiv, .microDiv, .viscDiv, .ambientAirDiv, .waterwastediv2, .gasEmDiv, .detoxdiv,.nosie_monidiv").hide();
            }
        });
    });

    $(".DWaterBtn").click(function () {
        $(".DWaterDiv").toggle();
        $(".ambDiv, .wasteWaterDiv, .vehicEmDiv, .luxDiv, .noiseDiv, .ppbagDiv, .machineOilDiv, .microDiv, .viscDiv, .ambientAirDiv, .waterwastediv2, .gasEmDiv, .detoxdiv,.nosie_monidiv").hide();
    });

    $(".ambientBtn").click(function () {
        $(".ambDiv").toggle();
        $(".waterFromDiv, .wasteWaterDiv, .vehicEmDiv, .luxDiv, .noiseDiv, .ppbagDiv, .machineOilDiv, .microDiv, .viscDiv, .ambientAirDiv, .waterwastediv2, .gasEmDiv, .detoxdiv,.nosie_monidiv").hide();
    });

    $(".wasteWaterBtn").click(function () {
        $(".wasteWaterDiv").toggle();
        $(".waterFromDiv, .ambDiv, .vehicEmDiv, .luxDiv, .noiseDiv, .ppbagDiv, .machineOilDiv, .microDiv, .viscDiv, .ambientAirDiv, .waterwastediv2, .gasEmDiv, .detoxdiv,.nosie_monidiv").hide();
    });

    $(".vehicEmBtn").click(function () {
        $(".vehicEmDiv").toggle();
        $(".waterFromDiv, .ambDiv, .wasteWaterDiv, .luxDiv, .noiseDiv, .ppbagDiv, .machineOilDiv, .microDiv, .viscDiv, .ambientAirDiv, .waterwastediv2, .gasEmDiv, .detoxdiv,.nosie_monidiv").hide();
    });

    $(".luxBtn").click(function () {
        $(".luxDiv").toggle();
        $(".waterFromDiv, .ambDiv, .wasteWaterDiv, .vehicEmDiv, .noiseDiv, .ppbagDiv, .machineOilDiv, .microDiv, .viscDiv, .ambientAirDiv, .waterwastediv2, .gasEmDiv, .detoxdiv,.nosie_monidiv").hide();
    });

    $(".noiseBtn").click(function () {
        $(".noiseDiv").toggle();
        $(".waterFromDiv, .ambDiv, .wasteWaterDiv, .vehicEmDiv, .luxDiv, .ppbagDiv, .machineOilDiv, .microDiv, .viscDiv, .ambientAirDiv, .waterwastediv2, .gasEmDiv, .detoxdiv,.nosie_monidiv").hide();
    });

    $(".ppbagBtn").click(function () {
        $(".ppbagDiv").toggle();
        $(".waterFromDiv, .ambDiv, .wasteWaterDiv, .vehicEmDiv, .luxDiv, .noiseDiv, .machineOilDiv, .microDiv, .viscDiv, .ambientAirDiv, .waterwastediv2, .gasEmDiv, .detoxdiv,.nosie_monidiv").hide();
    });

    $(".machineOilBtn").click(function () {
        $(".machineOilDiv").toggle();
        $(".waterFromDiv, .ambDiv, .wasteWaterDiv, .vehicEmDiv, .luxDiv, .noiseDiv, .ppbagDiv, .microDiv, .viscDiv, .ambientAirDiv, .waterwastediv2, .gasEmDiv, .detoxdiv,.nosie_monidiv").hide();
    });

    // $(".microBtn").click(function () {
    //     $(".microDiv").toggle();
    //     $(".waterFromDiv, .ambDiv, .wasteWaterDiv, .vehicEmDiv, .luxDiv, .noiseDiv, .ppbagDiv, .machineOilDiv, .viscDiv, .ambientAirDiv, .waterwastediv2, .gasEmDiv").hide();
    // });
    $(".microBtn").click(function () {
        var ambientAirDiv = $(".microDiv");
        if (ambientAirDiv.is(":hidden")) {
            ambientAirDiv.show();
            $(".waterFromDiv, .ambDiv, .wasteWaterDiv, .vehicEmDiv, .luxDiv, .noiseDiv, .ppbagDiv, .machineOilDiv, .viscDiv, .ambientAirDiv, .waterwastediv2, .gasEmDiv, .detoxdiv,.nosie_monidiv").hide();
        } else {
            ambientAirDiv.hide();
        }
    });

    $(".viscBtn").click(function () {
        $(".viscDiv").toggle();
        $(".waterFromDiv, .ambDiv, .wasteWaterDiv, .vehicEmDiv, .luxDiv, .noiseDiv, .ppbagDiv, .machineOilDiv, .microDiv, .ambientAirDiv, .waterwastediv2, .gasEmDiv, .detoxdiv,.nosie_monidiv").hide()
  
    });
    $(".ambientAirBtn").click(function () {
        var ambientAirDiv = $(".ambientAirDiv");
        if (ambientAirDiv.is(":hidden")) {
            ambientAirDiv.show();
            $(".waterFromDiv, .ambDiv, .vehicEmDiv, .luxDiv, .noiseDiv, .ppbagDiv, .machineOilDiv, .microDiv, .viscDiv, .waterwastediv2, .gasEmDiv, .detoxdiv,.nosie_monidiv").hide();
        } else {
            ambientAirDiv.hide();
        }
    });
    
    // Water Waste 2 Button
    $(".waterwastebtn2").click(function () {
        var waterwastediv2 = $(".waterwastediv2");
        if (waterwastediv2.is(":hidden")) {
            waterwastediv2.show();
            $(".waterFromDiv, .ambDiv, .vehicEmDiv, .luxDiv, .noiseDiv, .ppbagDiv, .machineOilDiv, .microDiv, .viscDiv, .ambientAirDiv, .gasEmDiv, .detoxdiv,.nosie_monidiv").hide();
        } else {
            waterwastediv2.hide();
        }
    });
    
    // Gaseous Emission Button
    $(".gasEmBtn").click(function () {
        var gasEmDiv = $(".gasEmDiv");
        if (gasEmDiv.is(":hidden")) {
            gasEmDiv.show();
            $(".waterFromDiv, .ambDiv, .vehicEmDiv, .luxDiv, .noiseDiv, .ppbagDiv, .machineOilDiv, .microDiv, .viscDiv, .ambientAirDiv, .waterwastediv2, .detoxdiv,.nosie_monidiv").hide();
        } else {
            gasEmDiv.hide();
        }
    });
    $(".detoxbtn").click(function () {
        var detoxdiv = $(".detoxdiv");
        if (detoxdiv.is(":hidden")) {
            detoxdiv.show();
            $(".waterFromDiv, .ambDiv, .vehicEmDiv, .luxDiv, .noiseDiv, .ppbagDiv, .machineOilDiv, .microDiv, .viscDiv, .ambientAirDiv, .gasEmDiv, .waterwastediv2, ").hide();
        } else {
            detoxdiv.hide();
        }
    });
    $(".nosie_monibtn").click(function () {
        var nosie_monidiv = $(".nosie_monidiv");
        if (nosie_monidiv.is(":hidden")) {
            nosie_monidiv.show();
            $(".waterFromDiv, .ambDiv, .vehicEmDiv, .luxDiv, .noiseDiv, .ppbagDiv, .machineOilDiv, .microDiv, .viscDiv, .ambientAirDiv, .gasEmDiv, .waterwastediv2, .detoxdiv").hide();
        } else {
            nosie_monidiv.hide();
        }
    });
    $(".QC_DW_Btn").click(function () {
        var QC_DW_DIV = $(".QC_DW_DIV");
        if (QC_DW_DIV.is(":hidden")) {
            QC_DW_DIV.show();
            $(".waterFromDiv, .ambDiv, .vehicEmDiv, .luxDiv, .noiseDiv, .ppbagDiv, .machineOilDiv, .microDiv, .viscDiv, .ambientAirDiv, .gasEmDiv, .waterwastediv2, .detoxdiv, .QC_WW_DIV,..nosie_monidiv").hide();
        } else {
            QC_DW_DIV.hide();
        }
    });
    $(".QC_WW_Btn").click(function () {
        var QC_WW_DIV = $(".QC_WW_DIV");
        if (QC_WW_DIV.is(":hidden")) {
            QC_WW_DIV.show();
            $(".waterFromDiv, .ambDiv, .vehicEmDiv, .luxDiv, .noiseDiv, .ppbagDiv, .machineOilDiv, .microDiv, .viscDiv, .ambientAirDiv, .gasEmDiv, .waterwastediv2, .detoxdiv, .QC_DW_DIV").hide();
        } else {
            QC_WW_DIV.hide();
        }
    });
    
  })

  
  
  
//   var profOpt = document.querySelector(".prof-opt")
//   var profImg = document.querySelector(".prof-img")
  
//   profImg.addEventListener("click",()=>{
//       if(
//           
//           wasteWaterDiv.style.display = "none"
//           vehicEmDiv.style.display = "none"
//           luxDiv.style.display = "none"
//           noiseDiv.style.display = "none"
//           ppbagDiv.style.display = "none"
//           microDiv.style.display = "none"
//           viscDiv.style.display = "none"
//           ambientAirDiv.style.display = "none"
//           waterwastediv2.style.display = "none"
//           gasEmDiv.style.display = "none"
  
//       }
//       else{
//           
  
//       }
//   })
  
  
//   var ur_Div = document.querySelector(".user-right-div")
//   var ur_Btn = document.querySelector(".user-right-Btn")
  
//   ur_Btn.addEventListener("click",()=>{
//       if(
//           
//           formMainDiv.style.display = "none"
//           
//           wasteWaterDiv.style.display = "none"
//           vehicEmDiv.style.display = "none"
//           luxDiv.style.display = "none"
//           noiseDiv.style.display = "none"
//           ppbagDiv.style.display = "none"
//           machineOilDiv.style.display = "none"
//           microDiv.style.display = "none"
//           viscDiv.style.display = "none"
//           ambientAirDiv.style.display = "none"
//           waterwastediv2.style.display = "none"
//           gasEmDiv.style.display = "none"
  
//       }else{
//           
//       }
//   })
  
  
//   var formMainDiv = document.querySelector(".formMainDiv")
//   var sideNavFormBtn = document.querySelector(".sideNavFormBtn")
  
//   sideNavFormBtn.addEventListener("click",()=>{
//       if(formMainDiv.style.display == "none"){
//           formMainDiv.style.display = "block"
          
          
//           wasteWaterDiv.style.display = "none"
//           luxDiv.style.display = "none"
//           noiseDiv.style.display = "none"
//           ppbagDiv.style.display = "none"
//           microDiv.style.display = "none"
//           viscDiv.style.display = "none"
//           ambientAirDiv.style.display = "none"
//           waterwastediv2.style.display = "none"
//           gasEmDiv.style.display = "none"
          
  
//       }else{
//           formMainDiv.style.display = "none"
//       }
//   })
  
//   var empDiv = document.querySelector(".empDiv")
//   var empBtn = document.querySelector(".empBtn")
  
//   empBtn.addEventListener("click",()=>{
//       if(
//           
//           
//           formMainDiv.style.display = "none"
//           
//           wasteWaterDiv.style.display = "none"
//           vehicEmDiv.style.display = "none"
//           luxDiv.style.display = "none"
//           noiseDiv.style.display = "none"
//           microDiv.style.display = "none"
//           viscDiv.style.display = "none"
//           ambientAirDiv.style.display = "none"
//           waterwastediv2.style.display = "none"
//           gasEmDiv.style.display = "none"
  
          
//       }else{
//           
//       }
//   })
  
  
  
  
  
//   var waterFromBtn = document.querySelector(".DWaterBtn")
//   var waterFromDiv = document.querySelector(".DWaterDiv")
  
//   waterFromBtn.addEventListener("click",()=>{
//       if(waterFromDiv.style.display == "none"){
//           waterFromDiv.style.display = "block"
          
//           ambDiv.style.display = "none"
//           wasteWaterDiv.style.display = "none"
//           vehicEmDiv.style.display = "none"
//           luxDiv.style.display = "none"
//           noiseDiv.style.display = "none"
//           ppbagDiv.style.display = "none"
//           machineOilDiv.style.display = "none"
//           microDiv.style.display = "none"
//           viscDiv.style.display = "none"
//           waterwastediv2.style.display = "none"
//           ambientAirDiv.style.display = "none"
//           gasEmDiv.style.display = "none"
//       }else{
//           waterFromDiv.style.display = "none"
          
//   }
//   })
  
//   //ambient btn
  
//   var ambientBtn = document.querySelector(".ambientBtn")
//   var ambDiv = document.querySelector(".ambDiv")
  
//   ambientBtn.addEventListener("click",()=>{
//       if(ambDiv.style.display == "none"){
//           ambDiv.style.display = "block"
          
//           waterFromDiv.style.display = "none"
//           wasteWaterDiv.style.display = "none"
//           vehicEmDiv.style.display = "none"
//           luxDiv.style.display = "none"
//           noiseDiv.style.display = "none"
//           ppbagDiv.style.display = "none"
//           machineOilDiv.style.display = "none"
//           microDiv.style.display = "none"
//           viscDiv.style.display = "none"
//           ambientAirDiv.style.display = "none"
//           waterwastediv2.style.display = "none"
//           gasEmDiv.style.display = "none"
  
//       }else{
//           ambDiv.style.display = "none"
//   }
//   })
  
  
//   //waste water sludge btn 
  
//   var wasteWaterBtn = document.querySelector(".wasteWaterBtn")
//   var wasteWaterDiv = document.querySelector(".wasteWaterDiv")
  
//   wasteWaterBtn.addEventListener("click",()=>{
//       if(wasteWaterDiv.style.display == "none"){
//         wasteWaterDiv.style.display = "block"
          
//           waterFromDiv.style.display = "none"
//           ambDiv.style.display = "none"
//           waterFromDiv.style.display = "none"
//           vehicEmDiv.style.display = "none"
//           luxDiv.style.display = "none"
//           noiseDiv.style.display = "none"
//           ppbagDiv.style.display = "none"
//           machineOilDiv.style.display = "none"
//           microDiv.style.display = "none"
//           viscDiv.style.display = "none"
//           ambientAirDiv.style.display = "none"
//           waterwastediv2.style.display = "none"
//           gasEmDiv.style.display = "none"
  
//       }else{
//         wasteWaterDiv.style.display = "none"
//   }
//   })
  
//   //vehicular emission btn
  
//   var vehicEmBtn = document.querySelector(".vehicEmBtn")
//   var vehicEmDiv = document.querySelector(".vehicEmDiv")
  
//   vehicEmBtn.addEventListener("click",()=>{
//       if(vehicEmDiv.style.display == "none"){
//         vehicEmDiv.style.display = "block"
          
//           waterFromDiv.style.display = "none"
//           ambDiv.style.display = "none"
//           waterFromDiv.style.display = "none"
//           luxDiv.style.display = "none"
//           noiseDiv.style.display = "none"
//           wasteWaterDiv.style.display = "none"
//           ppbagDiv.style.display = "none"
//           machineOilDiv.style.display = "none"
//           microDiv.style.display = "none"
//           viscDiv.style.display = "none"
//           ambientAirDiv.style.display = "none"
//           waterwastediv2.style.display = "none"
//           gasEmDiv.style.display = "none"
  
//       }else{
//         vehicEmDiv.style.display = "none"
//   }
//   })
  
//   //Lux Btn
  
//   var luxBtn = document.querySelector(".luxBtn")
//   var luxDiv = document.querySelector(".luxDiv")
  
//   luxBtn.addEventListener("click",()=>{
//       if(luxDiv.style.display == "none"){
//         luxDiv.style.display = "block"
          
//           waterFromDiv.style.display = "none"
//           ambDiv.style.display = "none"
//           waterFromDiv.style.display = "none"
//           vehicEmDiv.style.display = "none"
//           noiseDiv.style.display = "none"
//           ppbagDiv.style.display = "none"
//           machineOilDiv.style.display = "none"
//           microDiv.style.display = "none"
//           viscDiv.style.display = "none"
//           ambientAirDiv.style.display = "none"
//           waterwastediv2.style.display = "none"
//           gasEmDiv.style.display = "none"
  
//       }else{
//         luxDiv.style.display = "none"
//   }
//   })
  
//   // noise analysis btn
  
//   var noiseBtn = document.querySelector(".noiseBtn")
//   var noiseDiv = document.querySelector(".noiseDiv")
  
//   noiseBtn.addEventListener("click",()=>{
//       if(noiseDiv.style.display == "none"){
//         noiseDiv.style.display = "block"
          
//           waterFromDiv.style.display = "none"
//           ambDiv.style.display = "none"
//           waterFromDiv.style.display = "none"
//           vehicEmDiv.style.display = "none"
//           luxDiv.style.display = "none"
//           ppbagDiv.style.display = "none"
//           machineOilDiv.style.display = "none"
//           microDiv.style.display = "none"
//           viscDiv.style.display = "none"
//           ambientAirDiv.style.display = "none"
//           waterwastediv2.style.display = "none"
//           gasEmDiv.style.display = "none"
  
//       }else{
//         noiseDiv.style.display = "none"
//   }
//   })
  
//   // packing poly bag
  
//   var ppbagBtn = document.querySelector(".ppbagBtn")
//   var ppbagDiv = document.querySelector(".ppbagDiv")
  
//   ppbagBtn.addEventListener("click",()=>{
//       if(ppbagDiv.style.display == "none"){
//         ppbagDiv.style.display = "block"
          
//           waterFromDiv.style.display = "none"
//           ambDiv.style.display = "none"
//           waterFromDiv.style.display = "none"
//           vehicEmDiv.style.display = "none"
//           luxDiv.style.display = "none"
//           noiseDiv.style.display = "none"
//           machineOilDiv.style.display = "none"
//           microDiv.style.display = "none"
//           ambientAirDiv.style.display = "none"
//           waterwastediv2.style.display = "none"
//           viscDiv.style.display = "none"
//           gasEmDiv.style.display = "none"
          
//       }else{
//         ppbagDiv.style.display = "none"
//   }
//   })
  
//   //machine oil 
  
//   var machineOilBtn = document.querySelector(".machineOilBtn")
//   var machineOilDiv = document.querySelector(".machineOilDiv")
  
//   machineOilBtn.addEventListener("click",()=>{
//       if(machineOilDiv.style.display == "none"){
//         machineOilDiv.style.display = "block"
          
//           waterFromDiv.style.display = "none"
//           ambDiv.style.display = "none"
//           waterFromDiv.style.display = "none"
//           vehicEmDiv.style.display = "none"
//           luxDiv.style.display = "none"
//           noiseDiv.style.display = "none"
//           ppbagDiv.style.display = "none"
//           microDiv.style.display = "none"
//           viscDiv.style.display = "none"
//           ambientAirDiv.style.display = "none"
//           waterwastediv2.style.display = "none"
//           gasEmDiv.style.display = "none"
  
          
//       }else{
//         machineOilDiv.style.display = "none"
//   }
//   })
  
//   //microbial analysis 
  
//   var microBtn = document.querySelector(".microBtn")
//   var microDiv = document.querySelector(".microDiv")
  
//   microBtn.addEventListener("click",()=>{
//       if(microDiv.style.display == "none"){
//         microDiv.style.display = "block"
          
//           waterFromDiv.style.display = "none"
//           ambDiv.style.display = "none"
//           waterFromDiv.style.display = "none"
//           vehicEmDiv.style.display = "none"
//           luxDiv.style.display = "none"
//           noiseDiv.style.display = "none"
//           ppbagDiv.style.display = "none"
//           machineOilDiv.style.display = "none"
//           viscDiv.style.display = "none"
//           ambientAirDiv.style.display = "none"
//           waterwastediv2.style.display = "none"
//           gasEmDiv.style.display = "none"
          
//       }else{
//         microDiv.style.display = "none"
//   }
//   })
  
//   //viscous liquid
  
//   var viscBtn = document.querySelector(".viscBtn")
//   var viscDiv = document.querySelector(".viscDiv")
  
//   viscBtn.addEventListener("click",()=>{
//       if(viscDiv.style.display == "none"){
//         viscDiv.style.display = "block"
          
//           waterFromDiv.style.display = "none"
//           ambDiv.style.display = "none"
//           waterFromDiv.style.display = "none"
//           vehicEmDiv.style.display = "none"
//           luxDiv.style.display = "none"
//           noiseDiv.style.display = "none"
//           ppbagDiv.style.display = "none"
//           machineOilDiv.style.display = "none"
//           microDiv.style.display = "none"
//           ambientAirDiv.style.display = "none"
//           waterwastediv2.style.display = "none"
//           gasEmDiv.style.display = "none"
          
//       }else{
//         viscDiv.style.display = "none"
//   }
//   })
  
  
  /// ambient air 2
  
  
//   var ambientAirBtn = document.querySelector(".ambientAirBtn")
//   var ambientAirDiv = document.querySelector(".ambientAirDiv")
  
//   ambientAirBtn.addEventListener("click",()=>{
//       if(ambientAirDiv.style.display == "none"){
//         ambientAirDiv.style.display = "block"
          
//           waterFromDiv.style.display = "none"
//           ambDiv.style.display = "none"
//           waterFromDiv.style.display = "none"
//           vehicEmDiv.style.display = "none"
//           luxDiv.style.display = "none"
//           noiseDiv.style.display = "none"
//           ppbagDiv.style.display = "none"
//           machineOilDiv.style.display = "none"
//           microDiv.style.display = "none"
//           viscDiv.style.display = "none"
//           waterwastediv2.style.display = "none"
//           gasEmDiv.style.display = "none"
          
//       }else{
//         ambientAirDiv.style.display = "none"
//   }
//   })
  
//   //water waste 2
  
//   var waterwastebtn2 = document.querySelector(".waterwastebtn2")
//   var waterwastediv2 = document.querySelector(".waterwastediv2")
  
//   waterwastebtn2.addEventListener("click",()=>{
//       if(waterwastediv2.style.display == "none"){
//         waterwastediv2.style.display = "block"
          
//           waterFromDiv.style.display = "none"
//           ambDiv.style.display = "none"
//           waterFromDiv.style.display = "none"
//           vehicEmDiv.style.display = "none"
//           luxDiv.style.display = "none"
//           noiseDiv.style.display = "none"
//           ppbagDiv.style.display = "none"
//           machineOilDiv.style.display = "none"
//           microDiv.style.display = "none"
//           viscDiv.style.display = "none"
//           ambientAirDiv.style.display = "none"
//           gasEmDiv.style.display = "none"
          
//       }else{
//         waterwastediv2.style.display = "none"
//   }
//   })
  
  
//   //Gaseous Emission
  
  
//   var gasEmBtn = document.querySelector(".gasEmBtn")
//   var gasEmDiv = document.querySelector(".gasEmDiv")
  
//   gasEmBtn.addEventListener("click",()=>{
//       if(gasEmDiv.style.display == "none"){
//         gasEmDiv.style.display = "block"
          
//           waterFromDiv.style.display = "none"
//           ambDiv.style.display = "none"
//           waterFromDiv.style.display = "none"
//           vehicEmDiv.style.display = "none"
//           luxDiv.style.display = "none"
//           noiseDiv.style.display = "none"
//           ppbagDiv.style.display = "none"
//           machineOilDiv.style.display = "none"
//           microDiv.style.display = "none"
//           viscDiv.style.display = "none"
//           ambientAirDiv.style.display = "none"
//           waterwastediv2.style.display = "none"
          
//       }else{
//         gasEmDiv.style.display = "none"
//   }
//   })
  
  
  //adding employe form
  
//   var addempBtn =document.querySelector(".addempBtn")
//   var addelemdiv=document.querySelector("#divforAddingelements")
//   addempBtn.addEventListener("click",()=>{
  
//     addelemdiv.innerHTML =""
      
      
//       var form = document.createElement("div")
//       form.classList.add('addemployeeform')
//       form.innerHTML =   `
//       <center>
//       <div class= "emplList">
//       <form action="" id="addemployeeform" class="w-9/12 border-2 border-gray-200 bg-gray-100 shadow-2xl rounded-xl" >
  
  
                      
//       <h1 class="m-10 text-3xl text-left">New Employee</h1>
//       <div class="flex flex-wrap">
//       <div class="w-full lg:w-6/12 px-4">
//         <div class="relative w-full mb-3">
//           <label class="block uppercase text-blueGray-600 text-xs font-bold mb-2" htmlfor="grid-password">
//             Full Name
//           </label>
//           <input type="text" class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" >
//         </div>
//       </div>
//       <div class="w-full lg:w-6/12 px-4">
//         <div class="relative w-full mb-3">
//           <label class="block uppercase text-blueGray-600 text-xs font-bold mb-2" htmlfor="grid-password">
//             Login Name
//           </label>
//           <input type="text" class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" >
//         </div>
//       </div>
//       <div class="w-full lg:w-6/12 px-4">
//         <div class="relative w-full mb-3">
//           <label class="block uppercase text-blueGray-600 text-xs font-bold mb-2" htmlfor="grid-password">
//             Email Address
//           </label>
//           <input type="email" class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" >
//         </div>
//       </div>
//       <div class="w-full lg:w-6/12 px-4">
//         <div class="relative w-full mb-3">
//           <label class="block uppercase text-blueGray-600 text-xs font-bold mb-2" htmlfor="grid-password">
//             CNIC NO
//           </label>
//           <input type="text" class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" >
//         </div>
//       </div>
//       <div class="w-full lg:w-6/12 px-4">
//           <div class="relative w-full mb-3">
//             <label class="block uppercase text-blueGray-600 text-xs font-bold mb-2" htmlfor="grid-password">
//               Mobile Number
//             </label>
//             <input type="text" class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" >
//           </div>
//         </div>
//         <div class="w-full lg:w-6/12 px-4">
//           <div class="relative w-full mb-3">
//             <label class="block uppercase text-blueGray-600 text-xs font-bold mb-2" htmlfor="grid-password">
//               Password
//             </label>
//             <input type="password" class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" >
//           </div>
//         </div>
//         <div class="w-full lg:w-6/12 px-4">
//           <div class="relative w-full mb-3">
//             <label class="block uppercase text-blueGray-600 text-xs font-bold mb-2" htmlfor="grid-password">
//               Re-Password
//             </label>
//             <input type="password" class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" >
//           </div>
//         </div>
//       <div class="w-full lg:w-12/12 px-4">
//           <div class="relative w-full mb-3">
//             <label class="block uppercase text-blueGray-600 text-xs font-bold mb-2" htmlfor="grid-password">
//               Address
//             </label>
//             <input type="text" class="border-0 px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150" >
//           </div>
//         </div>
        
//         <div class="w-full lg:w-12/12 px-4 pt-8 flex justify-center">
//           <div class="relative w-10/12 mb-3 ">
            
//             <input type="submit" class="border-0 cursor-pointer px-3 py-3 placeholder-blueGray-300 text-blueGray-600 bg-blue-400 rounded text-lg text-gray-200 shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150">
//           </div>
//         </div>
  
              
//     </div>
//     </form>
//     </div>
//     </center>
//                   `
//                   addelemdiv.appendChild(form)
     
      
//   })
  
  
//   //adding employee list table 
  
  
//   var emplistBtn = document.querySelector(".listempbtn")
//   var emplisttable = document.querySelector(".emListTable")
//   emplistBtn.addEventListener("click",()=>{
  
//     addelemdiv.innerHTML =""
//     var emplList = document.createElement("div")
//     emplList.classList.add('emplList')
//     emplList.innerHTML = `
  
//     <table id="example" class="empListTable border border-black " style="width:100%; "cellspacing=10 >
//     <thead>
//         <tr>
//             <th>Name</th>
//             <th>CNIC</th>
//             <th>MOBILE</th>
//             <th>Email</th>
//             <th>ADDRESS</th>
//             <th>Edit</th>
//             <th>Delete</th>
            
            
//         </tr>
//     </thead>
//     <tbody>
//         <tr>
//             <td>Tiger Nixon</td>
//             <td>4240425457780</td>
//             <td>0310228801</td>
//             <td>lab@envitechal.com</td>
//             <td>345, First Floor, Street-15, Block-3, Bahadurabad, Karachi.</td>
//             <td><button><i class="fa-solid fa-user-pen text-blue-600 text-xl cursor-pointer"></i></button></i></td>
//             <td><button><i class="fa-solid fa-trash text-red-600 text-xl cursor-pointer"></i></button></i></td>
//         </tr>
//         <tr>
//             <td>Saba Qadeer</td>
//             <td>423577889907654</td>
//             <td>0310228801</td>
//             <td>saba@envitechal.com</td>
//             <td>Envi Tech AL Lahore office</td>
//             <td><button><i class="fa-solid fa-user-pen text-blue-600 text-xl cursor-pointer"></i></button></i></td>
//             <td><button><i class="fa-solid fa-trash text-red-600 text-xl cursor-pointer"></i></button></i></td>
//         </tr>
//         <tr>
//             <td>Samia Gul</td>
//             <td>4240425457780</td>
//             <td>0310228801</td>
//             <td>ABC@ABC.COM</td>
//             <td>345, First Floor, Street-15, Block-3, Bahadurabad, Karachi.</td>
//             <td><button><i class="fa-solid fa-user-pen text-blue-600 text-xl cursor-pointer"></i></button></i></td>
//             <td><button><i class="fa-solid fa-trash text-red-600 text-xl cursor-pointer"></i></button></i></td>
//         </tr>
//         <tr>
//             <td>Sana Ashraf</td>
//             <td>4240425457780</td>
//             <td>0310228801</td>
//             <td>ABC@ABC.COM</td>
//             <td>345, First Floor, Street-15, Block-3, Bahadurabad, Karachi.</td>
//             <td><button><i class="fa-solid fa-user-pen text-blue-600 text-xl cursor-pointer"></i></button></i></td>
//             <td><button><i class="fa-solid fa-trash text-red-600 text-xl cursor-pointer"></i></button></i></td>
//         </tr>
//         <tr>
//             <td>Tiger Nixon</td>
//             <td>4240425457780</td>
//             <td>0310228801</td>
//             <td>ABC@ABC.COM</td>
//             <td>345, First Floor, Street-15, Block-3, Bahadurabad, Karachi.</td>
//             <td><button><i class="fa-solid fa-user-pen text-blue-600 text-xl cursor-pointer"></i></button></i></td>
//             <td><button><i class="fa-solid fa-trash text-red-600 text-xl cursor-pointer"></i></button></i></td>
//         </tr>
        
//     </tbody>
//     <tfoot>
        
//     </tfoot>
//   </table>
  
//     `
//       addelemdiv.appendChild(emplList)
//       var table = $('#example').DataTable({
//         responsive: true
//       })
//       .columns.adjust()
//   })
  
  
  
  
  
  
  ///addding drinking water form
  
//   var addDrinkFormBtn = document.querySelector(".addDrinkFormBtn")
//   var addelemdiv = document.querySelector("#divforAddingelements")
  
//   addDrinkFormBtn.addEventListener("click",()=>{
//         addelemdiv.innerHTML = " "
//         var DrinkWaterFrom = document.createElement("div")
//         DrinkWaterFrom.classList.add('drinkingWaterFormMain')
//         DrinkWaterFrom.innerHTML =
//         `
        
       
        
        
//         `
//         addelemdiv.appendChild(DrinkWaterFrom)
//   })
  
//   // drinking water list
//   var ListDrinkBtn =  document.querySelector(".ListDrinkBtn")
  
  
//   ListDrinkBtn.addEventListener("click",()=>{
//     addelemdiv.innerHTML =" "
//     var drinkListForm = document.createElement("div")
//     drinkListForm.classList.add("drinklistform")
//     drinkListForm.innerHTML =  `
//     <form action="" class="flex flex-col justify-around  w-11/12 mt-10 ">
//     <h1 class="text-center mt-10 text-3xl py-16">List Drinking Water</h1>
//     <div class="flex justify-between">
//         <div class="flex flex-col">
//             <label class="font-bold text-lg" for="">Date From</label>
//             <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="">
//         </div>
//         <div class="flex flex-col">
//             <label class="font-bold text-lg" for="">Date To</label>
//             <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
//         </div>
//         <div class="flex flex-col">
//             <label class="font-bold text-lg" for="">Lab report No</label>
//             <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//         </div>
//     </div>
//     <div class="flex justify-between mt-10">
//         <div class="flex flex-col">
//             <label class="font-bold text-lg" for="">Invoice Bill No</label>
//             <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
//         </div>
//         <div class="flex flex-col">
//             <label class="font-bold text-lg" for="">Report To</label>
//             <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//         </div>
//         <div class="flex flex-col">
//             <label class="font-bold text-lg" for="">Attention</label>
//             <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//         </div>
//     </div>
//     <div class="flex justify-between mt-10">
//         <div class="flex flex-col">
//             <label class="font-bold text-lg" for="">Email Address</label>
//             <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;"  type="text" >
//         </div>
//         <div class="flex flex-col">
//             <label class="font-bold text-lg" for="">Test ID</label>
//             <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;" type="text" >
//         </div>
        
//     </div>
//     <div class="flex flex-col justify-center items-center mt-16 w-full">
            
//         <input class="  h-10 w-96 rounded text-lg bg-blue-500 text-white hover:bg-blue-400 cursor-pointer w-8/12 " type="submit" >
//     </div>
//   </form>
    
    
    
    
//     `
//         addelemdiv.appendChild(drinkListForm)
  
//   })
  
//   ///adding gaseous emission form
  
  
  
  
//   /// List Gaseous Emission 
  
//   var addGaseousListBtn = document.querySelector(".addGaseousListBtn")
  
//   addGaseousListBtn.addEventListener("click",()=>{
//       addelemdiv.innerHTML = " "
//       var gaseousList = document.createElement("div")
//       gaseousList.classList.add("gaseousListDiv")
//       gaseousList.innerHTML = `
//       <div class="w-full flex justify-center items-center  h-11/12">
//       <form action="" class="flex flex-col justify-around  w-11/12 mt-10">
//           <h1 class="text-center mt-10 text-3xl py-16">List Gaseous Emission</h1>
//           <div class="flex justify-between">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date From</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Lab report No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Invoice Bill No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Report To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Attention</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Email Address</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;"  type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Test ID</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;" type="text" >
//               </div>
              
//           </div>
//           <div class="flex flex-col justify-center items-center mt-16 w-full">
                  
//               <input class="  h-10 w-96 rounded text-lg bg-blue-500 text-white hover:bg-blue-400 cursor-pointer w-8/12 " type="submit" >
//           </div>
//         </form>
//   </div>
  
//       `
//       addelemdiv.appendChild(gaseousList)
//   })
  
  
//   ///adding ambient air form
  
//   var ambientAirFormBtn = document.querySelector(".ambientAirFormBtn")
//   ambientAirFormBtn.addEventListener("click",()=>{
//       addelemdiv.innerHTML = ""
//       var ambientform = document.createElement("div")
//       ambientform.classList.add("ambientform")
//       ambientform.innerHTML=`
      
      
  
//       `
  
//       addelemdiv.appendChild(ambientform)
//   })
  
  
//   //ambient Air List 
  
//   var ambientAirList = document.querySelector(".ambientAirList")
  
//   ambientAirList.addEventListener("click",()=>{
//       addelemdiv.innerHTML = " "
//       var ambientAirList = document.createElement("div")
//       ambientAirList.classList.add("ambientAirListDiv")
//       ambientAirList.innerHTML = `
//       <div class="w-full flex justify-center items-center  h-11/12">
//       <form action="" class="flex flex-col justify-around  w-11/12 mt-10">
//           <h1 class="text-center mt-10 text-3xl py-16">List Of Ambient Air</h1>
//           <div class="flex justify-between">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date From</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Lab report No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Invoice Bill No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Report To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Attention</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Email Address</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;"  type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Test ID</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;" type="text" >
//               </div>
              
//           </div>
//           <div class="flex flex-col justify-center items-center mt-16 w-full">
                  
//               <input class="  h-10 w-96 rounded text-lg bg-blue-500 text-white hover:bg-blue-400 cursor-pointer w-8/12 " type="submit" >
//           </div>
//         </form>
//   </div>
  
//       `
//       addelemdiv.appendChild(ambientAirList)
//   })
   
  
//   //adding waste water sludge form
  
//   var wasteWatewrSludgeBtn = document.querySelector(".wasteWatewrSludgeBtn")
//   var addelemdiv = document.querySelector("#divforAddingelements")
  
//   wasteWatewrSludgeBtn.addEventListener("click",()=>{
//         addelemdiv.innerHTML = " "
//         var wasteWaterSludgediv = document.createElement("div")
//         wasteWaterSludgediv.classList.add('wasteWatersludge')
//         wasteWaterSludgediv.innerHTML =
//           `
//           <div class="wasteWatersludge h-full w-full flex flex-col items-center ">
                          
  
//           <form action="" class="flex flex-col justify-around w-11/12 mt-10 ">
//               <h1 class="text-center mt-10 text-3xl py-16">Waste Water Sludge Form</h1>
//               <div class="flex justify-between">
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Lab Report No</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
//                   </div>
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Invoice Bill No</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//                   </div>
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Reporting Date</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
//                   </div>
//               </div>
//               <hr class="broder border-black mt-10">
  
//               <div class="flex justify-between mt-4">
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Report To :</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
//                   </div>
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Address</label>
//                       <input class="border-2 border-black p-2 h-10 rounded text-lg" style="width: 35rem;" type="text" >
//                   </div>
                  
                  
//               </div>
  
//               <div class="flex justify-between mt-4">
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Attention</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
//                   </div>
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Email</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
//                   </div>
//               </div>
  
//               <hr class="broder border-black mt-10">
  
//               <div class="flex justify-between mt-4">
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Sample ID</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="${currentDate}">
//                   </div>
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Sample Collection Date</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="date" >
//                   </div>
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Sample Description</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="Wastewater Sludge">
//                   </div>
//               </div>
  
//               <div class="flex justify-between mt-4">
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Sample Type</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="Semi solid - Grab Sample">
//                   </div>
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Sample Collected By</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="Envi Tech AL">
//                   </div>
//                   <div class="flex flex-col ">
//                       <label class="font-bold text-lg" for="">Date of Analysis From</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="date" >
//                   </div>
//               </div>
  
//               <div class="flex justify-between mt-4">
                  
//                   <div class="flex flex-col ">
//                       <label class="font-bold text-lg" for="">Test Description</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 79.5rem;" type="text" value="Heavy Metals Testing in Sludge (13 Metals)">
//                   </div>
                  
//               </div>
//               <hr class="broder border-black mt-10">
  
  
  
//               <div class="w-full flex flex-col justify-center">
//                   <table id="" class=" water-form-table border-collapse border-2 border-gray-700 mt-10 " cellspacing="15">
//                       <thead>
//                           <tr>
//                               <th>Sr.#</th>
//                               <th>Parameter/Analytes Description</th>
//                               <th>Methods</th>
//                               <th>Unit</th>
//                               <th>Test Result</th>
                              
                              
                              
//                           </tr>
//                       </thead>
//                       <tbody class="">
//                           <tr class="text-center border h-16">
//                               <td>01</td>
//                               <td>Cadmium (Cd)</td>
//                               <td>*APHA 3111- B</td>
//                               <td>mg/Kg</td>
//                               <td><input class="border-2 border-black w-72" type="text"></td>
                              
//                           </tr>
//                           <tr class="text-center border h-16">
//                               <td>02</td>
//                               <td>Copper (Cu)</td>
//                               <td>*APHA 3111- B</td>
//                               <td>mg/Kg</td>
//                               <td><input class="border-2 border-black w-72" type="text"></td>
                              
//                           </tr>
//                           <tr class="text-center border h-16">
//                               <td>03</td>
//                               <td>Iron (Fe)</td>
//                               <td>*APHA 3111- B</td>
//                               <td>mg/Kg</td>
//                               <td><input class="border-2 border-black w-72" type="text"></td>
                              
//                           </tr>
//                           <tr class="text-center border h-16">
//                               <td>04</td>
//                               <td>Boron (B)</td>
//                               <td>HACH 8025</td>
//                               <td>mg/Kg</td>
//                               <td><input class="border-2 border-black w-72" type="text"></td>
                              
//                           </tr>
//                           <tr class="text-center border h-16">
//                               <td>05</td>
//                               <td>Lead (Pb)</td>
//                               <td>APHA 3111- B</td>
//                               <td>mg/Kg</td>
//                               <td><input class="border-2 border-black w-72" type="text"></td>
                              
//                           </tr>
//                           <tr class="text-center border h-16">
//                               <td>06</td>
//                               <td>Mercury (Hg)</td>
//                               <td>*APHA 3112- B</td>
//                               <td>mg/Kg</td>
//                               <td><input class="border-2 border-black w-72" type="text"></td>
                              
//                           </tr>
//                           <tr class="text-center border h-16">
//                               <td>07</td>
//                               <td>Selenium (Se)</td>
//                               <td>*APHA 3114- B</td>
//                               <td>mg/Kg</td>
//                               <td><input class="border-2 border-black w-72" type="text"></td>
                              
//                           </tr>
//                           <tr class="text-center border h-16">
//                               <td>08</td>
//                               <td>Silver (Ag)</td>
//                               <td>*APHA 3111- B</td>
//                               <td>mg/Kg</td>
//                               <td><input class="border-2 border-black w-72" type="text"></td>
                              
//                           </tr>
//                           <tr class="text-center border h-16">
//                               <td>09</td>
//                               <td>Nickel (Ni)</td>
//                               <td>*APHA 3111- B</td>
//                               <td>mg/Kg</td>
//                               <td><input class="border-2 border-black w-72" type="text"></td>
                              
//                           </tr>
//                           <tr class="text-center border h-16">
//                               <td>10</td>
//                               <td>Zinc (Zn)</td>
//                               <td>*APHA 3111- B</td>
//                               <td>mg/Kg</td>
//                               <td><input class="border-2 border-black w-72" type="text"></td>
                              
//                           </tr>
//                           <tr class="text-center border h-16">
//                               <td>11</td>
//                               <td>Arsenic (As)</td>
//                               <td>*APHA 3114- B</td>
//                               <td>mg/Kg</td>
//                               <td><input class="border-2 border-black w-72" type="text"></td>
                              
//                           </tr>
//                           <tr class="text-center border h-16">
//                               <td>12</td>
//                               <td>Manganese (Mn)</td>
//                               <td>*APHA 3111- B</td>
//                               <td>mg/Kg</td>
//                               <td><input class="border-2 border-black w-72" type="text"></td>
                              
//                           </tr>
//                           <tr class="text-center border h-16">
//                               <td>13</td>
//                               <td>Chromium</td>
//                               <td>*APHA 3111- B</td>
//                               <td>mg/Kg</td>
//                               <td><input class="border-2 border-black w-72" type="text"></td>
                              
                          
//                       </tbody>
//                   </table>
  
//                   <hr class="broder border-black mt-10">
  
//                   <div class="flex justify-between mt-4">
//                       <div class="flex flex-col">
//                           <label class="font-bold text-lg" for="">Conclusion</label>
//                           <textarea class="border-2 border-black w-96 rounded " name="" id="" cols="30" rows="3"></textarea>
//                       </div>
                          
//                   </div>
  
//                       <h2 class="py-2 font-bold">LEGENDS</h2>
                  
                  
  
                      
//                           <table class="w-full border-2 border-black">
//                               <tr class="bg-gray-200">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>Test Results = M</span></td>
//                               </tr>
//                               <tr class="">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>*APHA Standard Methods for Examination of water & wastewater 23rd Edition (2017).</span></td>
//                               </tr>
//                               <tr class="bg-gray-200">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>SEQS Limits = Sindh Environmental Quality Standard (Reference: SEQS 2016).</span></td>
//                               </tr>
//                               <tr class="">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>PEQS Limits = Punjab Environmental Quality Standard</span></td>
//                               </tr>
//                               <tr class="bg-gray-200">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>NEQS Limits = National Environmental Quality Standard</span></td>
//                               </tr>
//                               <tr class="">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>1=SEQS for Municipal & Liquid Industrial Effluent into inland waters.</span></td>
//                               </tr>
//                               <tr class="bg-gray-200">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>2= SEQS for Municipal & Liquid Industrial Effluent into Sewage Treatment.</span></td>
//                               </tr>
//                               <tr class="">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>3=SEQS for Municipal & Liquid Industrial Effluent into Sea.</span></td>
//                               </tr>
//                               <tr class="bg-gray-200">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>** Discharge Concentration at or below Sea Concentration (SC).</span></td>
//                               </tr>
//                               <tr class="">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>M = Meet SEQS-2016 requirements.</span></td>
//                               </tr>
//                               <tr class="bg-gray-200">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>F = Below SEQS-2016 requirements.</span></td>
//                               </tr>
//                               <tr class="">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>N.D. = Not Detected.</span></td>
//                               </tr>
//                               <tr class="bg-gray-200">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>N.A = Not Available</span></td>
//                               </tr>
//                               <tr class="">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>Customer Requirement: N.A</span></td>
//                               </tr>
                              
//                           </table>
  
//                           <div class="flex flex-col justify-between mt-6">
//                               <div class="flex flex-col">
//                                   <label class="font-bold text-lg" for="">Edit Note</label>
//                                   <input class="border-2 border-black p-2 h-10 rounded text-lg" style="width: 79rem;" type="text" >
//                               </div>
//                               <div class="flex flex-col mt-4">
//                                   <label class="font-bold text-lg" for="">Custom Legend (if any):</label>
//                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" value="Drinking-Water-test as per SEQS-2016">
//                               </div>
                              
//                           </div>
  
//                           <div class="flex justify-between mt-6">
//                               <div class="flex flex-col">
//                                   <label class="font-bold text-lg" for=""> Doc. Controller 1:</label>
//                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="ETAL-LAB-708-FF-04">
//                               </div>
//                               <div class="flex flex-col">
//                                   <label class="font-bold text-lg" for="">Doc. Controller 2:</label>
//                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="Issue Date: 15-05-22">
//                               </div>
//                               <div class="flex flex-col">
//                                   <label class="font-bold text-lg" for="">Doc. Controller 3:</label>
//                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="Issue No 01">
//                               </div>
//                           </div>
  
//                           <div class="h-32  mt-8 flex justify-center items-center">
//                              <div class="space-x-8">
//                               <button class="bg-blue-600 h-12 w-60 rounded shadow-2xl text-white hover:bg-blue-500 "><i class="fa-solid fa-download pr-4  "></i>Save & Add New</button>
//                               <button class="h-12 bg-green-500 rounded  shadow-2xl w-60 hover:bg-green-400 text-white"><i class="fa-solid fa-file pr-4"></i>Save & View Report</button>
//                              </div>
//                           </div>
  
                   
//                   </div>
  
                  
  
//           </form>
//           <section class="bg-gray-900 h-20 flex justify-center items-center w-full ">
//                     <div class="">
//                           <p class="text-lg text-gray-300">© Copyright 2023 EnviTechAl. All Rights Reserved.</p>
//                           <p></p>
//                     </div>
//                   </section>
          
//       </div>
//           `
//         addelemdiv.appendChild(wasteWaterSludgediv)
//   })
  
  
//   //waste water sludge List
  
//   var wasteWaterSludgeListBtn = document.querySelector(".wasteWaterSludgeListBtn")
  
//   wasteWaterSludgeListBtn.addEventListener("click",()=>{
//       addelemdiv.innerHTML = " "
//       var wasteWaterSludgeListBtn = document.createElement("div")
//       wasteWaterSludgeListBtn.classList.add("wasteWaterSludgeListBtnDiv")
//       wasteWaterSludgeListBtn.innerHTML = `
//       <div class="w-full flex justify-center items-center  h-11/12">
//       <form action="" class="flex flex-col justify-around  w-11/12 mt-10">
//           <h1 class="text-center mt-10 text-3xl py-16">List Of Waste Water Sludge</h1>
//           <div class="flex justify-between">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date From</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Lab report No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Invoice Bill No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Report To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Attention</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Email Address</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;"  type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Test ID</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;" type="text" >
//               </div>
              
//           </div>
//           <div class="flex flex-col justify-center items-center mt-16 w-full">
                  
//               <input class="  h-10 w-96 rounded text-lg bg-blue-500 text-white hover:bg-blue-400 cursor-pointer w-8/12 " type="submit" >
//           </div>
//         </form>
//   </div>
  
//       `
//       addelemdiv.appendChild(wasteWaterSludgeListBtn)
//   })
  
  
//   ///adding vehicular Emission form
  
//   var vehicularEmisFormBtn = document.querySelector(".vehicularEmisFormBtn")
//   var addelemdiv = document.querySelector("#divforAddingelements")
  
//   vehicularEmisFormBtn.addEventListener("click",()=>{
//         addelemdiv.innerHTML = " "
//         var vehicularemisDiv = document.createElement("div")
//         vehicularemisDiv.classList.add('vehicularemisDiv')
//         vehicularemisDiv.innerHTML =
//           `
          
//           `
//         addelemdiv.appendChild(vehicularemisDiv)
//   })
  
//   //vehicular emission List
  
//   var vehicularemisListBtn = document.querySelector(".vehicularemisListBtn")
  
//   vehicularemisListBtn.addEventListener("click",()=>{
//       addelemdiv.innerHTML = " "
//       var vehicularemisList = document.createElement("div")
//       vehicularemisList.classList.add("vehicularemisListDiv")
//       vehicularemisList.innerHTML = `
//       <div class="w-full flex justify-center items-center  h-11/12">
//       <form action="" class="flex flex-col justify-around  w-11/12 mt-10">
//           <h1 class="text-center mt-10 text-3xl py-16">List Of Vehicular Emission</h1>
//           <div class="flex justify-between">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date From</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Lab report No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Invoice Bill No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Report To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Attention</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Email Address</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;"  type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Test ID</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;" type="text" >
//               </div>
              
//           </div>
//           <div class="flex flex-col justify-center items-center mt-16 w-full">
                  
//               <input class="  h-10 w-96 rounded text-lg bg-blue-500 text-white hover:bg-blue-400 cursor-pointer w-8/12 " type="submit" >
//           </div>
//         </form>
//   </div>
  
//       `
//       addelemdiv.appendChild(vehicularemisList)
//   })
  
//   // lux analysis form 
  
//   var luxAnalysisFormBtn = document.querySelector(".luxAnalysisFormBtn")
//   var addelemdiv = document.querySelector("#divforAddingelements")
  
//   luxAnalysisFormBtn.addEventListener("click",()=>{
//         addelemdiv.innerHTML = " "
//         var luxFormDiv = document.createElement("div")
//         luxFormDiv.classList.add('luxFormDiv')
//         luxFormDiv.innerHTML =
//           `
          
//           `
//         addelemdiv.appendChild(luxFormDiv)
//   })
  
//   //lux analysis list
  
//   var luxAnalysisListBtn = document.querySelector(".luxAnalysisListBtn")
  
//   luxAnalysisListBtn.addEventListener("click",()=>{
//       addelemdiv.innerHTML = " "
//       var luxanalysisList = document.createElement("div")
//       luxanalysisList.classList.add("luxanalysisListDiv")
//       luxanalysisList.innerHTML = `
//       <div class="w-full flex justify-center items-center  h-11/12">
//       <form action="" class="flex flex-col justify-around  w-11/12 mt-10">
//           <h1 class="text-center mt-10 text-3xl py-16">List Of Lux Analysis</h1>
//           <div class="flex justify-between">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date From</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Lab report No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Invoice Bill No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Report To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Attention</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Email Address</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;"  type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Test ID</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;" type="text" >
//               </div>
              
//           </div>
//           <div class="flex flex-col justify-center items-center mt-16 w-full">
                  
//               <input class="  h-10 w-96 rounded text-lg bg-blue-500 text-white hover:bg-blue-400 cursor-pointer w-8/12 " type="submit" >
//           </div>
//         </form>
//   </div>
  
//       `
//       addelemdiv.appendChild(luxanalysisList)
//   })
  
//   //Noise Analysis Form
  
//   var noiseAnalysisFormBtn = document.querySelector(".noiseAnalysisFormBtn")
//   var addelemdiv = document.querySelector("#divforAddingelements")
  
//   noiseAnalysisFormBtn.addEventListener("click",()=>{
//         addelemdiv.innerHTML = " "
//         var noiseAnalysisFormDiv = document.createElement("div")
//         noiseAnalysisFormDiv.classList.add('noiseAnalysisFormDiv')
//         noiseAnalysisFormDiv.innerHTML =
//           `
//           <div class="noiseAnalysis h-full w-full flex flex-col items-center ">
                          
  
//                           <form action="" class="flex flex-col justify-around w-11/12 mt-10 ">
//                               <h1 class="text-center mt-10 text-3xl py-16">Noise Analysis</h1>
//                               <div class="flex justify-between">
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Lab Report No</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Invoice Bill No</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Reporting Date</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
//                                   </div>
//                               </div>
//                               <hr class="broder border-black mt-10">
                  
//                               <div class="flex justify-between mt-4">
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Report To :</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Address</label>
//                                       <input class="border-2 border-black p-2 h-10 rounded text-lg" style="width: 35rem;" type="text" >
//                                   </div>
                                  
                                  
//                               </div>
                  
//                               <div class="flex justify-between mt-4">
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Attention</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Email</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
//                                   </div>
//                               </div>
                  
//                               <hr class="broder border-black mt-10">
                  
//                               <div class="flex justify-between mt-4">
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Test ID</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="${currentDate}">
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Test Performed Date </label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="date">
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Test Type</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="Noise Analysis">
//                                   </div>
//                               </div>
                  
//                               <div class="flex justify-between mt-4">
                                  
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Test Performed By</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="Envi Tech AL">
//                                   </div>
//                                   <div class="flex flex-col ">
//                                       <label class="font-bold text-lg" for="">Test Description</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="Noise Analysis as per SEQS-2016">
//                                   </div>
//                                   <div class="flex flex-col ">
//                                       <label class="font-bold text-lg" for="">Types</label>
//                                       <select class="border-2 border-black p-2 h-10 w-96 rounded text-lg " style="width: 24rem;" name="" id="">
//                                           <option value="">Residential (Day)</option>
//                                           <option value="">Residential (Night)</option>
//                                           <option value="">Commercial (Day)</option>
//                                           <option value="">Commercila (Night)</option>
//                                           <option value="">Industrial (Day)</option>
//                                           <option value="">Industrial (Night)</option>
//                                           <option value="">Silence Zone (Day)</option>
//                                           <option value="">Silence Zone (Night)</option>
//                                       </select>
//                                   </div>
//                               </div>
                  
                              
//                               <hr class="broder border-black mt-10">
                  
                  
                  
//                               <div class="w-full flex flex-col justify-center">
//                                   <table id="" class=" water-form-table border-collapse border-2 border-gray-700 mt-10 " cellspacing="15">
//                                       <thead>
//                                           <tr>
//                                               <th>Sr.#</th>
//                                               <th>Parameter/Analytes Description</th>
//                                               <th>Method</th>
//                                               <th>Unit</th>
//                                               <th>Test Result</th>
//                                               <th><select class="h-8 text-center w-36 font-bold">        
//                                                   <option value="SEQS">SEQS Limits</option>
//                                                   <option value="PEQS">PEQS Limits</option>
//                                                   <option value="NEQS">NEQS Limits</option>
                                                  
//                                              </select></th>
                                              
                                              
                                              
//                                           </tr>
//                                       </thead>
//                                       <tbody class="">
//                                           <tr class="text-center border h-16">
//                                               <td>01</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
//                                               <td>ASTM E1686-16</td>
//                                               <td>dB</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
//                                               <td>65</td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>02</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>ASTM E1686-16</td>
//                                               <td>dB</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>65</td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>03</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>ASTM E1686-16</td>
//                                               <td>dB</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>65</td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>04</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>ASTM E1686-16</td>
//                                               <td>dB</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>65</td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>05</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>ASTM E1686-16</td>
//                                               <td>dB</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>65</td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>06</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>ASTM E1686-16</td>
//                                               <td>dB</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>65</td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>07</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>ASTM E1686-16</td>
//                                               <td>dB</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>65</td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>08</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>ASTM E1686-16</td>
//                                               <td>dB</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>65</td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>09</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>ASTM E1686-16</td>
//                                               <td>dB</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>65</td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>10</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>ASTM E1686-16</td>
//                                               <td>dB</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>65</td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>11</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>ASTM E1686-16</td>
//                                               <td>dB</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>65</td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>12</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>ASTM E1686-16</td>
//                                               <td>dB</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>65</td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>13</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>ASTM E1686-16</td>
//                                               <td>dB</td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2 "type="text"></td>
//                                               <td>65</td>
//                                           </tr>
                                          
                                          
//                                       </tbody>
//                                   </table>
                  
//                                   <hr class="broder border-black mt-10">
                  
//                                   <div class="flex justify-between mt-4">
//                                       <div class="flex flex-col">
//                                           <label class="font-bold text-lg" for="">Conclusion</label>
//                                           <textarea class="border-2 border-black w-96 rounded " name="" id="" cols="30" rows="3"></textarea>
//                                       </div>
                                          
//                                   </div>
                  
//                                       <h2 class="py-2 font-bold">LEGENDS</h2>
                                  
                                  
                  
                                      
//                                           <table class="w-full border-2 border-black">
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>Test Results = M</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>*APHA Standard Methods for Examination of water & wastewater 23rd Edition (2017).</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>SEQS Limits = Sindh Environmental Quality Standard (Reference: SEQS 2016).</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>PEQS Limits = Punjab Environmental Quality Standard</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>NEQS Limits = National Environmental Quality Standard</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>1=SEQS for Municipal & Liquid Industrial Effluent into inland waters.</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>2= SEQS for Municipal & Liquid Industrial Effluent into Sewage Treatment.</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>3=SEQS for Municipal & Liquid Industrial Effluent into Sea.</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>** Discharge Concentration at or below Sea Concentration (SC).</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>M = Meet SEQS-2016 requirements.</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>F = Below SEQS-2016 requirements.</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>N.D. = Not Detected.</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>N.A = Not Available</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>Customer Requirement: N.A</span></td>
//                                               </tr>
                                              
//                                           </table>
                  
//                                           <div class="flex flex-col justify-between mt-6">
//                                               <div class="flex flex-col">
//                                                   <label class="font-bold text-lg" for="">Edit Note</label>
//                                                   <input class="border-2 border-black p-2 h-10 rounded text-lg" style="width: 79rem;" type="text" >
//                                               </div>
//                                               <div class="flex flex-col mt-4">
//                                                   <label class="font-bold text-lg" for="">Custom Legend (if any):</label>
//                                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" value="Drinking-Water-test as per SEQS-2016">
//                                               </div>
                                              
//                                           </div>
                  
//                                           <div class="flex justify-between mt-6">
//                                               <div class="flex flex-col">
//                                                   <label class="font-bold text-lg" for=""> Doc. Controller 1:</label>
//                                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="ETAL-LAB-708-FF-09">
//                                               </div>
//                                               <div class="flex flex-col">
//                                                   <label class="font-bold text-lg" for="">Doc. Controller 2:</label>
//                                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="Issue Date: 15-05-22">
//                                               </div>
//                                               <div class="flex flex-col">
//                                                   <label class="font-bold text-lg" for="">Doc. Controller 3:</label>
//                                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="Issue No 01">
//                                               </div>
//                                           </div>
                  
//                                           <div class="h-32  mt-8 flex justify-center items-center">
//                                              <div class="space-x-8">
//                                               <button class="bg-blue-600 h-12 w-60 rounded shadow-2xl text-white hover:bg-blue-500 "><i class="fa-solid fa-download pr-4  "></i>Save & Add New</button>
//                                               <button class="h-12 bg-green-500 rounded  shadow-2xl w-60 hover:bg-green-400 text-white"><i class="fa-solid fa-file pr-4"></i>Save & View Report</button>
//                                              </div>
//                                           </div>
                  
                                   
//                                   </div>
                  
                                  
                  
//                           </form>
//                           <section class="bg-gray-900 h-20 flex justify-center items-center w-full ">
//                                     <div class="">
//                                           <p class="text-lg text-gray-300">© Copyright 2023 EnviTechAl. All Rights Reserved.</p>
//                                           <p></p>
//                                     </div>
//                                   </section>
                          
//                       </div>
//           `
//         addelemdiv.appendChild(noiseAnalysisFormDiv)
//   })
  
  //noise Analysis List
  
  // var noiseAnalysisListBtn = document.querySelector(".noiseAnalysisListBtn")
  
  // noiseAnalysisListBtn.addEventListener("click",()=>{
  //     addelemdiv.innerHTML = " "
  //     var noiseAnalysisList = document.createElement("div")
  //     noiseAnalysisList.classList.add("noiseAnalysisListDiv")
  //     noiseAnalysisList.innerHTML = `
  //     <div class="w-full flex justify-center items-center  h-11/12">
  //     <form action="" class="flex flex-col justify-around  w-11/12 mt-10">
  //         <h1 class="text-center mt-10 text-3xl py-16">List Of Noise Analysis</h1>
  //         <div class="flex justify-between">
  //             <div class="flex flex-col">
  //                 <label class="font-bold text-lg" for="">Date From</label>
  //                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="">
  //             </div>
  //             <div class="flex flex-col">
  //                 <label class="font-bold text-lg" for="">Date To</label>
  //                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
  //             </div>
  //             <div class="flex flex-col">
  //                 <label class="font-bold text-lg" for="">Lab report No</label>
  //                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
  //             </div>
  //         </div>
  //         <div class="flex justify-between mt-10">
  //             <div class="flex flex-col">
  //                 <label class="font-bold text-lg" for="">Invoice Bill No</label>
  //                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
  //             </div>
  //             <div class="flex flex-col">
  //                 <label class="font-bold text-lg" for="">Report To</label>
  //                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
  //             </div>
  //             <div class="flex flex-col">
  //                 <label class="font-bold text-lg" for="">Attention</label>
  //                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
  //             </div>
  //         </div>
  //         <div class="flex justify-between mt-10">
  //             <div class="flex flex-col">
  //                 <label class="font-bold text-lg" for="">Email Address</label>
  //                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;"  type="text" >
  //             </div>
  //             <div class="flex flex-col">
  //                 <label class="font-bold text-lg" for="">Test ID</label>
  //                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;" type="text" >
  //             </div>
              
  //         </div>
  //         <div class="flex flex-col justify-center items-center mt-16 w-full">
                  
  //             <input class="  h-10 w-96 rounded text-lg bg-blue-500 text-white hover:bg-blue-400 cursor-pointer w-8/12 " type="submit" >
  //         </div>
  //       </form>
  // </div>
  
  //     `
  //     addelemdiv.appendChild(noiseAnalysisList)
  // })
  
  //packing poly bag 
  
  // var packingPolyFormBtn = document.querySelector(".packingPolyFormBtn")
  // var addelemdiv = document.querySelector("#divforAddingelements")
  
  // packingPolyFormBtn.addEventListener("click",()=>{
  //       addelemdiv.innerHTML = " "
  //       var packingPolyBagForm = document.createElement("div")
  //       packingPolyBagForm.classList.add('packingPolyBagForm')
  //       packingPolyBagForm.innerHTML =
  //         `
          
  //         `
  //       addelemdiv.appendChild(packingPolyBagForm)
  // })
  
  
  
  
  //packing poly bag list
  
  // var packingPolyListBtn = document.querySelector(".packingPolyListBtn")
  
  // packingPolyListBtn.addEventListener("click",()=>{
  //     addelemdiv.innerHTML = " "
  //     var packingPolyBagList = document.createElement("div")
  //     packingPolyBagList.classList.add("packingPolyBagListDiv")
  //     packingPolyBagList.innerHTML = `
  //     <div class="w-full flex justify-center items-center  h-11/12">
  //     <form action="" class="flex flex-col justify-around  w-11/12 mt-10">
  //         <h1 class="text-center mt-10 text-3xl py-16">List Of Packing Poly Bag</h1>
  //         <div class="flex justify-between">
  //             <div class="flex flex-col">
  //                 <label class="font-bold text-lg" for="">Date From</label>
  //                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="">
  //             </div>
  //             <div class="flex flex-col">
  //                 <label class="font-bold text-lg" for="">Date To</label>
  //                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
  //             </div>
  //             <div class="flex flex-col">
  //                 <label class="font-bold text-lg" for="">Lab report No</label>
  //                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
  //             </div>
  //         </div>
  //         <div class="flex justify-between mt-10">
  //             <div class="flex flex-col">
  //                 <label class="font-bold text-lg" for="">Invoice Bill No</label>
  //                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
  //             </div>
  //             <div class="flex flex-col">
  //                 <label class="font-bold text-lg" for="">Report To</label>
  //                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
  //             </div>
  //             <div class="flex flex-col">
  //                 <label class="font-bold text-lg" for="">Attention</label>
  //                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
  //             </div>
  //         </div>
  //         <div class="flex justify-between mt-10">
  //             <div class="flex flex-col">
  //                 <label class="font-bold text-lg" for="">Email Address</label>
  //                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;"  type="text" >
  //             </div>
  //             <div class="flex flex-col">
  //                 <label class="font-bold text-lg" for="">Test ID</label>
  //                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;" type="text" >
  //             </div>
              
  //         </div>
  //         <div class="flex flex-col justify-center items-center mt-16 w-full">
                  
  //             <input class="  h-10 w-96 rounded text-lg bg-blue-500 text-white hover:bg-blue-400 cursor-pointer w-8/12 " type="submit" >
  //         </div>
  //       </form>
  // </div>
  
  //     `
  //     addelemdiv.appendChild(packingPolyBagList)
  // })
  
  ///machine oil
  
  // var machineOilFormBtn = document.querySelector(".machineOilFormBtn")
  // var addelemdiv = document.querySelector("#divforAddingelements")
  
  // machineOilFormBtn.addEventListener("click",()=>{
  //       addelemdiv.innerHTML = " "
  //       var machineOilForm = document.createElement("div")
  //       machineOilForm.classList.add('machineOilForm')
  //       machineOilForm.innerHTML =
  //         `
  //         <div class="machineOil h-full w-full flex flex-col items-center ">
                          
  
  //                         <form action="" class="flex flex-col justify-around w-11/12 mt-10 ">
  //                             <h1 class="text-center mt-10 text-3xl py-16">Machine Oil</h1>
  //                             <div class="flex justify-between">
  //                                 <div class="flex flex-col">
  //                                     <label class="font-bold text-lg" for="">Lab Report No</label>
  //                                     <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
  //                                 </div>
  //                                 <div class="flex flex-col">
  //                                     <label class="font-bold text-lg" for="">Invoice Bill No</label>
  //                                     <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
  //                                 </div>
  //                                 <div class="flex flex-col">
  //                                     <label class="font-bold text-lg" for="">Reporting Date</label>
  //                                     <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
  //                                 </div>
  //                             </div>
  //                             <hr class="broder border-black mt-10">
                  
  //                             <div class="flex justify-between mt-4">
  //                                 <div class="flex flex-col">
  //                                     <label class="font-bold text-lg" for="">Report To :</label>
  //                                     <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
  //                                 </div>
  //                                 <div class="flex flex-col">
  //                                     <label class="font-bold text-lg" for="">Address</label>
  //                                     <input class="border-2 border-black p-2 h-10 rounded text-lg" style="width: 35rem;" type="text" >
  //                                 </div>
                                  
                                  
  //                             </div>
                  
  //                             <div class="flex justify-between mt-4">
  //                                 <div class="flex flex-col">
  //                                     <label class="font-bold text-lg" for="">Attention</label>
  //                                     <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
  //                                 </div>
  //                                 <div class="flex flex-col">
  //                                     <label class="font-bold text-lg" for="">Email</label>
  //                                     <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
  //                                 </div>
  //                             </div>
                  
  //                             <hr class="broder border-black mt-10">
                  
  //                             <div class="flex justify-between mt-4">
  //                                 <div class="flex flex-col">
  //                                     <label class="font-bold text-lg" for="">Sample ID</label>
  //                                     <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="${currentDate}">
  //                                 </div>
  //                                 <div class="flex flex-col">
  //                                     <label class="font-bold text-lg" for="">Sample Collection Date</label>
  //                                     <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="date">
  //                                 </div>
  //                                 <div class="flex flex-col">
  //                                     <label class="font-bold text-lg" for="">Sample Description</label>
  //                                     <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="Lux Analysis">
  //                                 </div>
  //                             </div>
                  
  //                             <div class="flex justify-between mt-4">
                                  
  //                                 <div class="flex flex-col">
  //                                     <label class="font-bold text-lg" for="">Sample Type</label>
  //                                     <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="Viscous Liquid">
  //                                 </div>
  //                                 <div class="flex flex-col ">
  //                                     <label class="font-bold text-lg" for="">Sample Collected By</label>
  //                                     <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="date" value="Envi Tech AL">
  //                                 </div>
  //                                 <div class="flex flex-col ">
  //                                     <label class="font-bold text-lg" for="">Test Description</label>
  //                                     <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="date" value="Heavy Metal Testing of Machine Oil – 16 Metals">
  //                                 </div>
  //                             </div>
                  
                              
  //                             <hr class="broder border-black mt-10">
                  
                  
                  
  //                             <div class="w-full flex flex-col justify-center">
  //                                 <table id="" class=" water-form-table border-collapse border-2 border-gray-700 mt-10 " cellspacing="15">
  //                                     <thead>
  //                                         <tr>
  //                                             <th>Sr.#</th>
  //                                             <th>Parameter/Analytes Description</th>
  //                                             <th>Testing Method</th>
  //                                             <th>Unit</th>
  //                                             <th>Test Result</th>
  //                                             <th>GOTS Limits</th>
                                              
                                              
                                              
  //                                         </tr>
  //                                     </thead>
  //                                     <tbody class="">
  //                                         <tr class="text-center border h-16">
  //                                             <td>01</td>
  //                                             <td>Antimony (Sb)</td>
  //                                             <td>ASTM D-5185</td>
  //                                             <td>mg/L</td>
  //                                             <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
  //                                             <td>50</td>
                                              
  //                                         </tr>
  //                                         <tr class="text-center border h-16">
  //                                             <td>02</td>
  //                                             <td>Arsenic (As)</td>
  //                                             <td>ASTM D-5185</td>
  //                                             <td>mg/L</td>
  //                                             <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
  //                                             <td>50</td>
                                              
  //                                         </tr>
  //                                         <tr class="text-center border h-16">
  //                                             <td>03</td>
  //                                             <td>Barium (Ba)</td>
  //                                             <td>ASTM D-5185</td>
  //                                             <td>mg/L</td>
  //                                             <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
  //                                             <td>100</td>
                                              
  //                                         </tr>
  //                                         <tr class="text-center border h-16">
  //                                             <td>04</td>
  //                                             <td>Cadmium (Cd)</td>
  //                                             <td>ASTM D-5185</td>
  //                                             <td>mg/L</td>
  //                                             <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
  //                                             <td>20</td>
                                              
  //                                         </tr>
  //                                         <tr class="text-center border h-16">
  //                                             <td>05</td>
  //                                             <td>Cobalt (Co)</td>
  //                                             <td>ASTM D-5185</td>
  //                                             <td>mg/L</td>
  //                                             <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
  //                                             <td>500</td>
                                              
  //                                         </tr>
  //                                         <tr class="text-center border h-16">
  //                                             <td>06</td>
  //                                             <td>Copper (Cu)</td>
  //                                             <td>ASTM D-5185</td>
  //                                             <td>mg/L</td>
  //                                             <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
  //                                             <td>250</td>
                                              
  //                                         </tr>
  //                                         <tr class="text-center border h-16">
  //                                             <td>07</td>
  //                                             <td>Chromium (Cr)</td>
  //                                             <td>ASTM D-5185</td>
  //                                             <td>mg/L</td>
  //                                             <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
  //                                             <td>100</td>
                                              
  //                                         </tr>
  //                                         <tr class="text-center border h-16">
  //                                             <td>08</td>
  //                                             <td>Iron (Fe)</td>
  //                                             <td>ASTM D-5185</td>
  //                                             <td>mg/L</td>
  //                                             <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
  //                                             <td>2500</td>
                                              
  //                                         </tr>
  //                                         <tr class="text-center border h-16">
  //                                             <td>09</td>
  //                                             <td>Lead (Pb)</td>
  //                                             <td>ASTM D-5185</td>
  //                                             <td>mg/L</td>
  //                                             <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
  //                                             <td>100</td>
                                              
  //                                         </tr>
  //                                         <tr class="text-center border h-16">
  //                                             <td>10</td>
  //                                             <td>Magnese (Mn)</td>
  //                                             <td>ASTM D-5185</td>
  //                                             <td>mg/L</td>
  //                                             <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
  //                                             <td>1000</td>
                                              
  //                                         </tr>
  //                                         <tr class="text-center border h-16">
  //                                             <td>11</td>
  //                                             <td>Nickel (Ni)</td>
  //                                             <td>ASTM D-5185</td>
  //                                             <td>mg/L</td>
  //                                             <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
  //                                             <td>200</td>
                                              
  //                                         </tr>
  //                                         <tr class="text-center border h-16">
  //                                             <td>12</td>
  //                                             <td>Mercury (Hg)</td>
  //                                             <td>ASTM D7622</td>
  //                                             <td>mg/L</td>
  //                                             <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
  //                                             <td>04</td>
                                              
  //                                         </tr>
  //                                         <tr class="text-center border h-16">
  //                                             <td>13</td>
  //                                             <td>Selenium (Se)</td>
  //                                             <td>ASTM D-5185</td>
  //                                             <td>mg/L</td>
  //                                             <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
  //                                             <td>20</td>
                                              
  //                                         </tr>
                                          
  //                                         <tr class="text-center border h-16">
  //                                             <td>14</td>
  //                                             <td>Silver (Ag)</td>
  //                                             <td>ASTM D-5185</td>
  //                                             <td>mg/L</td>
  //                                             <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
  //                                             <td>100</td>
                                              
  //                                         </tr>
  //                                         <tr class="text-center border h-16">
  //                                             <td>15</td>
  //                                             <td>Zinc (Zn)</td>
  //                                             <td>ASTM D-5185</td>
  //                                             <td>mg/L</td>
  //                                             <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
  //                                             <td>1500</td>
                                              
  //                                         </tr>
  //                                         <tr class="text-center border h-16">
  //                                             <td>16</td>
  //                                             <td>Tin (Sn)</td>
  //                                             <td>ASTM D-5185</td>
  //                                             <td>mg/L</td>
  //                                             <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
  //                                             <td>250</td>
                                              
  //                                         </tr>
                                          
                                          
                                          
  //                                     </tbody>
  //                                 </table>
                  
  //                                 <hr class="broder border-black mt-10">
                  
  //                                 <div class="flex justify-between mt-4">
  //                                     <div class="flex flex-col">
  //                                         <label class="font-bold text-lg" for="">Conclusion</label>
  //                                         <textarea class="border-2 border-black w-96 rounded " name="" id="" cols="30" rows="3"></textarea>
  //                                     </div>
                                          
  //                                 </div>
                  
  //                                     <h2 class="py-2 font-bold">LEGENDS</h2>
                                  
                                  
                  
                                      
  //                                         <table class="w-full border-2 border-black">
  //                                             <tr class="bg-gray-200">
  //                                                 <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>Test Results = M</span></td>
  //                                             </tr>
  //                                             <tr class="">
  //                                                 <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>*APHA Standard Methods for Examination of water & wastewater 23rd Edition (2017).</span></td>
  //                                             </tr>
  //                                             <tr class="bg-gray-200">
  //                                                 <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>SEQS Limits = Sindh Environmental Quality Standard (Reference: SEQS 2016).</span></td>
  //                                             </tr>
  //                                             <tr class="">
  //                                                 <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>PEQS Limits = Punjab Environmental Quality Standard</span></td>
  //                                             </tr>
  //                                             <tr class="bg-gray-200">
  //                                                 <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>NEQS Limits = National Environmental Quality Standard</span></td>
  //                                             </tr>
  //                                             <tr class="">
  //                                                 <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>1=SEQS for Municipal & Liquid Industrial Effluent into inland waters.</span></td>
  //                                             </tr>
  //                                             <tr class="bg-gray-200">
  //                                                 <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>2= SEQS for Municipal & Liquid Industrial Effluent into Sewage Treatment.</span></td>
  //                                             </tr>
  //                                             <tr class="">
  //                                                 <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>3=SEQS for Municipal & Liquid Industrial Effluent into Sea.</span></td>
  //                                             </tr>
  //                                             <tr class="bg-gray-200">
  //                                                 <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>** Discharge Concentration at or below Sea Concentration (SC).</span></td>
  //                                             </tr>
  //                                             <tr class="">
  //                                                 <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>M = Meet SEQS-2016 requirements.</span></td>
  //                                             </tr>
  //                                             <tr class="bg-gray-200">
  //                                                 <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>F = Below SEQS-2016 requirements.</span></td>
  //                                             </tr>
  //                                             <tr class="">
  //                                                 <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>N.D. = Not Detected.</span></td>
  //                                             </tr>
  //                                             <tr class="bg-gray-200">
  //                                                 <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>N.A = Not Available</span></td>
  //                                             </tr>
  //                                             <tr class="">
  //                                                 <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>Customer Requirement: N.A</span></td>
  //                                             </tr>
                                              
  //                                         </table>
                  
  //                                         <div class="flex flex-col justify-between mt-6">
  //                                             <div class="flex flex-col">
  //                                                 <label class="font-bold text-lg" for="">Edit Note</label>
  //                                                 <input class="border-2 border-black p-2 h-10 rounded text-s" style="width: 79rem;" type="text" value="Note: Measurement of uncertainty will be provided on customer Demand. Environmental Conditions at the time of Testing; Temperature: 25.1 ⁰C (+- 1⁰C) & Humidity: 47.5 % (+- 1%).">
  //                                             </div>
  //                                             <div class="flex flex-col mt-4">
  //                                                 <label class="font-bold text-lg" for="">Custom Legend (if any):</label>
  //                                                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" value="Drinking-Water-test as per SEQS-2016">
  //                                             </div>
                                              
  //                                         </div>
                  
  //                                         <div class="flex justify-between mt-6">
  //                                             <div class="flex flex-col">
  //                                                 <label class="font-bold text-lg" for=""> Doc. Controller 1:</label>
  //                                                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="ETAL-LAB-708-FF-13">
  //                                             </div>
  //                                             <div class="flex flex-col">
  //                                                 <label class="font-bold text-lg" for="">Doc. Controller 2:</label>
  //                                                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="Issue Date: 15-05-22">
  //                                             </div>
  //                                             <div class="flex flex-col">
  //                                                 <label class="font-bold text-lg" for="">Doc. Controller 3:</label>
  //                                                 <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="Issue No 01">
  //                                             </div>
  //                                         </div>
                  
  //                                         <div class="h-32  mt-8 flex justify-center items-center">
  //                                            <div class="space-x-8">
  //                                             <button class="bg-blue-600 h-12 w-60 rounded shadow-2xl text-white hover:bg-blue-500 "><i class="fa-solid fa-download pr-4  "></i>Save & Add New</button>
  //                                             <button class="h-12 bg-green-500 rounded  shadow-2xl w-60 hover:bg-green-400 text-white"><i class="fa-solid fa-file pr-4"></i>Save & View Report</button>
  //                                            </div>
  //                                         </div>
                  
                                   
  //                                 </div>
                  
                                  
                  
  //                         </form>
  //                         <section class="bg-gray-900 h-20 flex justify-center items-center w-full ">
  //                                   <div class="">
  //                                         <p class="text-lg text-gray-300">© Copyright 2023 EnviTechAl. All Rights Reserved.</p>
  //                                         <p></p>
  //                                   </div>
  //                                 </section>
                          
  //                     </div>
  //         `
  //       addelemdiv.appendChild(machineOilForm)
  // })
  
  //machine oil list
  
//   var machineOilListBtn = document.querySelector(".machineOilListBtn")
  
//   machineOilListBtn.addEventListener("click",()=>{
//       addelemdiv.innerHTML = " "
//       var machineOilListDiv = document.createElement("div")
//       machineOilListDiv.classList.add("machineOilListDivDiv")
//       machineOilListDiv.innerHTML = `
//       <div class="w-full flex justify-center items-center  h-11/12">
//       <form action="" class="flex flex-col justify-around  w-11/12 mt-10">
//           <h1 class="text-center mt-10 text-3xl py-16">List Of Machine Oil</h1>
//           <div class="flex justify-between">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date From</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Lab report No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Invoice Bill No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Report To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Attention</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Email Address</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;"  type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Test ID</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;" type="text" >
//               </div>
              
//           </div>
//           <div class="flex flex-col justify-center items-center mt-16 w-full">
                  
//               <input class="  h-10 w-96 rounded text-lg bg-blue-500 text-white hover:bg-blue-400 cursor-pointer w-8/12 " type="submit" >
//           </div>
//         </form>
//   </div>
  
//       `
//       addelemdiv.appendChild(machineOilListDiv)
//   })
  
//   ///microbial form
  
//   var microbialFormBtn = document.querySelector(".microbialFormBtn")
//   var addelemdiv = document.querySelector("#divforAddingelements")
  
//   microbialFormBtn.addEventListener("click",()=>{
//         addelemdiv.innerHTML = " "
//         var microbialForm = document.createElement("div")
//         microbialForm.classList.add('microbialForm')
//         microbialForm.innerHTML =
//           `
//           <div class="microbialAnalysis h-full w-full flex flex-col items-center ">
                          
  
//           <form action="" class="flex flex-col justify-around w-11/12 mt-10 ">
//               <h1 class="text-center mt-10 text-3xl py-16">Microbial Analysis</h1>
//               <div class="flex justify-between">
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Lab Report No</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
//                   </div>
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Invoice Bill No</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//                   </div>
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Reporting Date</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
//                   </div>
//               </div>
//               <hr class="broder border-black mt-10">
  
//               <div class="flex justify-between mt-4">
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Report To :</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
//                   </div>
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Address</label>
//                       <input class="border-2 border-black p-2 h-10 rounded text-lg" style="width: 35rem;" type="text" >
//                   </div>
                  
                  
//               </div>
  
//               <div class="flex justify-between mt-4">
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Attention</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
//                   </div>
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Email</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
//                   </div>
//               </div>
  
//               <hr class="broder border-black mt-10">
  
//               <div class="flex justify-between mt-4">
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Sample ID</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="${currentDate}">
//                   </div>
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Sample Collection Date </label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="date">
//                   </div>
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Sample Description</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="">
//                   </div>
//               </div>
  
//               <div class="flex justify-between mt-4">
                  
//                   <div class="flex flex-col">
//                       <label class="font-bold text-lg" for="">Sample Type</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="Drinking Water">
//                   </div>
//                   <div class="flex flex-col ">
//                       <label class="font-bold text-lg" for="">Sample Collected By</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="Envi Tech AL">
//                   </div>
//                   <div class="flex flex-col ">
//                       <label class="font-bold text-lg" for="">Date Of Analysis</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="date">
//                   </div>
//               </div>
//               <div class="flex justify-between mt-4">
              
//                   <div class="flex flex-col ">
//                       <label class="font-bold text-lg" for="">Test Description</label>
//                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="Microbiological Testing">
//                   </div>
//               </div>
  
              
//               <hr class="broder border-black mt-10">
  
  
  
//               <div class="w-full flex flex-col justify-center">
//                   <table id="" class=" water-form-table border-collapse border-2 border-gray-700 mt-10 " cellspacing="15">
//                       <thead>
//                           <tr>
//                               <th>Sr.#</th>
//                               <th>Parameter/Analytes Description</th>
                              
//                               <th>Unit</th>
//                               <th>Test Result</th>
                              
                              
                              
                              
//                           </tr>
//                       </thead>
//                       <tbody class="">
//                           <tr class="text-center border h-16">
//                               <td>01</td>
//                               <td>Total Colony Count</td>
//                               <td>CFU/ml</td>
//                               <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
//                           </tr>
//                           <tr class="text-center border h-16">
//                               <td>02</td>
//                               <td>Total Coliform</td>
//                               <td>CFU/ml</td>
//                               <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
//                           </tr>
//                           <tr class="text-center border h-16">
//                               <td>03</td>
//                               <td>Faecal E.coli</td>
//                               <td>CFU/ml</td>
//                               <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
//                           </tr>
//                           <tr class="text-center border h-16">
//                               <td>04</td>
//                               <td>Faecal Enterococci</td>
//                               <td>CFU/ml</td>
//                               <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
//                           </tr>
//                           <tr class="text-center border h-16">
//                               <td>05</td>
//                               <td>Pseudomonas aeruginosa</td>
//                               <td>CFU/ml</td>
//                               <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
//                           </tr>
//                           <tr class="text-center border h-16">
//                               <td>06</td>
//                               <td>Faecal Coliform</td>
//                               <td>CFU/ml</td>
//                               <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
//                           </tr>
                          
                          
                          
//                       </tbody>
//                   </table>
  
//                   <hr class="broder border-black mt-10">
  
//                   <div class="flex justify-between mt-4">
//                       <div class="flex flex-col">
//                           <label class="font-bold text-lg" for="">Conclusion</label>
//                           <textarea class="border-2 border-black  rounded " name="" id="" cols="40" rows="3"></textarea>
//                       </div>
                          
//                   </div>
  
//                       <h2 class="py-2 font-bold">LEGENDS</h2>
                  
                  
  
                      
//                           <table class="w-full border-2 border-black">
//                               <tr class="bg-gray-200">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>Test Results = M</span></td>
//                               </tr>
//                               <tr class="">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>*APHA Standard Methods for Examination of water & wastewater 23rd Edition (2017).</span></td>
//                               </tr>
//                               <tr class="bg-gray-200">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>SEQS Limits = Sindh Environmental Quality Standard (Reference: SEQS 2016).</span></td>
//                               </tr>
//                               <tr class="">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>PEQS Limits = Punjab Environmental Quality Standard</span></td>
//                               </tr>
//                               <tr class="bg-gray-200">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>NEQS Limits = National Environmental Quality Standard</span></td>
//                               </tr>
//                               <tr class="">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>1=SEQS for Municipal & Liquid Industrial Effluent into inland waters.</span></td>
//                               </tr>
//                               <tr class="bg-gray-200">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>2= SEQS for Municipal & Liquid Industrial Effluent into Sewage Treatment.</span></td>
//                               </tr>
//                               <tr class="">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>3=SEQS for Municipal & Liquid Industrial Effluent into Sea.</span></td>
//                               </tr>
//                               <tr class="bg-gray-200">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>** Discharge Concentration at or below Sea Concentration (SC).</span></td>
//                               </tr>
//                               <tr class="">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>M = Meet SEQS-2016 requirements.</span></td>
//                               </tr>
//                               <tr class="bg-gray-200">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>F = Below SEQS-2016 requirements.</span></td>
//                               </tr>
//                               <tr class="">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>N.D. = Not Detected.</span></td>
//                               </tr>
//                               <tr class="bg-gray-200">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>N.A = Not Available</span></td>
//                               </tr>
//                               <tr class="">
//                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>Customer Requirement: N.A</span></td>
//                               </tr>
                              
//                           </table>
  
//                           <div class="flex flex-col justify-between mt-6">
//                               <div class="flex flex-col">
//                                   <label class="font-bold text-lg" for="">Edit Note</label>
//                                   <input class="border-2 border-black p-2 h-10 rounded text-sm" style="width: 79rem;" type="text" value="Note: Measurement of uncertainty will be provided on customer Demand. Environmental Conditions at the time of Testing; Temperature: 25.1 ⁰C (+- 1⁰C) & Humidity: 47.5 % (+- 1%).">
//                               </div>
//                               <div class="flex flex-col mt-4">
//                                   <label class="font-bold text-lg" for="">Custom Legend (if any):</label>
//                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" value="Drinking-Water-test as per SEQS-2016">
//                               </div>
                              
//                           </div>
  
//                           <div class="flex justify-between mt-6">
//                               <div class="flex flex-col">
//                                   <label class="font-bold text-lg" for=""> Doc. Controller 1:</label>
//                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="ETAL-LAB-708-FF-03">
//                               </div>
//                               <div class="flex flex-col">
//                                   <label class="font-bold text-lg" for="">Doc. Controller 2:</label>
//                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="Issue Date: 15-05-22">
//                               </div>
//                               <div class="flex flex-col">
//                                   <label class="font-bold text-lg" for="">Doc. Controller 3:</label>
//                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="Issue No 01">
//                               </div>
//                           </div>
  
//                           <div class="h-32  mt-8 flex justify-center items-center">
//                              <div class="space-x-8">
//                               <button class="bg-blue-600 h-12 w-60 rounded shadow-2xl text-white hover:bg-blue-500 "><i class="fa-solid fa-download pr-4  "></i>Save & Add New</button>
//                               <button class="h-12 bg-green-500 rounded  shadow-2xl w-60 hover:bg-green-400 text-white"><i class="fa-solid fa-file pr-4"></i>Save & View Report</button>
//                              </div>
//                           </div>
  
                   
//                   </div>
  
                  
  
//           </form>
//           <section class="bg-gray-900 h-20 flex justify-center items-center w-full ">
//                     <div class="">
//                           <p class="text-lg text-gray-300">© Copyright 2023 EnviTechAl. All Rights Reserved.</p>
//                           <p></p>
//                     </div>
//                   </section>
          
//       </div>
//           `
//         addelemdiv.appendChild(microbialForm)
//   })
  
//   //microbial List
//   var microbialListBtn = document.querySelector(".microbialListBtn")
  
//   microbialListBtn.addEventListener("click",()=>{
//       addelemdiv.innerHTML = " "
//       var microbialListDDiv = document.createElement("div")
//       microbialListDDiv.classList.add("microbialListDDivDiv")
//       microbialListDDiv.innerHTML = `
//       <div class="w-full flex justify-center items-center  h-11/12">
//       <form action="" class="flex flex-col justify-around  w-11/12 mt-10">
//           <h1 class="text-center mt-10 text-3xl py-16">List Of Microbial</h1>
//           <div class="flex justify-between">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date From</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Lab report No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Invoice Bill No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Report To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Attention</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Email Address</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;"  type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Test ID</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;" type="text" >
//               </div>
              
//           </div>
//           <div class="flex flex-col justify-center items-center mt-16 w-full">
                  
//               <input class="  h-10 w-96 rounded text-lg bg-blue-500 text-white hover:bg-blue-400 cursor-pointer w-8/12 " type="submit" >
//           </div>
//         </form>
//   </div>
  
//       `
//       addelemdiv.appendChild(microbialListDDiv)
//   })
  
//   //Viscous Liquid 
//   var viscousLiquidFormBtn = document.querySelector(".viscousLiquidFormBtn")
//   var addelemdiv = document.querySelector("#divforAddingelements")
  
//   viscousLiquidFormBtn.addEventListener("click",()=>{
//         addelemdiv.innerHTML = " "
//         var viscousLiquidForm = document.createElement("div")
//         viscousLiquidForm.classList.add('viscousLiquidForm')
//         viscousLiquidForm.innerHTML =
//           `
//           <div class="viscousLiquid h-full w-full flex flex-col items-center ">
                          
  
//                           <form action="" class="flex flex-col justify-around w-11/12 mt-10 ">
//                               <h1 class="text-center mt-10 text-3xl py-16">Viscous Liquid</h1>
//                               <div class="flex justify-between">
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Lab Report No</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Invoice Bill No</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Reporting Date</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
//                                   </div>
//                               </div>
//                               <hr class="broder border-black mt-10">
                  
//                               <div class="flex justify-between mt-4">
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Report To :</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Address</label>
//                                       <input class="border-2 border-black p-2 h-10 rounded text-lg" style="width: 35rem;" type="text" >
//                                   </div>
                                  
                                  
//                               </div>
                  
//                               <div class="flex justify-between mt-4">
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Attention</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Email</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
//                                   </div>
//                               </div>
                  
//                               <hr class="broder border-black mt-10">
                  
//                               <div class="flex justify-between mt-4">
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Sample ID</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="${currentDate}">
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Sample Collection Date </label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="date">
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Sample Description</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="">
//                                   </div>
//                               </div>
                  
//                               <div class="flex justify-between mt-4">
                                  
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Sample Type</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="Viscous Liquid">
//                                   </div>
//                                   <div class="flex flex-col ">
//                                       <label class="font-bold text-lg" for="">Sample Collected By</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="Envi Tech AL">
//                                   </div>
//                                   <div class="flex flex-col ">
//                                       <label class="font-bold text-lg" for="">Date Of Analysis</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="date">
//                                   </div>
//                               </div>
//                               <div class="flex justify-between mt-4">
                              
//                                   <div class="flex flex-col ">
//                                       <label class="font-bold text-lg" for="">Test Description</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="Testing of Oil & grease">
//                                   </div>
//                               </div>
                  
                              
//                               <hr class="broder border-black mt-10">
                  
                  
                  
//                               <div class="w-full flex flex-col justify-center">
//                                   <table id="" class=" water-form-table border-collapse border-2 border-gray-700 mt-10 " cellspacing="15">
//                                       <thead>
//                                           <tr>
//                                               <th>Sr.#</th>
//                                               <th>Parameter/Analytes Description</th>
//                                               <th>Unit</th>
//                                               <th>Method</th>
//                                               <th>Test Result</th>
                                            
//                                           </tr>
//                                       </thead>
//                                       <tbody class="">
//                                           <tr class="text-center border h-16">
//                                               <td>01</td>
//                                               <td>Oil & Grease</td>
//                                               <td>mg/L</td>
//                                               <td><select name="" id="">
//                                                   <option value="">ASTM D-3921</option>
//                                                   <option value="">USEPA 1664</option>
//                                                   <option value="">APHA 5220-B</option>
//                                               </select></td>
//                                               <td><input class="border-2 border-black w-96 h-10 rounded p-2" type="text"></td>
//                                           </tr>
                                          
//                                       </tbody>
//                                   </table>
                  
//                                   <hr class="broder border-black mt-10">
                  
//                                   <div class="flex justify-between mt-4">
//                                       <div class="flex flex-col">
//                                           <label class="font-bold text-lg" for="">Conclusion</label>
//                                           <textarea class="border-2 border-black  rounded " name="" id="" cols="40" rows="3"></textarea>
//                                       </div>
                                          
//                                   </div>
                  
//                                       <h2 class="py-2 font-bold">LEGENDS</h2>
                                  
                                  
                  
                                      
//                                           <table class="w-full border-2 border-black">
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>Test Results = M</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>*APHA Standard Methods for Examination of water & wastewater 23rd Edition (2017).</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>SEQS Limits = Sindh Environmental Quality Standard (Reference: SEQS 2016).</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>PEQS Limits = Punjab Environmental Quality Standard</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>NEQS Limits = National Environmental Quality Standard</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>1=SEQS for Municipal & Liquid Industrial Effluent into inland waters.</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>2= SEQS for Municipal & Liquid Industrial Effluent into Sewage Treatment.</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>3=SEQS for Municipal & Liquid Industrial Effluent into Sea.</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>** Discharge Concentration at or below Sea Concentration (SC).</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>M = Meet SEQS-2016 requirements.</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>F = Below SEQS-2016 requirements.</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>N.D. = Not Detected.</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>N.A = Not Available</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>Customer Requirement: N.A</span></td>
//                                               </tr>
                                              
//                                           </table>
                  
//                                           <div class="flex flex-col justify-between mt-6">
//                                               <div class="flex flex-col">
//                                                   <label class="font-bold text-lg" for="">Edit Note</label>
//                                                   <input class="border-2 border-black p-2 h-10 rounded text-sm" style="width: 79rem;" type="text" value="Note: Measurement of uncertainty will be provided on customer Demand. Environmental Conditions at the time of Testing; Temperature: 25.1 ⁰C (+- 1⁰C) & Humidity: 47.5 % (+- 1%).">
//                                               </div>
//                                               <div class="flex flex-col mt-4">
//                                                   <label class="font-bold text-lg" for="">Custom Legend (if any):</label>
//                                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" value="Drinking-Water-test as per SEQS-2016">
//                                               </div>
                                              
//                                           </div>
                  
//                                           <div class="flex justify-between mt-6">
//                                               <div class="flex flex-col">
//                                                   <label class="font-bold text-lg" for=""> Doc. Controller 1:</label>
//                                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="ETAL-LAB-708-FF-14">
//                                               </div>
//                                               <div class="flex flex-col">
//                                                   <label class="font-bold text-lg" for="">Doc. Controller 2:</label>
//                                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="Issue Date: 15-05-22">
//                                               </div>
//                                               <div class="flex flex-col">
//                                                   <label class="font-bold text-lg" for="">Doc. Controller 3:</label>
//                                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="Issue No 01">
//                                               </div>
//                                           </div>
                  
//                                           <div class="h-32  mt-8 flex justify-center items-center">
//                                              <div class="space-x-8">
//                                               <button class="bg-blue-600 h-12 w-60 rounded shadow-2xl text-white hover:bg-blue-500 "><i class="fa-solid fa-download pr-4  "></i>Save & Add New</button>
//                                               <button class="h-12 bg-green-500 rounded  shadow-2xl w-60 hover:bg-green-400 text-white"><i class="fa-solid fa-file pr-4"></i>Save & View Report</button>
//                                              </div>
//                                           </div>
                  
                                   
//                                   </div>
                  
                                  
                  
//                           </form>
//                           <section class="bg-gray-900 h-20 flex justify-center items-center w-full ">
//                                     <div class="">
//                                           <p class="text-lg text-gray-300">© Copyright 2023 EnviTechAl. All Rights Reserved.</p>
//                                           <p></p>
//                                     </div>
//                                   </section>
                          
//                       </div>
//           `
//         addelemdiv.appendChild(viscousLiquidForm)
//   })
  
  
//   //viscous Liquid List
  
//   var viscousLiquidListBtn = document.querySelector(".viscousLiquidListBtn")
  
//   viscousLiquidListBtn.addEventListener("click",()=>{
//       addelemdiv.innerHTML = " "
//       var viscouseLiquidListDiv = document.createElement("div")
//       viscouseLiquidListDiv.classList.add("viscouseLiquidListDivDiv")
//       viscouseLiquidListDiv.innerHTML = `
//       <div class="w-full flex justify-center items-center  h-11/12">
//       <form action="" class="flex flex-col justify-around  w-11/12 mt-10">
//           <h1 class="text-center mt-10 text-3xl py-16">List Of Viscous Liquid</h1>
//           <div class="flex justify-between">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date From</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Lab report No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Invoice Bill No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Report To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Attention</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Email Address</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;"  type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Test ID</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;" type="text" >
//               </div>
              
//           </div>
//           <div class="flex flex-col justify-center items-center mt-16 w-full">
                  
//               <input class="  h-10 w-96 rounded text-lg bg-blue-500 text-white hover:bg-blue-400 cursor-pointer w-8/12 " type="submit" >
//           </div>
//         </form>
//   </div>
  
//       `
//       addelemdiv.appendChild(viscouseLiquidListDiv)
//   })
  
  
//   //ambient Air Quality 2
  
//   var ambientAir2FormBtn = document.querySelector(".ambientAir2FormBtn")
//   var addelemdiv = document.querySelector("#divforAddingelements")
  
//   ambientAir2FormBtn.addEventListener("click",()=>{
//         addelemdiv.innerHTML = " "
//         var ambientAir2Form = document.createElement("div")
//         ambientAir2Form.classList.add('ambientAir2Form')
//         ambientAir2Form.innerHTML =
//           `
//           <div class="viscousLiquid h-full w-full flex flex-col items-center ">
                          
  
//                           <form action="" class="flex flex-col justify-around w-11/12 mt-10 ">
//                               <h1 class="text-center mt-10 text-3xl py-16">Ambient Air Quality 2</h1>
//                               <div class="flex justify-between">
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Lab Report No</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Invoice Bill No</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Reporting Date</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
//                                   </div>
//                               </div>
//                               <hr class="broder border-black mt-10">
                  
//                               <div class="flex justify-between mt-4">
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Report To :</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Address</label>
//                                       <input class="border-2 border-black p-2 h-10 rounded text-lg" style="width: 35rem;" type="text" >
//                                   </div>
                                  
                                  
//                               </div>
                  
//                               <div class="flex justify-between mt-4">
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Attention</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Email</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
//                                   </div>
//                               </div>
                  
//                               <hr class="broder border-black mt-10">
                  
//                               <div class="flex justify-between mt-4">
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Test ID</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="${currentDate}">
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Test Performed Date</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="date">
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Test Type</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="Ambient Air Quality">
//                                   </div>
//                               </div>
                  
//                               <div class="flex justify-between mt-4">
                                  
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Test Description</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 38rem;" type="text" value="Ambient Air Quality as per SEQS-2016-24 Hours Monitoring">
//                                   </div>
//                                   <div class="flex flex-col ">
//                                       <label class="font-bold text-lg" for="">Test Performed By</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 38rem;" type="text" value="Envi Tech AL">
//                                   </div>
                                  
//                               </div>
                              
                  
                              
//                               <hr class="broder border-black mt-10">
                  
                  
                  
//                               <div class="w-full flex flex-col justify-center">
//                                   <table id="" class=" water-form-table border-collapse border-2 border-gray-700 mt-10 " cellspacing="15">
//                                       <thead>
//                                           <tr>
//                                               <th>Sr.#</th>
//                                               <th>Time</th>
//                                               <th>CO <br>mg/m³</th>
//                                               <th>NO <br>µg/m3</th>
//                                               <th>NO₂ <br>µg/m3</th>
//                                               <th>SO₂ <br>µg/m3</th>
//                                               <th>O₃ <br>µg/m3</th>
//                                               <th>PM10 <br>µg/m3</th>
//                                               <th>PM1.0<br>µg/m3</th>
//                                               <th>PM2.5<br>µg/m3</th>
//                                               <th>Lead<br>µg/m3</th>
                                              
//                                           </tr>
//                                       </thead>
//                                       <tbody class="">
//                                           <tr class="text-center border h-16">
//                                               <td>01</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="10:00 AM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>02</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="11:00 AM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>03</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="12:00 PM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>04</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="1:00 PM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>05</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="2:00 PM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>06</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="3:00 PM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>07</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="4:00 PM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>08</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="5:00 PM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>09</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="6:00 PM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>10</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="7:00 PM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>11</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="8:00 PM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>12</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="9:00 PM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>13</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="10:00 PM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>14</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="11:00 PM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>15</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="12:00 AM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>16</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="1:00 AM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>17</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="2:00 AM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>18</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="3:00 AM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>19</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="4:00 AM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>20</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="5:00 AM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>21</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="6:00 AM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>22</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="7:00 AM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>23</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="8:00 AM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>24</td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text" value="9:00 AM"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td colspan="2">Average</td>
                                              
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                               <td><input class="h-10 w-20 px-2 py-3 border-2 border-black" type="text"></td>
//                                           </tr>
//                                           <tr class="airbamibient2tr text-center border h-16">
//                                               <td colspan="2"><select class="aa2select h-8 text-center w-36 font-bold border border-black" name="" id="">
//                                                   <option class="ambientair2option1" value="">SEQS Limits</option>
//                                                   <option class = "ambientair2option2" value="PEQS">PEQS Limits</option>
//                                                   <option value="">NEQS Limits</option>
//                                               </select></td>
                                              
//                                               <td id = "aa2td1">05</td>
//                                               <td>40</td>
//                                               <td>80</td>
//                                               <td>120</td>
//                                               <td>-</td>
//                                               <td>150</td>
//                                               <td>500</td>
//                                               <td>75</td>
//                                               <td>1.5</td>
//                                           </tr>
                                          
  
                                          
//                                       </tbody>
//                                   </table>
                  
//                                   <hr class="broder border-black mt-10">
                  
//                                   <div class="flex justify-between mt-4">
//                                       <div class="flex flex-col">
//                                           <label class="font-bold text-lg" for="">Conclusion</label>
//                                           <textarea class="border-2 border-black  rounded " name="" id="" cols="40" rows="3"></textarea>
//                                       </div>
                                          
//                                   </div>
                  
//                                       <h2 class="py-2 font-bold">LEGENDS</h2>
                                  
                                  
                  
                                      
//                                           <table class="w-full border-2 border-black">
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>Test Results = M</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>*APHA Standard Methods for Examination of water & wastewater 23rd Edition (2017).</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>SEQS Limits = Sindh Environmental Quality Standard (Reference: SEQS 2016).</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>PEQS Limits = Punjab Environmental Quality Standard</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>NEQS Limits = National Environmental Quality Standard</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>1=SEQS for Municipal & Liquid Industrial Effluent into inland waters.</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>2= SEQS for Municipal & Liquid Industrial Effluent into Sewage Treatment.</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>3=SEQS for Municipal & Liquid Industrial Effluent into Sea.</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>** Discharge Concentration at or below Sea Concentration (SC).</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>M = Meet SEQS-2016 requirements.</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>F = Below SEQS-2016 requirements.</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>N.D. = Not Detected.</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>N.A = Not Available</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>Customer Requirement: N.A</span></td>
//                                               </tr>
                                              
//                                           </table>
                  
//                                           <div class="flex flex-col justify-between mt-6">
//                                               <div class="flex flex-col">
//                                                   <label class="font-bold text-lg" for="">Edit Note</label>
//                                                   <input class="border-2 border-black p-2 h-10 rounded text-sm" style="width: 79rem;" type="text" value="Note: Measurement of uncertainty will be provided on customer Demand. Environmental Conditions at the time of Testing; Temperature: 25.1 ⁰C (+- 1⁰C) & Humidity: 47.5 % (+- 1%).">
//                                               </div>
//                                               <div class="flex flex-col mt-4">
//                                                   <label class="font-bold text-lg" for="">Custom Legend (if any):</label>
//                                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" value="">
//                                               </div>
                                              
//                                           </div>
                  
//                                           <div class="flex justify-between mt-6">
//                                               <div class="flex flex-col">
//                                                   <label class="font-bold text-lg" for=""> Doc. Controller 1:</label>
//                                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="ETAL-LAB-708-FF-08">
//                                               </div>
//                                               <div class="flex flex-col">
//                                                   <label class="font-bold text-lg" for="">Doc. Controller 2:</label>
//                                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="Issue Date: 15-05-22">
//                                               </div>
//                                               <div class="flex flex-col">
//                                                   <label class="font-bold text-lg" for="">Doc. Controller 3:</label>
//                                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="Issue No 01">
//                                               </div>
//                                           </div>
                  
//                                           <div class="h-32  mt-8 flex justify-center items-center">
//                                              <div class="space-x-8">
//                                               <button class="bg-blue-600 h-12 w-60 rounded shadow-2xl text-white hover:bg-blue-500 "><i class="fa-solid fa-download pr-4  "></i>Save & Add New</button>
//                                               <button class="h-12 bg-green-500 rounded  shadow-2xl w-60 hover:bg-green-400 text-white"><i class="fa-solid fa-file pr-4"></i>Save & View Report</button>
//                                              </div>
//                                           </div>
                  
                                   
//                                   </div>
                  
                                  
                  
//                           </form>
//                           <section class="bg-gray-900 h-20 flex justify-center items-center w-full ">
//                                     <div class="">
//                                           <p class="text-lg text-gray-300">© Copyright 2023 EnviTechAl. All Rights Reserved.</p>
//                                           <p></p>
//                                     </div>
//                                   </section>
                          
//                       </div>
//           `
  
  
  
//         addelemdiv.appendChild(ambientAir2Form)
//   })
  
//   //ambient air 2 list
  
//   var ambientAir2ListBtn = document.querySelector(".ambientAir2ListBtn")
  
//   ambientAir2ListBtn.addEventListener("click",()=>{
//       addelemdiv.innerHTML = " "
//       var airambient2listdiv2 = document.createElement("div")
//       airambient2listdiv2.classList.add("airambient2listdiv2Div")
//       airambient2listdiv2.innerHTML = `
//       <div class="w-full flex justify-center items-center  h-11/12">
//       <form action="" class="flex flex-col justify-around  w-11/12 mt-10">
//           <h1 class="text-center mt-10 text-3xl py-16">List Of Ambient Air 2</h1>
//           <div class="flex justify-between">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date From</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Lab report No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Invoice Bill No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Report To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Attention</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Email Address</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;"  type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Test ID</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;" type="text" >
//               </div>
              
//           </div>
//           <div class="flex flex-col justify-center items-center mt-16 w-full">
                  
//               <input class="  h-10 w-96 rounded text-lg bg-blue-500 text-white hover:bg-blue-400 cursor-pointer w-8/12 " type="submit" >
//           </div>
//         </form>
//   </div>
  
//       `
//       addelemdiv.appendChild(airambient2listdiv2)
//   })
  
  
//   // waste water 2
  
//   var wasteWater2FormBtn = document.querySelector(".wasteWater2FormBtn")
//   var addelemdiv = document.querySelector("#divforAddingelements")
  
//   wasteWater2FormBtn.addEventListener("click",()=>{
//         addelemdiv.innerHTML = " "
//         var wastewater2FormDiv = document.createElement("div")
//         wastewater2FormDiv.classList.add('wastewater2FormDiv')
//         wastewater2FormDiv.innerHTML =
//           `
//           <div class="wasteWaters2 h-full w-full flex flex-col items-center ">
                          
  
//                           <form action="" class="flex flex-col justify-around w-11/12 mt-10 ">
//                               <h1 class="text-center mt-10 text-3xl py-16">Waste Water 2</h1>
//                               <div class="flex justify-between">
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Lab Report No</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Invoice Bill No</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Reporting Date</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
//                                   </div>
//                               </div>
//                               <hr class="broder border-black mt-10">
                  
//                               <div class="flex justify-between mt-4">
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Report To :</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Address</label>
//                                       <input class="border-2 border-black p-2 h-10 rounded text-lg" style="width: 35rem;" type="text" >
//                                   </div>
                                  
                                  
//                               </div>
                  
//                               <div class="flex justify-between mt-4">
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Attention</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Email</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" >
//                                   </div>
//                               </div>
                  
//                               <hr class="broder border-black mt-10">
                  
//                               <div class="flex justify-between mt-4">
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Sample ID</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="${currentDate}">
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Sample Collection Date</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="date" >
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Sample Description</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="Waste water">
//                                   </div>
//                               </div>
                  
//                               <div class="flex justify-between mt-4">
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Sampling Method</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="Liquid – Grab Sample">
//                                   </div>
//                                   <div class="flex flex-col">
//                                       <label class="font-bold text-lg" for="">Sample Type</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="">
//                                   </div>
//                                   <div class="flex flex-col ">
//                                       <label class="font-bold text-lg" for="">Samle Collected By</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 24rem;" type="text" value="Envi Tech Al">
//                                   </div>
//                               </div>
                  
//                               <div class="flex justify-between mt-4">
//                                   <div class="flex flex-col ">
//                                       <label class="font-bold text-lg" for="">Date of Analysis From</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 38rem;" type="date" >
//                                   </div>
//                                   <div class="flex flex-col ">
//                                       <label class="font-bold text-lg" for="">Test Description</label>
//                                       <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 38rem;" type="text" value="Wastewater Testing as per SEQS- 2016">
//                                   </div>
                                 
//                               </div>
//                               <hr class="broder border-black mt-10">
                  
                  
                  
//                               <div class="w-full flex flex-col justify-center">
//                                   <table id="" class=" water-form-table border-collapse border-2 border-gray-700 mt-10 " cellspacing="15">
//                                       <thead>
//                                           <tr>
//                                               <th>Sr.#</th>
//                                               <th>Parameter/Analytes Description</th>
//                                               <th>Methods</th>
//                                               <th>Unit</th>
//                                               <th>Inlet Result</th>
//                                               <th>Outlet Result</th>
//                                               <th><select>
//                                                   <option value="SEQS">SEQS Limits</option>
//                                                   <option value="PEQS">PEQS Limits</option>
//                                                   <option value="NEQS">SEQS Limits</option>
//                                               </select>
//                                               <br>
//                                               <div class="flex justify-around pt-6 text-lg">
//                                               <div class="">1</div>
//                                               <div class="">2</div>
//                                               <div class="">3</div>
//                                               </div>
//                                           </th>
                                              
                                              
                                              
//                                           </tr>
//                                       </thead>
//                                       <tbody class="">
//                                           <tr class="text-center border h-16">
//                                               <td>01</td>
//                                               <td>Temperature 40mg/L</td>
//                                               <td>*APHA 2550</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 3C</div>
//                                                       <div class=""> 3C</div>
//                                                       <div class=""> 3C</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>02</td>
//                                               <td>pH</td>
//                                               <td>*APHA 4500 H-B</td>
//                                               <td>-</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 6-9</div>
//                                                       <div class=""> 6-9</div>
//                                                       <div class=""> 6-9</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>03</td>
//                                               <td>Sulphide</td>
//                                               <td>*APHA 4500-S2-D</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 1</div>
//                                                       <div class=""> 1</div>
//                                                       <div class=""> 1</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>04</td>
//                                               <td>Biological Oxygen Demand(BOD)5</td>
//                                               <td>HACH 10099</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 80</div>
//                                                       <div class=""> 250</div>
//                                                       <div class=""> 80</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>05</td>
//                                               <td>Chemical Oxygen Demand(COD)</td>
//                                               <td>*HACH 8000</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 150</div>
//                                                       <div class=""> 400</div>
//                                                       <div class=""> 400</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>06</td>
//                                               <td>Total Dissolved Solids (TDS)</td>
//                                               <td>*APHA 2540-C</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 3500</div>
//                                                       <div class=""> 3500</div>
//                                                       <div class=""> 3500</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>07</td>
//                                               <td>Total Suspended Solids (TSS)</td>
//                                               <td>*APHA 2540-D</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 200</div>
//                                                       <div class=""> 400</div>
//                                                       <div class=""> 200</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>08</td>
//                                               <td>Oil & Grease</td>
//                                               <td><select class="border border-black " name="" id="">
//                                                   <option value="">ASTM D-3921</option>
//                                                   <option value="">USEPA 1664</option>
//                                                   <option value="">APHA 5220-B</option>
//                                               </select></td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 10</div>
//                                                       <div class=""> 10</div>
//                                                       <div class=""> 10</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>09</td>
//                                               <td>Cadmium</td>
//                                               <td>*APHA 3111-B</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 0.1</div>
//                                                       <div class=""> 0.1</div>
//                                                       <div class=""> 0.1</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>10</td>
//                                               <td>Copper</td>
//                                               <td>*APHA 3111-B</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 1</div>
//                                                       <div class=""> 1</div>
//                                                       <div class=""> 1</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>11</td>
//                                               <td>Iron</td>
//                                               <td>*APHA 3111-B</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 8</div>
//                                                       <div class=""> 8</div>
//                                                       <div class=""> 8</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>12</td>
//                                               <td>Lead</td>
//                                               <td>*APHA 3111-B</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 0.5</div>
//                                                       <div class=""> 0.5</div>
//                                                       <div class=""> 0.5</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>14</td>
//                                               <td>Mercury</td>
//                                               <td>*APHA 3112-B</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 0.01</div>
//                                                       <div class=""> 0.01</div>
//                                                       <div class=""> 0.01</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>15</td>
//                                               <td>Nickel</td>
//                                               <td>*APHA 3111-B</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 1</div>
//                                                       <div class=""> 1</div>
//                                                       <div class=""> 1</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>16</td>
//                                               <td>Selenium</td>
//                                               <td>*APHA 3114-B</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 0.5</div>
//                                                       <div class=""> 0.5</div>
//                                                       <div class=""> 0.5</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>17</td>
//                                               <td>Chromium</td>
//                                               <td>*APHA 3111-B</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 1</div>
//                                                       <div class=""> 1</div>
//                                                       <div class=""> 1</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>18</td>
//                                               <td>Zinc</td>
//                                               <td>*APHA 3111-B</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 5</div>
//                                                       <div class=""> 5</div>
//                                                       <div class=""> 5</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>19</td>
//                                               <td>Arsenic</td>
//                                               <td>*APHA 3114-B</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 1</div>
//                                                       <div class=""> 1</div>
//                                                       <div class=""> 1</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>20</td>
//                                               <td>Chlorine</td>
//                                               <td>HACH 10069</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 1</div>
//                                                       <div class=""> 1</div>
//                                                       <div class=""> 1</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>21</td>
//                                               <td>Chloride</td>
//                                               <td>*APHA 4500 CL-B</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 1000</div>
//                                                       <div class=""> 1000</div>
//                                                       <div class=""> **SC</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>22</td>
//                                               <td>Cyanide</td>
//                                               <td>HACH 8027</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 1</div>
//                                                       <div class=""> 1</div>
//                                                       <div class=""> 1</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>23</td>
//                                               <td>Fluoride</td>
//                                               <td>*HACH 8029</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 10</div>
//                                                       <div class=""> 10</div>
//                                                       <div class=""> 10</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>24</td>
//                                               <td>Ammonia</td>
//                                               <td>*HACH 8038</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 40</div>
//                                                       <div class=""> 40</div>
//                                                       <div class=""> 40</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>25</td>
//                                               <td>Total Toxic Metals</td>
//                                               <td>	APHA 3111</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 2</div>
//                                                       <div class=""> 2</div>
//                                                       <div class=""> 2</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>26</td>
//                                               <td>Sulphate</td>
//                                               <td>HACH 8051</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 600</div>
//                                                       <div class=""> 1000</div>
//                                                       <div class=""> **SC</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>27</td>
//                                               <td>An Ionic Detergent As MBAs</td>
//                                               <td>*APHA 5540 C</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 20</div>
//                                                       <div class=""> 20</div>
//                                                       <div class=""> 20</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>28</td>
//                                               <td>Pesticides</td>
//                                               <td>USEPA-614.1</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 0.15</div>
//                                                       <div class=""> 0.15</div>
//                                                       <div class=""> 0.15</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>29</td>
//                                               <td>Phenolic Compounds(as Phenol)</td>
//                                               <td>HACH 8047</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 0.1</div>
//                                                       <div class=""> 0.3</div>
//                                                       <div class=""> 0.3</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>30</td>
//                                               <td>Boron</td>
//                                               <td>HACH 8015</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 6</div>
//                                                       <div class=""> 6</div>
//                                                       <div class=""> 6</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
  
//                                           <tr class="text-center border h-16">
//                                               <td>31</td>
//                                               <td>Barium</td>
//                                               <td>HACH 8014</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 1.5</div>
//                                                       <div class=""> 1.5</div>
//                                                       <div class=""> 1.5</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
//                                           <tr class="text-center border h-16">
//                                               <td>32</td>
//                                               <td>Silver</td>
//                                               <td>*APHA 3111-B</td>
//                                               <td>mg/L</td>
//                                               <td><input class="border-2 border-black  px-2" type="text"></td>
//                                               <td><input class="border-2 border-black px-2" type="text"></td>
//                                               <td>
//                                                   <div class="flex justify-around">
//                                                       <div class=""> 1</div>
//                                                       <div class=""> 1</div>
//                                                       <div class=""> 1</div>
                                                      
//                                                   </div>
//                                               </td>
                                              
//                                           </tr>
                                          
                                         
                                          
//                                       </tbody>
//                                   </table>
                  
//                                   <hr class="broder border-black mt-10">
                  
//                                   <div class="flex justify-between mt-4">
//                                       <div class="flex flex-col">
//                                           <label class="font-bold text-lg" for="">Conclusion</label>
//                                           <textarea class="border-2 border-black w-96 rounded " name="" id="" cols="30" rows="3"></textarea>
//                                       </div>
                                          
//                                   </div>
                  
//                                       <h2 class="py-2 font-bold">LEGENDS</h2>
                                  
                                  
                  
                                      
//                                           <table class="w-full border-2 border-black">
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>Test Results = M</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>*APHA Standard Methods for Examination of water & wastewater 23rd Edition (2017).</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>SEQS Limits = Sindh Environmental Quality Standard (Reference: SEQS 2016).</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>PEQS Limits = Punjab Environmental Quality Standard</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>NEQS Limits = National Environmental Quality Standard</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>1=SEQS for Municipal & Liquid Industrial Effluent into inland waters.</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>2= SEQS for Municipal & Liquid Industrial Effluent into Sewage Treatment.</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>3=SEQS for Municipal & Liquid Industrial Effluent into Sea.</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>** Discharge Concentration at or below Sea Concentration (SC).</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>M = Meet SEQS-2016 requirements.</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>F = Below SEQS-2016 requirements.</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>N.D. = Not Detected.</span></td>
//                                               </tr>
//                                               <tr class="bg-gray-200">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>N.A = Not Available</span></td>
//                                               </tr>
//                                               <tr class="">
//                                                   <td class="p-2 text-lg"><input class="mr-4 h-4 w-4" type="checkbox"><span>Customer Requirement: N.A</span></td>
//                                               </tr>
                                              
//                                           </table>
                  
//                                           <div class="flex flex-col justify-between mt-6">
//                                               <div class="flex flex-col">
//                                                   <label class="font-bold text-lg" for="">Edit Note</label>
//                                                   <input class="border-2 border-black p-2 h-10 rounded text-lg" style="width: 79rem;" type="text" >
//                                               </div>
//                                               <div class="flex flex-col mt-4">
//                                                   <label class="font-bold text-lg" for="">Custom Legend (if any):</label>
//                                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 35rem;" type="text" value="Drinking-Water-test as per SEQS-2016">
//                                               </div>
                                              
//                                           </div>
                  
//                                           <div class="flex justify-between mt-6">
//                                               <div class="flex flex-col">
//                                                   <label class="font-bold text-lg" for=""> Doc. Controller 1:</label>
//                                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="ETAL-LAB-708-FF-01">
//                                               </div>
//                                               <div class="flex flex-col">
//                                                   <label class="font-bold text-lg" for="">Doc. Controller 2:</label>
//                                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="Issue Date: 15-05-22">
//                                               </div>
//                                               <div class="flex flex-col">
//                                                   <label class="font-bold text-lg" for="">Doc. Controller 3:</label>
//                                                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="Issue No 01">
//                                               </div>
//                                           </div>
                  
//                                           <div class="h-32  mt-8 flex justify-center items-center">
//                                              <div class="space-x-8">
//                                               <button class="bg-blue-600 h-12 w-60 rounded shadow-2xl text-white hover:bg-blue-500 "><i class="fa-solid fa-download pr-4  "></i>Save & Add New</button>
//                                               <button class="h-12 bg-green-500 rounded  shadow-2xl w-60 hover:bg-green-400 text-white"><i class="fa-solid fa-file pr-4"></i>Save & View Report</button>
//                                              </div>
//                                           </div>
                  
                                   
//                                   </div>
                  
                                  
                  
//                           </form>
//                           <section class="bg-gray-900 h-20 flex justify-center items-center w-full ">
//                                     <div class="">
//                                           <p class="text-lg text-gray-300">© Copyright 2023 EnviTechAl. All Rights Reserved.</p>
//                                           <p></p>
//                                     </div>
//                                   </section>
                          
//                       </div>
//           `
  
  
  
//         addelemdiv.appendChild(wastewater2FormDiv)
//   })
  
//   /// waste water 2 List
  
//   var wasteWater2ListBtn = document.querySelector(".wasteWater2ListBtn")
  
//   wasteWater2ListBtn.addEventListener("click",()=>{
//       addelemdiv.innerHTML = " "
//       var wasteWaterListDiv = document.createElement("div")
//       wasteWaterListDiv.classList.add("wasteWaterListDivDiv")
//       wasteWaterListDiv.innerHTML = `
//       <div class="w-full flex justify-center items-center  h-11/12">
//       <form action="" class="flex flex-col justify-around  w-11/12 mt-10">
//           <h1 class="text-center mt-10 text-3xl py-16">List Of Waste Water 2</h1>
//           <div class="flex justify-between">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date From</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" value="">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Date To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="date" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Lab report No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Invoice Bill No</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" value="${currentDate}">
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Report To</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Attention</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" type="text" >
//               </div>
//           </div>
//           <div class="flex justify-between mt-10">
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Email Address</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;"  type="text" >
//               </div>
//               <div class="flex flex-col">
//                   <label class="font-bold text-lg" for="">Test ID</label>
//                   <input class="border-2 border-black p-2 h-10 w-96 rounded text-lg" style="width: 34rem;" type="text" >
//               </div>
              
//           </div>
//           <div class="flex flex-col justify-center items-center mt-16 w-full">
                  
//               <input class="  h-10 w-96 rounded text-lg bg-blue-500 text-white hover:bg-blue-400 cursor-pointer w-8/12 " type="submit" >
//           </div>
//         </form>
//   </div>
  
//       `
//       addelemdiv.appendChild(wasteWaterListDiv)
//   })
  
  
  