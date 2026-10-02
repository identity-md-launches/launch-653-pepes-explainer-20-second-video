import os, shutil, subprocess, urllib.parse, urllib.request
ROOT=os.path.dirname(os.path.abspath(__file__)); ff=shutil.which('ffmpeg') or 'ffmpeg'
lines=[
 'Hold Pepes. Earn IMD.',
 'Every time someone trades Pepes, three percent goes straight to holders, paid in IMD.',
 'Pepes holders have already earned almost thirteen thousand dollars in IMD.',
 'Your rewards are paid in IMD. If IMD goes ten x, those same rewards are worth a hundred and twenty-nine thousand.',
 "And Pepes at twenty-two million? That's a hundred x.",
 "Many aren't ready. PepesFamily dot fun. Not financial advice."
]
os.makedirs(os.path.join(ROOT,'assets'),exist_ok=True)
for i,line in enumerate(lines):
    out=os.path.join(ROOT,'assets',f'voice{i}.mp3')
    if not os.path.exists(out):
        q=urllib.parse.quote(line)
        url='https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q='+q+'&tl=en&idx=0&total=1&textlen='+str(len(line))
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req) as r, open(out,'wb') as f: f.write(r.read())
inputs=[os.path.join(ROOT,'artifacts','silent.mp4')]+[os.path.join(ROOT,'assets',f'voice{i}.mp3') for i in range(6)]
cmd=[ff,'-y','-i',inputs[0]]
for x in inputs[1:]: cmd += ['-i',x]
filters=[]
starts=[0,3,7,10,14,17]
for i,start in enumerate(starts): filters.append(f'[{i+1}:a]aresample=48000,adelay={start*1000}|{start*1000},volume=1.15[v{i}]')
filters.append('sine=frequency=110:sample_rate=48000:duration=20,volume=0.035[m1]')
filters.append('sine=frequency=165:sample_rate=48000:duration=20,volume=0.018[m2]')
filters.append('[m1][m2]amix=inputs=2:duration=longest,afade=t=out:st=19.7:d=0.3[music]')
filters.append('[v0][v1][v2][v3][v4][v5][music]amix=inputs=7:duration=longest:dropout_transition=0,alimiter=limit=0.95[a]')
vf=','.join([
 "drawtext=fontfile='%s':text='HOLD $PEPES · EARN $IMD':fontcolor=black:fontsize=38:x=(w-text_w)/2:y=62:enable='between(t,0,3)'"%os.path.join(ROOT,'assets','IBMPlexMono-Bold.ttf'),
 "drawtext=fontfile='%s':text='EVERY TRADE PAYS 3%% TO HOLDERS':fontcolor=black:fontsize=28:x=(w-text_w)/2:y=62:enable='between(t,3,7)'"%os.path.join(ROOT,'assets','IBMPlexMono-Bold.ttf'),
 "drawtext=fontfile='%s':text='$12.9K EARNED BY $PEPES HOLDERS':fontcolor=black:fontsize=28:x=(w-text_w)/2:y=62:enable='between(t,7,10)'"%os.path.join(ROOT,'assets','IBMPlex-Mono-Bold.ttf').replace('IBMPlex-Mono','IBMPlexMono'),
 "drawtext=fontfile='%s':text='WHAT IF $IMD GOES 10x?':fontcolor=0x3DDC84:fontsize=38:x=(w-text_w)/2:y=62:enable='between(t,10,14)'"%os.path.join(ROOT,'assets','IBMPlexMono-Bold.ttf'),
 "drawtext=fontfile='%s':text='$PEPES AT $22M = 100x':fontcolor=0x3DDC84:fontsize=42:x=(w-text_w)/2:y=62:enable='between(t,14,17)'"%os.path.join(ROOT,'assets','IBMPlexMono-Bold.ttf'),
 "drawtext=fontfile='%s':text='P':fontcolor=black:fontsize=52:x=160:y=178:enable='between(t,17,20)'"%os.path.join(ROOT,'assets','IBMPlexMono-Bold.ttf'),
 "drawtext=fontfile='%s':text='PEPESFAMILY':fontcolor=white:fontsize=30:x=460:y=180:enable='between(t,17,20)'"%os.path.join(ROOT,'assets','IBMPlexMono-Bold.ttf'),
 "drawtext=fontfile='%s':text=\"MANY AREN'T READY 🐸\":fontcolor=black:fontsize=36:x=(w-text_w)/2:y=820:enable='between(t,17,20)'"%os.path.join(ROOT,'assets','IBMPlexMono-Bold.ttf'),
 "drawtext=fontfile='%s':text='pepesfamily.fun':fontcolor=0x3DDC84:fontsize=34:x=(w-text_w)/2:y=900:enable='between(t,17,20)'"%os.path.join(ROOT,'assets','IBMPlexMono-Bold.ttf'),
 "drawtext=fontfile='%s':text='Hypothetical scenarios, not financial advice. DYOR.':fontcolor=0x777777:fontsize=19:x=(w-text_w)/2:y=1250:enable='between(t,17,20)'"%os.path.join(ROOT,'assets','IBMPlexMono-Bold.ttf')
])
cmd += ['-filter_complex',';'.join(filters),'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','128k','-ar','48000','-ac','2','-movflags','+faststart','-t','20','-metadata','comment=20-second $PEPES explainer; hypothetical scenarios, not financial advice','-y',os.path.join(ROOT,'artifacts','video.mp4')]
subprocess.run(cmd,check=True)
