#!/usr/bin/env python3
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FD="/mnt/skills/examples/canvas-design/canvas-fonts"
SERIF=os.path.join(FD,"IBMPlexSerif-Bold.ttf")
SANS=os.path.join(FD,"WorkSans-Bold.ttf")
BILDER="/home/user/schaefer-dotternhausen/bilder"
OUT="/home/user/schaefer-dotternhausen/creatives"
os.makedirs(OUT,exist_ok=True)
RED=(180,20,18)
LOGO=Image.open(os.path.join(BILDER,"schaefer-logo-weiss.png")).convert("RGBA")

def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
def grad_v(W,H,stops):
    base=Image.new("RGB",(1,H)); px=base.load()
    for y in range(H):
        t=y/(H-1); col=stops[-1][1]
        for i in range(len(stops)-1):
            p0,c0=stops[i]; p1,c1=stops[i+1]
            if p0<=t<=p1: col=lerp(c0,c1,(t-p0)/(p1-p0) if p1>p0 else 0); break
        px[0,y]=col
    return base.resize((W,H)).convert("RGBA")
def radial(W,H,cx,cy,rad,color,amax):
    R=300; rg=Image.new("L",(R,R),0); rp=rg.load()
    for j in range(R):
        for i in range(R):
            dx=(i-R/2)/(R/2); dy=(j-R/2)/(R/2); d=min(1,math.hypot(dx,dy))
            rp[i,j]=int(amax*(1-d)**2.2)
    rg=rg.resize((rad*2,rad*2)); g=Image.new("L",(W,H),0); g.paste(rg,(int(cx-rad),int(cy-rad)))
    lay=Image.new("RGBA",(W,H),color+(255,)); lay.putalpha(g); return lay
def fit(path,lines,maxw,start):
    s=start; d=ImageDraw.Draw(Image.new("RGB",(4,4)))
    while s>14:
        f=ImageFont.truetype(path,s)
        if all(d.textlength(x,font=f)<=maxw for x in lines): return f,s
        s-=2
    return ImageFont.truetype(path,14),14
def center(d,cx,y,lines,f,fill,lh,sh=(0,0,0,0)):
    for ln in lines:
        bb=d.textbbox((0,0),ln,font=f); w=bb[2]-bb[0]; x=cx-w/2-bb[0]; yy=y-bb[1]
        if sh[3]: d.text((x+2,yy+3),ln,font=f,fill=sh)
        d.text((x,yy),ln,font=f,fill=fill); y+=lh
    return y
def tracked(d,cx,y,text,f,fill,tr):
    ws=[d.textlength(c,font=f)+tr for c in text]; x=cx-(sum(ws)-tr)/2
    for c,w in zip(text,ws): d.text((x,y),c,font=f,fill=fill); x+=w

def skyline(W,H,ground_y):
    """dunkle Silhouette: Baum, Haus mit PV-Dach, Wärmepumpe."""
    s=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(s)
    DARK=(7,30,22,255); u=W/1080.0
    # Boden
    d.rectangle([0,ground_y,W,H],fill=DARK)
    # leichte Hügelkuppe
    d.ellipse([-W*0.3,ground_y-int(60*u),W*0.6,ground_y+int(300*u)],fill=DARK)
    d.ellipse([W*0.5,ground_y-int(40*u),W*1.3,ground_y+int(300*u)],fill=DARK)
    # Haus (Mitte-rechts)
    hx=int(W*0.57); hy=ground_y; hw=int(150*u); hh=int(120*u)
    d.rectangle([hx,hy-hh,hx+hw,hy],fill=DARK)
    d.polygon([(hx-int(14*u),hy-hh),(hx+hw//2,hy-hh-int(70*u)),(hx+hw+int(14*u),hy-hh)],fill=DARK)
    # PV-Linien auf Dach (dünne helle Striche)
    for k in range(3):
        d.line([(hx+int(18*u),hy-hh-int(14*u)-k*int(16*u)),(hx+hw//2-int(6*u),hy-hh-int(50*u)-k*int(16*u))],fill=(240,210,120,170),width=max(2,int(3*u)))
    # Baum (links)
    tx=int(W*0.30); d.rectangle([tx-int(8*u),ground_y-int(90*u),tx+int(8*u),ground_y],fill=DARK)
    d.ellipse([tx-int(60*u),ground_y-int(190*u),tx+int(60*u),ground_y-int(70*u)],fill=DARK)
    # kleine Wärmepumpe neben Haus
    wx=hx+hw+int(26*u); d.rectangle([wx,ground_y-int(52*u),wx+int(70*u),ground_y],fill=DARK)
    d.line([(wx+int(14*u),ground_y-int(26*u)),(wx+int(56*u),ground_y-int(26*u))],fill=(240,210,120,150),width=max(2,int(3*u)))
    return s

def make(size,out):
    W,H=size; u=W/1080.0
    img=grad_v(W,H,[(0,(10,38,31)),(0.4,(14,60,44)),(0.63,(26,96,64)),(0.78,(224,150,66)),(0.9,(150,78,36)),(1,(10,40,30))])
    # Sonnenglow am Horizont
    gy=int(H*0.80)
    img=Image.alpha_composite(img,radial(W,H,W*0.5,gy,int(W*0.62),(255,196,96),210))
    # Skyline-Silhouette
    img=Image.alpha_composite(img,skyline(W,H,gy))
    # leichte Abdunklung oben für Textkontrast
    img=Image.alpha_composite(img,grad_v(W,H,[(0,(6,24,18)),(0.5,(6,24,18)),(1,(6,24,18))]).point(lambda:0) if False else Image.new("RGBA",(W,H),(0,0,0,0)))
    top=Image.new("RGBA",(W,H),(0,0,0,0)); td=ImageDraw.Draw(top)
    td.rectangle([0,0,W,int(H*0.5)],fill=(6,26,20,90))
    img=Image.alpha_composite(img,top)
    d=ImageDraw.Draw(img)

    # Logo
    lw=int(W*0.42); lh=int(lw*LOGO.height/LOGO.width)
    img.alpha_composite(LOGO.resize((lw,lh),Image.LANCZOS),((W-lw)//2,int(H*0.07)))
    y=int(H*0.07)+lh+int(H*0.035)
    d=ImageDraw.Draw(img)
    # Eyebrow
    ef=ImageFont.truetype(SANS,int(31*u))
    tracked(d,W//2,y,"NACHHALTIGER INFOABEND",ef,(247,214,150,255),int(7*u)); y+=int(54*u)
    # Headline
    hf,hs=fit(SERIF,["Energiesysteme","mit Zukunft"],W*0.86,int(100*u))
    y=center(d,W//2,y,["Energiesysteme","mit Zukunft"],hf,(255,255,255,255),int(hs*1.06),sh=(5,20,14,150))
    # Claim
    cf,cs=fit(SANS,["Ihr Zuhause. Ihre Energie. Ihre Unabhängigkeit."],W*0.84,int(31*u))
    y=center(d,W//2,y+int(8*u),["Ihr Zuhause. Ihre Energie. Ihre Unabhängigkeit."],cf,(214,240,222,255),int(cs*1.3))

    # Info unten: Datum-Zeile + Pills
    by=int(H*0.845) if H/W>=1.2 else int(H*0.83)
    df,ds=fit(SANS,["Montag, 12. Oktober 2026 · 18.00 Uhr"],W*0.8,int(40*u))
    center(d,W//2,by,["Montag, 12. Oktober 2026 · 18.00 Uhr"],df,(255,255,255,255),int(ds*1.2),sh=(5,20,14,120))
    # Pills: Eintritt frei (rot) + Themen
    pf=ImageFont.truetype(SANS,int(28*u)); py=by+int(58*u)
    def pill(cx,text,bg,fg):
        tw=d.textlength(text,font=pf); pw=tw+int(44*u); ph=int(54*u)
        x0=cx-pw/2
        d.rounded_rectangle([x0,py,x0+pw,py+ph],radius=ph//2,fill=bg)
        bb=d.textbbox((0,0),text,font=pf)
        d.text((cx-tw/2, py+ph/2-(bb[3]-bb[1])/2-bb[1]),text,font=pf,fill=fg)
        return pw
    gap=int(16*u)
    w1=d.textlength("Eintritt frei",font=pf)+int(44*u)
    w2=d.textlength("Wärmepumpe · PV · Biomasse",font=pf)+int(44*u)
    total=w1+w2+gap; startx=W/2-total/2
    pill(startx+w1/2,"Eintritt frei",RED+(255,),(255,255,255,255))
    pill(startx+w1+gap+w2/2,"Wärmepumpe · PV · Biomasse",(255,255,255,235),(14,60,44,255))
    # Footer-Ort
    of=ImageFont.truetype(SANS,int(26*u))
    center(d,W//2,py+int(80*u),["Schäfer intelligente Haustechnik · Dotternhausen"],of,(206,232,214,235),int(32*u))

    img.convert("RGB").save(out,quality=90); print("saved",os.path.basename(out),size)

for fk,sz in {"4x5":(1080,1350),"1x1":(1080,1080),"9x16":(1080,1920)}.items():
    make(sz,os.path.join(OUT,f"event_nachhaltig_{fk}.jpg"))
print("DONE")
