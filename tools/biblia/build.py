import sys, re, subprocess, os
sys.path.insert(0,'/home/claude/bib')
from lib import *
import p1,p2,p3,p4
OUT='/home/claude/bib/build'
caps=[p1.cap_jogo(),p1.cap_ficha(),p1.cap_insp(),p1.cap_mda(),p1.cap_gdd(),
      p2.cap_narrativa(),p2.cap_level(),p2.cap_personagens(),
      p3.cap_1991(),p3.cap_1994(),p3.cap_1996(),p3.cap_resultados(),
      p4.cap_cultura(),p4.cap_arte(),p4.cap_ferr(),p4.cap_escrita(),p4.cap_estado()]
def doc(sum_items):
    body=p1.capa()+p1.sumario_html(sum_items)+p1.nota_leitura()+''.join(caps)
    return '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>O balcão da vó · Bíblia do jogo</title><style>'+CSS+'</style></head><body>'+body+'</body></html>'
def render(html,pdf):
    open(OUT+'/biblia.html','w',encoding='utf-8').write(html)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=b.new_page(); pg.goto('file://'+OUT+'/biblia.html'); pg.wait_for_timeout(1500)
        pg.pdf(path=pdf,prefer_css_page_size=True,print_background=True)
        b.close()
# itens do sumário: h1 e abre com data-toc
heads=[]
for c in caps:
    for m in re.finditer(r'<(?:h1|section)[^>]*data-toc="([^"]*)"[^>]*data-n="([^"]*)"',c):
        heads.append((m.group(2),m.group(1)))
print(len(heads),'cabeçalhos')
def pages(pdf):
    n=int(re.search(r'Pages:\s+(\d+)',subprocess.run(['pdfinfo',pdf],capture_output=True,text=True).stdout).group(1))
    txt=[subprocess.run(['pdftotext','-f',str(i),'-l',str(i),'-layout',pdf,'-'],capture_output=True,text=True).stdout for i in range(1,n+1)]
    return n,txt
from html import unescape
def lvl(n): return 2 if n.endswith('b') or n in('9d',) else 1
heads=[(n,unescape(t)) for n,t in heads]
# "Como ler" e "em detalhe" ficam fora do primeiro nível
def entries(pgs=None):
    out=[]
    for i,(n,t) in enumerate(heads):
        if t=='Como ler este documento': continue
        det=t.endswith('em detalhe')
        out.append((2 if det else 1,'' if det else n,('Gabarito completo' if det else t),pgs[i] if pgs else ''))
    return out
render(doc(entries()),OUT+'/p1.pdf')
n,txt=pages(OUT+'/p1.pdf')
pgs=[];start=3
for num,t in heads:
    key=re.escape(t[:16]); pg='?'
    pat=re.compile(r'^\s*(?:%s\s+)?%s'%(re.escape(re.sub('[a-z]','',num)),key),re.M)
    for i in range(start,n):
        if pat.search(txt[i]) and not txt[i].lstrip().startswith('Sumário'):
            pg=i+1; start=i+(0 if t.endswith('detalhe') else 0); break
    pgs.append(pg)
print(list(zip([h[1][:20] for h in heads],pgs)))
render(doc(entries(pgs)),OUT+'/biblia.pdf')
n2,txt2=pages(OUT+'/biblia.pdf'); print('páginas',n,n2)
