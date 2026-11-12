#!/bin/bash
# uso: shotc.sh "query" saida.png [largura altura]
google-chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars --window-size=${3:-980},${4:-640} --virtual-time-budget=${5:-4000} --screenshot=$2 "file:///home/claude/balcao/game/index_casa_dev.html?$1" >/dev/null 2>&1
