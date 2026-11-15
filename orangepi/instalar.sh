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
if [ -z "$NAV" ]; then echo "Não consegui instalar o Chromium. Tire uma foto desta tela."; exit 1; fi

echo "[2/5] Jogo"
mkdir -p "$JOGO"
wget -q --show-progress -O "$JOGO/index.html.novo" "$REPO/index.html"
wget -q --show-progress -O "$JOGO/rua96.html.novo" "$REPO/rua96.html"
mv "$JOGO/index.html.novo" "$JOGO/index.html"
mv "$JOGO/rua96.html.novo" "$JOGO/rua96.html"

echo "[3/5] Abrir o jogo"
cat > "$JOGO/abrir.sh" <<EOF
#!/bin/bash
# tela sempre acesa (a TV não apaga no meio do jogo)
xset s off 2>/dev/null; xset -dpms 2>/dev/null; xset s noblank 2>/dev/null
xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/dpms-enabled -s false 2>/dev/null
xfconf-query -c xfce4-screensaver -p /saver/enabled -s false 2>/dev/null
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

echo "[5/5] Teclado brasileiro e entrar sem senha"
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
echo "Para sair do jogo: Alt+F4 no teclado. Para abrir de novo: ícone 'A cidade que somos' na área de trabalho."
echo "Para atualizar o jogo: rode este mesmo comando outra vez."
echo
echo "Para testar agora, digite:  sudo reboot"
