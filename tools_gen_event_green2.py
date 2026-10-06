#!/usr/bin/env python3
import os, math
from PIL import Image, ImageDraw, ImageFont

FD="/mnt/skills/examples/canvas-design/canvas-fonts"
SERIF=os.path.join(FD,"IBMPlexSerif-Bold.ttf")
SANS=os.path.join(FD,"WorkSans-Bold.ttf")
SANSR=os.path.join(FD,"WorkSans-Regular.ttf")
BILDER="/home/user/schaefer-dotternhausen/bilder"
OUT="/home/user/schaefer-dotternhausen/creatives"
RED=(180,20,18); GREEN=(31,107,69); INK=(16,54,40); GOLD=(214,150,52)
LOGO=Image.open(os.path.join(BILDER,"RZ_schaefer_logo.png")).convert("RGBA")  # farbig für hellen Grund

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
    R=260; rg=Image.new("L",(R,R),0); rp=rg.load()
    for j in range(R):
        for i in range(R):
            dx=(i-R/2)/(R/2); dy=(j-R/2)/(R/2); dd=min(1,math.hypot(dx,dy))
            rp[i,j]=int(amax*(1-dd)**2.2)
    rg=rg.resize((rad*2,rad*2)); g=Image.new("L",(W,H),0); g.paste(rg,(int(cx-rad),int(cy-rad)))
    lay=Image.new("RGBA",(W,H),color+(255,)); lay.putalpha(g); return lay
def fit(path,lines,maxw,start):
    s=start; d=ImageDraw.Draw(Image.new("RGB",(4,4)))
    while s>14:
        f=ImageFont.truetype(path,s)
        if all(d.textlength(x,font=f)<=maxw for x in lines): return f,s
        s-=2
    return ImageFont.truetype(path,14),14
def center(d,cx,y,lines,f,fill,lh):
    for ln in lines:
        bb=d.textbbox((0,0),ln,font=f); w=bb[2]-bb[0]; d.text((cx-w/2-bb[0],y-bb[1]),ln,font=f,fill=fill); y+=lh
    return y
def tracked(d,cx,y,text,f,fill,tr):
    ws=[d.textlength(c,font=f)+tr for c in text]; x=cx-(sum(ws)-tr)/2
    for c,w in zip(text,ws): d.text((x,y),c,font=f,fill=fill); x+=w

def i_sun(d,cx,cy,r,col,w):
    rr=r*0.5
    d.ellipse([cx-rr,cy-rr,cx+rr,cy+rr],outline=col,width=w)
    for k in range(8):
        a=k*math.pi/4; x0=cx+math.cos(a)*r*0.72; y0=cy+math.sin(a)*r*0.72; x1=cx+math.cos(a)*r*0.98; y1=cy+math.sin(a)*r*0.98
        d.line([(x0,y0),(x1,y1)],fill=col,width=w)
def i_waves(d,cx,cy,r,col,w):
    for row in range(3):
        yy=cy-r*0.45+row*r*0.45; pts=[]
        for t in range(0,41):
            x=cx-r*0.8+ (1.6*r)*t/40; y=yy+math.sin(t/40*math.pi*2)*r*0.16; pts.append((x,y))
        d.line(pts,fill=col,width=w,joint="curve")
def i_leaf(d,cx,cy,r,col,w):
    bb=[cx-r*0.7,cy-r*0.8,cx+r*0.7,cy+r*0.8]
    d.arc(bb,start=-90,end=90,fill=col,width=w)
    d.arc(bb,start=90,end=270,fill=col,width=w)
    d.line([(cx,cy-r*0.8),(cx,cy+r*0.8)],fill=col,width=w)

def chip(img,cx,cy,r,icon,label,u):
    d=ImageDraw.Draw(img)
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(255,255,255,235),outline=(31,107,69,120),width=max(2,int(3*u)))
    icon(d,cx,cy,r*0.6,GREEN+(255,),max(3,int(5*u)))
    lf=ImageFont.truetype(SANS,int(28*u)); tw=d.textlength(label,font=lf)
    d.text((cx-tw/2,cy+r+int(14*u)),label,font=lf,fill=INK+(255,))

def pill(d,cx,py,text,bg,fg,u,pf):
    tw=d.textlength(text,font=pf); pw=tw+int(46*u); ph=int(56*u); x0=cx-pw/2
    d.rounded_rectangle([x0,py,x0+pw,py+ph],radius=ph//2,fill=bg)
    bb=d.textbbox((0,0),text,font=pf); d.text((cx-tw/2,py+ph/2-(bb[3]-bb[1])/2-bb[1]),text,font=pf,fill=fg)

def make(size,out):
    W,H=size; u=W/1080.0
    img=grad_v(W,H,[(0,(244,248,241)),(0.55,(235,243,232)),(1,(223,235,221))])
    img=Image.alpha_composite(img,radial(W,H,W*0.82,H*0.12,int(W*0.5),(246,214,140),150))  # sanfte Sonne
    # weicher grüner Hügel unten
    hill=Image.new("RGBA",(W,H),(0,0,0,0)); hd=ImageDraw.Draw(hill)
    hd.ellipse([-W*0.4,int(H*0.9),W*0.8,int(H*1.25)],fill=(210,228,205,255))
    hd.ellipse([W*0.45,int(H*0.92),W*1.4,int(H*1.25)],fill=(198,222,196,255))
    img=Image.alpha_composite(img,hill)
    d=ImageDraw.Draw(img)

    lw=int(W*0.40); lh=int(lw*LOGO.height/LOGO.width)
    img.alpha_composite(LOGO.resize((lw,lh),Image.LANCZOS),((W-lw)//2,int(H*0.07)))
    y=int(H*0.07)+lh+int(H*0.03); d=ImageDraw.Draw(img)
    ef=ImageFont.truetype(SANS,int(30*u)); tracked(d,W//2,y,"NACHHALTIGER INFOABEND",ef,GREEN+(255,),int(7*u)); y+=int(52*u)
    hf,hs=fit(SERIF,["Energiesysteme","mit Zukunft"],W*0.86,int(100*u))
    y=center(d,W//2,y,["Energiesysteme","mit Zukunft"],hf,INK+(255,),int(hs*1.06))
    cf,cs=fit(SANSR,["Ihr Zuhause. Ihre Energie. Ihre Unabhängigkeit."],W*0.84,int(31*u))
    y=center(d,W//2,y+int(8*u),["Ihr Zuhause. Ihre Energie. Ihre Unabhängigkeit."],cf,(70,96,82,255),int(cs*1.3))

    # Icon-Reihe
    cy=y+int(90*u); r=int(66*u); step=int(300*u)
    chip(img,W//2-step,cy,r,i_sun,"Photovoltaik",u)
    chip(img,W//2,cy,r,i_waves,"Wärmepumpe",u)
    chip(img,W//2+step,cy,r,i_leaf,"Biomasse",u)
    d=ImageDraw.Draw(img)

    # Info unten
    by=int(H*0.83) if H/W>=1.2 else int(H*0.80)
    df,ds=fit(SANS,["Montag, 12. Oktober 2026 · 18.00 Uhr"],W*0.82,int(40*u))
    center(d,W//2,by,["Montag, 12. Oktober 2026 · 18.00 Uhr"],df,INK+(255,),int(ds*1.2))
    pf=ImageFont.truetype(SANS,int(28*u))
    pill(d,W//2,by+int(56*u),"Eintritt frei",RED+(255,),(255,255,255,255),u,pf)
    of=ImageFont.truetype(SANS,int(26*u))
    center(d,W//2,by+int(130*u),["Schäfer intelligente Haustechnik · Dotternhausen"],of,(70,96,82,255),int(32*u))

    img.convert("RGB").save(out,quality=90); print("saved",os.path.basename(out),size)

for fk,sz in {"4x5":(1080,1350),"1x1":(1080,1080),"9x16":(1080,1920)}.items():
    make(sz,os.path.join(OUT,f"event_nachhaltig_hell_{fk}.jpg"))
print("DONE")
