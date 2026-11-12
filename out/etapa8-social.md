# Etapa 7 (spec) — Simulação social, autonomia e relações · seções 1–8
Status: implementado `sim/s16_social.js` (camada única sobre Relations/Memory e o mundo da rua). O arquivo da spec veio truncado no início da seção 9; **seções 9+ (conversas dinâmicas, expressividade, testes/entrega) aguardam o restante do texto.**
Tudo abaixo é PROPOSTA; itens `revisar` precisam de leitura cultural.

## 1 Personalidade
Cada morador (e Vó Áurea, fora do mapa) tem: traços 0..1 (sociável, reservado, desconfiado, pavio, paciência, curioso, prestativo, fofoqueiro), temperamento, interesses, preferências, hábitos, preocupações, opiniões por tema, objetivo, o que sabe e segredos. Sem caricatura: traços orientam *probabilidades*, nunca respostas fixas.
## 2 Necessidades (invisíveis)
comer, trabalhar, descansar, socializar, comprar, visitar, coletivo, resolver, informar. Crescem por minuto de jogo, escaladas por persona; são satisfeitas por conversar, sentar, jogar, comprar, pedir ajuda. Nunca aparecem como barras.
## 3 Decisão autônoma
Só decide quem está livre (parado, sentado fora do dominó ou entre trechos de patrulha). Utilidade = necessidade + relação + traços + ambiente; opções: conversar, comprar pão, descansar, observar o jogo, pedir ajuda, ficar. Anti-ciclo: histerese ("ficar" pesa), intervalo mínimo entre decisões, 20 min entre mudanças de atividade, 45 min de cooldown por tipo, prazo da próxima tarefa da agenda, assentos reservados pela agenda não são tomados. Quem joga dominó não sai no meio da mão.
## 4 Comportamentos espontâneos
Conversas de calçada (2–3 trocas, tema vindo de rumores/interesses), cumprimentos ao passar (frio se há tensão), compra rápida na padaria (encontro com Vó Áurea), observar a mesa, pedir ajuda (Cícera: corda do varal; Dandara: aviso; Tonho: troco) com aceite/recusa por confiança, prestatividade e tensão; discussão ou provocação na mesa; paz depois da mão; abandono de conversa por impaciência/prazo.
## 5 Relações
Por par e direção: afinidade, confiança, tensão (Relations) + amizade, intimidade, conflito, contatos, histórico. Ganhos com rendimento decrescente, teto diário (aff .07, conf .06), desconfiado confia devagar, pavio curto esquenta mais. Uma conversa ≈ +0,01.
## 6 NPC–NPC
Relações iniciais entre moradores independentes da Lia (ex.: Zé×Nonato com tensão leve; Cícera×Júnior forte; Lúcia com pouca confiança de quase todos). Evoluem sem a Lia.
## 7 Memória
Fatos tipados (conversou, ajudou, desentendimento, presenciou_discussao, recebeu_info, lia_ajudou, lia_conversou, lia_indevida…), com relevância; teto de 14 por pessoa, descarta o menos relevante. Efeitos: saudação à Lia muda conforme a lembrança, quem teve desentendimento evita/esfria, quem foi ajudado reconhece.
## 8 Informações e rumores
Catálogo `INFOS` (medição, Programa [revisar], reunião, fiado [revisar], obra, gato) + informações dinâmicas (discussões). Cada pessoa guarda: tipo (fato conhecido, testemunhada, ouvido de terceiros, suposição, boato, incorreta), versão (0 fiel → 2 distorcida), confiança, via. Compartilhar depende de relação, sigilo, traços e segredos; cada boca pode perder/mudar detalhe; testemunha mantém a sua versão e passa a duvidar. A Lia pergunta "O que andam comentando?", o que ouve vai ao caderno com o tipo; revelar sigilo ouvido de outro pode quebrar a confiança (`revelarA`, 25 min depois).
## Integração
`Sim.Rua.World.social`; salva em `salvar()` (`soc`); `EventSystem.count` agora usa contador (não o log de 600 eventos). Rua build agora embute s4 + s16.
## Testes
`tests/social_suite.js` (41), regressão rua 33, rua_ui 18, rua_ctx 7, casa 10, padaria 14, mundo 24 + 14.
## Limites / pendências
Sem UI para a Lia contar rumores a terceiros (existe em `revelarA`, sem botão). Visitas à padaria são abstratas (sem trocar de ambiente). Seções 9+ pendentes.
