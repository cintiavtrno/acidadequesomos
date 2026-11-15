#!/bin/bash
# A cidade que somos — instalador para o Orange Pi (Armbian com área de trabalho Xfce)
# Uso, no Terminal do Orange Pi (uma vez só):
#   curl -sL https://raw.githubusercontent.com/cintiavtrno/acidadequesomos/main/orangepi/instalar.sh | bash
# Faz: instala o Chromium, baixa o jogo, liga o login automático, faz o jogo abrir em tela cheia quando a placa liga
# e impede a TV de apagar a tela. Rodar de novo atualiza o jogo para a versão mais nova do GitHub.
set -e
REPO="https://raw.githubusercontent.com/cintiavtrno/acidadequesomos/main"
EU="$(id -un)"
JOGO="$HOME/jogo"

if [ "$EU" = "root" ]; then
  echo "Rode com o seu usuário (não como root). Abra o Terminal normal e cole o comando de novo."
  exit 1
fi

echo
echo "== A cidade que somos: instalando no Orange Pi =="
echo "Se pedir senha, é a do seu usuário (as letras não aparecem enquanto digita)."
echo

echo "[1/5] Navegador"
if ! command -v chromium >/dev/null 2>&1 && ! command -v chromium-browser >/dev/null 2>&1; then
  # sem perguntas no meio (uma pergunta do apt "comia" o resto deste script quando ele vem pelo curl)
  APT="sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confold"
  $APT update </dev/null
  $APT install chromium </dev/null || $APT install chromium-browser </dev/null
fi
NAV="$(command -v chromium || command -v chromium-browser)"
# esconde o ponteiro do mouse parado em cima do jogo
if ! command -v unclutter >/dev/null 2>&1; then
  sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confold install unclutter </dev/null || true
fi
if [ -z "$NAV" ]; then echo "Não consegui instalar o Chromium. Tire uma foto desta tela."; exit 1; fi

echo "[2/5] Jogo"
mkdir -p "$JOGO"
wget -q --show-progress -O "$JOGO/index.html.novo" "$REPO/index.html"
wget -q --show-progress -O "$JOGO/rua96.html.novo" "$REPO/rua96.html"
mv "$JOGO/index.html.novo" "$JOGO/index.html"
mv "$JOGO/rua96.html.novo" "$JOGO/rua96.html"
wget -q -O "$JOGO/desligar_controle.py" "$REPO/orangepi/desligar_controle.py" && chmod +x "$JOGO/desligar_controle.py"

echo "[3/5] Abrir o jogo"
cat > "$JOGO/abrir.sh" <<EOF
#!/bin/bash
# tela sempre acesa (a TV não apaga no meio do jogo)
xset s off 2>/dev/null; xset -dpms 2>/dev/null; xset s noblank 2>/dev/null
xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/dpms-enabled -s false 2>/dev/null
xfconf-query -c xfce4-screensaver -p /saver/enabled -s false 2>/dev/null
# TV em 1280x720: a placa monta menos pixels por quadro e a TV amplia sozinha (o jogo é pixel art, não perde nitidez)
SAIDA=\$(xrandr 2>/dev/null | awk '/ connected/{print \$1; exit}')
[ -n "\$SAIDA" ] && xrandr 2>/dev/null | grep -q ' 1280x720' && xrandr --output "\$SAIDA" --mode 1280x720 2>/dev/null
command -v unclutter >/dev/null 2>&1 && (pkill unclutter 2>/dev/null; unclutter -idle 1 -root >/dev/null 2>&1 &)
# SELECT + START por 3 s desliga a placa (programa que vigia o controle)
pkill -f desligar_controle.py 2>/dev/null; python3 "$JOGO/desligar_controle.py" >/dev/null 2>&1 &
sleep 3
exec "$NAV" --kiosk --noerrdialogs --disable-session-crashed-bubble --disable-infobars \\
  --check-for-update-interval=31536000 --autoplay-policy=no-user-gesture-required \\
  --password-store=basic "file://$JOGO/index.html"
EOF
chmod +x "$JOGO/abrir.sh"
# atalho na área de trabalho, para abrir de novo depois de sair com Alt+F4
mkdir -p "$HOME/Desktop" "$HOME/.local/share/applications"
ATALHO="[Desktop Entry]
Type=Application
Name=A cidade que somos
Exec=$JOGO/abrir.sh
Terminal=false
Categories=Game;"
printf '%s\n' "$ATALHO" > "$HOME/.local/share/applications/a-cidade-que-somos.desktop"
printf '%s\n' "$ATALHO" > "$HOME/Desktop/a-cidade-que-somos.desktop"
chmod +x "$HOME/Desktop/a-cidade-que-somos.desktop"
command -v gio >/dev/null 2>&1 && gio set "$HOME/Desktop/a-cidade-que-somos.desktop" metadata::trusted true 2>/dev/null || true

echo "[4/5] Abrir sozinho quando ligar"
mkdir -p "$HOME/.config/autostart"
printf '%s\n' "$ATALHO" > "$HOME/.config/autostart/a-cidade-que-somos.desktop"

echo "[5/5] Teclado brasileiro, entrar sem senha e desligar pelo controle"
# o controle visto como joystick do Linux (/dev/input/js0) e permissão para lê-lo e para desligar sem senha
sudo modprobe joydev 2>/dev/null || true
grep -qx joydev /etc/modules 2>/dev/null || echo joydev | sudo tee -a /etc/modules >/dev/null
sudo usermod -aG input "$EU" 2>/dev/null || true
printf '%s ALL=(root) NOPASSWD: /usr/sbin/poweroff, /sbin/poweroff\n' "$EU" | sudo tee /etc/sudoers.d/a-cidade-que-somos >/dev/null
sudo chmod 440 /etc/sudoers.d/a-cidade-que-somos
sudo visudo -cf /etc/sudoers.d/a-cidade-que-somos >/dev/null 2>&1 || sudo rm -f /etc/sudoers.d/a-cidade-que-somos
# teclado ABNT2 (ç, acentos, dois-pontos no lugar certo) também depois de reiniciar
if [ -f /etc/default/keyboard ]; then
  sudo sed -i 's/^XKBMODEL=.*/XKBMODEL="abnt2"/; s/^XKBLAYOUT=.*/XKBLAYOUT="br"/; s/^XKBVARIANT=.*/XKBVARIANT=""/' /etc/default/keyboard
fi
command -v localectl >/dev/null 2>&1 && sudo localectl set-x11-keymap br abnt2 2>/dev/null || true
if [ -d /etc/lightdm ]; then
  sudo mkdir -p /etc/lightdm/lightdm.conf.d
  printf '[Seat:*]\nautologin-user=%s\nautologin-user-timeout=0\n' "$EU" | sudo tee /etc/lightdm/lightdm.conf.d/22-armbian-autologin.conf >/dev/null
fi

echo
echo "Pronto. A partir de agora é só ligar o Orange Pi na TV: o jogo abre sozinho."
echo "Para desligar só com o controle: segure SELECT + START por 3 segundos."
echo "Para sair do jogo: Alt+F4 no teclado. Para abrir de novo: ícone 'A cidade que somos' na área de trabalho."
echo "Para atualizar o jogo: rode este mesmo comando outra vez."
echo
echo "Para testar agora, digite:  sudo reboot"
