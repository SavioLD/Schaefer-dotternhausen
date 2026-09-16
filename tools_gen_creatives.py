#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/mnt/skills/examples/canvas-design/canvas-fonts"
SERIF = os.path.join(FONT_DIR, "IBMPlexSerif-Bold.ttf")
SANS  = os.path.join(FONT_DIR, "WorkSans-Bold.ttf")
BILDER = "/home/user/schaefer-dotternhausen/bilder"
OUT = "/home/user/schaefer-dotternhausen/creatives"
os.makedirs(OUT, exist_ok=True)

RED = (180, 20, 18)   # Schäfer-CI Feuerrot (RAL 3000), Online RGB 180/20/18
LOGO = Image.open(os.path.join(BILDER, "schaefer-logo-weiss.png")).convert("RGBA")

def f(path, size): return ImageFont.truetype(path, size)

def cover(img, W, H):
    iw, ih = img.size
    s = max(W/iw, H/ih)
    img = img.resize((int(iw*s+1), int(ih*s+1)), Image.LANCZOS)
    nw, nh = img.size
    x = (nw-W)//2; y = (nh-H)//2
    return img.crop((x, y, x+W, y+H))

def vgrad(W, H, stops):
    g = Image.new("L", (1, H), 0); px = g.load()
    for y in range(H):
        t = y/(H-1); a = stops[-1][1]
        for i in range(len(stops)-1):
            p0, a0 = stops[i]; p1, a1 = stops[i+1]
            if p0 <= t <= p1:
                k = (t-p0)/(p1-p0) if p1 > p0 else 0
                a = a0 + (a1-a0)*k; break
        px[0, y] = int(a)
    overlay = Image.new("RGBA", (W, H), (18, 9, 11, 255))
    overlay.putalpha(g.resize((W, H)))
    return overlay

def center(draw, cx, y, lines, font, fill, lh, shadow=True):
    for ln in lines:
        bb = draw.textbbox((0, 0), ln, font=font)
        w = bb[2]-bb[0]
        x = cx - w/2 - bb[0]; yy = y - bb[1]
        if shadow: draw.text((x+2, yy+3), ln, font=font, fill=(10, 5, 6, 170))
        draw.text((x, yy), ln, font=font, fill=fill)
        y += lh
    return y

def make(photo, size, out, headline, pos_lines, fach, sub):
    W, H = size
    base = cover(Image.open(os.path.join(BILDER, photo)).convert("RGB"), W, H).convert("RGBA")
    base = Image.alpha_composite(base, vgrad(W, H, [(0.0,165),(0.28,95),(0.5,70),(0.6,120),(1.0,205)]))
    d = ImageDraw.Draw(base); u = W/1080.0

    # Logo
    lw = int(W*0.46); lh = int(lw*LOGO.height/LOGO.width)
    base.alpha_composite(LOGO.resize((lw, lh), Image.LANCZOS), ((W-lw)//2, int(H*0.072)))
    ly = int(H*0.072)+lh

    # Headline
    hf = f(SERIF, int(94*u))
    center(d, W//2, ly+int(H*0.05), headline, hf, (255,255,255,255), int(102*u))

    # Band: position (big) + Fachrichtung (klein)
    pf = f(SANS, int(58*u)); ff = f(SANS, int(37*u))
    line_h = int(72*u); fach_h = int(46*u)
    pad = int(40*u); gap = int(14*u)
    band_h = pad + line_h*len(pos_lines) + gap + fach_h + pad
    band_y = int(H*0.665)
    if band_y+band_h > H-int(0.115*H): band_y = H-int(0.115*H)-band_h
    band = Image.new("RGBA", (W, band_h), RED+(236,))
    base.alpha_composite(band, (0, band_y))
    d = ImageDraw.Draw(base)
    ty = center(d, W//2, band_y+pad, pos_lines, pf, (255,255,255,255), line_h, shadow=False)
    center(d, W//2, ty+gap, [fach], ff, (255,255,255,245), fach_h, shadow=False)

    # Subline unter dem Band
    sf = f(SANS, int(41*u))
    center(d, W//2, band_y+band_h+int(26*u), [sub], sf, (255,255,255,240), int(50*u))

    base.convert("RGB").save(out, quality=90)
    print("saved", os.path.basename(out), size)

HEAD = ["Bewerbung in", "nur 37 Sekunden"]
POS  = ["Technischer Systemplaner /", "Technischer Zeichner (m/w/d)"]
FACH = "Fachrichtung Versorgungs- und Anlagentechnik"
SUB  = "Heizung · Lüftung · Klima · Sanitär"

jobs = [("schaefer_pv_planung.jpg","planung"), ("schaefer_lueftungstechnik.jpg","technik")]
formats = {"1x1": (1080,1080), "4x5": (1080,1350), "9x16": (1080,1920)}
for photo, tag in jobs:
    for fk, sz in formats.items():
        if tag == "technik" and fk == "9x16": continue
        make(photo, sz, os.path.join(OUT, f"creative_{tag}_{fk}.jpg"), HEAD, POS, FACH, SUB)
print("DONE")
