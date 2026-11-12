# Etapa 8.5 — posicionamento dos objetos menores, da toalha dos sete meninos e da bandeira de Cosme e Damião.
# Estende quintal_data.py SEM alterar a planta aprovada (exceto o que está em AJUSTES). Unidades: metros do mundo.
import quintal_data as Q

# Nomes de zona da etapa 8.5 (mapeamento do rótulo antigo -> novo)
ZNOME = {'Z1': 'Cozinha e preparação', 'Z2': 'Serviço e distribuição', 'Z3': 'Mesa e refeição', 'Z4': 'Mangueira e convivência', 'Z5': 'Recepção', 'ZE': 'Sete meninos e altar de Cosme e Damião'}
ZONA_RECT = {'Z1': (0.0, 0.0, 7.6, 5.2), 'Z2': (9.8, 0.0, 18.0, 1.9), 'Z3': (10.3, 2.4, 20.1, 7.0), 'Z4': (18.6, 1.0, 27.8, 7.2), 'Z5': (0.0, 5.4, 7.6, 8.0), 'ZE': (8.1, 2.9, 10.3, 5.1)}
# zona de cada objeto já aprovado
ZONA_OBJ = {}
for i in ('F08','F09','F10','F11','D03'): ZONA_OBJ[i] = 'Z1'
for i in ('F12','M27'): ZONA_OBJ[i] = 'Z2'
for i in ['M%02d' % n for n in range(1, 14)]: ZONA_OBJ[i] = 'Z3'
for i in ('M14','M15','M16','M17','M18','M20','F14','D04'): ZONA_OBJ[i] = 'Z4'
for i in ('D01','D02'): ZONA_OBJ[i] = 'Z5'
ZONA_OBJ['M22'] = 'Z3'
for i in ('F01','F02','F03','F04'): ZONA_OBJ[i] = 'Arquitetura'
ALTURA = {o[0]: o[7] for o in Q.OBJ}

# ----------------------------------------------------------------------------- bandeira de Cosme e Damião (parede da casa, F01)
# Parede da casa: X 0–11, Z 0–4. Trecho livre = entre o puxadinho (X 7,6) e o canto (X 11), menos a porta de serviço (X 8,0–9,2; Z 0–2,3).
PAREDE_LIVRE_M2 = (11.0 - 7.6) * 4.0 - 1.2 * 2.3            # 10,84 m²
BANDEIRA = dict(id='B01', nome='Bandeira de Cosme e Damião (pano pendurado)', x0=9.325, x1=10.875, z0=1.35, z1=3.80, y=0.0,
                nota='pano vertical preso por duas varetas de madeira no topo e no pé; fixada na parede da casa (F01)')
BANDEIRA['area'] = (BANDEIRA['x1'] - BANDEIRA['x0']) * (BANDEIRA['z1'] - BANDEIRA['z0'])

# ----------------------------------------------------------------------------- toalha dos sete meninos
TOALHA = dict(id='E01', cx=4.9, cy=4.2, lado=3.0, buffer=0.4)      # quadrada 3,0 m, ocupando o chão livre à esquerda; faixa de respeito de 0,4 m ao redor
TOALHA['x0'], TOALHA['x1'] = TOALHA['cx'] - TOALHA['lado'] / 2, TOALHA['cx'] + TOALHA['lado'] / 2
TOALHA['y0'], TOALHA['y1'] = TOALHA['cy'] - TOALHA['lado'] / 2, TOALHA['cy'] + TOALHA['lado'] / 2
import math
RAIO_RODA, RAIO_PRATO = 1.15, 0.68
ANG = [-138, -96, -54, 54, 96, 138, 180]       # graus a partir da frente (+Y); roda aberta (lacuna de 108°) voltada para a câmera, escolhida por busca de menor oclusão
def polar(r, a): return (round(TOALHA['cx'] + r * math.sin(math.radians(a)), 3), round(TOALHA['cy'] + r * math.cos(math.radians(a)), 3))
MENINOS = ['junior', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6']
ROD = {m: polar(RAIO_RODA, a) for m, a in zip(MENINOS, ANG)}
PRATOS = {m: polar(RAIO_PRATO, a) for m, a in zip(MENINOS, ANG)}
# figurantes infantis (5–9 anos) para completar os sete meninos
CH_EXTRA = {f'm{i}': (f'Menino {i} (figurante)', h, 0.20) for i, h in zip(range(1, 7), (1.05, 1.12, 1.18, 1.10, 1.22, 1.15))}

# ----------------------------------------------------------------------------- objetos menores
# id, nome, zona, suporte (id do objeto onde apoia ou 'chão'), x, y (canto), w, d, h, z (base), orientação, colisão, ponto de uso (chave em STAND2), camada, estado inicial, uso
L5, L4, L3 = 'L5 objeto (ordem pelo y da base)', 'L4 piso/decalque', 'L3 parede'
S = [
 # Z1 — cozinha
 ('S01', 'Panela de vatapá (fogão)', 'Z1', 'F08', 3.12, 0.15, 0.34, 0.34, 0.22, 0.90, 'frente', False, 'F08', L5, 'no fogo, tampada', 'Mexer; provar'),
 ('S02', 'Caçarola de camarão e dendê (fogão)', 'Z1', 'F08', 3.60, 0.45, 0.30, 0.30, 0.16, 0.90, 'frente', False, 'F08', L5, 'no fogo, tampada', 'Mexer; provar'),
 ('S03', 'Tábua de corte', 'Z1', 'F09', 4.45, 0.20, 0.60, 0.40, 0.04, 0.90, 'frente', False, 'F09', L5, 'com cebolas picadas', 'Cortar'),
 ('S04', 'Bacia de quiabo cortado', 'Z1', 'F09', 5.15, 0.20, 0.40, 0.40, 0.14, 0.90, 'frente', False, 'F09', L5, 'cheia', 'Pegar quiabo'),
 ('S05', 'Bacia de camarão seco e castanha', 'Z1', 'F09', 5.65, 0.25, 0.30, 0.30, 0.10, 0.90, 'frente', False, 'F09', L5, 'cheia', 'Pegar ingredientes'),
 ('S06', 'Cesto de temperos (cebola, tomate, pimenta)', 'Z1', 'F09', 6.05, 0.20, 0.40, 0.40, 0.20, 0.90, 'frente', False, 'F09b', L5, 'cheio', 'Pegar temperos'),
 ('S07', 'Faca e colheres de pau (bandeja)', 'Z1', 'F09', 6.50, 0.20, 0.25, 0.25, 0.03, 0.90, 'frente', False, 'F09b', L5, 'arrumados', 'Pegar utensílios'),
 ('S08', 'Balde de água (borda do tanque)', 'Z1', 'F10', 1.20, 0.12, 0.35, 0.35, 0.30, 0.90, 'frente', False, 'F10', L5, 'cheio', 'Encher/lavar'),
 # Z2 — serviço (aparador F12: X 9,8–13,2 · Y 0,1–1,0 · topo 0,9)
 ('E12', 'Prato dos santos (primeira porção)', 'ZE', 'F12', 9.90, 0.55, 0.30, 0.30, 0.03, 0.90, 'frente', False, 'F12a', L5, 'servido; `revisar`', 'Observar; ninguém mexe'),
 ('E13', 'Vela em pires', 'ZE', 'F12', 10.30, 0.25, 0.14, 0.14, 0.12, 0.90, 'frente', False, 'F12a', L5, 'acesa; `revisar`', 'Observar'),
 ('E14', 'Vasinho com flores brancas', 'ZE', 'F12', 10.45, 0.55, 0.18, 0.18, 0.28, 0.90, 'frente', False, 'F12a', L5, 'com flores; `revisar`', 'Observar'),
 ('S12', 'Pilha de pratos', 'Z2', 'F12', 10.80, 0.60, 0.30, 0.30, 0.18, 0.90, 'frente', False, 'F12a', L5, 'cheia', 'Pegar prato'),
 ('S13', 'Travessa de caruru', 'Z2', 'F12', 11.15, 0.60, 0.50, 0.35, 0.08, 0.90, 'frente', False, 'F12a', L5, 'cheia', 'Servir'),
 ('S14', 'Travessa de vatapá', 'Z2', 'F12', 11.75, 0.60, 0.50, 0.35, 0.08, 0.90, 'frente', False, 'F12b', L5, 'cheia', 'Servir'),
 ('S15', 'Travessa de arroz e farofa', 'Z2', 'F12', 12.35, 0.60, 0.55, 0.35, 0.08, 0.90, 'frente', False, 'F12b', L5, 'cheia', 'Servir'),
 ('S16', 'Cuia com talheres', 'Z2', 'F12', 10.85, 0.25, 0.22, 0.22, 0.10, 0.90, 'frente', False, 'F12a', L5, 'cheia', 'Pegar talher'),
 ('S17', 'Bandeja de copos', 'Z2', 'F12', 11.20, 0.20, 0.50, 0.30, 0.10, 0.90, 'frente', False, 'F12a', L5, 'cheia', 'Pegar copo'),
 ('S18', 'Conchas e colheres de servir', 'Z2', 'F12', 11.85, 0.22, 0.30, 0.25, 0.10, 0.90, 'frente', False, 'F12b', L5, 'penduradas no pote', 'Pegar utensílio'),
 ('S19', 'Jarra de água', 'Z2', 'F12', 12.30, 0.22, 0.25, 0.25, 0.28, 0.90, 'frente', False, 'F12b', L5, 'cheia', 'Servir água'),
 # Z2 — tabuleiro de Nena (M27: X 17,0–17,9 · Y 0,2–0,9 · topo 0,9), só fase C; `revisar`
 ('S20', 'Tacho de dendê (tabuleiro)', 'Z2', 'M27', 17.05, 0.30, 0.35, 0.35, 0.18, 0.90, 'frente', False, 'M27', L5, 'quente; `revisar`', 'Observar; Nena atende'),
 ('S21', 'Bacia de massa coberta com pano', 'Z2', 'M27', 17.50, 0.30, 0.32, 0.32, 0.18, 0.90, 'frente', False, 'M27', L5, 'coberta; `revisar`', 'Observar'),
 # Z3 — mesa longa M01 (X 11,5–16,5 · Y 3,6–4,6 · topo 0,75) e mesinha M09
 ('S22', 'Toalha da mesa longa', 'Z3', 'M01', 11.50, 3.60, 5.00, 1.00, 0.01, 0.75, 'frente', False, 'M01', L5, 'estendida', 'Decorativa'),
 ('S23', 'Travessa central de caruru', 'Z3', 'M01', 13.55, 3.95, 0.55, 0.35, 0.08, 0.76, 'frente', False, 'M01', L5, 'cheia na fase C', 'Servir-se'),
 ('S24', 'Travessa de vatapá', 'Z3', 'M01', 14.25, 3.95, 0.55, 0.35, 0.08, 0.76, 'frente', False, 'M01', L5, 'cheia na fase C', 'Servir-se'),
 ('S25', 'Cesto de acarajé e banana frita', 'Z3', 'M01', 12.65, 3.95, 0.50, 0.35, 0.10, 0.76, 'frente', False, 'M01', L5, 'cheio na fase C', 'Servir-se'),
 ('S26', 'Jarra de água', 'Z3', 'M01', 15.00, 3.80, 0.22, 0.22, 0.26, 0.76, 'frente', False, 'M01', L5, 'cheia', 'Servir água'),
 ('S27', 'Jarra de suco', 'Z3', 'M01', 15.40, 3.80, 0.22, 0.22, 0.26, 0.76, 'frente', False, 'M01', L5, 'cheia', 'Servir suco'),
 ('S28', 'Pratos individuais (10 lugares)', 'Z3', 'M01', 11.90, 3.70, 0.30, 0.25, 0.03, 0.76, 'frente', False, 'M01', L5, 'postos na fase C; 10 pratos: ver tabela', 'Comer'),
 ('S29', 'Prato de cocada (mesinha das crianças)', 'Z3', 'M09', 17.95, 5.85, 0.35, 0.30, 0.05, 0.50, 'frente', False, 'M09', L5, 'com cocada (presente de Tonho)', 'Pegar cocada'),
 # Z4 — dominó
 ('S30', 'Peças de dominó', 'Z4', 'M14', 20.35, 4.20, 0.50, 0.35, 0.03, 0.75, 'frente', False, 'M14', L5, 'espalhadas na fase D', 'Jogar'),
 # ZE — toalha e sete meninos
 ('E01', 'Toalha de chita dos sete meninos', 'ZE', 'chão', TOALHA['x0'], TOALHA['y0'], TOALHA['lado'], TOALHA['lado'], 0.01, 0.0, 'frente', False, 'toalha', L4, 'guardada (fases A–B); posta em C1; recolhida em C/D', 'Área de respeito (sem passagem)'),
 ('E02', 'Bacia central de caruru', 'ZE', 'E01', TOALHA['cx'] - 0.20, TOALHA['cy'] - 0.20, 0.40, 0.40, 0.14, 0.01, 'frente', False, 'toalha', L5, 'cheia em C1', 'Repor (Zefa); observar'),
] + [
 (f'E{3+i:02d}', f'Pratinho de barro {i+1}', 'ZE', 'E01', PRATOS[m][0] - 0.14, PRATOS[m][1] - 0.14, 0.28, 0.28, 0.04, 0.01, 'frente', False, 'toalha', L5, 'servido em C1', 'Comer com as mãos')
 for i, m in enumerate(MENINOS)
] + [
 ('E10', 'Bandeja de doces e banana', 'ZE', 'E01', TOALHA['cx'] - 0.20, TOALHA['cy'] + 0.50, 0.40, 0.25, 0.05, 0.01, 'frente', False, 'toalha', L5, 'posta em C1', 'Pegar doce'),
 ('E11', 'Sete copinhos (um à direita de cada pratinho; grupo)', 'ZE', 'E01', TOALHA['cx'] + 0.20, TOALHA['cy'] + 0.45, 0.08, 0.08, 0.09, 0.01, 'frente', False, 'toalha', L5, 'postos em C1', 'Beber; Zefa serve o suco'),
]
# pontos de uso novos (x, y, direção)
STAND2 = dict(Q.STAND)
STAND2.update({'F12a': (11.2, 1.32, 'up'), 'F12b': (12.3, 1.32, 'up'), 'F09b': (6.2, 1.3, 'up'),                      # ajuste: lado a lado ao longo do aparador (antes F12a (10,8; 1,55) / F12b (12,2; 1,55))
               'banner': (10.1, 1.95, 'up'), 'toalha_zefa': (TOALHA['cx'], TOALHA['y1'] + 0.35, 'up'), 'M27': (17.45, 1.35, 'up'),
               'M09': (18.5, 5.0, 'down')})
# bandeira: área de interação (Lia olha/examina): faixa em frente ao aparador, a ≤ 2,2 m da parede
BANNER_VIEW = (9.0, 1.45, 11.3, 2.2)
