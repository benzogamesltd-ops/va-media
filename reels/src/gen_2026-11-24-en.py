#!/usr/bin/env python3
"""Generator for reels/src/2026-11-24-en.html (Plasma synthwave sunset, synthwave music, "Agent. Game. App. Pick one.")."""
import random, pathlib
T = 10.0
rng = random.Random(241124)
def p(t): return f"{t / T * 100:.2f}%"
def scene(name, a, b, enter="translateY(90px)", leave="translateX(-220px)"):
    if a == 0:  # hook: visible at t=0, leaves at b, returns at the very end for the loop
        return (f"@keyframes {name}{{0%{{opacity:1;transform:none}}{p(b-0.12)}{{opacity:1;transform:none}}"
                f"{p(b+0.1)}{{opacity:0;transform:scale(1.18)}}{p(9.8)}{{opacity:0;transform:scale(1.06)}}100%{{opacity:1;transform:none}}}}\n")
    return (f"@keyframes {name}{{0%,{p(a-0.02)}{{opacity:0;transform:{enter}}}{p(a+0.22)}{{opacity:1;transform:none}}"
            f"{p(b-0.14)}{{opacity:1;transform:none}}{p(b+0.08)}{{opacity:0;transform:{leave}}}100%{{opacity:0;transform:{leave}}}}}\n")
def slam(name, t, frm="scale(1.6)", dur=0.26):
    return f"@keyframes {name}{{0%,{p(t)}{{opacity:0;transform:{frm}}}{p(t+dur)}{{opacity:1;transform:none}}100%{{opacity:1;transform:none}}}}\n"
def slamo(name, t, frm, dur=0.26):  # slam in, hidden again before the loop point
    return f"@keyframes {name}{{0%,{p(t)}{{opacity:0;transform:{frm}}}{p(t+dur)}{{opacity:1;transform:none}}{p(9.6)}{{opacity:1;transform:none}}{p(9.7)}{{opacity:0;transform:none}}100%{{opacity:0;transform:none}}}}\n"
def punch(name, t):  # word highlight punch at t (visible all the time)
    return (f"@keyframes {name}{{0%,{p(t-0.01)}{{transform:none;color:#FFFFFF}}{p(t+0.06)}{{transform:scale(1.16);color:#FFE066}}"
            f"{p(t+0.3)}{{transform:scale(1);color:#FFE066}}{p(9.7)}{{color:#FFE066}}100%{{transform:none;color:#FFFFFF}}}}\n")

S = [(0, 2.1), (2.1, 3.8), (3.8, 5.5), (5.5, 7.2), (7.2, 8.3), (8.3, T)]
CUTS = [0.7, 1.05, 1.4, 2.1, 3.8, 5.5, 7.2, 8.3]
kf = ""
for i, (a, b) in enumerate(S, 1):
    kf += scene(f"s{i}", a, b)
# hook interrupts: 0.7 Agent, 1.05 Game, 1.4 App + chip
kf += punch("w1", 0.7) + punch("w2", 1.05) + punch("w3", 1.4)
kf += slamo("pick", 1.4, "scale(1.6)")
for i, t in enumerate([0.7, 1.05, 1.4]):
    kf += f"@keyframes pd{i}{{0%,{p(t-0.01)}{{background:rgba(255,255,255,.25);transform:none}}{p(t+0.05)}{{background:#FFE066;transform:scale(1.5)}}{p(t+0.25)}{{background:#FFE066;transform:none}}{p(9.7)}{{background:#FFE066}}100%{{background:rgba(255,255,255,.25)}}}}\n"
kf += f"@keyframes glitch{{0%,{p(1.38)}{{transform:none;filter:none}}{p(1.42)}{{transform:translateX(-26px) skewX(-8deg);filter:hue-rotate(-25deg) brightness(1.4)}}{p(1.46)}{{transform:translateX(18px)}}{p(1.52)}{{transform:none;filter:none}}100%{{transform:none}}}}\n"
# flashes + camera punches
fl = "@keyframes flash{0%{opacity:0}"
for t, o in [(0.7, .3), (1.05, .3), (1.4, .45), (2.1, .55), (3.8, .5), (5.5, .5), (7.2, .45), (8.3, .95)]:
    fl += f"{p(t-0.01)}{{opacity:0}}{p(t+0.02)}{{opacity:{o}}}{p(t+0.25)}{{opacity:0}}"
kf += fl + "100%{opacity:0}}\n"
cam = "@keyframes cam{0%{transform:scale(1.06)}" + f"{p(0.3)}{{transform:scale(1)}}"
for t in CUTS:
    cam += f"{p(t-0.01)}{{transform:scale(1)}}{p(t+0.05)}{{transform:scale(1.045)}}{p(t+0.3)}{{transform:scale(1)}}"
kf += cam + f"{p(9.7)}{{transform:scale(1)}}100%{{transform:scale(1.06)}}}}\n"
# sun path: top hero -> small corner -> low horizon during game -> corner -> center for VA
kf += ("@keyframes orbmove{0%{transform:translate(0,0) scale(1)}" + f"{p(2.0)}{{transform:translate(0,0) scale(1)}}"
       f"{p(2.35)}{{transform:translate(330px,-170px) scale(.4)}}{p(3.7)}{{transform:translate(330px,-170px) scale(.4)}}"
       f"{p(4.05)}{{transform:translate(0,660px) scale(1.2)}}{p(5.4)}{{transform:translate(0,660px) scale(1.2)}}"
       f"{p(5.75)}{{transform:translate(330px,-170px) scale(.4)}}{p(8.15)}{{transform:translate(330px,-170px) scale(.4)}}"
       f"{p(8.45)}{{transform:translate(0,40px) scale(1)}}{p(9.7)}{{transform:translate(0,40px) scale(1)}}100%{{transform:translate(0,0) scale(1)}}}}\n")
kf += f"@keyframes vain{{0%,{p(8.3)}{{opacity:0;transform:scale(.3)}}{p(8.55)}{{opacity:1;transform:scale(1.12)}}{p(8.7)}{{opacity:1;transform:none}}{p(9.72)}{{opacity:1;transform:none}}100%{{opacity:0;transform:none}}}}\n"
# grid speeds up during the game scene
kf += f"@keyframes gridglow{{0%,{p(3.75)}{{opacity:.75}}{p(3.9)}{{opacity:1}}{p(5.45)}{{opacity:1}}{p(5.6)}{{opacity:.75}}100%{{opacity:.75}}}}\n"
# S2 chat
kf += slam("b1", 2.3, "translateX(-80px) scale(.8)")
kf += f"@keyframes typ{{0%,{p(2.58)}{{opacity:0}}{p(2.62)}{{opacity:1}}{p(2.92)}{{opacity:1}}{p(2.95)}{{opacity:0}}100%{{opacity:0}}}}\n"
kf += slam("b2", 2.95, "translateX(80px) scale(.8)", 0.22)
kf += slam("ok2", 3.25, "scale(2)")
# S3 game: score counter, coins, runner
for i in range(5):
    t = 3.95 + i * 0.3
    kf += f"@keyframes sc{i}{{0%,{p(t)}{{opacity:0}}{p(t+0.01)}{{opacity:1}}{p(t+0.3)}{{opacity:1}}{p(t+0.31)}{{opacity:0}}100%{{opacity:0}}}}\n" if i < 4 else \
          f"@keyframes sc{i}{{0%,{p(t)}{{opacity:0}}{p(t+0.01)}{{opacity:1}}100%{{opacity:1}}}}\n"
kf += f"@keyframes runner{{0%,{p(3.8)}{{transform:translateX(0)}}{p(4.3)}{{transform:translateX(-170px)}}{p(4.8)}{{transform:translateX(170px)}}{p(5.3)}{{transform:translateX(-60px)}}100%{{transform:translateX(-60px)}}}}\n"
kf += f"@keyframes coin{{0%{{transform:translateY(-120px) scale(.35);opacity:0}}15%{{opacity:1}}100%{{transform:translateY(420px) scale(1.25);opacity:1}}}}\n"
kf += slam("lvl", 4.9, "scale(2)")
# S4 dashboard bars
for i in range(6):
    kf += f"@keyframes bar{i}{{0%,{p(5.65+i*0.07)}{{transform:scaleY(.05)}}{p(6.1+i*0.07)}{{transform:scaleY(1)}}100%{{transform:scaleY(1)}}}}\n"
kf += slam("tg", 6.3, "scale(.5)") + slam("ok4", 6.6, "scale(2)")
kf += f"@keyframes knob{{0%,{p(6.35)}{{transform:none}}{p(6.5)}{{transform:translateX(70px)}}100%{{transform:translateX(70px)}}}}\n"
kf += f"@keyframes tgbg{{0%,{p(6.35)}{{background:rgba(255,255,255,.2)}}{p(6.5)}{{background:#22C55E}}100%{{background:#22C55E}}}}\n"
# S5 we build all three
for i in range(3):
    kf += slam(f"c{i}", 7.35 + i * 0.12, "translateY(80px) scale(1.3)", 0.22)
kf += slam("ask", 7.8, "scale(1.5)")
# S6 brand
kf += slam("bw", 8.4, "scale(1.5)") + slam("bt", 8.55, "translateY(40px)") + slam("cta", 8.7, "scale(1.6)") + slam("url", 8.85, "scale(1.4)")
kf += f"@keyframes s6out{{0%,{p(9.6)}{{opacity:1}}{p(9.8)}{{opacity:0}}100%{{opacity:0}}}}\n"

stars = ""
for i in range(160):
    x, y = rng.randint(0, 1080), rng.randint(0, 1250)
    s = rng.choice([2, 3, 3, 4, 5, 7])
    c = rng.choice(["", "", " g", " b"])
    stars += f'<i class="dot{c}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;animation-duration:{rng.uniform(1.0,2.4):.2f}s;animation-delay:-{rng.uniform(0,2):.2f}s"></i>'
coins = "".join(f'<i class="coin" style="left:{x}px;animation-delay:-{d:.2f}s"></i>' for x, d in [(330, 0), (540, .45), (750, .2), (430, .75), (650, .95)])
bars = "".join(f'<i class="bar" style="left:{60+i*120}px;height:{h}px;animation:bar{i} {T}s cubic-bezier(.2,.8,.2,1) forwards"></i>' for i, h in enumerate([120, 190, 160, 250, 220, 300]))
A = lambda n, e="cubic-bezier(.2,.9,.3,1.3)": f"animation:{n} {T}s {e} forwards"
SCORES = ["00 420", "02 960", "05 380", "08 710", "12 840"]

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden;font-family:'Montserrat',sans-serif;background:#120C3D}}
.st{{position:relative;width:1080px;height:1920px;overflow:hidden;background:linear-gradient(180deg,#120C3D 0%,#24197A 34%,#2A1F8F 50%,#1A1446 68%,#7A2E0C 84%,#E0611F 94%,#FF7A2F 100%)}}
.cam{{position:absolute;inset:0;animation:cam {T}s cubic-bezier(.2,.8,.2,1) forwards}}
.blob{{position:absolute;border-radius:50%;filter:blur(120px)}}
.g1{{left:140px;top:40px;width:800px;height:700px;background:#F59E0B;opacity:.33;animation:drift 6s ease-in-out infinite alternate}}
.g2{{left:-320px;top:700px;width:760px;height:760px;background:#6C4DFF;opacity:.45;animation:drift 7s ease-in-out infinite alternate-reverse}}
.g3{{left:520px;top:1480px;width:760px;height:560px;background:#FF7A2F;opacity:.45;animation:drift 5s ease-in-out infinite alternate}}
@keyframes drift{{to{{transform:translate(80px,-90px) scale(1.12)}}}}
.dot{{position:absolute;border-radius:50%;background:#fff;box-shadow:0 0 10px #fff;animation:tw 2s ease-in-out infinite alternate}}
.dot.g{{background:#FFE066;box-shadow:0 0 12px #FFE066}}.dot.b{{background:#A5B4FF;box-shadow:0 0 12px #A5B4FF}}
@keyframes tw{{to{{opacity:.15}}}}
.sky{{position:absolute;inset:0;animation:rise {T}s linear forwards}}@keyframes rise{{to{{transform:translateY(-100px)}}}}
.mtn{{position:absolute;left:0;right:0;bottom:600px;height:220px;z-index:2;background:linear-gradient(180deg,#2B1C6E,#140E3A);
 clip-path:polygon(0 100%,0 62%,9% 40%,17% 58%,28% 22%,38% 52%,47% 34%,58% 60%,68% 26%,79% 50%,88% 30%,100% 55%,100% 100%)}}
.grid{{position:absolute;left:-420px;bottom:-260px;width:1920px;height:880px;z-index:3;transform:perspective(800px) rotateX(72deg);
 background-image:linear-gradient(rgba(255,170,70,.85) 3px,transparent 3px),linear-gradient(90deg,rgba(255,170,70,.7) 3px,transparent 3px);background-size:120px 120px;
 -webkit-mask-image:linear-gradient(to top,#000 25%,transparent 92%);animation:gridmove .62s linear infinite,gridglow {T}s linear forwards}}
@keyframes gridmove{{to{{background-position:0 120px}}}}
.floor{{position:absolute;left:0;right:0;bottom:0;height:640px;z-index:2;background:linear-gradient(180deg,#2A0F2E00,#3A1606 40%,#6B2A08)}}
.orbG{{position:absolute;left:540px;top:400px;width:0;height:0;z-index:5;animation:orbmove {T}s cubic-bezier(.7,0,.3,1) forwards}}
.sunO{{position:absolute;left:-200px;top:-200px;width:400px;height:400px;border-radius:50%;background:radial-gradient(circle at 42% 34%,#FFF7DE 0%,#FFD37A 36%,#FFC15E 60%,#F07A1A 100%);
 box-shadow:0 0 150px 60px rgba(255,160,50,.55),0 0 0 12px rgba(255,247,222,.3);animation:pulse .5s ease-in-out infinite alternate}}
.stripes{{position:absolute;left:-200px;top:-200px;width:400px;height:400px;border-radius:50%;overflow:hidden}}
.stripes i{{position:absolute;left:0;right:0;background:#2A1F8F;opacity:.85}}
@keyframes pulse{{to{{box-shadow:0 0 220px 90px rgba(255,160,50,.7),0 0 0 20px rgba(255,247,222,.45)}}}}
.ring{{position:absolute;left:-280px;top:-280px;width:560px;height:560px;border-radius:50%;border:5px solid rgba(255,224,102,.85);border-left-color:transparent;border-bottom-color:rgba(165,180,255,.8);animation:spin 2.6s linear infinite}}
.ring.b{{left:-340px;top:-340px;width:680px;height:680px;border:3px dashed rgba(165,180,255,.5);animation:spin 9s linear infinite reverse}}
.dg{{position:absolute;left:-200px;top:-200px;width:400px;height:400px;display:flex;align-items:center;justify-content:center;font-weight:900;color:#2A1400;letter-spacing:-.03em}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.scan{{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.04) 0 2px,transparent 2px 5px);z-index:60}}
.flash{{position:absolute;inset:0;background:radial-gradient(circle at 50% 30%,#FFFDF5,#FFE9B8 55%,#FFC15E);opacity:0;z-index:70;animation:flash {T}s linear forwards}}
.sc{{position:absolute;inset:0;z-index:10}}
.s1{{animation:s1 {T}s cubic-bezier(.7,0,.3,1) forwards}}
.s2,.s3,.s4,.s5,.s6{{opacity:0}}
.s2{{animation:s2 {T}s cubic-bezier(.2,.8,.2,1) forwards}}.s3{{animation:s3 {T}s cubic-bezier(.2,.8,.2,1) forwards}}
.s4{{animation:s4 {T}s cubic-bezier(.2,.8,.2,1) forwards}}.s5{{animation:s5 {T}s cubic-bezier(.2,.8,.2,1) forwards}}.s6{{animation:s6 {T}s cubic-bezier(.2,.8,.2,1) forwards}}
.c{{position:absolute;left:0;width:1080px;text-align:center}}
.hk{{font-weight:900;color:#FFFFFF;letter-spacing:-.02em;line-height:1;text-shadow:0 6px 40px rgba(18,12,61,.95),0 0 3px #120C3D}}
.w{{display:inline-block;font-size:168px}}
.pill{{display:inline-block;background:#FFC15E;color:#120C3D;padding:12px 46px 22px;border-radius:40px;text-shadow:none;box-shadow:0 0 70px rgba(255,193,94,.55),0 0 0 5px rgba(255,247,222,.6)}}
.mono{{font-family:'DejaVu Sans Mono',monospace;font-size:26px;letter-spacing:.14em;color:#FFE066;font-weight:700}}
.glass{{position:absolute;background:rgba(22,15,72,.68);backdrop-filter:blur(16px);border:2px solid rgba(255,224,102,.45);border-radius:30px;box-shadow:0 24px 80px rgba(0,0,0,.45),inset 0 0 40px rgba(165,180,255,.1)}}
.chip{{display:inline-block;background:#FFE066;color:#120C3D;font-weight:800;font-size:46px;padding:18px 44px;border-radius:60px;box-shadow:0 0 50px rgba(255,224,102,.5)}}
.ttl{{font-weight:900;font-size:124px;color:#fff;letter-spacing:-.02em;line-height:1.02;text-shadow:0 6px 40px rgba(18,12,61,.95)}}
.num{{font-family:'DejaVu Sans Mono',monospace;font-weight:700;font-size:54px;color:#FFE066;letter-spacing:.1em;text-shadow:0 0 20px rgba(255,224,102,.6)}}
.ok{{display:inline-block;background:#16A34A;color:#fff;font-weight:900;font-size:40px;letter-spacing:.06em;padding:14px 34px;border-radius:20px;box-shadow:0 14px 40px rgba(22,163,74,.45);opacity:0}}
.bub{{position:absolute;padding:28px 36px;border-radius:34px;font-family:'Inter';font-weight:700;font-size:42px;line-height:1.22;opacity:0}}
.bu{{left:44px;background:#F2F5FA;color:#120C3D;border-bottom-left-radius:8px}}
.ba{{right:44px;background:#FFC15E;color:#120C3D;border-bottom-right-radius:8px;box-shadow:0 0 40px rgba(255,193,94,.4)}}
.dots{{display:flex;gap:26px;justify-content:center}}.dots i{{width:30px;height:30px;border-radius:50%;background:rgba(255,255,255,.25);border:3px solid #FFE066}}
.runner{{position:absolute;left:470px;top:1420px;width:140px;height:140px;border-radius:50%;z-index:6;background:radial-gradient(circle at 40% 34%,#F2F5FF,#A5B4FF 55%,#6C4DFF);box-shadow:0 0 60px 20px rgba(108,77,255,.6),0 30px 40px rgba(0,0,0,.4);animation:runner {T}s cubic-bezier(.7,0,.3,1) forwards}}
.coin{{position:absolute;top:1150px;width:64px;height:64px;border-radius:50%;background:radial-gradient(circle at 40% 34%,#FFF7DE,#FFE066 55%,#F59E0B);box-shadow:0 0 30px rgba(255,224,102,.8);animation:coin .9s linear infinite}}
.bar{{position:absolute;bottom:40px;width:84px;border-radius:14px 14px 4px 4px;background:linear-gradient(180deg,#FFE066,#F59E0B);transform-origin:bottom;box-shadow:0 0 30px rgba(255,193,94,.45)}}
.tog{{position:absolute;width:150px;height:80px;border-radius:40px;background:rgba(255,255,255,.2)}}.tog i{{position:absolute;left:6px;top:6px;width:68px;height:68px;border-radius:50%;background:#fff}}
.card{{left:90px;width:900px;height:160px;padding:0 50px;display:flex;align-items:center;gap:34px;opacity:0}}
.card b{{font-size:60px;font-weight:900;color:#fff}}
.ic{{width:84px;height:84px;border-radius:50%;flex:none;background:radial-gradient(circle at 40% 34%,#FFF7DE,#FFC15E 60%,#F07A1A);box-shadow:0 0 30px rgba(255,193,94,.6)}}
.ic.b{{background:radial-gradient(circle at 40% 34%,#F2F5FF,#A5B4FF 60%,#6C4DFF);box-shadow:0 0 30px rgba(108,77,255,.6)}}
.ic.cy{{background:radial-gradient(circle at 40% 34%,#ECFEFF,#67E8F9 60%,#0891B2);box-shadow:0 0 30px rgba(103,232,249,.6)}}
</style></head><body><div class="st"><div class="cam">
<div class="blob g1"></div><div class="blob g2"></div><div class="blob g3"></div>
<div class="sky">{stars}</div>
<div class="floor"></div><div class="mtn"></div>
<div class="grid"></div>
<div class="orbG"><div class="ring b"></div><div class="ring"></div><div class="sunO"></div>
 <div class="stripes">{''.join(f'<i style="top:{y}px;height:{h}px"></i>' for y,h in [(250,10),(290,16),(328,22),(366,28)])}</div>
 <div class="dg" style="font-size:160px;opacity:0;{A('vain')}">VA</div></div>

<!-- S1 hook (fully visible at t=0) -->
<div class="sc s1"><div style="position:absolute;inset:0;animation:glitch {T}s linear forwards">
 <div class="c hk" style="top:640px"><span class="w" style="{A('w1','cubic-bezier(.2,.9,.3,1.3)')}">Agent.</span></div>
 <div class="c hk" style="top:815px"><span class="w" style="{A('w2','cubic-bezier(.2,.9,.3,1.3)')}">Game.</span></div>
 <div class="c hk" style="top:990px"><span class="w" style="{A('w3','cubic-bezier(.2,.9,.3,1.3)')}">App.</span></div>
 <div class="c" style="top:1185px"><span class="pill hk" style="font-size:104px;padding:10px 50px 22px">Pick one.</span></div>
 <div class="c" style="top:1365px"><div class="dots">{''.join(f'<i style="{A(f"pd{i}","linear")}"></i>' for i in range(3))}</div></div>
 <div class="c" style="top:1440px;opacity:0;{A('pick')}"><span class="chip">Comment your pick ↓</span></div>
</div></div>

<!-- S2 #1 AI agent -->
<div class="sc s2">
 <div class="c mono" style="top:380px;font-size:34px">#1 · AI AGENT</div>
 <div class="c ttl" style="top:440px;font-size:112px">It works<br><span style="color:#FFE066">while you sleep.</span></div>
 <div class="glass" style="left:70px;top:780px;width:940px;height:620px">
  <div class="mono" style="position:absolute;left:44px;top:32px">AGENT_01 · <span style="color:#4ADE80">ONLINE ●</span></div>
  <div class="bub bu" style="top:100px;{A('b1')}">Can I book a call<br>for Friday?</div>
  <div class="bub ba" style="top:300px;opacity:0;animation:typ {T}s linear forwards">• • •</div>
  <div class="bub ba" style="top:300px;{A('b2')}">Sure! Friday 10:00<br>is free. Booked ✓</div>
  <div style="position:absolute;left:44px;bottom:34px"><span class="ok" style="{A('ok2')}">INSTANT ✓</span></div>
 </div>
</div>

<!-- S3 #2 game -->
<div class="sc s3">
 <div class="c mono" style="top:300px;font-size:34px">#2 · GAME</div>
 <div class="c ttl" style="top:360px">Worlds you<br><span style="color:#FFE066">can play.</span></div>
 <div class="glass" style="left:140px;top:640px;width:800px;height:150px;display:flex;align-items:center;justify-content:space-between;padding:0 44px">
  <div><div class="mono">SCORE</div><div style="position:relative;height:60px;width:330px">{''.join(f'<div class="num" style="position:absolute;left:0;top:0;opacity:0;animation:sc{i} {T}s linear forwards">{s}</div>' for i,s in enumerate(SCORES))}</div></div>
  <span class="ok" style="background:#6C4DFF;box-shadow:0 14px 40px rgba(108,77,255,.5);{A('lvl')}">LEVEL UP</span>
 </div>
 {coins}
 <div class="runner"></div>
</div>

<!-- S4 #3 app -->
<div class="sc s4">
 <div class="c mono" style="top:380px;font-size:34px">#3 · APP</div>
 <div class="c ttl" style="top:440px">Software that<br><span style="color:#FFE066">runs your day.</span></div>
 <div class="glass" style="left:90px;top:790px;width:900px;height:640px">
  <div class="mono" style="position:absolute;left:44px;top:32px">DASHBOARD · LIVE</div>
  <div style="position:absolute;left:40px;top:90px;width:820px;height:360px">{bars}</div>
  <div style="position:absolute;left:44px;bottom:50px;display:flex;align-items:center;gap:26px;opacity:0;{A('tg')}">
   <div class="tog" style="position:relative;animation:tgbg {T}s linear forwards"><i style="animation:knob {T}s cubic-bezier(.2,.8,.2,1) forwards"></i></div>
   <b style="font-family:Inter;font-weight:700;font-size:40px;color:#fff">Auto-reports</b></div>
  <div style="position:absolute;right:44px;bottom:56px"><span class="ok" style="{A('ok4')}">ON ✓</span></div>
 </div>
</div>

<!-- S5 we build all three -->
<div class="sc s5">
 <div class="c ttl" style="top:380px;font-size:116px">We build<br><span style="color:#FFE066">all three.</span></div>
 {''.join(f'<div class="glass card" style="top:{690+i*190}px;{A(f"c{i}")}"><i class="ic{k}"></i><div><div class="mono">{m}</div><b>{n}</b></div></div>' for i,(m,n,k) in enumerate([("01 · AI","AI agents",""),("02 · PLAY","Games"," b"),("03 · IT","Software"," cy")]))}
 <div class="c" style="top:1300px;opacity:0;{A('ask')}"><span class="chip">Which one do you need?</span></div>
</div>

<!-- S6 brand -->
<div class="sc s6"><div style="position:absolute;inset:0;animation:s6out {T}s linear forwards">
 <div class="c hk" style="top:720px;font-size:104px;opacity:0;{A('bw')}">VA Corporation</div>
 <div class="c" style="top:850px;font-family:Inter;font-weight:700;font-size:44px;color:#FFE9B8;text-shadow:0 2px 18px #120C3D;opacity:0;{A('bt','cubic-bezier(.2,.8,.2,1)')}">AI agents · Games · Software</div>
 <div class="c" style="top:980px;opacity:0;{A('cta')}"><span class="pill hk" style="font-size:104px;padding:16px 60px 26px">Follow us</span></div>
 <div class="c" style="top:1230px;opacity:0;{A('url')}"><span class="glass" style="position:relative;display:inline-block;padding:24px 46px;font-weight:800;font-size:64px;color:#fff">va-corporation.github.io</span></div>
</div></div>

<div class="flash"></div><div class="scan"></div>
</div></div>
<style>{kf}</style></body></html>"""
pathlib.Path(__file__).with_name("2026-11-24-en.html").write_text(html, encoding="utf-8")
print("ok", len(html))
