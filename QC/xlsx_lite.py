"""Minimal .xlsx writer without third-party packages (the server has no openpyxl): several sheets of text cells
with a small fixed set of styles, merged title rows, column widths, frozen header and auto-filter.

    wb = Workbook()
    ws = wb.sheet('Current')
    ws.widths([8, 30, ...]); ws.row(['Title'], style='title', merge=8); ws.row(['A', 'B'], style='head', header=True)
    data = wb.save()   # bytes
"""
import io
import zipfile
from xml.sax.saxutils import escape as _esc

# style ids (cellXfs order below)
STYLES = {'text': 0, 'title': 1, 'sub': 2, 'head': 3, 'cell': 4, 'group': 5, 'cell_ok': 6, 'cell_info': 7, 'cell_muted': 8, 'note': 9}

_STYLES_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<fonts count="7">
<font><sz val="10"/><name val="Calibri"/></font>
<font><b/><sz val="15"/><color rgb="FF0F5132"/><name val="Calibri"/></font>
<font><b/><sz val="10"/><color rgb="FF333333"/><name val="Calibri"/></font>
<font><b/><sz val="10"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>
<font><b/><sz val="10"/><color rgb="FF0F5132"/><name val="Calibri"/></font>
<font><sz val="10"/><color rgb="FF64748B"/><name val="Calibri"/></font>
<font><i/><sz val="9"/><color rgb="FF475569"/><name val="Calibri"/></font>
</fonts>
<fills count="6">
<fill><patternFill patternType="none"/></fill>
<fill><patternFill patternType="gray125"/></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FF0F5132"/><bgColor indexed="64"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFE8F3EC"/><bgColor indexed="64"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFDCFCE7"/><bgColor indexed="64"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFE0F2FE"/><bgColor indexed="64"/></patternFill></fill>
</fills>
<borders count="2">
<border><left/><right/><top/><bottom/><diagonal/></border>
<border><left style="thin"><color rgb="FFB0BEC5"/></left><right style="thin"><color rgb="FFB0BEC5"/></right><top style="thin"><color rgb="FFB0BEC5"/></top><bottom style="thin"><color rgb="FFB0BEC5"/></bottom><diagonal/></border>
</borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="10">
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>
<xf numFmtId="0" fontId="2" fillId="0" borderId="0" xfId="0" applyFont="1"/>
<xf numFmtId="0" fontId="3" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>
<xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
<xf numFmtId="0" fontId="4" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1"/>
<xf numFmtId="0" fontId="0" fillId="4" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
<xf numFmtId="0" fontId="0" fillId="5" borderId="1" xfId="0" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
<xf numFmtId="0" fontId="5" fillId="0" borderId="1" xfId="0" applyFont="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
<xf numFmtId="0" fontId="6" fillId="0" borderId="0" xfId="0" applyFont="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
</cellXfs>
<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>'''


def _col(n):
    s = ''
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _clean(v):
    s = '' if v is None else str(v)
    return ''.join(ch for ch in s if ch in '\t\n' or ord(ch) >= 32)


class Sheet:
    def __init__(self, name):
        self.name = _clean(name)[:31] or 'Sheet'
        self.rows, self.merges, self._widths, self.header_row, self.ncols, self.data_end = [], [], [], None, 0, None

    def end_data(self):
        """Mark the last data row: the auto-filter stops here (notes written later stay outside it)."""
        if self.data_end is None:
            self.data_end = len(self.rows)

    def _last(self):
        return self.data_end if self.data_end is not None else len(self.rows)

    def has_filter(self):
        return bool(self.header_row and self.ncols and self._last() > self.header_row)

    def widths(self, ws):
        self._widths = list(ws)

    def row(self, values, style='cell', styles=None, merge=0, header=False, height=None):
        r = len(self.rows) + 1
        self.rows.append((list(values), style, styles, height))
        if merge:
            self.merges.append('A%d:%s%d' % (r, _col(merge - 1), r))
        if header:
            self.header_row = r
            self.ncols = len(values)
        return r

    def xml(self):
        out = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
               '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
               'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">']
        if self.header_row:
            out.append('<sheetViews><sheetView workbookViewId="0"><pane ySplit="%d" topLeftCell="A%d" activePane="bottomLeft" state="frozen"/>'
                       '</sheetView></sheetViews>' % (self.header_row, self.header_row + 1))
        if self._widths:
            out.append('<cols>' + ''.join('<col min="%d" max="%d" width="%s" customWidth="1"/>' % (i + 1, i + 1, w)
                                          for i, w in enumerate(self._widths)) + '</cols>')
        out.append('<sheetData>')
        for i, (vals, style, styles, height) in enumerate(self.rows, 1):
            attrs = ' ht="%s" customHeight="1"' % height if height else ''
            out.append('<row r="%d"%s>' % (i, attrs))
            for j, v in enumerate(vals):
                st = STYLES.get((styles[j] if styles and j < len(styles) and styles[j] else style), 0)
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    out.append('<c r="%s%d" s="%d"><v>%s</v></c>' % (_col(j), i, st, v))
                else:
                    out.append('<c r="%s%d" t="inlineStr" s="%d"><is><t xml:space="preserve">%s</t></is></c>' % (_col(j), i, st, _esc(_clean(v))))
            out.append('</row>')
        out.append('</sheetData>')
        if self.has_filter():
            out.append('<autoFilter ref="A%d:%s%d"/>' % (self.header_row, _col(self.ncols - 1), self._last()))
        if self.merges:
            out.append('<mergeCells count="%d">%s</mergeCells>' % (len(self.merges), ''.join('<mergeCell ref="%s"/>' % m for m in self.merges)))
        out.append('<pageMargins left="0.4" right="0.4" top="0.5" bottom="0.5" header="0.3" footer="0.3"/>')
        out.append('<pageSetup orientation="landscape" paperSize="9" fitToHeight="0"/>')
        out.append('</worksheet>')
        return ''.join(out)


class Workbook:
    def __init__(self):
        self.sheets = []

    def sheet(self, name):
        s = Sheet(name)
        self.sheets.append(s)
        return s

    def _defined_names(self):
        names = ['<definedName name="_xlnm._FilterDatabase" localSheetId="%d" hidden="1">\'%s\'!$A$%d:$%s$%d</definedName>'
                 % (i, _esc(s.name.replace("'", "''")), s.header_row, _col(s.ncols - 1), s._last())
                 for i, s in enumerate(self.sheets) if s.has_filter()]
        return '<definedNames>%s</definedNames>' % ''.join(names) if names else ''

    def save(self):
        buf = io.BytesIO()
        n = len(self.sheets)
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
            z.writestr('[Content_Types].xml',
                       '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                       '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                       '<Default Extension="xml" ContentType="application/xml"/>'
                       '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                       '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
                       + ''.join('<Override PartName="/xl/worksheets/sheet%d.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' % (i + 1) for i in range(n))
                       + '</Types>')
            z.writestr('_rels/.rels',
                       '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                       '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
            z.writestr('xl/workbook.xml',
                       '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                       'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'
                       + ''.join('<sheet name="%s" sheetId="%d" r:id="rId%d"/>' % (_esc(s.name, {'"': '&quot;'}), i + 1, i + 1) for i, s in enumerate(self.sheets))
                       + '</sheets>'
                       + self._defined_names()
                       + '</workbook>')
            z.writestr('xl/_rels/workbook.xml.rels',
                       '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                       + ''.join('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet%d.xml"/>' % (i + 1, i + 1) for i in range(n))
                       + '<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>' % (n + 1))
            z.writestr('xl/styles.xml', _STYLES_XML)
            for i, s in enumerate(self.sheets):
                z.writestr('xl/worksheets/sheet%d.xml' % (i + 1), s.xml())
        return buf.getvalue()
