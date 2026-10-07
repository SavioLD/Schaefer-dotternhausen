#!/usr/bin/env python3
# Helles Event-Creative: Foto oben + weisse Infoflaeche mit Key-Facts (Eye-Catcher).
# Aufruf:  python3 tools_overlay_event.py <bildpfad>
import os, sys
from PIL import Image, ImageDraw, ImageFont

FD="/mnt/skills/examples/canvas-design/canvas-fonts"
SERIF=os.path.join(FD,"IBMPlexSerif-Bold.ttf")
SANS=os.path.join(FD,"WorkSans-Bold.ttf")
BILDER="/home/user/schaefer-dotternhausen/bilder"
OUT="/home/user/schaefer-dotternhausen/creatives"
SRC=sys.argv[1] if len(sys.argv)>1 else os.path.join(BILDER,"ki_abend.jpg")
RED=(180,20,18); INK=(18,46,34); GREEN=(31,107,69); GOLD=(198,140,46); PANEL=(255,255,255)
LOGO=Image.open(os.path.join(BILDER,"RZ_schaefer_logo.png")).convert("RGBA")  # farbig fuer hellen Grund

def cover(img,W,H):
    iw,ih=img.size; s=max(W/iw,H/ih); img=img.resize((int(iw*s+1),int(ih*s+1)),Image.LANCZOS)
    nw,nh=img.size; x=(nw-W)//2; y=int((nh-H)*0.35); y=max(0,min(y,nh-H)); return img.crop((x,y,x+W,y+H))
def fit(path,lines,maxw,start):
    s=start; d=ImageDraw.Draw(Image.new("RGB",(4,4)))
    while s>12:
        f=ImageFont.truetype(path,s)
        if all(d.textlength(x,font=f)<=maxw for x in lines): return f,s
        s-=2
    return ImageFont.truetype(path,12),12
def center(d,cx,y,lines,f,fill,lh):
    for ln in lines:
        bb=d.textbbox((0,0),ln,font=f); w=bb[2]-bb[0]; d.text((cx-w/2-bb[0],y-bb[1]),ln,font=f,fill=fill); y+=lh
    return y
def tracked(d,cx,y,text,f,fill,tr):
    ws=[d.textlength(c,font=f)+tr for c in text]; x=cx-(sum(ws)-tr)/2
    for c,w in zip(text,ws): d.text((x,y),c,font=f,fill=fill); x+=w
def pill(d,cx,py,text,bg,fg,pf,u,outline=None):
    tw=d.textlength(text,font=pf); pw=tw+int(48*u); ph=int(60*u); x0=cx-pw/2
    d.rounded_rectangle([x0,py,x0+pw,py+ph],radius=ph//2,fill=bg,outline=outline,width=max(2,int(3*u)) if outline else 0)
    bb=d.textbbox((0,0),text,font=pf); d.text((cx-tw/2,py+ph/2-(bb[3]-bb[1])/2-bb[1]),text,font=pf,fill=fg)
    return pw

def make(size,frac,out):
    W,H=size; u=W/1080.0
    ph=int(H*frac)
    canvas=Image.new("RGB",(W,H),PANEL);
    canvas.paste(cover(Image.open(SRC).convert("RGB"),W,ph),(0,0))
    d=ImageDraw.Draw(canvas)
    # Markenkante an der Naht
    d.rectangle([0,ph-max(4,int(7*u)),W,ph],fill=RED)
    cx=W//2; y=ph+int(30*u)
    # Logo
    lw=int(W*0.31); lh=int(lw*LOGO.height/LOGO.width)
    canvas.paste(LOGO.resize((lw,lh),Image.LANCZOS),((W-lw)//2,y),LOGO.resize((lw,lh),Image.LANCZOS))
    y+=lh+int(16*u)
    # Eyebrow
    ef=ImageFont.truetype(SANS,int(28*u)); tracked(d,cx,y,"KOSTENLOSER INFOABEND",ef,RED,int(6*u)); y+=int(46*u)
    # Headline
    hf,hs=fit(SERIF,["Energiesysteme mit Zukunft"],W*0.9,int(58*u))
    y=center(d,cx,y,["Energiesysteme mit Zukunft"],hf,INK,int(hs*1.1))
    y+=int(8*u)
    # Datum GROSS (Eye-Catcher)
    df,ds=fit(SANS,["Montag, 12. Oktober 2026"],W*0.9,int(60*u))
    y=center(d,cx,y,["Montag, 12. Oktober 2026"],df,INK,int(ds*1.12))
    # goldene Linie
    lwid=int(W*0.30); d.rectangle([cx-lwid//2,y+int(4*u),cx+lwid//2,y+int(4*u)+max(3,int(5*u))],fill=GOLD);
    tf,ts=fit(SANS,["18.00 Uhr · Dotternhausen"],W*0.85,int(42*u))
    y=center(d,cx,y+int(24*u),["18.00 Uhr · Dotternhausen"],tf,GREEN,int(ts*1.2))
    # Pills
    pf=ImageFont.truetype(SANS,int(29*u)); py=y+int(18*u)
    t1="EINTRITT FREI"; t2="Wärmepumpe · PV · Biomasse"
    w1=d.textlength(t1,font=pf)+int(48*u); w2=d.textlength(t2,font=pf)+int(48*u); gap=int(16*u)
    sx=cx-(w1+w2+gap)/2
    pill(d,sx+w1/2,py,t1,RED,(255,255,255),pf,u)
    pill(d,sx+w1+gap+w2/2,py,t2,(255,255,255),INK,pf,u,outline=(31,107,69))
    canvas.save(out,quality=90); print("saved",os.path.basename(out),size)

os.makedirs(OUT,exist_ok=True)
for fk,sz,frac in [("4x5",(1080,1350),0.54),("1x1",(1080,1080),0.40),("9x16",(1080,1920),0.60)]:
    make(sz,frac,os.path.join(OUT,f"event_ki_{fk}.jpg"))
print("DONE")
