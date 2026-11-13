import json, html, re
D = json.load(open('/home/claude/bib/dados.json'))
IMG = 'img/'
def esc(s): return html.escape(s, quote=False)

CSS = """
@font-face{font-family:'Inter';font-weight:400;src:url('file:///usr/share/fonts/opentype/inter/Inter-Regular.otf')}
@font-face{font-family:'Inter';font-weight:400;font-style:italic;src:url('file:///usr/share/fonts/opentype/inter/Inter-Italic.otf')}
@font-face{font-family:'Inter';font-weight:500;src:url('file:///usr/share/fonts/opentype/inter/Inter-Medium.otf')}
@font-face{font-family:'Inter';font-weight:600;src:url('file:///usr/share/fonts/opentype/inter/Inter-SemiBold.otf')}
@font-face{font-family:'Inter';font-weight:700;src:url('file:///usr/share/fonts/opentype/inter/Inter-Bold.otf')}
@font-face{font-family:'InterD';font-weight:500;src:url('file:///usr/share/fonts/opentype/inter/InterDisplay-Medium.otf')}
@font-face{font-family:'InterD';font-weight:700;src:url('file:///usr/share/fonts/opentype/inter/InterDisplay-Bold.otf')}
@font-face{font-family:'InterD';font-weight:800;src:url('file:///usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf')}
@font-face{font-family:'Caveat';font-weight:500;src:url('file:///home/claude/bib/fonts/Caveat500.woff2')}
@font-face{font-family:'Caveat';font-weight:700;src:url('file:///home/claude/bib/fonts/Caveat700.woff2')}

:root{--ink:#1d1519}
@page{size:A4;margin:16mm 16mm 20mm 16mm}
@page az{background:#1f4fa3;@bottom-left{content:"A cidade que somos · Bíblia do jogo";font-family:'Inter',sans-serif;font-size:7pt;font-weight:500;color:#f7f0de}@bottom-right{content:counter(page);font-family:'InterD',sans-serif;font-size:9pt;font-weight:800;color:#ffc93c}}
@page lj{background:#e8692a;@bottom-left{content:"A cidade que somos · Bíblia do jogo";font-family:'Inter',sans-serif;font-size:7pt;font-weight:500;color:#1d1519}@bottom-right{content:counter(page);font-family:'InterD',sans-serif;font-size:9pt;font-weight:800;color:#0d2459}}
@page am{background:#f2b82e;@bottom-left{content:"A cidade que somos · Bíblia do jogo";font-family:'Inter',sans-serif;font-size:7pt;font-weight:500;color:#1d1519}@bottom-right{content:counter(page);font-family:'InterD',sans-serif;font-size:9pt;font-weight:800;color:#1b3f93}}
@page az0{margin:0;background:#1f4fa3;@bottom-left{content:none}@bottom-right{content:none}}
@page lj0{margin:0;background:#e8692a;@bottom-left{content:none}@bottom-right{content:none}}
@page am0{margin:0;background:#f2b82e;@bottom-left{content:none}@bottom-right{content:none}}
*{box-sizing:border-box}

body{margin:0;font:400 8.9pt/1.5 'Inter',sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact;hyphens:auto;text-align:justify}
img{display:block;image-rendering:pixelated}
.t-az{--fg:#f7f0de;--soft:#cfdcf4;--acc:#ffc93c;--rev:#ffb59c;--line:rgba(247,240,222,.38);--g1:#f7f0de;--g2:#ffc93c;--g3:#ff9a62;--g4:#8fd0ff;--bg:#1f4fa3}
.t-lj{--fg:#1d1519;--soft:#2e1408;--acc:#0a1f52;--rev:#400608;--line:rgba(29,21,25,.4);--g1:#1d1519;--g2:#0d2459;--g3:#fff1c4;--g4:#ffd24a;--bg:#e8692a}
.t-am{--fg:#1d1519;--soft:#4a3508;--acc:#1b3f93;--rev:#8a1812;--line:rgba(29,21,25,.4);--g1:#1d1519;--g2:#1b3f93;--g3:#8a1812;--g4:#ffffff;--bg:#f2b82e}
.cap,.front,.abre,.cover{color:var(--fg)}
.cap{column-count:2;column-gap:7mm}
.front{column-count:1}
.cover{page:az0;width:210mm;height:297mm;position:relative;overflow:hidden;break-after:page}
.abre{width:210mm;height:297mm;position:relative;overflow:hidden;break-after:page;background:var(--bg)}
.abre.t-az{page:az0}.abre.t-lj{page:lj0}.abre.t-am{page:am0}
h1{column-span:all;display:flex;align-items:flex-end;gap:6mm;font:800 32pt/1.0 'InterD';letter-spacing:-.018em;margin:0 0 7mm;break-before:page;break-after:avoid;text-align:left}
h1 .n{font:800 70pt/.78 'InterD';color:var(--acc);letter-spacing:-.05em;flex:none}
h1 .n:empty{display:none}
h1.first{break-before:auto}
h2{font:800 13.5pt/1.15 'InterD';margin:6mm 0 2mm;break-after:avoid;text-align:left;letter-spacing:-.005em}
h3{font:700 9.4pt/1.3 'Inter';margin:4mm 0 1.2mm;break-after:avoid;text-align:left}
p{margin:0 0 2.6mm;orphans:3;widows:3}
p.lead{column-span:all;font:500 12.2pt/1.42 'InterD';max-width:150mm;margin:0 0 7mm;text-align:left;hyphens:manual}
ul,ol{margin:0 0 3mm;padding-left:4.4mm} li{margin:0 0 1.3mm}
.rev{color:var(--rev);font-weight:700;font-size:.82em}
.soft{color:var(--soft)}
.ap{font:700 13.6pt/1.08 'Caveat';color:var(--acc);margin:3mm 0 3.6mm;break-inside:avoid;text-align:left;hyphens:manual}
.pen{font-family:'Caveat';font-weight:700;color:var(--acc)}
table{column-span:all;border-collapse:collapse;width:100%;font-size:8.3pt;line-height:1.42;margin:2mm 0 5mm;text-align:left;hyphens:manual}
th{font:700 7.8pt 'Inter';text-align:left;padding:1.4mm 3mm 1.4mm 0;border-bottom:1.1pt solid var(--fg);vertical-align:bottom}
td{padding:1.7mm 3mm 1.7mm 0;border-bottom:.5pt solid var(--line);vertical-align:top}
td:first-child{font-weight:700}
tr{break-inside:avoid}
figure{margin:0 0 4.5mm;break-inside:avoid;width:100%}
figure.fw{column-span:all}
figure img{width:100%;height:auto}
figcaption{font:400 7.5pt/1.4 'Inter';color:var(--soft);margin-top:1.6mm;text-align:left;hyphens:manual}
.pair{column-span:all;display:grid;grid-template-columns:1fr 1fr;gap:7mm;margin:0 0 5mm;break-inside:avoid}
.pair figure{margin:0}
.sumw{width:100%}
.sum ul{padding:0;margin:0}
.sum li{list-style:none;margin:0;display:grid;grid-template-columns:19mm 1fr 12mm;align-items:baseline;padding:3.1mm 0;border-bottom:.5pt solid var(--line);text-align:left}
.sum .n{font:800 20pt/1 'InterD';color:var(--acc);letter-spacing:-.03em}
.sum .t{font:700 11.4pt/1.2 'InterD'}
.sum .p{font:700 10pt 'InterD';text-align:right}
.sum .l2{padding:.9mm 0 .9mm;border-bottom:none}
.sum .l2 .t{font:400 8.6pt 'Inter';color:var(--soft)}
.sum .l2 .p{font:400 8.4pt 'Inter';color:var(--soft)}
.fp{display:grid;grid-template-columns:20mm 1fr;gap:4mm;margin:0 0 5.5mm;break-inside:avoid;text-align:left;hyphens:manual}
.fp .sp{display:flex;align-items:flex-start;justify-content:center}
.fp .sp img{max-height:34mm;max-width:19mm;width:auto}
.fp h3{margin:0 0 .4mm;font:800 13pt/1.1 'InterD'}
.fp .pap{font:600 7.8pt 'Inter';color:var(--soft);margin-bottom:1.6mm}
.fp p{margin:0 0 1.5mm;font-size:8.3pt;line-height:1.43;text-align:left;hyphens:manual}
.fp b{font-weight:700}
.gab{display:block}
.gab .e{break-inside:avoid;display:grid;grid-template-columns:4.2mm 1fr;gap:0 2mm;margin:0 0 3.4mm;text-align:left;hyphens:manual}
.gab .e svg{margin-top:1.4mm}
.gab .tt{font:700 13pt/1.05 'Caveat';color:var(--acc)}
.gab .tx{font-size:8pt;line-height:1.38;margin:.5mm 0 .6mm}
.gab .mt{font-size:7pt;line-height:1.34;color:var(--soft)}
.leg{margin:1mm 0 4mm;font-size:8.6pt;text-align:left;hyphens:manual;break-inside:avoid}
.leg span{display:inline-flex;gap:2mm;align-items:center;margin:0 6mm 1.4mm 0}
.leg.v span{display:flex;align-items:flex-start;margin:0 0 2mm 0}
.leg.v span span{display:block;margin:0}
.mda{column-span:all;display:grid;grid-template-columns:repeat(3,1fr);gap:7mm;margin:2mm 0 5mm;text-align:left;hyphens:manual}
.mda h3{font:800 11.5pt 'InterD';margin:0 0 1.5mm}
.mda ul{padding-left:3.6mm;font-size:8.2pt;line-height:1.42}
.src li{font-size:7.8pt;line-height:1.4;margin-bottom:1mm;text-align:left}
.q{break-inside:avoid}
.w{column-span:all}
table.c1{column-span:none;font-size:8pt}
h2+ol,h2+ul,h2+p,h3+p,h3+ul{break-before:avoid}
h2,h3{break-inside:avoid}
.esq{column-span:all;margin:1mm 0 5mm;break-inside:avoid}
.esq svg{width:100%;height:auto;display:block}
"""
SH = {
 'q': '<svg width="11" height="11" viewBox="0 0 11 11"><rect x="1.5" y="1.5" width="8" height="8" style="fill:var(--g1)"/></svg>',
 'l': '<svg width="11" height="11" viewBox="0 0 11 11"><polygon points="5.5,0.6 10.4,5.5 5.5,10.4 0.6,5.5" style="fill:var(--g4);stroke:var(--fg);stroke-width:.7"/></svg>',
 'c': '<svg width="11" height="11" viewBox="0 0 11 11"><circle cx="5.5" cy="5.5" r="4.3" style="fill:var(--g3)"/></svg>',
 't': '<svg width="11" height="11" viewBox="0 0 11 11"><polygon points="5.5,1 10.3,9.9 0.7,9.9" style="fill:var(--g2)"/></svg>'}
def ap(t): return '<aside class="ap">%s</aside>' % t
def fig(src, cap='', cls=''):
    return '<figure class="%s"><img src="%s%s">%s</figure>' % (cls, IMG, src, '<figcaption>%s</figcaption>' % cap if cap else '')
def h1(num, titulo, first=False):
    return '<h1 class="%s" data-toc="%s" data-n="%s"><span class="n">%s</span><span>%s</span></h1>' % ('first' if first else '', esc(titulo), num, num, esc(titulo))
TEMA = {}
def abre(num, titulo, resumo, cena, tocn):
    tema = TEMA.get(str(tocn), 'am')
    return f'''<section class="abre t-{tema}" data-toc="{esc(titulo)}" data-n="{tocn}">
<img src="{IMG}{cena}" style="width:210mm;height:118mm;object-fit:cover;object-position:center">
<div style="position:absolute;left:16mm;top:132mm"><img src="{IMG}y_{num}_{'cream' if tema=='az' else 'ink'}.png" style="height:34mm;width:auto"></div>
<div style="position:absolute;left:16mm;top:176mm;width:178mm"><div style="font:800 30pt/1.04 'InterD';letter-spacing:-.018em;max-width:150mm">{esc(titulo.split(': ',1)[-1][:1].upper()+titulo.split(': ',1)[-1][1:])}</div>
<div style="margin-top:8mm;font:500 12pt/1.45 'InterD';max-width:132mm">{resumo}</div></div></section>'''
