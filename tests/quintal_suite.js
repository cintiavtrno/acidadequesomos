const fs=require('fs');const L=(...a)=>fs.appendFileSync('/tmp/o.txt',a.join(' ')+'\n');
const Q=require('/home/claude/balcao/quintal/quintal.js'); const D=require('/home/claude/balcao/quintal/qdata.json'); D.SPEED={ze:0.57,nonato:1.1,junior:1.7};
L('start');const s=new Q.Sim(D);L('sim ok'); let ok=0,bad=[];
L('livre m2', (s.base.reduce((a,v)=>a+(v>0.25?1:0),0)*0.01).toFixed(1));
// 1. todos os assentos e pontos de uso alcançáveis da soleira (Lia e NPC)
(x=>0)("reach");const src=[4.5,7.5];
for(const [id,v] of Object.entries(D.SEATS)){ for(const [nm,r,l] of [['Lia',0.25,true],['NPC',0.30,false]]){ if(!s.achar(s.base,src,v[3],r,l)) bad.push(id+'/'+nm);} }
for(const [k,v] of Object.entries(D.STAND)){ if(k==='toalha_zefa'||k==='telhado') continue; if(!s.achar(s.base,src,[v[0],v[1]],0.25,true)) bad.push('stand '+k); }
(x=>0)("reach");L("inalcançáveis:",bad);
// 2. fase C1: toalha bloqueia; Lia chega ao banner
s.fase('C1',true); const p=s.achar(s.c1,src,[10.1,1.95],0.25,true); L('C1 banner', !!p, p&&p.length);
const T=D.TOALHA; L('centro andável na C1?', s.walk(s.c1,T.cx,T.cy,0.25,true));
// 3. transição A -> B -> C1 -> C -> D com NPCs andando; checar presos
for (const f of ['B','C1','C','D','A']) { s.fase(f,false); let t=0; while(t<240){ s.update(0.1); t+=0.1; } 
  const pres=Object.values(s.npcs).filter(n=>n.vis&&(n.state==='preso')).map(n=>n.id); const and=Object.values(s.npcs).filter(n=>n.vis&&n.state==='andando').map(n=>n.id);
  const vis=Object.values(s.npcs).filter(n=>n.vis).length; L(f,'visíveis',vis,'presos',pres,'andando',and); }
