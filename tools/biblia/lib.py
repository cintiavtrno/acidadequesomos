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
:root{--ink:#2a2638;--soft:#5d5046;--paper:#f1e5ca;--gold:#f0c98c;--dark:#1d1519;--pen:#2f4c86;--pencil:#b23a2c;--olive:#6f6224}
@page{size:A4;margin:22mm 16mm 22mm 24mm;background:#f1e5ca;
  @bottom-left{content:"O balcão da vó · Bíblia do jogo";font:400 7pt 'Inter';color:#5d5046}
  @bottom-right{content:counter(page);font:500 7.5pt 'Inter';color:#2a2638}}
@page cover{margin:0;@bottom-left{content:none}@bottom-right{content:none}}
@page abre{margin:0;@bottom-left{content:none}@bottom-right{content:none}}
*{box-sizing:border-box}
html{background:var(--paper)}
body{margin:0;font:400 9.4pt/1.56 'Inter',sans-serif;color:var(--ink);background:var(--paper);-webkit-print-color-adjust:exact;print-color-adjust:exact;hyphens:auto;text-align:left}
img{display:block;image-rendering:pixelated}
.cover{page:cover;width:210mm;height:297mm;background:var(--dark);position:relative;overflow:hidden;break-after:page}
.abre{page:abre;width:210mm;height:297mm;background:var(--dark);position:relative;overflow:hidden;break-after:page;color:#efe6d4}
h1{font:800 26pt/1.05 'InterD';letter-spacing:-.012em;margin:0 0 7mm;color:var(--ink);break-before:page;break-after:avoid;max-width:140mm}
h1 .n{font:700 40pt/1 'Caveat';color:var(--pen);margin-right:3.5mm;vertical-align:-1.5mm}
h1.first{break-before:auto}
h2{font:700 13.2pt/1.2 'InterD';margin:8mm 0 2.4mm;color:var(--ink);break-after:avoid;max-width:112mm}
h3{font:600 9.7pt/1.3 'Inter';margin:5mm 0 1.2mm;color:var(--ink);break-after:avoid;max-width:112mm}
p{margin:0 0 2.8mm;orphans:3;widows:3;max-width:112mm}
p.lead{font:500 11pt/1.5 'Inter';max-width:118mm;margin-bottom:5mm}
ul,ol{margin:0 0 3mm;padding-left:4.6mm;max-width:112mm} li{margin:0 0 1.3mm}
.pen{font-family:'Caveat';font-weight:700;color:var(--pen)}
.rev{color:var(--pencil);font-weight:600;font-size:.82em}
.soft{color:var(--soft)}
.ap{float:right;clear:right;width:46mm;margin:.4mm 0 3mm 0;font:500 12.4pt/1.13 'Caveat';color:var(--pen);break-inside:avoid}
.ap b{font-weight:700}
.w{clear:both;max-width:none}
table{border-collapse:collapse;width:100%;font-size:8.5pt;line-height:1.42;margin:2mm 0 4mm;clear:both}
th{font:600 7.9pt 'Inter';text-align:left;padding:1.4mm 3mm 1.4mm 0;border-bottom:.8pt solid var(--ink);vertical-align:bottom}
td{padding:1.8mm 3mm 1.8mm 0;border-bottom:.4pt solid rgba(42,38,56,.25);vertical-align:top}
td:first-child{font-weight:600}
tr{break-inside:avoid}
figure{margin:3mm 0 4.5mm;break-inside:avoid;max-width:112mm}
figure.fw{max-width:170mm;clear:both}
figure img{width:100%}
figcaption{font:400 7.7pt/1.42 'Inter';color:var(--soft);margin-top:1.6mm;max-width:112mm}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:5mm;clear:both;margin:3mm 0 4.5mm;break-inside:avoid}
.pair figure{margin:0}
.sum ul{padding:0;margin:0;max-width:none}
.sum li{list-style:none;display:flex;align-items:baseline;gap:2mm;margin:0;padding:1.15mm 0;max-width:150mm}
.sum .n{width:9mm;font:700 10.5pt 'Caveat';color:var(--pen)}
.sum .t{flex:0 1 auto}
.sum .d{flex:1;border-bottom:1pt dotted rgba(42,38,56,.4);transform:translateY(-1mm)}
.sum .p{font:500 8.6pt 'Inter'}
.sum .l1 .t{font:700 10.6pt 'InterD'}
.sum .l1{margin-top:2.2mm}
.sum .l2 .t{font-size:8.8pt;color:var(--soft)}
.sum .l2{padding-left:9mm}
.fp{display:grid;grid-template-columns:23mm 1fr;gap:5mm;margin:0 0 6mm;break-inside:avoid;max-width:150mm}
.fp .sp{display:flex;align-items:flex-end;justify-content:center;padding-bottom:1mm}
.fp .sp img{max-height:36mm;max-width:21mm;width:auto}
.fp h3{margin:0 0 .5mm;font:700 12.5pt/1.15 'InterD';max-width:none}
.fp .pap{font:500 8.2pt 'Inter';color:var(--soft);margin-bottom:1.8mm}
.fp p{margin:0 0 1.6mm;font-size:8.8pt;line-height:1.48;max-width:none}
.fp b{font-weight:600}
.gab{column-count:2;column-gap:8mm;clear:both}
.gab .e{break-inside:avoid;display:grid;grid-template-columns:4.2mm 1fr;gap:0 2mm;margin:0 0 3.2mm}
.gab .e svg{margin-top:1.5mm}
.gab .tt{font:700 12.4pt/1.05 'Caveat';color:var(--pen)}
.gab .tx{font-size:8pt;line-height:1.38;margin:.5mm 0 .6mm}
.gab .mt{font-size:7.1pt;line-height:1.34;color:var(--soft)}
.gab h3{break-after:avoid;margin:0 0 2mm}
.leg{display:grid;grid-template-columns:5mm 1fr;gap:1.4mm 2.4mm;align-items:start;margin:2mm 0 4mm;font-size:8.8pt;max-width:130mm}
.leg svg{margin-top:1.1mm}
.cols2{column-count:2;column-gap:8mm;clear:both}
.cols2 p,.cols2 ul{max-width:none}
.mda{display:grid;grid-template-columns:repeat(3,1fr);gap:7mm;margin:2mm 0 4mm;clear:both}
.mda h3{font:700 11pt 'InterD';margin:0 0 1.5mm}
.mda ul{padding-left:3.6mm;font-size:8.3pt;line-height:1.42;max-width:none}
.src li{font-size:8pt;line-height:1.4;margin-bottom:1mm}
.q{break-inside:avoid}
"""
SH = {
 'q': '<svg width="11" height="11" viewBox="0 0 11 11"><rect x="1.5" y="1.5" width="8" height="8" fill="#2a2638"/></svg>',
 'l': '<svg width="11" height="11" viewBox="0 0 11 11"><polygon points="5.5,0.6 10.4,5.5 5.5,10.4 0.6,5.5" fill="#2f4c86"/></svg>',
 'c': '<svg width="11" height="11" viewBox="0 0 11 11"><circle cx="5.5" cy="5.5" r="4.3" fill="#b23a2c"/></svg>',
 't': '<svg width="11" height="11" viewBox="0 0 11 11"><polygon points="5.5,1 10.3,9.9 0.7,9.9" fill="#6f6224"/></svg>'}
def ap(t): return '<aside class="ap">%s</aside>' % t
def fig(src, cap='', cls=''):
    return '<figure class="%s"><img src="%s%s">%s</figure>' % (cls, IMG, src, '<figcaption>%s</figcaption>' % cap if cap else '')
def h1(num, titulo, first=False):
    return '<h1 class="%s" data-toc="%s" data-n="%s"><span class="n">%s</span>%s</h1>' % ('first' if first else '', esc(titulo), num, num, esc(titulo))
def abre(num, titulo, resumo, cena, tocn):
    return f'''<section class="abre" data-toc="{esc(titulo)}" data-n="{tocn}">
<img src="{IMG}{cena}" style="width:210mm;height:112mm;object-fit:cover;object-position:center">
<div style="position:absolute;left:24mm;top:127mm"><img src="{IMG}t_{num}.png" style="height:13mm;width:auto"></div>
<div style="position:absolute;left:24mm;top:149mm;width:150mm"><div style="font:800 30pt/1.05 'InterD';color:#f6efe0;letter-spacing:-.01em">{esc(titulo)}</div>
<div style="margin-top:9mm;font:400 10.4pt/1.58 'Inter';color:#d8ccb4;max-width:116mm">{resumo}</div></div></section>'''
