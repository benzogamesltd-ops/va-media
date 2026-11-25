#!/usr/bin/env python3
"""Generator for reels/src/2026-11-25-de.html (Aurora, deep_house, "Deine Idee verdient eine App.")."""
import random, pathlib
T = 22.6
rng = random.Random(25112)
def p(t): return f"{max(0,min(t,T)) / T * 100:.3f}%"
# scene windows (text screens). hook visible at t=0 and returns at the end for the loop
S = [(0, 4.0), (4.0, 8.0), (8.0, 12.0), (12.0, 16.0), (16.0, 19.3), (19.3, T)]
LOOP = 22.3
def scene(name, a, b, enter="translateY(70px) scale(.96)", leave="translateY(-60px) scale(1.04)"):
    if a == 0:
        return (f"@keyframes {name}{{0%{{opacity:1;transform:none}}{p(b-0.2)}{{opacity:1;transform:none}}"
                f"{p(b+0.05)}{{opacity:0;transform:scale(1.12)}}{p(LOOP)}{{opacity:0;transform:scale(1.04)}}100%{{opacity:1;transform:none}}}}\n")
    if b >= T:
        return (f"@keyframes {name}{{0%,{p(a-0.02)}{{opacity:0;transform:{enter}}}{p(a+0.25)}{{opacity:1;transform:none}}"
                f"{p(LOOP)}{{opacity:1;transform:none}}100%{{opacity:0;transform:scale(.97)}}}}\n")
    return (f"@keyframes {name}{{0%,{p(a-0.02)}{{opacity:0;transform:{enter}}}{p(a+0.25)}{{opacity:1;transform:none}}"
            f"{p(b-0.2)}{{opacity:1;transform:none}}{p(b+0.05)}{{opacity:0;transform:{leave}}}100%{{opacity:0;transform:{leave}}}}}\n")
def slam(name, t, frm="scale(1.5)", dur=0.3, end=None):
    s = f"@keyframes {name}{{0%,{p(t)}{{opacity:0;transform:{frm}}}{p(t+dur)}{{opacity:1;transform:none}}"
    if end: s += f"{p(end-0.15)}{{opacity:1;transform:none}}{p(end)}{{opacity:0;transform:none}}"
    return s + "100%{opacity:" + ("0" if end else "1") + ";transform:none}}\n"

code = ["const app = createApp(idea);", "app.design({ theme: 'aurora' });", "app.addFeature('Login', 'Chat');", "await app.test();", "app.deploy('live');"]
kf = ""
for i, (a, b) in enumerate(S, 1):
    kf += scene(f"s{i}", a, b)
# hook extras (around the hook words, words never change)
kf += slam("hcard", 1.0, "translateX(160px) scale(.9)", 0.45, LOOP - 0.05)
kf += slam("hchip", 1.9, "scale(1.4)", 0.3, LOOP - 0.05)
for i in range(3):
    kf += f"@keyframes pd{i}{{0%,{p(S[i+1][0]-0.05)}{{background:rgba(255,255,255,.25);transform:scale(1)}}{p(S[i+1][0]+0.2)}{{background:#A3E635;transform:scale(1.35)}}{p(S[i+1][1]-0.1)}{{background:#A3E635;transform:scale(1.35)}}{p(S[i+1][1]+0.1)}{{background:rgba(255,255,255,.25);transform:scale(1)}}100%{{background:rgba(255,255,255,.25)}}}}\n"
# flashes on cuts
fl = "@keyframes flash{0%{opacity:.0}"
for t, o in [(4.0, .35), (8.0, .35), (12.0, .4), (16.0, .35), (19.3, .95)]:
    fl += f"{p(t-0.01)}{{opacity:0}}{p(t+0.03)}{{opacity:{o}}}{p(t+0.35)}{{opacity:0}}"
kf += fl + "100%{opacity:0}}\n"
# camera: slow push inside every scene, soft bump on each cut
cam = "@keyframes cam{0%{transform:scale(1.0)}"
for a, b in S[:-1]:
    cam += f"{p(a+0.02)}{{transform:scale(1.0)}}{p(b-0.05)}{{transform:scale(1.045)}}"
cam += f"{p(19.32)}{{transform:scale(1.0)}}{p(LOOP)}{{transform:scale(1.03)}}100%{{transform:scale(1.0)}}}}\n"
kf += cam
# hero orb path: centre-top in hook -> corners -> back
kf += ("@keyframes orbmove{0%{transform:translate(0,0) scale(1)}" + f"{p(3.85)}{{transform:translate(0,0) scale(1)}}"
       f"{p(4.4)}{{transform:translate(330px,-120px) scale(.45)}}{p(15.85)}{{transform:translate(330px,-120px) scale(.45)}}"
       f"{p(16.4)}{{transform:translate(-330px,-120px) scale(.45)}}{p(19.15)}{{transform:translate(-330px,-120px) scale(.45)}}"
       f"{p(19.5)}{{transform:translate(0,0) scale(0)}}{p(LOOP)}{{transform:translate(0,0) scale(0)}}100%{{transform:translate(0,0) scale(1)}}}}\n")
# S2 roadmap milestones
for i in range(4):
    kf += slam(f"m{i}", 4.6 + i * 0.55, "scale(.3)", 0.35)
kf += f"@keyframes rbar{{0%,{p(4.5)}{{width:0}}{p(6.4)}{{width:720px}}100%{{width:720px}}}}\n"
# S3 code typing + building blocks
for i in range(5):
    kf += f"@keyframes cl{i}{{0%,{p(8.5+i*0.45)}{{width:0}}{p(8.9+i*0.45)}{{width:{len(code[i])*19+10}px}}100%{{width:{len(code[i])*19+10}px}}}}\n"
for i in range(4):
    kf += slam(f"bk{i}", 8.8 + i * 0.5, "translateY(-60px) scale(.6)", 0.35)
kf += f"@keyframes pct{{0%,{p(8.4)}{{width:0}}{p(11.6)}{{width:100%}}100%{{width:100%}}}}\n"
# S4 live
kf += slam("live", 12.8, "scale(2)", 0.3)
for i in range(4):
    kf += slam(f"pn{i}", 13.2 + i * 0.3, "scale(.2)", 0.35)
kf += f"@keyframes tog{{0%,{p(13.6)}{{left:6px;background:#9CA3AF}}{p(13.9)}{{left:66px;background:#A3E635}}100%{{left:66px;background:#A3E635}}}}\n"
kf += f"@keyframes togb{{0%,{p(13.6)}{{background:rgba(255,255,255,.2)}}{p(13.9)}{{background:rgba(163,230,53,.35)}}100%{{background:rgba(163,230,53,.35)}}}}\n"
# S5 cards
for i in range(3):
    kf += slam(f"c{i}", 16.5 + i * 0.3, "translateX(-120px)", 0.35)
# S6 brand
kf += f"@keyframes vain{{0%,{p(19.3)}{{opacity:0;transform:scale(.3)}}{p(19.6)}{{opacity:1;transform:scale(1.12)}}{p(19.8)}{{opacity:1;transform:none}}100%{{opacity:1;transform:none}}}}\n"
kf += slam("bw", 19.45, "scale(1.4)") + slam("bt", 19.6, "translateY(40px)") + slam("cta", 19.7, "scale(1.5)") + slam("url", 19.8, "scale(1.3)")

stars = ""
for i in range(160):
    x, y = rng.randint(0, 1080), rng.randint(0, 1920)
    s = rng.choice([2, 3, 3, 4, 5, 6])
    c = rng.choice(["", "", " l", " y"])
    stars += f'<i class="dot{c}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;animation-duration:{rng.uniform(1.2,2.8):.2f}s;animation-delay:-{rng.uniform(0,2.5):.2f}s"></i>'
A = lambda n, e="cubic-bezier(.2,.9,.3,1.2)": f"animation:{n} {T}s {e} forwards"
code = ["const app = createApp(idea);", "app.design({ theme: 'aurora' });", "app.addFeature('Login', 'Chat');", "await app.test();", "app.deploy('live');"]
lines = "".join(f'<div class="cline" style="{A(f"cl{i}","steps(24,end)")}">{code[i]}</div>' for i in range(5))

html = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden;font-family:'Montserrat',sans-serif;background:#031F1D}}
.st{{position:relative;width:1080px;height:1920px;overflow:hidden;background:linear-gradient(180deg,#031F1D 0%,#05332F 45%,#08524A 80%,#0E6F63 100%)}}
.cam{{position:absolute;inset:0;animation:cam {T}s cubic-bezier(.4,0,.6,1) forwards}}
.blob{{position:absolute;border-radius:50%;filter:blur(110px)}}
.g1{{left:-200px;top:-150px;width:900px;height:600px;background:#0E8F7C;opacity:.55;animation:drift 7s ease-in-out infinite alternate}}
.g2{{left:420px;top:1150px;width:800px;height:800px;background:#67E8F9;opacity:.2;animation:drift 8s ease-in-out infinite alternate-reverse}}
.g3{{left:-250px;top:1300px;width:700px;height:600px;background:#A3E635;opacity:.13;animation:drift 6s ease-in-out infinite alternate}}
@keyframes drift{{to{{transform:translate(110px,-90px) scale(1.12)}}}}
.aur{{position:absolute;left:-300px;width:1700px;height:260px;border-radius:50%;filter:blur(40px);mix-blend-mode:screen}}
.a1{{top:120px;background:linear-gradient(90deg,transparent,rgba(103,232,249,.55),rgba(163,230,53,.45),transparent);transform:rotate(-12deg);animation:wave 6s ease-in-out infinite alternate}}
.a2{{top:300px;background:linear-gradient(90deg,transparent,rgba(163,230,53,.35),rgba(14,143,124,.6),transparent);transform:rotate(8deg);animation:wave 7.5s ease-in-out infinite alternate-reverse}}
@keyframes wave{{to{{transform:translateX(160px) rotate(-4deg) scaleY(1.4)}}}}
.dot{{position:absolute;border-radius:50%;background:#F0FDFA;box-shadow:0 0 10px #fff;animation:tw 2s ease-in-out infinite alternate}}
.dot.l{{background:#A3E635;box-shadow:0 0 12px #A3E635}}.dot.y{{background:#67E8F9;box-shadow:0 0 12px #67E8F9}}
@keyframes tw{{to{{opacity:.15}}}}
.sky{{position:absolute;inset:0;animation:rise {T}s linear forwards}}@keyframes rise{{to{{transform:translateY(-160px)}}}}
.grid{{position:absolute;left:-420px;bottom:-330px;width:1920px;height:760px;transform:perspective(900px) rotateX(74deg);
 background-image:linear-gradient(rgba(103,232,249,.5) 2px,transparent 2px),linear-gradient(90deg,rgba(103,232,249,.4) 2px,transparent 2px);background-size:110px 110px;
 -webkit-mask-image:linear-gradient(to top,#000 20%,transparent 85%);animation:gridmove 2.3s linear infinite}}
@keyframes gridmove{{to{{background-position:0 110px}}}}
.orbG{{position:absolute;left:540px;top:430px;width:0;height:0;z-index:5;animation:orbmove {T}s cubic-bezier(.7,0,.3,1) forwards}}
.pl{{position:absolute;left:-200px;top:-200px;width:400px;height:400px;border-radius:50%;
 background:radial-gradient(circle at 36% 30%,#F0FDFA 0%,#67E8F9 22%,#0E8F7C 55%,#053B36 100%);
 box-shadow:0 0 140px 50px rgba(103,232,249,.45),inset -40px -50px 80px rgba(2,30,28,.7),inset 10px 10px 30px rgba(255,255,255,.35);animation:pulse .492s ease-in-out infinite alternate}}
@keyframes pulse{{to{{box-shadow:0 0 200px 80px rgba(103,232,249,.6),inset -40px -50px 80px rgba(2,30,28,.7),inset 10px 10px 30px rgba(255,255,255,.35)}}}}
.spark{{position:absolute;left:-46px;top:-46px;width:92px;height:92px;border-radius:50%;background:radial-gradient(circle,#FFFDE8,#FACC15 55%,rgba(250,204,21,0) 72%);filter:drop-shadow(0 0 30px #FACC15);animation:sp 1.4s ease-in-out infinite alternate}}
@keyframes sp{{to{{transform:scale(1.35)}}}}
.ring{{position:absolute;left:-300px;top:-300px;width:600px;height:600px;border-radius:50%;border:5px solid rgba(163,230,53,.85);border-left-color:transparent;border-bottom-color:rgba(103,232,249,.75);animation:spin 3.6s linear infinite}}
.ring.b{{left:-370px;top:-370px;width:740px;height:740px;border:3px dashed rgba(103,232,249,.45);animation:spin 11s linear infinite reverse}}
.moon{{position:absolute;left:0;top:0;animation:spin 5s linear infinite}}
.moon i{{position:absolute;left:330px;top:-18px;width:36px;height:36px;border-radius:50%;background:#FACC15;box-shadow:0 0 24px #FACC15}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.scan{{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.03) 0 2px,transparent 2px 5px);z-index:60}}
.flash{{position:absolute;inset:0;background:radial-gradient(circle at 50% 36%,#FFFDF5,#FFE9B8 55%,#FFC15E);opacity:0;z-index:70;animation:flash {T}s linear forwards}}
.sc{{position:absolute;inset:0;z-index:10}}
.s1{{animation:s1 {T}s cubic-bezier(.7,0,.3,1) forwards}}
.s2,.s3,.s4,.s5,.s6{{opacity:0}}
{''.join(f'.s{i}{{animation:s{i} {T}s cubic-bezier(.2,.8,.2,1) forwards}}' for i in range(2,7))}
.c{{position:absolute;left:0;width:1080px;text-align:center}}
.hk{{font-weight:900;color:#FFFFFF;letter-spacing:-.02em;line-height:1.0;text-shadow:0 6px 40px rgba(2,24,22,.95),0 0 3px #021816}}
.lime{{color:#A3E635}}
.en{{font-family:'Inter',sans-serif;font-weight:700;color:#CFFAFE;font-size:44px;text-shadow:0 2px 18px #021816}}
.mono{{font-family:'DejaVu Sans Mono',monospace;font-size:26px;letter-spacing:.14em;color:#67E8F9;font-weight:700}}
.glass{{position:absolute;background:rgba(3,40,37,.72);border:2px solid rgba(103,232,249,.45);border-radius:30px;box-shadow:0 24px 80px rgba(0,0,0,.45),inset 0 0 40px rgba(103,232,249,.08)}}
.chip{{display:inline-block;background:#A3E635;color:#052E2B;font-weight:800;font-size:42px;padding:18px 44px;border-radius:60px;box-shadow:0 0 50px rgba(163,230,53,.45)}}
.ttl{{font-weight:900;font-size:112px;color:#fff;letter-spacing:-.02em;line-height:1.04;text-shadow:0 6px 40px rgba(2,24,22,.95)}}
.step{{display:inline-block;font-weight:800;font-size:40px;letter-spacing:.2em;color:#052E2B;background:#FACC15;padding:10px 30px;border-radius:14px}}
.pdots{{display:flex;gap:22px;justify-content:center}}.pdots i{{width:26px;height:26px;border-radius:50%;background:rgba(255,255,255,.25)}}
.ms{{position:absolute;top:150px;width:150px;margin-left:-75px;text-align:center;opacity:0}}
.ms b{{display:block;margin:0 auto 18px;width:64px;height:64px;border-radius:50%;background:radial-gradient(circle at 40% 34%,#F7FEE7,#A3E635 60%,#4D7C0F);box-shadow:0 0 30px rgba(163,230,53,.7)}}
.ms span{{font-family:Inter;font-weight:700;font-size:30px;color:#fff}}
.cline{{font-family:'DejaVu Sans Mono',monospace;font-size:31px;color:#E6FFFB;white-space:nowrap;overflow:hidden;width:0;height:52px;line-height:52px}}
.blk{{position:absolute;left:30px;width:300px;border-radius:16px;opacity:0}}
.phone{{position:absolute;width:360px;height:640px;border-radius:54px;background:#04312D;border:6px solid #67E8F9;box-shadow:0 0 80px rgba(103,232,249,.45)}}
.node{{position:absolute;padding:20px 34px;font-weight:800;font-size:38px;color:#fff;opacity:0;white-space:nowrap}}
.card{{left:110px;width:860px;height:160px;padding:0 50px;display:flex;align-items:center;gap:34px;opacity:0}}
.card b{{font-size:56px;font-weight:900;color:#fff}}
.ic{{width:80px;height:80px;border-radius:50%;flex:none;background:radial-gradient(circle at 40% 34%,#FFFDE8,#FACC15 60%,#CA8A04);box-shadow:0 0 30px rgba(250,204,21,.6)}}
.ic.c2{{background:radial-gradient(circle at 40% 34%,#F0FDFA,#67E8F9 60%,#0E8F7C)}}.ic.c3{{background:radial-gradient(circle at 40% 34%,#F7FEE7,#A3E635 60%,#4D7C0F)}}
.sun{{position:absolute;left:340px;top:470px;width:400px;height:400px;border-radius:50%;background:radial-gradient(circle at 40% 34%,#FFF7DE 0%,#FFC15E 58%,#F07A1A 100%);
 box-shadow:0 0 170px 70px rgba(255,170,60,.55),0 0 0 16px rgba(255,247,222,.3);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:170px;color:#3A1A00;letter-spacing:-.03em;opacity:0}}
</style></head><body><div class="st"><div class="cam">
<div class="blob g1"></div><div class="blob g2"></div><div class="blob g3"></div>
<div class="aur a1"></div><div class="aur a2"></div>
<div class="sky">{stars}</div>
<div class="grid"></div>
<div class="orbG"><div class="ring b"></div><div class="ring"></div><div class="moon"><i></i></div><div class="pl"></div><div class="spark"></div></div>

<!-- S1 hook: fully visible at t=0 -->
<div class="sc s1">
 <div class="c hk" style="top:640px;font-size:138px">Deine Idee</div>
 <div class="c hk" style="top:790px;font-size:138px">verdient</div>
 <div class="c hk lime" style="top:940px;font-size:150px">eine App.</div>
 <div class="c en" style="top:1120px">Your idea deserves an app.</div>
 <div class="glass" style="left:230px;top:1230px;width:620px;padding:24px 34px;opacity:0;{A('hcard')}">
  <div class="mono">IDEE_01 · <span style="color:#A3E635">BEREIT ●</span></div>
  <div class="pdots" style="margin-top:22px">{''.join(f'<i style="{A(f"pd{i}","linear")}"></i>' for i in range(3))}</div></div>
 <div class="c" style="top:1440px;opacity:0;{A('hchip')}"><span class="chip">3 Schritte ↓</span></div>
</div>

<!-- S2 plan -->
<div class="sc s2">
 <div class="c" style="top:560px"><span class="step">SCHRITT 1</span></div>
 <div class="c ttl" style="top:650px">Wir planen<br><span class="lime">mit dir.</span></div>
 <div class="c en" style="top:910px">Step 1: we plan it with you.</div>
 <div class="glass" style="left:90px;top:1040px;width:900px;height:380px">
  <div class="mono" style="position:absolute;left:44px;top:34px">ROADMAP · PLAN</div>
  <div style="position:absolute;left:90px;top:182px;width:720px;height:8px;border-radius:4px;background:rgba(255,255,255,.15)"></div>
  <div style="position:absolute;left:90px;top:182px;height:8px;border-radius:4px;background:linear-gradient(90deg,#67E8F9,#A3E635);box-shadow:0 0 20px #A3E635;{A('rbar','cubic-bezier(.4,0,.2,1)')}"></div>
  {''.join(f'<div class="ms" style="left:{90+i*240}px;{A(f"m{i}")}"><b></b><span>{n}</span></div>' for i, n in enumerate(["Idee", "Konzept", "Design", "Start"]))}
 </div>
</div>

<!-- S3 build -->
<div class="sc s3">
 <div class="c" style="top:300px"><span class="step">SCHRITT 2</span></div>
 <div class="c ttl" style="top:390px">Wir bauen<br><span class="lime">sie.</span></div>
 <div class="c en" style="top:650px">Step 2: we build it.</div>
 <div class="glass" style="left:60px;top:790px;width:960px;height:420px;padding:80px 40px 0">
  <div class="mono" style="position:absolute;left:40px;top:28px">BUILD · app.js</div>{lines}
  <div style="position:absolute;left:40px;right:40px;bottom:26px;height:10px;border-radius:5px;background:rgba(255,255,255,.15)"><div style="height:10px;border-radius:5px;background:#A3E635;{A('pct','linear')}"></div></div>
 </div>
 <div class="phone" style="left:360px;top:1260px;height:520px">
  {''.join(f'<div class="blk" style="top:{40+i*112}px;height:{[80,90,90,70][i]}px;background:{["#67E8F9","rgba(240,253,250,.85)","#A3E635","#FACC15"][i]};{A(f"bk{i}")}"></div>' for i in range(4))}
 </div>
</div>

<!-- S4 live -->
<div class="sc s4">
 <div class="c" style="top:300px"><span class="step">SCHRITT 3</span></div>
 <div class="c ttl" style="top:390px">Sie geht<br><span class="lime">live.</span></div>
 <div class="c en" style="top:650px">Step 3: it goes live.</div>
 <div class="phone" style="left:360px;top:800px">
  <div class="mono" style="position:absolute;left:34px;top:40px;font-size:22px">DEINE APP</div>
  <div style="position:absolute;left:34px;top:90px;width:280px;height:150px;border-radius:22px;background:linear-gradient(135deg,#0E8F7C,#67E8F9)"></div>
  <div style="position:absolute;left:34px;top:270px;font-family:Inter;font-weight:700;font-size:28px;color:#fff">Benachrichtigungen</div>
  <div style="position:absolute;left:34px;top:320px;width:130px;height:66px;border-radius:33px;{A('togb','linear')}"><i style="position:absolute;top:6px;left:6px;width:54px;height:54px;border-radius:50%;{A('tog','cubic-bezier(.2,.8,.2,1)')}"></i></div>
  <div style="position:absolute;left:34px;top:420px;width:280px;height:22px;border-radius:11px;background:rgba(240,253,250,.25)"></div>
  <div style="position:absolute;left:34px;top:460px;width:200px;height:22px;border-radius:11px;background:rgba(240,253,250,.25)"></div>
  <div style="position:absolute;left:0;width:100%;top:530px;text-align:center"><span class="chip" style="font-size:36px;padding:12px 32px;opacity:0;{A('live')}">LIVE ●</span></div>
 </div>
 {''.join(f'<div class="glass node" style="left:{x}px;top:{y}px;{A(f"pn{i}")}">{n}</div>' for i, (n, x, y) in enumerate([("App Store", 50, 880), ("Web", 790, 960), ("Android", 40, 1320), ("iOS", 800, 1380)]))}
</div>

<!-- S5 question -->
<div class="sc s5">
 <div class="c ttl" style="top:450px;font-size:108px">Was baust du<br><span class="lime">als Nächstes?</span></div>
 <div class="c en" style="top:710px">What are you building next?</div>
 <div class="glass card" style="top:870px;{A('c0','cubic-bezier(.2,.8,.2,1)')}"><span class="ic"></span><b>KI-Agenten</b></div>
 <div class="glass card" style="top:1070px;{A('c1','cubic-bezier(.2,.8,.2,1)')}"><span class="ic c2"></span><b>Spiele</b></div>
 <div class="glass card" style="top:1270px;{A('c2','cubic-bezier(.2,.8,.2,1)')}"><span class="ic c3"></span><b>Software</b></div>
 <div class="c en" style="top:1490px;color:#FACC15">Schreib es in die Kommentare ↓</div>
</div>

<!-- S6 brand reveal -->
<div class="sc s6">
 <div class="sun" style="{A('vain')}">VA</div>
 <div class="c hk" style="top:960px;font-size:96px;opacity:0;{A('bw')}">VA Corporation</div>
 <div class="c en" style="top:1080px;font-size:46px;color:#FACC15;opacity:0;{A('bt')}">KI-Agenten · Spiele · Software</div>
 <div class="c" style="top:1200px;opacity:0;{A('cta')}"><span class="chip" style="font-size:52px">Folgt uns</span></div>
 <div class="c hk" style="top:1360px;font-size:64px;opacity:0;{A('url')}">va-corporation.github.io</div>
</div>
</div><div class="scan"></div><div class="flash"></div></div>
<style>{kf}</style></body></html>"""
pathlib.Path(__file__).with_name("2026-11-25-de.html").write_text(html)
print("ok", len(html))
