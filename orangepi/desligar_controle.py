#!/usr/bin/env python3
# A cidade que somos — desligar o Orange Pi pelo controle.
# Segurar SELECT + START por 3 segundos desliga a placa com segurança (o jogo mostra a contagem na tela).
# Lê o controle pela interface de joystick do Linux (/dev/input/js*). Roda junto com o jogo (ver abrir.sh).
import glob, os, select, struct, subprocess, sys, time

SELECT, START = 8, 9          # numeração do Linux; é a mesma de controles genéricos e de PlayStation
SEGURAR = 3.0
EVENTO = struct.Struct('IhBB')  # tempo, valor, tipo, número

def desligar():
    for cmd in (['systemctl', 'poweroff'], ['sudo', '-n', '/usr/sbin/poweroff'], ['sudo', '-n', '/sbin/poweroff']):
        try:
            if subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                sys.exit(0)
        except Exception:
            pass

def vigiar(caminho):
    apertado = set(); desde = None
    with open(caminho, 'rb', buffering=0) as f:
        while True:
            pronto, _, _ = select.select([f], [], [], 0.2)
            if pronto:
                dado = f.read(EVENTO.size)
                if not dado or len(dado) < EVENTO.size:
                    return
                _, valor, tipo, num = EVENTO.unpack(dado)
                if tipo & 0x7f == 1:                      # botão (o bit 0x80 marca o estado inicial)
                    if valor: apertado.add(num)
                    else: apertado.discard(num)
            if SELECT in apertado and START in apertado:
                desde = desde or time.monotonic()
                if time.monotonic() - desde >= SEGURAR:
                    desligar(); desde = None
            else:
                desde = None

while True:
    controles = sorted(glob.glob('/dev/input/js*'))
    if not controles:
        time.sleep(2); continue
    try:
        vigiar(controles[0])
    except OSError:
        time.sleep(1)                               # controle desconectado: espera ele voltar
