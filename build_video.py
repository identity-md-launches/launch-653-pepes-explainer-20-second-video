import math, os, random, struct, subprocess, sys, shutil

W, H, FPS = 360, 450, 30
ROOT = os.path.dirname(os.path.abspath(__file__))
FF = shutil.which('ffmpeg') or 'ffmpeg'
FONT = os.path.join(ROOT, 'assets', 'IBMPlexMono-Bold.ttf')
FONT5={
'A':'01110 10001 10001 11111 10001 10001 10001','B':'11110 10001 10001 11110 10001 10001 11110','C':'01111 10000 10000 10000 10000 10000 01111','D':'11110 10001 10001 10001 10001 10001 11110','E':'11111 10000 10000 11110 10000 10000 11111','F':'11111 10000 10000 11110 10000 10000 10000','G':'01111 10000 10000 10111 10001 10001 01111','H':'10001 10001 10001 11111 10001 10001 10001','I':'11111 00100 00100 00100 00100 00100 11111','J':'00111 00010 00010 00010 00010 10010 01100','K':'10001 10010 10100 11000 10100 10010 10001','L':'10000 10000 10000 10000 10000 10000 11111','M':'10001 11011 10101 10101 10001 10001 10001','N':'10001 11001 10101 10011 10001 10001 10001','O':'01110 10001 10001 10001 10001 10001 01110','P':'11110 10001 10001 11110 10000 10000 10000','Q':'01110 10001 10001 10001 10101 10010 01101','R':'11110 10001 10001 11110 10100 10010 10001','S':'01111 10000 10000 01110 00001 00001 11110','T':'11111 00100 00100 00100 00100 00100 00100','U':'10001 10001 10001 10001 10001 10001 01110','V':'10001 10001 10001 10001 10001 01010 00100','W':'10001 10001 10001 10101 10101 10101 01010','X':'10001 10001 01010 00100 01010 10001 10001','Y':'10001 10001 01010 00100 00100 00100 00100','Z':'11111 00001 00010 00100 01000 10000 11111','0':'01110 10001 10011 10101 11001 10001 01110','1':'00100 01100 00100 00100 00100 00100 01110','2':'01110 10001 00001 00010 00100 01000 11111','3':'11110 00001 00001 01110 00001 00001 11110','4':'00010 00110 01010 10010 11111 00010 00010','5':'11111 10000 10000 11110 00001 00001 11110','6':'01110 10000 10000 11110 10001 10001 01110','7':'11111 00001 00010 00100 01000 01000 01000','8':'01110 10001 10001 01110 10001 10001 01110','9':'01110 10001 10001 01111 00001 00001 01110',' ':'00000 00000 00000 00000 00000 00000 00000','$':'00100 01111 10100 01110 00101 11110 00100','.':'00000 00000 00000 00000 00000 00110 00110',',':'00000 00000 00000 00000 00110 00110 00100','%':'11001 11010 00100 01000 10110 00110 00000','?':'01110 10001 00001 00010 00100 00000 00100','=':'00000 00000 11111 00000 11111 00000 00000',"'":'00100 00100 00000 00000 00000 00000 00000','-':'00000 00000 00000 11111 00000 00000 00000'}
def draw_text(im,txt,x,y,s=2,col=(0,0,0)):
    for j,ch in enumerate(txt.upper()):
        rows=FONT5.get(ch,FONT5[' ']).split()
        for gy,row in enumerate(rows):
            for gx,v in enumerate(row):
                if v=='1': rect(im,x+j*6*s+gx*s,y+gy*s,x+j*6*s+(gx+1)*s,y+(gy+1)*s,col)
def centered(im,txt,y,s=2,col=(0,0,0)): draw_text(im,txt,(W-len(txt)*6*s)//2,y,s,col)

def frame_base():
    return bytearray([255]) * (W*H*3)
def px(im,x,y,c):
    if 0<=x<W and 0<=y<H:
        i=(y*W+x)*3; im[i:i+3]=bytes(c)
def rect(im,x0,y0,x1,y1,c):
    for y in range(max(0,y0),min(H,y1)):
        a=(y*W+max(0,x0))*3; b=(y*W+min(W,x1))*3; im[a:b]=bytes(c)*((b-a)//3)
def circ(im,cx,cy,r,col):
    rr=r*r
    for y in range(max(0,cy-r),min(H,cy+r+1)):
        dx=int(math.sqrt(max(0,rr-(y-cy)*(y-cy))))
        for x in range(max(0,cx-dx),min(W,cx+dx+1)): px(im,x,y,col)
def ellipse(im,cx,cy,rx,ry,col):
    for y in range(max(0,cy-ry),min(H,cy+ry+1)):
        q=(y-cy)/ry
        dx=int(rx*math.sqrt(max(0,1-q*q)))
        for x in range(max(0,cx-dx),min(W,cx+dx+1)): px(im,x,y,col)
def line(im,x0,y0,x1,y1,col,w=2):
    n=max(abs(x1-x0),abs(y1-y0),1)
    for k in range(n+1):
        x=round(x0+(x1-x0)*k/n); y=round(y0+(y1-y0)*k/n); circ(im,x,y,w,col)
def frog(im,cx,cy,s=1,lead=False,smile=True):
    black=(14,14,14); green=(91,191,58); shirt=(35,80,230); shorts=(74,74,74); mouth=(200,105,58)
    # legs and clothes
    rect(im,int(cx-24*s),int(cy+35*s),int(cx+24*s),int(cy+84*s),black)
    rect(im,int(cx-21*s),int(cy+37*s),int(cx+21*s),int(cy+80*s),shorts)
    ellipse(im,int(cx-17*s),int(cy+77*s),int(10*s),int(12*s),black); ellipse(im,int(cx-17*s),int(cy+76*s),int(7*s),int(8*s),green)
    ellipse(im,int(cx+17*s),int(cy+77*s),int(10*s),int(12*s),black); ellipse(im,int(cx+17*s),int(cy+76*s),int(7*s),int(8*s),green)
    # blue torso and arms
    rect(im,int(cx-35*s),int(cy+8*s),int(cx+35*s),int(cy+48*s),black)
    rect(im,int(cx-31*s),int(cy+10*s),int(cx+31*s),int(cy+46*s),shirt)
    line(im,int(cx-30*s),int(cy+15*s),int(cx-52*s),int(cy+40*s),black,int(6*s)); line(im,int(cx+30*s),int(cy+15*s),int(cx+52*s),int(cy+40*s),black,int(6*s))
    line(im,int(cx-29*s),int(cy+15*s),int(cx-50*s),int(cy+38*s),shirt,int(3*s)); line(im,int(cx+29*s),int(cy+15*s),int(cx+50*s),int(cy+38*s),shirt,int(3*s))
    # head
    ellipse(im,int(cx),int(cy),int(55*s),int(48*s),black); ellipse(im,int(cx),int(cy-2*s),int(50*s),int(43*s),green)
    # eyes, lids, pupils
    for ex in (-22,22):
        ellipse(im,int(cx+ex*s),int(cy-35*s),int(18*s),int(22*s),black)
        ellipse(im,int(cx+ex*s),int(cy-36*s),int(14*s),int(17*s),(230,245,220))
        ellipse(im,int(cx+(ex+3)*s),int(cy-34*s),int(5*s),int(7*s),black)
        line(im,int(cx+(ex-13)*s),int(cy-42*s),int(cx+(ex+13)*s),int(cy-39*s),black,int(4*s))
    # mouth
    ellipse(im,int(cx),int(cy+17*s),int(31*s),int(17*s),black); ellipse(im,int(cx),int(cy+15*s),int(27*s),int(12*s),mouth)
    if smile: line(im,int(cx-16*s),int(cy+14*s),int(cx+16*s),int(cy+14*s),black,int(2*s))
    if lead:
        line(im,int(cx+35*s),int(cy+18*s),int(cx+72*s),int(cy-8*s),black,int(6*s)); line(im,int(cx+35*s),int(cy+18*s),int(cx+72*s),int(cy-8*s),green,int(3*s))

def text_filter(text, start, end, y, size=28, color='black'):
    # text is intentionally restricted to the supplied script words.
    esc=text.replace('\\','\\\\').replace(':','\\:').replace("'","\\'")
    return f"drawtext=fontfile='{FONT}':text='{esc}':fontcolor={color}:fontsize={size}:x=(w-text_w)/2:y={y}:enable='between(t,{start},{end})'"

def render():
    p=subprocess.Popen([FF,'-y','-f','image2pipe','-vcodec','ppm','-r',str(FPS),'-i','-','-vf','scale=1080:1350:flags=neighbor','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-an','-movflags','+faststart',os.path.join(ROOT,'artifacts','silent.mp4')],stdin=subprocess.PIPE)
    for n in range(600):
        t=n/FPS; im=frame_base()
        if t<3:
            for j in range(10): frog(im,38+j%5*72,315+(j//5)*35,0.52)
            frog(im,180,260,1.25,True)
            centered(im,'HOLD $PEPES - EARN $IMD',18,2)
        elif t<7:
            for j in range(9): frog(im,40+j%5*72,340+(j//5)*36,0.48)
            # terminal behind the crowd
            rect(im,40,70,320,190,(15,15,15)); rect(im,48,78,312,182,(232,246,238))
            for k in range(3):
                yy=98+k*26; line(im,63,yy,160,yy,(35,80,230),2); line(im,190,yy,280,yy,(61,220,132),2)
                ellipse(im,292,yy,8,8,(244,190,50))
            frog(im,180,275,1.05,False)
            centered(im,'EVERY TRADE PAYS 3% TO HOLDERS',18,1)
            for k in range(5):
                x=65+k*60; y=205+((n+k*9)%55); circ(im,x,y,8,(244,190,50)); line(im,x-5,y,x+5,y,(20,20,20),1)
        elif t<10:
            for j in range(8): frog(im,45+j%4*90,345+(j//4)*38,0.5)
            frog(im,180,260,1.2)
            # bag and coins
            ellipse(im,245,265,30,38,(14,14,14)); ellipse(im,245,260,26,34,(244,190,50)); line(im,229,232,261,232,(14,14,14),3)
            for k in range(4): circ(im,242+k*10,250+k%2*12,7,(255,208,70))
            rect(im,98,50,262,105,(255,255,255))
            centered(im,'$12.9K EARNED BY $PEPES HOLDERS',18,1)
        elif t<14:
            for j in range(9): frog(im,42+j%5*70,345+(j//5)*36,0.5)
            frog(im,180,275,1.05)
            line(im,250,300,285,90,(61,220,132),7); line(im,285,90,270,112,(61,220,132),7); line(im,285,90,260,96,(61,220,132),7)
            circ(im,285,75,34,(61,220,132)); circ(im,285,75,27,(255,255,255))
            centered(im,'WHAT IF $IMD GOES 10X?',18,2,(20,150,70))
        elif t<17:
            for j in range(10): frog(im,38+j%5*72,330+(j//5)*38,0.52)
            frog(im,180,250,1.15,False)
            # upward bounce implied by pose and accent stamp
            rect(im,107,72,253,150,(61,220,132)); rect(im,114,79,246,143,(255,255,255))
            centered(im,'$PEPES AT $22M = 100X',18,2,(20,150,70))
        else:
            # end card logo
            rect(im,57,150,303,222,(12,12,12)); rect(im,63,156,125,216,(255,255,255)); rect(im,125,150,303,222,(12,12,12))
            draw_text(im,'P',83,169,6,(12,12,12)); draw_text(im,'PEPESFAMILY',137,177,2,(255,255,255))
            centered(im,"MANY AREN'T READY",250,2); centered(im,'PEPESFAMILY.FUN',290,2,(20,150,70)); centered(im,'HYPOTHETICAL SCENARIOS, NOT FINANCIAL ADVICE. DYOR.',410,1,(120,120,120))
        p.stdin.write(b'P6\n%d %d\n255\n'%(W,H)+im)
    p.stdin.close(); p.wait()

def main(): render()
if __name__=='__main__': main()
