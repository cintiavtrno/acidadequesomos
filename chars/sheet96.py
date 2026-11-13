import sys, math
from PIL import Image
import drv96
def sheet(whos, anims, yaws, scale=6, out='/home/claude/out96/s.png'):
    cols = []
    for w in whos:
        for a, n in anims:
            for y in yaws:
                cols.append([drv96.fr(w, a, k, y) for k in range(n)])
    cw, ch = 40, 52
    mx = max(len(c) for c in cols)
    W = (cw + 2) * len(cols); H = (ch + 2) * mx
    im = Image.new('RGBA', (W, H), (214, 200, 170, 255))
    for i, c in enumerate(cols):
        for j, f in enumerate(c): im.alpha_composite(f, (i * (cw + 2), j * (ch + 2)))
    im = im.resize((W * scale, H * scale), Image.NEAREST); im.save(out); print(im.size)
if __name__ == '__main__':
    sheet(sys.argv[1].split(','), [(a.split(':')[0], int(a.split(':')[1])) for a in sys.argv[2].split(',')], [float(y) for y in sys.argv[3].split(',')], int(sys.argv[4]), sys.argv[5])
