#!/usr/bin/env python3
import os, math
from PIL import Image, ImageDraw, ImageFont

FD="/mnt/skills/examples/canvas-design/canvas-fonts"
SERIF=os.path.join(FD,"IBMPlexSerif-Bold.ttf")
SANS=os.path.join(FD,"WorkSans-Bold.ttf")
BILDER="/home/user/schaefer-dotternhausen/bilder"
OUT="/home/user/schaefer-dotternhausen/creatives"
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
            dx=(i-R/2)/(R/2); dy=(j-R/2)/(R/2); dd=min(1,math.hypot(dx,dy))
            rp[i,j]=int(amax*(1-dd)**2.2)
    rg=rg.resize((rad*2,rad*2)); g=Image.new("L",(W,H),0); g.paste(rg,(int(cx-rad),int(cy-rad)))
    lay=Image.new("RGBA",(W,H),color+(255,)); lay.putalpha(g); return lay
def disc(W,H,cx,cy,r,color):
    g=Image.new("L",(W,H),0); ImageDraw.Draw(g).ellipse([cx-r,cy-r,cx+r,cy+r],fill=255)
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

def scenery(W,H,gy,u):
    s=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(s); DARK=(7,28,21,255)
    d.rectangle([0,gy,W,H],fill=DARK)
    d.ellipse([-W*0.35,gy-int(50*u),W*0.55,gy+int(320*u)],fill=DARK)
    d.ellipse([W*0.55,gy-int(30*u),W*1.35,gy+int(320*u)],fill=DARK)
    # Solarpanel-Reihe (links)
    pw=int(96*u); ph=int(16*u); legh=int(34*u); gap=int(22*u)
    for i in range(3):
        px=int(W*0.08)+i*(pw+gap); py=gy-legh
        d.line([(px+pw*0.5,py),(px+pw*0.5,py+legh)],fill=DARK,width=max(3,int(5*u)))
        d.polygon([(px,py),(px+pw,py-int(34*u)),(px+pw+int(10*u),py-int(22*u)),(px+int(10*u),py+int(12*u))],fill=DARK)
        for k in range(1,3):  # Rasterlinien
            t=k/3
            d.line([(px+pw*t,py+12*u*(1-t)-t*0),(px+pw*t+int(10*u),py-int(22*u)*t)],fill=(246,206,120,120),width=max(1,int(2*u)))
    # Haus mit PV-Dach (Mitte-rechts)
    hx=int(W*0.58); hw=int(150*u); hh=int(120*u)
    d.rectangle([hx,gy-hh,hx+hw,gy],fill=DARK)
    d.polygon([(hx-int(14*u),gy-hh),(hx+hw//2,gy-hh-int(70*u)),(hx+hw+int(14*u),gy-hh)],fill=DARK)
    for k in range(3):
        d.line([(hx+int(18*u),gy-hh-int(14*u)-k*int(16*u)),(hx+hw//2-int(6*u),gy-hh-int(50*u)-k*int(16*u))],fill=(246,206,120,150),width=max(2,int(3*u)))
    # Baum (rechts)
    tx=int(W*0.86); d.rectangle([tx-int(8*u),gy-int(92*u),tx+int(8*u),gy],fill=DARK)
    d.ellipse([tx-int(58*u),gy-int(188*u),tx+int(58*u),gy-int(72*u)],fill=DARK)
    return s

def make(size,out):
    W,H=size; u=W/1080.0
    img=grad_v(W,H,[(0,(11,34,38)),(0.38,(13,54,48)),(0.6,(28,92,66)),(0.76,(236,170,80)),(0.86,(214,120,46)),(1,(120,54,26))])
    gy=int(H*0.78)
    img=Image.alpha_composite(img,radial(W,H,W*0.5,gy-int(10*u),int(W*0.66),(255,201,104),225))
    img=Image.alpha_composite(img,disc(W,H,W*0.5,gy-int(70*u),int(W*0.14),(255,224,150)))  # Sonne
    img=Image.alpha_composite(img,radial(W,H,W*0.5,gy-int(70*u),int(W*0.22),(255,210,120),150))
    img=Image.alpha_composite(img,scenery(W,H,gy,u))
    top=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(top).rectangle([0,0,W,int(H*0.5)],fill=(6,24,22,100))
    img=Image.alpha_composite(img,top)
    d=ImageDraw.Draw(img)

    lw=int(W*0.42); lh=int(lw*LOGO.height/LOGO.width)
    img.alpha_composite(LOGO.resize((lw,lh),Image.LANCZOS),((W-lw)//2,int(H*0.068)))
    y=int(H*0.068)+lh+int(H*0.03); d=ImageDraw.Draw(img)
    ef=ImageFont.truetype(SANS,int(31*u)); tracked(d,W//2,y,"NACHHALTIGER INFOABEND",ef,(247,214,150,255),int(7*u)); y+=int(54*u)
    hf,hs=fit(SERIF,["Energiesysteme","mit Zukunft"],W*0.86,int(100*u))
    center(d,W//2,y,["Energiesysteme","mit Zukunft"],hf,(255,255,255,255),int(hs*1.06),sh=(5,20,14,150))

    # Rote Datums-Leiste (wie erster Stil)
    pf,ps=fit(SANS,["Montag, 12. Oktober 2026 · 18.00 Uhr"],W*0.84,int(52*u))
    sf=ImageFont.truetype(SANS,int(33*u))
    line_h=int(ps*1.2); pad=int(34*u); gap=int(14*u); sub_h=int(40*u)
    band_h=pad+line_h+gap+sub_h+pad
    band_y=int(H*0.80) if H/W>=1.2 else int(H*0.775)
    if band_y+band_h>H-int(0.085*H): band_y=H-int(0.085*H)-band_h
    band=Image.new("RGBA",(W,band_h),RED+(240,)); img.alpha_composite(band,(0,band_y)); d=ImageDraw.Draw(img)
    ty=center(d,W//2,band_y+pad,["Montag, 12. Oktober 2026 · 18.00 Uhr"],pf,(255,255,255,255),line_h)
    center(d,W//2,ty+gap,["Eintritt frei · Wärmepumpe · Photovoltaik · Biomasse"],sf,(255,255,255,248),int(sub_h))
    of=ImageFont.truetype(SANS,int(26*u))
    center(d,W//2,band_y+band_h+int(22*u),["Schäfer intelligente Haustechnik · Dotternhausen"],of,(224,236,222,235),int(32*u))

    img.convert("RGB").save(out,quality=90); print("saved",os.path.basename(out),size)

for fk,sz in {"4x5":(1080,1350),"1x1":(1080,1080),"9x16":(1080,1920)}.items():
    make(sz,os.path.join(OUT,f"event_nachhaltig_sonne_{fk}.jpg"))
print("DONE")
