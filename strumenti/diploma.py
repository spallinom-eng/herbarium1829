import sys
from PIL import Image, ImageDraw, ImageFont
import os
HERE=os.path.dirname(os.path.abspath(__file__))
# font da github.com/google/fonts: ZillaSlab-SemiBold, IBMPlexMono-Medium, PinyonScript-Regular
FD=os.path.join(HERE,'fonts')+'/'
BASE=os.path.join(HERE,'..','a','attestato-0004-t3N0SrHnq0bdtvOR.jpg')
def fit(fontfile,text,target_w):
    lo,hi=10,300
    while hi-lo>0.25:
        m=(lo+hi)/2; f=ImageFont.truetype(fontfile,m)
        w=f.getbbox(text)[2]-f.getbbox(text)[0]
        lo,hi=(m,hi) if w<target_w else (lo,m)
    return lo
NAME_SIZE=fit(FD+'ZillaSlab-SemiBold.ttf','Rita Guarcello',1551-894+1)
DATE_SIZE=fit(FD+'PinyonScript-Regular.ttf','Castelbuono, 20 ottobre 2026',1504-943+1)
def make(name,num,date,out):
    im=Image.open(BASE).convert('RGB'); d=ImageDraw.Draw(im)
    # name: cover with clean paper from the top band
    im.paste(im.crop((880,20,2080,140)),(880,440))
    size=NAME_SIZE; f=ImageFont.truetype(FD+'ZillaSlab-SemiBold.ttf',size)
    while f.getlength(name)>2040-894: size-=1; f=ImageFont.truetype(FD+'ZillaSlab-SemiBold.ttf',size)
    ref=ImageFont.truetype(FD+'ZillaSlab-SemiBold.ttf',NAME_SIZE)
    x0=891-ref.getbbox('R')[0]
    d.text((x0,531),name,font=f,fill=(63,60,60),anchor='ls')
    n=f'{int(num):04d}'
    # header digits
    im.paste(im.crop((1760,388,1850,420)),(1668,388))
    fm=ImageFont.truetype(FD+'IBMPlexMono-Medium.ttf',24.4)
    for i,c in enumerate(n): d.text((1675+i*18.3-fm.getbbox('0')[0],412),c,font=fm,fill=(58,42,66),anchor='ls')
    # card: digits and date on rotated layer
    d.rectangle((1616,827,1682,850),fill=(255,253,246))
    d.rectangle((935,869,1516,948),fill=(255,253,246))
    L=Image.new('RGBA',im.size,(0,0,0,0)); dl=ImageDraw.Draw(L)
    fd=ImageFont.truetype(FD+'PinyonScript-Regular.ttf',DATE_SIZE)
    dl.text((943-fd.getbbox('C')[0],926),date,font=fd,fill=(44,40,52),anchor='ls')
    L=L.rotate(1.0,center=(943,926),resample=Image.BICUBIC)
    im.paste(L,(0,0),L)
    fr=ImageFont.truetype(FD+'IBMPlexMono-Medium.ttf',20.5)
    for i,c in enumerate(n): d.text((1623+i*15-fr.getbbox('0')[0],846),c,font=fr,fill=(93,85,66),anchor='ls')
    im.save(out,quality=88)
if __name__=='__main__':
    make(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
