#!/bin/bash
# uso: shot.sh "query" saida.png [largura altura]
google-chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars --window-size=${3:-980},${4:-640} --virtual-time-budget=4000 --screenshot=$2 "file:///home/claude/balcao/game/index_dev.html?$1" >/dev/null 2>&1
