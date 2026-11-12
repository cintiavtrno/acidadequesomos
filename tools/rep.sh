#!/bin/bash
google-chrome --headless=new --no-sandbox --disable-gpu --virtual-time-budget=2500 --dump-dom "file:///home/claude/balcao/game/index_dev.html?$1&report=1" 2>/dev/null | grep -o "<title>[^<]*</title>" | sed 's/<[^>]*>//g'
