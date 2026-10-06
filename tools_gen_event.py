#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

FD = "/mnt/skills/examples/canvas-design/canvas-fonts"
SERIF = os.path.join(FD, "IBMPlexSerif-Bold.ttf")
SANS  = os.path.join(FD, "WorkSans-Bold.ttf")
BILDER = "/home/user/schaefer-dotternhausen/bilder"
OUT = "/home/user/schaefer-dotternhausen/creatives"
os.makedirs(OUT, exist_ok=True)
RED = (180, 20, 18)
LOGO = Image.open(os.path.join(BILDER, "schaefer-logo-weiss.png")).convert("RGBA")

def cover(img, W, H):
    iw, ih = img.size; s = max(W/iw, H/ih)
    img = img.resize((int(iw*s+1), int(ih*s+1)), Image.LANCZOS)
    nw, nh = img.size; x=(nw-W)//2; y=(nh-H)//2
    return img.crop((x, y, x+W, y+H))

def vgrad(W, H, stops):
    g = Image.new("L", (1, H), 0); px = g.load()
    for y in range(H):
        t=y/(H-1); a=stops[-1][1]
        for i in range(len(stops)-1):
            p0,a0=stops[i]; p1,a1=stops[i+1]
            if p0<=t<=p1:
                k=(t-p0)/(p1-p0) if p1>p0 else 0; a=a0+(a1-a0)*k; break
        px[0,y]=int(a)
    ov=Image.new("RGBA",(W,H),(18,9,11,255)); ov.putalpha(g.resize((W,H))); return ov

def fit(path, lines, maxw, start):
    s=start
    while s>16:
        f=ImageFont.truetype(path,s)
        d=ImageDraw.Draw(Image.new("RGB",(10,10)))
        if all(d.textlength(ln,font=f)<=maxw for ln in lines): return f,s
        s-=2
    return ImageFont.truetype(path,16),16

def center(draw, cx, y, lines, font, fill, lh, shadow=True):
    for ln in lines:
        bb=draw.textbbox((0,0),ln,font=font); w=bb[2]-bb[0]
        x=cx-w/2-bb[0]; yy=y-bb[1]
        if shadow: draw.text((x+2,yy+3),ln,font=font,fill=(10,5,6,170))
        draw.text((x,yy),ln,font=font,fill=fill); y+=lh
    return y

def tracked(draw, cx, y, text, font, fill, track):
    widths=[draw.textlength(ch,font=font)+track for ch in text]
    total=sum(widths)-track; x=cx-total/2
    for ch,w in zip(text,widths):
        draw.text((x,y),ch,font=font,fill=fill); x+=w

def make(photo, size, out):
    W,H=size; u=W/1080.0
    base=cover(Image.open(os.path.join(BILDER,photo)).convert("RGB"),W,H).convert("RGBA")
    base=Image.alpha_composite(base,vgrad(W,H,[(0,170),(0.3,100),(0.5,80),(0.6,125),(1,210)]))
    d=ImageDraw.Draw(base)
    # Logo
    lw=int(W*0.44); lh=int(lw*LOGO.height/LOGO.width)
    base.alpha_composite(LOGO.resize((lw,lh),Image.LANCZOS),((W-lw)//2,int(H*0.066)))
    y=int(H*0.066)+lh+int(H*0.035)
    d=ImageDraw.Draw(base)
    # Eyebrow
    ef=ImageFont.truetype(SANS,int(33*u))
    tracked(d,W//2,y,"KOSTENLOSER INFOABEND",ef,(255,255,255,255),int(6*u))
    y+=int(58*u)
    # Headline (serif, auto-fit)
    head=["Energiesysteme","mit Zukunft"]
    hf,hs=fit(SERIF,head,W*0.86,int(104*u))
    y=center(d,W//2,y,head,hf,(255,255,255,255),int(hs*1.07))
    # Red band: date (big) + info (small)
    pos=["Montag, 12. Oktober 2026","um 18.00 Uhr · Eintritt frei"]
    pf,ps=fit(SANS,pos,W*0.9,int(56*u))
    info="Schäfer intelligente Haustechnik · Dotternhausen"
    inf,ins=fit(SANS,[info],W*0.9,int(36*u))
    line_h=int(ps*1.26); pad=int(40*u); gap=int(16*u)
    band_h=pad+line_h*len(pos)+gap+int(ins*1.2)+pad
    band_y=int(H*0.665)
    if band_y+band_h>H-int(0.1*H): band_y=H-int(0.1*H)-band_h
    band=Image.new("RGBA",(W,band_h),RED+(238,)); base.alpha_composite(band,(0,band_y))
    d=ImageDraw.Draw(base)
    ty=center(d,W//2,band_y+pad,pos,pf,(255,255,255,255),line_h,shadow=False)
    center(d,W//2,ty+gap,[info],inf,(255,255,255,245),int(ins*1.2),shadow=False)
    # Subline
    sf,ss=fit(SANS,["Wärmepumpe · Photovoltaik · Biomasse"],W*0.9,int(42*u))
    center(d,W//2,band_y+band_h+int(24*u),["Wärmepumpe · Photovoltaik · Biomasse"],sf,(255,255,255,240),int(ss*1.2))
    base.convert("RGB").save(out,quality=90); print("saved",os.path.basename(out),size)

jobs=[("schaefer_lueftungstechnik.jpg","waerme"),("schaefer_pv_planung.jpg","plan")]
fmts={"1x1":(1080,1080),"4x5":(1080,1350),"9x16":(1080,1920)}
for photo,tag in jobs:
    for fk,sz in fmts.items():
        if tag=="plan" and fk=="9x16": continue
        make(photo,sz,os.path.join(OUT,f"event_energiesysteme_{tag}_{fk}.jpg"))
print("DONE")
