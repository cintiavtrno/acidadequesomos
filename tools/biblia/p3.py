from lib import *
from p1 import tabela

NOMES = dict(D['nomes']); NOMES.update({'aurea': 'Vó Áurea', 'zefa': 'Dona Zefa', 'nena': 'Dona Nena', 'rita': 'Dona Rita', 'davi': 'Davi', 'caio': 'Caio', 'bia': 'Bia', 'm': 'um dos meninos', 'lugar': 'lugar', 'assist_b': 'a assistente de produção', 'assist_a': 'a assistente de produção'})
FASEQ = {'A': 'preparo (12h)', 'B': 'chegada (13h)', 'C1': 'crianças na toalha (14h)', 'C': 'mesa dos grandes (15h)', 'D': 'depois da mesa (16h30)'}
VIU = {'viu_jogo': 'ter assistido a uma partida de dominó', 'viu_medicao': 'ter visto Lúcia medir uma fachada', 'ouviu_programa': 'ter ouvido falar do Programa',
       'viu_aviso': 'ter lido o aviso no quadro', 'ouviu_reuniao': 'ter ouvido falar da reunião da associação', 'viu_varal': 'ter visto Cícera no varal', 'viu_gato': 'ter visto o gato',
       'viu_tonho': 'ter visto Tonho vender', 'viu_junior': 'ter visto Júnior', 'viu_banner': 'ter olhado a bandeira de Cosme e Damião', 'viu_mangueira': 'ter olhado a mangueira',
       'viu_toalha': 'ter olhado a toalha das crianças', 'viu_portao': 'ter olhado o portão de Dona Rita', 'viu_mesa': 'ter olhado a mesa dos adultos', 'viu_cocada': 'ter olhado as cocadas',
       'viu_oferenda': 'ter olhado a mesa da oferenda', 'ouviu_cicera': 'ter ouvido Dona Cícera'}
LABELS = {}
for src in ('src91', 'src94'):
    for k, v in D[src].items():
        for r in v: LABELS[(r['p'], r['t'])] = r['label']
for k, v in D['srcQ'].items():
    for r in v: LABELS[(r['p'], r['t'])] = r['label']
for k, v in D['src96'].items():
    for r in v: LABELS[(r['p'], r['t'])] = r['label']

def gate(q):
    if q in VIU: return VIU[q]
    if q.startswith('nivel:'): return 'ter confiança de nível ' + q.split(':')[1]
    if q.startswith('apos:'):
        _, p, t = q.split(':'); return 'ter conversado com %s sobre "%s"' % (NOMES.get(p, p), LABELS.get((p, t), t))
    return q

def ou(lst):
    if not lst: return ''
    if len(lst) == 1: return lst[0]
    return ', '.join(lst[:-1]) + ' ou ' + lst[-1]

FIO91 = {'mesa': 'a mesa de dominó', 'rua': 'a vida da rua', 'comercio': 'o comércio miúdo', 'programa': 'o Programa', 'medicao': 'a medição', 'olhares': 'os olhares de fora', 'associacao': 'a associação'}
CAT = {'central': 'central', 'complementar': 'complementar', 'exploratoria': 'exploratória'}
FIO96 = {'clipe': 'o clipe e a imagem da rua', 'fase2': 'a segunda fase do Programa', 'ficou': 'quem ficou e quem saiu', 'renda': 'o que um dia de evento rende'}

def via_src(srcs, fases_ok=False):
    linhas = []
    for r in srcs:
        s = '%s, assunto "%s"' % (NOMES.get(r['p'], r['p']), r['label'])
        q = r.get('quando') or []
        extra = []
        if r.get('nivel'): extra.append('confiança de nível %s' % ('/'.join(map(str, r['nivel'])) if isinstance(r['nivel'], list) else r['nivel']))
        if q: extra.append('abre com ' + ou([gate(x) for x in q]))
        if r.get('fases'): extra.append('fases ' + ', '.join(r['fases']))
        linhas.append(s + (' (' + '; '.join(extra) + ')' if extra else ''))
    return ' · '.join(linhas)

OAJUDA = {'kp_raimundo_agua', 'kp_vo_ajuda', 'kp_lucia_trena', 'kp_dandara_vez', 'kp_c_cafe', 'kp_c_sacola_pao', 'kp_c_cafe_juntos', 'kp_96_pedido'}
OOUVE = {'kp_raimundo_fiado', 'kp_raimundo_reza', 'kp_lucia_ouvir', 'kp_conversa_dl', 'kp_conversa_rd', 'kp_radio', 'kp_c_rotina'}
OOBJ = {'kp_calendario', 'kp_lousa'}

def entrada(forma, titulo, texto, meta, rev):
    return '<div class="e">%s<div><div class="tt">%s</div><div class="tx">%s%s</div><div class="mt">%s</div></div></div>' % (
        SH[forma], esc(titulo), esc(texto), ' <span class="rev">revisar</span>' if rev else '', meta)

def gab_rua91():
    h = ''
    for e in D['rua91']:
        m = e['meta']; k = e['id']; s = D['src91'].get(k)
        if s: forma = 'q'; via = via_src(s)
        else: forma = 'c'; via = 'examinar o objeto na rua'
        meta = '%s · %s, %s · disponível a partir do dia %s' % (via, CAT[m['cat']], FIO91[m['fio']], m['dia'])
        h += entrada(forma, e['t'], e['x'], meta, e['rev'])
    return h

def gab_ambiente(lista, tipo):
    h = ''
    for e in lista:
        k = e['id']; q = e.get('q')
        if q == 'lugar': forma = 'c'; meta = 'examinar o lugar'
        else:
            forma = 'l' if k in OAJUDA else ('t' if (k in OOUVE) else ('c' if k in OOBJ else 'q'))
            quem = NOMES.get(q, q) if q else ''
            meta = {'l': 'ajudar %s' % quem, 't': 'ouvir ou observar %s' % quem, 'c': 'examinar o objeto', 'q': 'conversar com %s' % quem}[forma]
        h += entrada(forma, e['t'], e['x'], meta, e['rev'])
    return h

def gab_rua94():
    h = ''
    for e in D['rua94']:
        k = e['id']; s = D['src94'].get(k)
        if s: forma = 'q'; via = via_src(s)
        else: forma = 'c'; via = 'examinar o objeto na rua'
        h += entrada(forma, e['t'], e['x'], via, e['rev'])
    return h

def gab_quintal():
    h = ''
    for e in D['quintal']:
        k = e['id']
        if k in D['srcQ']:
            forma = 'q'; via = via_src(D['srcQ'][k])
        elif k in D['ouveQ']:
            forma = 't'; via = 'ficar ouvindo ' + ou([NOMES.get(r['p'], r['p']) + ' na fase ' + r['f'] for r in D['ouveQ'][k]])
        else:
            forma = 'c'; via = 'examinar o objeto no quintal'
        h += entrada(forma, e['t'], e['x'], via, e['rev'])
    return h

def gab_96():
    h = ''
    for e in D['k96']:
        k = e['id']
        if k in D['src96']:
            forma = 'l' if k in OAJUDA else 'q'
            via = ' · '.join('%s, assunto "%s"' % (NOMES.get(r['p'], r['p']), r['label']) for r in D['src96'][k])
        else: forma = 'c'; via = 'examinar o objeto na rua'
        h += entrada(forma, e['t'], e['x'], via + ' · ' + FIO96[e['fio']], e['rev'])
    return h

def gab(titulo, itens, intro=''):
    return '<h2 class="w">%s</h2>%s<div class="gab">%s</div>' % (esc(titulo), ('<p>%s</p>' % intro if intro else ''), itens)

def legenda():
    return '<div class="leg"><span>%s Conversa</span><span>%s Escuta ou observação</span><span>%s Objeto ou lugar</span><span>%s Ajuda</span></div>' % (SH['q'], SH['t'], SH['c'], SH['l'])

def cap_1991():
    ab = abre('1991', '1991: o Programa foi anunciado', 'O rádio deu a notícia e a rua inteira ouviu. Ninguém sabe direito o que vai mudar. Lia tem 10 anos e passa as manhãs entre o balcão da vó e a calçada.', 'cena91.png', 9)
    return ab + f'''
<h1 data-toc="1991 em detalhe" data-n="9b" style="break-before:auto"><span class="n"></span>1991 em detalhe</h1>
<p class="lead">Quatro dias, sem pressa. A fase ensina quem é quem na rua, como a confiança entre vizinhos funciona e o que significam as medições, o quadro de avisos e a associação.</p>
<h2>O que a fase pede</h2>
<p>O objetivo é reunir informações sobre o Programa e sobre quem vive na rua. O jogador conversa com os moradores, observa, ajuda no que pedirem e anota. O relógio anda enquanto ele explora e para quando abre o caderninho. Quando entardece, a Lia sobe a escada da padaria e dorme. A confiança e as anotações seguem para o dia seguinte.</p>
{ap('Nenhum morador é vilão. Cada um tem uma razão para ficar do jeito que está.')}
<h2>Os quatro dias</h2>
{tabela(['Dia','O que acontece'], [
['1','A rua se apresenta. Mesa de dominó, varal de Cícera, cocada de Tonho, gato sem nome. As pistas desse dia são de convivência.'],
['2','A mesa se abre para quem ficou por perto: o lugar na mesa, a lata do bairro, os pontos de venda. À tarde chove. Cícera recolhe a roupa, Júnior e a mesa vão para a padaria, e a Lia pode ajudar com a roupa.'],
['3','Às 9h os técnicos colam o papel do Programa no quadro de avisos e Lúcia passa a marcar as portas a giz. Lia pode segurar a trena. É o dia das pistas centrais sobre medição, Programa e associação.'],
['4','Seu Raimundo conta do sobrado e Dona Bela dos olhares de fora. À tarde volta a chover e às 18h há reunião da associação, com cartaz no poste. Ao fim, a tela de 1991 mostra quantas anotações a Lia fez e oferece seguir para 1994.']])}
<h2>A missão do pão</h2>
<p>Seu Raimundo esquece o pão no balcão da padaria, entre a vitrine e a caixa. A Lia pode pegar a sacola, levar até o sobrado e entregar. A missão atravessa os dias, só acontece uma vez e, depois de entregue, nunca mais aparece. Seu Raimundo só chega em casa por volta das 10h, e o jogo avisa se a Lia chegar antes.</p>
<h2>O que o jogador leva</h2>
<p>Quem termina 1991 sabe que o Programa mede casas, que a associação existe para quem não tem advogado, que alguns moradores não foram consultados e que há gente de fora olhando a rua. Também conhece o jeito de cada pessoa da mesa, e essa familiaridade faz diferença em 1994.</p>
<h2 style="clear:both">Como ler o gabarito</h2>
<p>As listas abaixo trazem todas as pistas de 1991, divididas em três ambientes: a rua, a padaria e a casa de Seu Raimundo. Cada entrada mostra o título que aparece no caderninho, o texto, e como obtê-la.</p>
{legenda()}
<p>Para as pistas da rua, "disponível a partir do dia N" indica o dia em que a pista passa a existir. Depois disso ela fica disponível até o fim do dia 4. A categoria diz o peso da pista na história: <b>central</b>, <b>complementar</b> ou <b>exploratória</b>. As condições de abertura listam alternativas, e basta uma delas.</p>
{gab('A rua em 1991: 20 pistas', gab_rua91(), 'Neste ambiente a rua é o mapa inteiro. As pistas vêm de conversa com moradores e de objetos da calçada.')}
{gab('A padaria: 38 pistas', gab_ambiente(D['padaria'], 'p'), 'Na padaria a Lia atende a fila, ouve o balcão e examina os lugares. As pistas de pessoas vêm de quem entra e das ajudas que ela oferece. As pistas de lugar vêm dos objetos da cena.')}
{gab('A casa de Seu Raimundo: 20 pistas', gab_ambiente(D['casa'], 'c'), 'A casa abre quando Seu Raimundo recebe a Lia. As pistas de lugar mostram quem ele é sem que ele precise dizer.')}
'''

def cap_1994():
    ab = abre('1994', '1994: o caruru de Dona Zefa', 'Três anos depois, Lia tem 13 anos. De 1992 a 1995 o Programa acelerou: obra pesada, casa interditada, moradores saindo. Dona Zefa, que gosta do Programa, convida a rua para um caruru no quintal.', 'cena94.png', 10)
    return ab + f'''
<h1 data-toc="1994 em detalhe" data-n="10b" style="break-before:auto"><span class="n"></span>1994 em detalhe</h1>
<p class="lead">Um dia só, sem prazo. A fase mostra o efeito do Programa nas fachadas e nas famílias, e põe a rua inteira à mesa do quintal.</p>
<h2>O que a fase pede</h2>
<p>O jogo abre às 11h30, com a Lia ao lado do arco da padaria. A padaria, a rua e o sobrado estão abertos antes do caruru. O caruru começa ao meio-dia no quintal de Dona Zefa. Às 12h15 a vó deixa o balcão e vai para lá, e a Lia atende a padaria quando ela vai. A meta é anotar seis informações novas, e quando o essencial está feito aparece o botão para encerrar.</p>
{ap('Em 1994 a rua é a mesma. Mudaram as fachadas, as portas fechadas e o que as pessoas contam.')}
<h2>O que mudou na rua</h2>
<p>Um aviso de vistoria e uma fita zebrada cobrem a porta do sobrado de Seu Raimundo, com um X de tinta laranja. A casa verde está tapada e cercada de andaime, com placa de obra de 1994. A padaria ganhou uma plaquinha em português e inglês e um aviso de aluguel novo na vidraça. A associação pendurou uma faixa: AQUI MORA GENTE. O cartaz do Pelourinho Dia & Noite anuncia shows de graça nos largos.</p>
<div class="pair">{fig('cena94.png','A rua em 1994: sobrado com tábua e marca de tinta, plaquinha BREAD e PÃO na padaria.')}{fig('cenaq.png','O quintal de Dona Zefa, com a mesa posta, a casa ao fundo e a mangueira à direita.')}</div>
<h2>As cinco fases do caruru</h2>
{tabela(['Fase','Hora','O que acontece'], [
['A, preparo','12h','Dona Zefa corta o quiabo, Dona Nena cuida da vela e do azeite. Poucos chegaram.'],
['B, chegada','13h','A rua chega. A bandeira de Cosme e Damião está pendurada e a oferenda posta.'],
['C1, crianças','14h','Sete meninos sentam na toalha e comem primeiro, com a mão. Os adultos esperam.'],
['C, mesa dos grandes','15h','Os adultos comem. Aparece a conversa sobre o Programa, o turista e a casa de cada um.'],
['D, depois da mesa','16h30','A conversa continua. Ouvem-se os desacordos entre Zefa e Raimundo e entre Dandara e Lúcia.']])}
<h2>A mensagem da fase</h2>
<p>A aposta do Programa nesse momento é que turistas do Brasil e de fora sustentem sozinhos o comércio da rua. Quem sente que a aposta não basta (Tonho, Áurea, Zé, Bela, Lúcia) deixa uma pista de que a próxima fase trocará a estratégia por eventos culturais para moradores de Salvador. Dona Zefa fala a favor do Programa, porque a casa dela foi restaurada e devolvida ao dono. <span class="rev">revisar</span></p>
<h2 style="clear:both">Gabarito de 1994</h2>
{legenda()}
<p>Na rua de 1994 a categoria das pistas não é separada em central e complementar. No quintal, cada assunto existe só em certas fases do caruru e alguns dependem de ter olhado um objeto ou de já ter conversado com a pessoa. As condições listam alternativas, e basta uma delas.</p>
{gab('A rua em 1994: 25 pistas', gab_rua94(), 'Aqui estão as pistas que a Lia pode juntar na rua e na padaria antes do caruru, e as que dependem de objetos novos de 1994: o aviso, a placa, a faixa, o tapume e o cartaz.')}
{gab('O quintal: 44 pistas', gab_quintal(), 'No quintal as pistas vêm de conversa por fase, de objetos examinados e de falas ouvidas sem perguntar.')}
'''

def cap_1996():
    ab = abre('1996', '1996: o dia da gravação', 'Dois anos depois, a rua fecha para a gravação de um clipe. O Programa entra na segunda fase e muda a conta. Lia tem 15 anos e ajuda a vó a fechar o dia.', 'cena96.png', 11)
    miss = D['miss96']
    lig = D['lig96']
    lig_rows = []
    for l in lig:
        mem = ', '.join(l.get('mem', [])) or 'nenhuma, vale só pelo que se aprendeu hoje'
        lig_rows.append([', '.join(l['se']), mem, esc(l['t']) + (' <span class="rev">revisar</span>' if l.get('rev') else '')])
    return ab + f'''
<h1 data-toc="1996 em detalhe" data-n="11b" style="break-before:auto"><span class="n"></span>1996 em detalhe</h1>
<p class="lead">Um dia parado, sem relógio. A fase ensina o que as anteriores não ensinaram: a rua como imagem, a segunda fase do Programa, quem ficou e quem saiu e o que um dia de evento rende.</p>
<h2>O que a fase pede</h2>
<p>A rua está fechada para a gravação de um clipe. A produção veio de fora, com equipe, câmera e grade, e a polícia fecha as esquinas. O clipe fica fora do Programa e mostra a rua que ele quer mostrar: pintada, policiada e desejada. A Lia fecha o dia depois de cumprir três missões, em qualquer ordem.</p>
{fig('final_palco.png','Palco da gravação, com percussionistas, câmeras e plateia atrás das barreiras.', 'fw')}
<h2>As três missões</h2>
{tabela(['Missão','Passos'], [[esc(m['titulo']), '<br>'.join('%d. %s' % (i + 1, esc(t)) for i, t in enumerate(m['txt']))] for m in miss])}
<p>Com as três feitas, Dona Áurea fecha o dia e aparece a tela final com as ligações. O botão de pular existe também em 1996. Quem pula recebe um resumo do que a rua ia contar.</p>
<h2>O que 1996 ensina</h2>
<ul>
<li><b>A rua como imagem.</b> O monitor da produção mostra o palco e a parede pintada, e o prédio de tijolo de Dona Rita não entra no quadro.</li>
<li><b>A segunda fase do Programa.</b> De 1996 a 1999 a obra pesada diminui, o órgão procura dinheiro de fora e aposta em eventos para a classe média de Salvador. <span class="rev">revisar</span></li>
<li><b>Quem ficou e quem saiu.</b> Dona Bela atende cinco casas, a associação tem lista menor, Seu Raimundo olha a rua pela fresta.</li>
<li><b>O que um dia de evento rende.</b> Tonho vende num dia o que vende de terça a quinta, e no dia seguinte o movimento volta ao normal.</li>
</ul>
<p>O texto de 1996 não cita pessoa real. O cantor aparece como figurante sem nome e sem fala.</p>
<h2 style="clear:both">Gabarito de 1996</h2>
{legenda()}
{gab('A rua em 1996: 20 pistas', gab_96(), 'Todas as pistas têm um fio. As que nascem de conversa abrem na primeira vez que o jogador escolhe o assunto, com exceção das que dependem de uma missão.')}
<h2 class="w">As 12 ligações com 1991 e 1994</h2>
<p>A página de 1996 lê o que a Lia anotou nos jogos anteriores. Cada ligação aparece no caderno quando o jogador tem as anotações de 1996 da primeira coluna e, quando há, uma das anotações antigas da segunda.</p>
{tabela(['Anotações de 1996 que precisam existir','Anotações antigas que ativam','Texto da ligação'], lig_rows, 'w')}
<p>Duas ligações não pedem memória e valem só pelo que o jogador aprendeu no dia. As outras dez só aparecem para quem jogou as fases anteriores. Em partidas com todas as anotações, são 12 ligações. Em partidas novas, são 2.</p>
'''

def cap_resultados():
    return h1(12, 'Resultados possíveis') + f'''
<p class="lead">O jogo não tem finais alternativos. A mesma história acontece para todos, e o que muda de uma partida para outra é o que o jogador entendeu e o que o caderno mostra no fim.</p>
<h2>O que está definido hoje</h2>
{tabela(['Fase','Como termina','O que varia entre partidas'], [
['1991','Depois do quarto dia, a tela de 1991 diz quantas anotações a Lia fez e oferece seguir para 1994.','Quais pistas foram achadas, quais pessoas ganharam confiança e se a missão do pão foi entregue.'],
['1994','O jogador encerra a fase quando as anotações essenciais estão feitas. A tela diz que o turista não bastou e que a próxima fase tentará eventos culturais, e oferece seguir para 1996 ou recomeçar.','Quais das 44 anotações do quintal e das 25 da rua o jogador juntou, em que fases do caruru.'],
['1996','Dona Áurea fecha o dia e a tela final mostra o resumo e as ligações. A fase seguinte ainda não existe neste protótipo.','Quais das 20 pistas do dia e quais das 12 ligações o caderno escreveu.']])}
<h2>Perfis de jogador em 1991</h2>
<p>O repositório simula três perfis de jogador que não conhecem o gabarito. Os números abaixo vêm de 20 partidas simuladas por perfil e cobrem a rua de 1991, com as 20 pistas e as 7 centrais. O modelo põe a Lia ao lado do alvo sem andar, então o tempo de caminhada fica de fora.</p>
{tabela(['Perfil','Como joga','Pistas de 20','Centrais de 7','Fios entendidos de 4'], [
['Livre','Explora ao acaso: conversa, examina objetos, afaga o gato, senta à mesa.','16,6','5,0','3 ou 4 em todas as partidas (4 em 12 de 20)'],
['Conversador','Vai a quem foi menos ouvido, faz uma pergunta por visita e não examina objetos.','16,0','6,0','4 em todas as partidas'],
['Observador','Só examina objetos e conversa com três pessoas.','9,7','2,8','3 ou 4 em todas as partidas (4 em 6 de 20)']])}
{ap('O teste exige que quase toda partida entenda 3 dos 4 fios e que nenhuma fique abaixo de 2.')}
<p>Dois resultados chamam atenção. O conversador não acha nenhuma das quatro pistas de objeto, mas chega a 6 das 7 centrais. O observador, que só examina objetos, sai com pelo menos a pista do quadro de avisos, que conta o essencial do Programa e da reunião.</p>
<h2>Leituras que o jogo produz</h2>
<p>Os perfis acima são simulados. As cinco leituras a seguir descrevem o que o desenho do jogo deve produzir em quem joga, e ainda não foram observadas com jogadores reais.</p>
{tabela(['Leitura','Como joga','O que entende','O que perde'], [
['Observador','Olha a rua e os objetos, fala pouco.','O Programa e a reunião, pelo quadro. Os olhares de fora.','A confiança dos moradores e o que eles contam de si.'],
['Conversador','Pergunta a todos, volta a quem respondeu pouco.','A história principal inteira e o jeito de cada pessoa.','Os detalhes de objetos e lugares.'],
['Explorador','Vai de objeto em objeto, de casa em casa, entra em tudo.','A casa de Seu Raimundo e a padaria em profundidade.','Os assuntos que só abrem com confiança.'],
['Completista','Quer tudo. Repete dias e anota tudo.','As 167 pistas de 1991 e 1994 e as 12 ligações de 1996.','Nada, mas pode perder a calma da rua.'],
['Quem pulou','Usa o botão de pular em qualquer dia ou fase.','O que anotou até ali. Em 1996 recebe o resumo do que a rua ia contar.','As ligações, que dependem das anotações antigas.']])}
<p>O total de 167 pistas soma as 20 da rua de 1991, as 38 da padaria, as 20 da casa, as 25 da rua de 1994 e as 44 do quintal, mais as 20 de 1996.</p>
<h2>Como o jogador vê o resultado</h2>
<p>Em 1991 e 1994 o jogo diz ao jogador, com palavras, se a rua ainda tem o que contar ou se já contou o essencial. Em 1996 ele mostra "Anotações de hoje: N de 20" e, quando a Lia tem memória, o número de ligações com 1991 e 1994.</p>
<h2>O que falta decidir</h2>
<ul>
<li>Uma tela final da história inteira, depois de 1996, que ainda não existe.</li>
<li>Se algum comportamento da Lia deve mudar o rumo de uma cena, o que hoje não acontece.</li>
<li>Se o jogo deve testar leituras com jogadores reais e ajustar o peso das pistas.</li>
</ul>
'''
