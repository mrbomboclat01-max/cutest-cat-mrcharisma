#!/usr/bin/env python3
"""Kawaii tabby kitten — cutest-cat-01 entry for make.fun."""
import math, struct, zlib, os

S = 512
buf = [[(0, 0, 0)] * S for _ in range(S)]

# ── helpers ───────────────────────────────────────────────────────────
def cc(v): return max(0, min(255, round(v)))
def lc(a, b, t): return tuple(cc(a[k]*(1-t)+b[k]*t) for k in range(3))

def put(x, y, col, a=1.0):
    if 0 <= x < S and 0 <= y < S:
        xi, yi = int(x), int(y)
        if a >= 0.999:
            buf[yi][xi] = col
        else:
            q = buf[yi][xi]
            buf[yi][xi] = (cc(q[0]*(1-a)+col[0]*a),
                           cc(q[1]*(1-a)+col[1]*a),
                           cc(q[2]*(1-a)+col[2]*a))

def disk(cx, cy, r, col, aa=1.2):
    ri2, ro = (r-aa)*(r-aa), r+aa
    ro2 = ro*ro
    bx0 = max(0, int(cx-ro)); bx1 = min(S, int(cx+ro)+1)
    by0 = max(0, int(cy-ro)); by1 = min(S, int(cy+ro)+1)
    for y in range(by0, by1):
        dy2 = (y-cy)*(y-cy)
        for x in range(bx0, bx1):
            d2 = (x-cx)*(x-cx)+dy2
            if d2 < ri2:
                put(x, y, col)
            elif d2 < ro2:
                put(x, y, col, (ro-math.sqrt(d2))/(2*aa))

def oval(cx, cy, rx, ry, col, aa=1.2):
    bx0 = max(0, int(cx-rx-2)); bx1 = min(S, int(cx+rx+2))
    by0 = max(0, int(cy-ry-2)); by1 = min(S, int(cy+ry+2))
    e = aa/min(rx, ry); lo = 1-e; hi = 1+e
    for y in range(by0, by1):
        for x in range(bx0, bx1):
            d = math.sqrt(((x-cx)/rx)**2+((y-cy)/ry)**2)
            if d < lo:
                put(x, y, col)
            elif d < hi:
                put(x, y, col, (hi-d)/(2*e))

def tri(pts, col):
    s = sorted(pts, key=lambda p: p[1])
    (ax,ay),(bx,by),(cx,cy) = s
    def xi(y, y0, x0, y1, x1):
        return x0 if y1==y0 else x0+(x1-x0)*(y-y0)/(y1-y0)
    for y in range(max(0, int(ay)), min(S, int(cy)+1)):
        xl = xi(y,ay,ax,by,bx) if y<=by else xi(y,by,bx,cy,cx)
        xr = xi(y,ay,ax,cy,cx)
        if xl>xr: xl,xr=xr,xl
        for x in range(max(0, int(xl)), min(S, int(xr)+1)):
            put(x, y, col)

def stroke(x0, y0, x1, y1, col, w=2.0):
    dx, dy = x1-x0, y1-y0
    l = math.hypot(dx,dy) or 1
    n = max(int(l)+1, 3)
    for i in range(n+1):
        t = i/n
        disk(x0+dx*t, y0+dy*t, w/2, col, aa=0.5)

# ── palette ───────────────────────────────────────────────────────────
F  = (255, 164,  58)   # orange fur
FD = (205, 110,  15)   # dark tabby stripe
FL = (255, 202, 120)   # light fur / highlight
EP = (255, 170, 190)   # ear inner pink
SC = (250, 247, 238)   # eye sclera
IR = (190, 152,  12)   # golden amber iris
PU = ( 10,   6,   2)   # pupil
WH = (255, 255, 255)   # sparkle white
NO = (255, 108, 150)   # nose pink
MO = (148,  55,  12)   # mouth
WK = (240, 236, 224)   # whisker cream
BL = (255, 138, 170)   # blush rose
PT = (252, 250, 243)   # petal off-white
YL = (255, 220,  15)   # daisy center yellow
GR = (100, 165,  60)   # leaf green
DK = ( 18,  10,   3)   # dark outline

# ── BACKGROUND ────────────────────────────────────────────────────────
for y in range(S):
    for x in range(S):
        t = min(1., math.hypot(x-256, y-285)/295)
        buf[y][x] = lc((255,245,248), (255,178,202), t)

# ── BODY & CHEST ──────────────────────────────────────────────────────
oval(256, 452, 112, 72, F)
oval(256, 462, 68, 50, FL)   # lighter chest patch

# ── EARS (drawn before head so head overlaps base) ────────────────────
tri([(108,183),(172,190),(118,70)], F)       # left outer ear
tri([(116,178),(162,184),(122,93)], EP)      # left inner ear
tri([(404,183),(340,190),(394,70)], F)       # right outer ear
tri([(396,178),(350,184),(390,93)], EP)      # right inner ear

# ── HEAD ──────────────────────────────────────────────────────────────
HX, HY, HR = 256, 258, 175
disk(HX, HY, HR, F)
oval(HX, HY-52, 90, 62, FL)   # lighter forehead highlight

# ── TABBY STRIPES (M-mark on forehead) ───────────────────────────────
for x0,y0,x1,y1 in [(221,110,232,165),(256,100,256,162),(291,110,280,165)]:
    stroke(x0, y0, x1, y1, FD, w=10)

# ── EYES ──────────────────────────────────────────────────────────────
ELX, ERX, EY = 190, 322, 220
# White sclera
disk(ELX, EY, 51, SC); disk(ERX, EY, 51, SC)
# Golden iris
disk(ELX, EY, 43, IR); disk(ERX, EY, 43, IR)
# Iris inner radial highlight (brightens upper iris)
oval(ELX, EY-10, 18, 20, lc(IR, WH, 0.35))
oval(ERX, EY-10, 18, 20, lc(IR, WH, 0.35))
# Pupil (vertical oval for dreamy look)
oval(ELX, EY, 15, 32, PU); oval(ERX, EY, 15, 32, PU)
# Dark limbal ring and lash arc at top of each eye
for ex, ey in [(ELX,EY),(ERX,EY)]:
    ri, ro = 41., 52.
    ri2, ro2 = ri*ri, ro*ro
    bx0 = max(0, int(ex-ro-1)); bx1 = min(S, int(ex+ro+1))
    by0 = max(0, int(ey-ro-1)); by1 = min(S, int(ey))
    for yy in range(by0, by1):
        dy2 = (yy-ey)*(yy-ey)
        for xx in range(bx0, bx1):
            d2 = (xx-ex)*(xx-ex)+dy2
            if ri2 <= d2 <= ro2:
                d = math.sqrt(d2)
                a = min(1., (d-ri)/6)*0.9
                put(xx, yy, DK, a)
# Sparkle highlights
disk(ELX+15, EY-14, 12, WH); disk(ERX+15, EY-14, 12, WH)
disk(ELX-10, EY+13,  5, WH); disk(ERX-10, EY+13,  5, WH)
# Small star sparkle in upper-right of iris
for ex, ey in [(ELX,EY),(ERX,EY)]:
    sx, sy = ex+20, ey-20
    for arm in range(4):
        ang = math.radians(arm*45)
        stroke(sx, sy, sx+math.cos(ang)*7, sy+math.sin(ang)*7, WH, w=1.5)

# ── NOSE ──────────────────────────────────────────────────────────────
tri([(256,278),(244,267),(268,267)], NO)
disk(256, 278, 5, NO, aa=0.8)

# ── MOUTH ─────────────────────────────────────────────────────────────
# Center philtrum line down then two upward-curving lip corners
stroke(256, 278, 256, 288, MO, w=2.5)   # philtrum line
# Upward-curving corners: arc from center outward and slightly up
for t in [i/10 for i in range(11)]:
    xi = 256 - t*20; yi = 288 + 6*t*(1-t)*6 - t*4   # left curve up
    if t < 0.95:
        xi2 = 256 - (t+0.1)*20; yi2 = 288 + 6*(t+0.1)*(1-(t+0.1))*6 - (t+0.1)*4
        stroke(xi, yi, xi2, yi2, MO, w=2.5)
for t in [i/10 for i in range(11)]:
    xi = 256 + t*20; yi = 288 + 6*t*(1-t)*6 - t*4   # right curve up
    if t < 0.95:
        xi2 = 256 + (t+0.1)*20; yi2 = 288 + 6*(t+0.1)*(1-(t+0.1))*6 - (t+0.1)*4
        stroke(xi, yi, xi2, yi2, MO, w=2.5)

# ── BLUSH PATCHES ─────────────────────────────────────────────────────
for cx_, cy_ in [(162,258),(350,258)]:
    for yy in range(int(cy_-26), int(cy_+26)):
        for xx in range(int(cx_-44), int(cx_+44)):
            d = math.sqrt(((xx-cx_)/42)**2+((yy-cy_)/24)**2)
            if d < 1.:
                put(xx, yy, BL, 0.55*(1-d*0.5))

# ── WHISKERS ──────────────────────────────────────────────────────────
# 3 whiskers each side: start at nose sides, spread to edges
wh_sy = [263, 272, 281]
wh_ly = [257, 272, 287]   # end y on left
wh_ry = [257, 272, 287]   # end y on right
for i in range(3):
    stroke(237, wh_sy[i],  75, wh_ly[i], WK, w=1.1)   # left
    stroke(275, wh_sy[i], 437, wh_ry[i], WK, w=1.1)   # right

# ── RAISED RIGHT PAW (waving, clearly visible outside head) ───────────
oval(390, 350, 22, 42, F)   # forearm angled upward
oval(400, 312, 34, 28, F)   # paw pad
disk(390, 304, 9, FD)       # toe bean 1
disk(403, 299, 9, FD)       # toe bean 2
disk(416, 304, 9, FD)       # toe bean 3
disk(394, 316, 7, EP)       # inner pad 1
disk(409, 318, 7, EP)       # inner pad 2
# Slight outline to separate paw from background
for ex, ey, er in [(400,312,36),(390,304,11),(403,299,11),(416,304,11)]:
    for yy in range(int(ey-er-1),int(ey+er+1)):
        for xx in range(int(ex-er-1),int(ex+er+1)):
            d = math.hypot(xx-ex,yy-ey)
            if er-0.5 < d < er+1.5:
                put(xx,yy,FD,0.25)

# ── FLOWER CROWN ──────────────────────────────────────────────────────
for fx, fy in [(136,122),(178,98),(256,88),(334,98),(376,122)]:
    for i in range(6):
        ang = math.radians(i*60+30)
        disk(fx+math.cos(ang)*15, fy+math.sin(ang)*15, 8, PT)
    disk(fx, fy, 10, GR)   # green calyx base
    disk(fx, fy,  8, YL)   # yellow center

# ── PNG ENCODE ────────────────────────────────────────────────────────
raw = b''
for row in buf:
    raw += b'\x00'
    for r, g, b_ in row:
        raw += bytes([r, g, b_])

comp = zlib.compress(raw, 6)

def ck(tag, data):
    body = tag + data
    return struct.pack('>I', len(data)) + body + struct.pack('>I', zlib.crc32(body) & 0xFFFFFFFF)

hdr = struct.pack('>IIBBBBB', S, S, 8, 2, 0, 0, 0)
png = (b'\x89PNG\r\n\x1a\n'
       + ck(b'IHDR', hdr)
       + ck(b'IDAT', comp)
       + ck(b'IEND', b''))

out_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
os.makedirs(out_dir, exist_ok=True)
out = os.path.join(out_dir, 'entry.png')
with open(out, 'wb') as f:
    f.write(png)
