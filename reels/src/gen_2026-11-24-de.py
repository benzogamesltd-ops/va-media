#!/usr/bin/env python3
"""Generator for reels/src/2026-11-24-de.html (Deep Indigo night city, melodic_techno, "3 Uhr nachts. Wer antwortet?")."""
import random, pathlib
T = 10.0
rng = random.Random(24112)
def p(t): return f"{t / T * 100:.2f}%"
def scene(name, a, b, enter="translateY(90px)", leave="translateX(-220px)"):
    if a == 0:  # hook: visible at t=0, leaves at b, returns at the very end for the loop
        return (f"@keyframes {name}{{0%{{opacity:1;transform:none}}{p(b-0.12)}{{opacity:1;transform:none}}"
                f"{p(b+0.1)}{{opacity:0;transform:scale(1.18)}}{p(9.72)}{{opacity:0;transform:scale(1.06)}}100%{{opacity:1;transform:none}}}}\n")
    return (f"@keyframes {name}{{0%,{p(a-0.02)}{{opacity:0;transform:{enter}}}{p(a+0.22)}{{opacity:1;transform:none}}"
            f"{p(b-0.14)}{{opacity:1;transform:none}}{p(b+0.08)}{{opacity:0;transform:{leave}}}100%{{opacity:0;transform:{leave}}}}}\n")
def slam(name, t, frm="scale(1.6)", dur=0.26):
    return f"@keyframes {name}{{0%,{p(t)}{{opacity:0;transform:{frm}}}{p(t+dur)}{{opacity:1;transform:none}}100%{{opacity:1;transform:none}}}}\n"
def win(name, a, b):  # visible only between a and b (opacity)
    s = f"@keyframes {name}{{0%,{p(a-0.02)}{{opacity:0}}{p(a+0.04)}{{opacity:1}}"
    s += f"{p(b-0.04)}{{opacity:1}}{p(b+0.02)}{{opacity:0}}100%{{opacity:0}}}}\n" if b < T else "100%{opacity:1}}\n"
    return s

kf = ""
S = [(0, 2.1), (2.1, 3.6), (3.6, 5.1), (5.1, 6.6), (6.6, 8.2), (8.2, T)]
for i, (a, b) in enumerate(S, 1):
    kf += scene(f"s{i}", a, b)
# hook interrupts: 0.7 clock flips + glitch, 1.0 message slams, 1.4 chip + flash
kf += f"@keyframes glitch{{0%,{p(0.68)}{{transform:none;filter:none}}{p(0.72)}{{transform:translateX(-26px) skewX(-8deg);filter:hue-rotate(-30deg) brightness(1.4)}}{p(0.76)}{{transform:translateX(18px)}}{p(0.82)}{{transform:none;filter:none}}100%{{transform:none}}}}\n"
def slamo(name, t, frm, dur=0.26):  # slam in, hidden again before the loop point
    return f"@keyframes {name}{{0%,{p(t)}{{opacity:0;transform:{frm}}}{p(t+dur)}{{opacity:1;transform:none}}{p(9.6)}{{opacity:1;transform:none}}{p(9.7)}{{opacity:0;transform:none}}100%{{opacity:0;transform:none}}}}\n"
kf += slamo("msg", 1.0, "translateY(120px) scale(.7)", 0.28)
kf += slamo("wait", 1.4, "scale(1.5)")
# clock digits in the orb
kf += f"@keyframes d0{{0%,{p(0.68)}{{opacity:1}}{p(0.72)}{{opacity:0}}{p(9.74)}{{opacity:0}}100%{{opacity:1}}}}\n"
kf += win("d1", 0.7, 5.1) + win("d2", 5.1, 8.2)
kf += f"@keyframes vain{{0%,{p(8.2)}{{opacity:0;transform:scale(.3)}}{p(8.5)}{{opacity:1;transform:scale(1.12)}}{p(8.65)}{{opacity:1;transform:none}}{p(9.72)}{{opacity:1;transform:none}}100%{{opacity:0;transform:none}}}}\n"
# flashes
fl = "@keyframes flash{0%{opacity:0}"
for t, o in [(0.7, .35), (1.4, .5), (2.1, .6), (3.6, .55), (5.1, .45), (6.6, .5), (8.2, .95)]:
    fl += f"{p(t-0.01)}{{opacity:0}}{p(t+0.02)}{{opacity:{o}}}{p(t+0.25)}{{opacity:0}}"
kf += fl + "100%{opacity:0}}\n"
cam = "@keyframes cam{0%{transform:scale(1.06)}" + f"{p(0.3)}{{transform:scale(1)}}"
for t in [0.7, 1.4, 2.1, 3.6, 5.1, 6.6, 8.2]:
    cam += f"{p(t-0.01)}{{transform:scale(1)}}{p(t+0.05)}{{transform:scale(1.045)}}{p(t+0.3)}{{transform:scale(1)}}"
kf += cam + f"{p(9.7)}{{transform:scale(1)}}100%{{transform:scale(1.06)}}}}\n"
# orb path
kf += ("@keyframes orbmove{0%{transform:translate(0,0) scale(1)}" + f"{p(2.0)}{{transform:translate(0,0) scale(1)}}"
       f"{p(2.35)}{{transform:translate(310px,-190px) scale(.42)}}{p(5.0)}{{transform:translate(310px,-190px) scale(.42)}}"
       f"{p(5.35)}{{transform:translate(0,640px) scale(.6)}}{p(6.5)}{{transform:translate(0,640px) scale(.6)}}"
       f"{p(6.85)}{{transform:translate(310px,-190px) scale(.42)}}{p(8.05)}{{transform:translate(310px,-190px) scale(.42)}}"
       f"{p(8.35)}{{transform:translate(0,0) scale(1)}}100%{{transform:translate(0,0) scale(1)}}}}\n")
# city lights go out while "team sleeps", back on with the agent
kf += f"@keyframes lights{{0%,{p(2.1)}{{opacity:1}}{p(2.4)}{{opacity:.18}}{p(3.55)}{{opacity:.18}}{p(3.7)}{{opacity:1}}100%{{opacity:1}}}}\n"
# S2 sleeping team
for i in range(3):
    kf += slam(f"av{i}", 2.3 + i * 0.12, "translateY(60px) scale(.6)", 0.22)
kf += f"@keyframes zz{{0%{{transform:translate(0,0);opacity:0}}30%{{opacity:1}}100%{{transform:translate(40px,-120px);opacity:0}}}}\n"
kf += slam("off", 2.85, "scale(2)")
# S3 chat
kf += slam("b1", 3.75, "translateX(-80px) scale(.8)")
kf += slam("typing", 4.05, "scale(.6)", 0.12)
kf += f"@keyframes typingout{{0%,{p(4.35)}{{opacity:1}}{p(4.4)}{{opacity:0}}100%{{opacity:0}}}}\n"
kf += slam("b2", 4.4, "translateX(80px) scale(.8)", 0.22)
kf += slam("ok3", 4.65, "scale(2)")
# S4 orbit nodes
for i in range(4):
    kf += slam(f"n{i}", 5.3 + i * 0.14, "scale(.3)", 0.3)
# S5 cards
for i in range(3):
    kf += slam(f"c{i}", 6.85 + i * 0.2, "translateY(80px) scale(1.3)", 0.25)
kf += slam("biz", 7.6, "scale(1.5)")
# S6
kf += slam("bw", 8.35, "scale(1.5)") + slam("bt", 8.5, "translateY(40px)") + slam("cta", 8.65, "scale(1.6)") + slam("url", 8.8, "scale(1.4)")
kf += f"@keyframes s6out{{0%,{p(9.72)}{{opacity:1}}100%{{opacity:0}}}}\n"

stars = ""
for i in range(170):
    x, y = rng.randint(0, 1080), rng.randint(0, 1500)
    s = rng.choice([2, 3, 3, 4, 5, 7])
    c = rng.choice(["", "", " g", " b"])
    stars += f'<i class="dot{c}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;animation-duration:{rng.uniform(1.0,2.4):.2f}s;animation-delay:-{rng.uniform(0,2):.2f}s"></i>'
city, winds, x = "", "", -20
while x < 1100:
    w, h = rng.randint(90, 170), rng.randint(180, 520)
    city += f'<div class="bld" style="left:{x}px;width:{w}px;height:{h}px"></div>'
    for wy in range(1920 - h + 30, 1900, 46):
        for wx in range(x + 16, x + w - 20, 34):
            if rng.random() < 0.42:
                winds += f'<i class="wn" style="left:{wx}px;top:{wy}px"></i>'
    x += w + rng.randint(4, 18)
rays = "".join(f'<i class="ray" style="transform:rotate({a}deg)"></i>' for a in range(0, 360, 24))
A = lambda n, e="cubic-bezier(.2,.9,.3,1.3)": f"animation:{n} {T}s {e} forwards"

html = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden;font-family:'Montserrat',sans-serif;background:#0B1033}}
.st{{position:relative;width:1080px;height:1920px;overflow:hidden;background:linear-gradient(180deg,#0B1033 0%,#151F5C 50%,#1E2A78 100%)}}
.cam{{position:absolute;inset:0;animation:cam {T}s cubic-bezier(.2,.8,.2,1) forwards}}
.blob{{position:absolute;border-radius:50%;filter:blur(120px)}}
.g1{{left:120px;top:60px;width:840px;height:760px;background:#FFC15E;opacity:.32;animation:drift 6s ease-in-out infinite alternate}}
.g2{{left:-300px;top:900px;width:800px;height:800px;background:#7DD3FC;opacity:.22;animation:drift 7s ease-in-out infinite alternate-reverse}}
.g3{{left:560px;top:1250px;width:700px;height:600px;background:#3B5BDB;opacity:.4;animation:drift 5s ease-in-out infinite alternate}}
@keyframes drift{{to{{transform:translate(90px,-110px) scale(1.12)}}}}
.dot{{position:absolute;border-radius:50%;background:#F2F5FA;box-shadow:0 0 10px #fff;animation:tw 2s ease-in-out infinite alternate}}
.dot.g{{background:#FFC15E;box-shadow:0 0 12px #FFC15E}}.dot.b{{background:#7DD3FC;box-shadow:0 0 12px #7DD3FC}}
@keyframes tw{{to{{opacity:.15}}}}
.sky{{position:absolute;inset:0;animation:rise {T}s linear forwards}}@keyframes rise{{to{{transform:translateY(-120px)}}}}
.city{{position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:2}}
.bld{{position:absolute;bottom:0;background:linear-gradient(180deg,#18235F,#0D1440);border-top:2px solid rgba(125,211,252,.35)}}
.wins{{position:absolute;inset:0;animation:lights {T}s linear forwards}}
.wn{{position:absolute;width:14px;height:20px;border-radius:3px;background:#FFC15E;box-shadow:0 0 12px rgba(255,193,94,.8)}}
.grid{{position:absolute;left:-420px;bottom:-330px;width:1920px;height:760px;z-index:3;transform:perspective(900px) rotateX(74deg);
 background-image:linear-gradient(rgba(125,211,252,.55) 2px,transparent 2px),linear-gradient(90deg,rgba(125,211,252,.45) 2px,transparent 2px);background-size:110px 110px;
 -webkit-mask-image:linear-gradient(to top,#000 20%,transparent 85%);animation:gridmove 1.9s linear infinite}}
@keyframes gridmove{{to{{background-position:0 110px}}}}
.orbG{{position:absolute;left:540px;top:420px;width:0;height:0;z-index:5;animation:orbmove {T}s cubic-bezier(.7,0,.3,1) forwards}}
.rays{{position:absolute;left:0;top:0;animation:spin 18s linear infinite}}
.ray{{position:absolute;left:-6px;top:-520px;width:12px;height:520px;transform-origin:6px 520px;background:linear-gradient(to top,transparent,rgba(255,224,150,.55) 45%,transparent);filter:blur(5px)}}
.sunO{{position:absolute;left:-210px;top:-210px;width:420px;height:420px;border-radius:50%;background:radial-gradient(circle at 40% 34%,#FFF7DE 0%,#FFD37A 38%,#FFC15E 62%,#F07A1A 100%);
 box-shadow:0 0 150px 60px rgba(255,170,60,.55),0 0 0 14px rgba(255,247,222,.35);animation:pulse .469s ease-in-out infinite alternate}}
@keyframes pulse{{to{{box-shadow:0 0 220px 90px rgba(255,170,60,.7),0 0 0 22px rgba(255,247,222,.5)}}}}
.ring{{position:absolute;left:-290px;top:-290px;width:580px;height:580px;border-radius:50%;border:5px solid rgba(125,211,252,.85);border-left-color:transparent;border-bottom-color:rgba(255,193,94,.7);animation:spin 2.8s linear infinite}}
.ring.b{{left:-350px;top:-350px;width:700px;height:700px;border:3px dashed rgba(125,211,252,.45);animation:spin 9s linear infinite reverse}}
.dg{{position:absolute;left:-210px;top:-210px;width:420px;height:420px;display:flex;align-items:center;justify-content:center;font-weight:900;color:#2A1400;letter-spacing:-.03em}}
.ws{{position:absolute;left:0;top:0;animation:glitch {T}s linear forwards}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.scan{{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.035) 0 2px,transparent 2px 5px);z-index:60}}
.flash{{position:absolute;inset:0;background:radial-gradient(circle at 50% 30%,#FFFDF5,#FFE9B8 55%,#FFC15E);opacity:0;z-index:70;animation:flash {T}s linear forwards}}
.sc{{position:absolute;inset:0;z-index:10}}
.s1{{animation:s1 {T}s cubic-bezier(.7,0,.3,1) forwards}}
.s2,.s3,.s4,.s5,.s6{{opacity:0}}
.s2{{animation:s2 {T}s cubic-bezier(.2,.8,.2,1) forwards}}.s3{{animation:s3 {T}s cubic-bezier(.2,.8,.2,1) forwards}}
.s4{{animation:s4 {T}s cubic-bezier(.2,.8,.2,1) forwards}}.s5{{animation:s5 {T}s cubic-bezier(.2,.8,.2,1) forwards}}.s6{{animation:s6 {T}s cubic-bezier(.2,.8,.2,1) forwards}}
.c{{position:absolute;left:0;width:1080px;text-align:center}}
.hk{{font-weight:900;color:#FFFFFF;letter-spacing:-.02em;line-height:1;text-shadow:0 6px 40px rgba(11,16,51,.9),0 0 2px #0B1033}}
.pill{{display:inline-block;background:#FFC15E;color:#0B1033;padding:12px 46px 22px;border-radius:40px;text-shadow:none;box-shadow:0 0 70px rgba(255,193,94,.55),0 0 0 5px rgba(255,247,222,.6)}}
.en{{font-family:'Inter',sans-serif;font-weight:700;color:#BFE9FF;font-size:44px;text-shadow:0 2px 18px #0B1033}}
.mono{{font-family:'DejaVu Sans Mono',monospace;font-size:26px;letter-spacing:.14em;color:#7DD3FC;font-weight:700}}
.glass{{position:absolute;background:rgba(18,28,84,.62);backdrop-filter:blur(16px);border:2px solid rgba(125,211,252,.45);border-radius:30px;box-shadow:0 24px 80px rgba(0,0,0,.45),inset 0 0 40px rgba(125,211,252,.08)}}
.chip{{display:inline-block;background:#7DD3FC;color:#0B1033;font-weight:800;font-size:44px;padding:18px 44px;border-radius:60px;box-shadow:0 0 50px rgba(125,211,252,.5)}}
.ttl{{font-weight:900;font-size:120px;color:#fff;letter-spacing:-.02em;line-height:1.02;text-shadow:0 6px 40px rgba(11,16,51,.9)}}
.ok{{display:inline-block;background:#16A34A;color:#fff;font-weight:900;font-size:40px;letter-spacing:.06em;padding:14px 34px;border-radius:20px;box-shadow:0 14px 40px rgba(22,163,74,.45);opacity:0}}
.bub{{position:absolute;padding:28px 36px;border-radius:34px;font-family:'Inter';font-weight:700;font-size:40px;line-height:1.22;opacity:0}}
.bu{{left:44px;background:#F2F5FA;color:#0B1033;border-bottom-left-radius:8px}}
.ba{{right:44px;background:#FFC15E;color:#0B1033;border-bottom-right-radius:8px;box-shadow:0 0 40px rgba(255,193,94,.4)}}
.av{{position:absolute;top:150px;width:200px;height:200px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#3A4A9A,#1A2466);border:3px solid rgba(125,211,252,.4);opacity:0}}
.av:after{{content:'';position:absolute;left:62px;top:42px;width:76px;height:76px;border-radius:50%;background:#55639F}}
.av:before{{content:'';position:absolute;left:35px;top:128px;width:130px;height:60px;border-radius:65px 65px 10px 10px;background:#55639F}}
.z{{position:absolute;font-weight:900;color:#7DD3FC;font-size:46px;animation:zz 1.3s ease-out infinite}}
.node{{position:absolute;width:280px;height:110px;margin:-55px 0 0 -140px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:38px;color:#fff;opacity:0}}
.orb{{position:absolute;left:540px;top:1060px;width:0;height:0;animation:spin 7s linear infinite}}
.orb .k{{position:absolute;animation:spin 7s linear infinite reverse}}
.card{{left:90px;width:900px;height:170px;padding:0 50px;display:flex;align-items:center;gap:34px;opacity:0}}
.card b{{font-size:58px;font-weight:900;color:#fff}}
.ic{{width:84px;height:84px;border-radius:50%;flex:none;background:radial-gradient(circle at 40% 34%,#FFF7DE,#FFC15E 60%,#F07A1A);box-shadow:0 0 30px rgba(255,193,94,.6)}}
.ic.b{{background:radial-gradient(circle at 40% 34%,#F2FBFF,#7DD3FC 60%,#2563EB);box-shadow:0 0 30px rgba(125,211,252,.6)}}
</style></head><body><div class="st"><div class="cam">
<div class="blob g1"></div><div class="blob g2"></div><div class="blob g3"></div>
<div class="sky">{stars}</div>
<div class="city">{city}<div class="wins">{winds}</div></div>
<div class="grid"></div>
<div class="orbG"><div class="rays">{rays}</div><div class="ring b"></div><div class="ring"></div><div class="sunO"></div>
 <div class="ws"><div class="dg" style="font-size:104px;{A('d0','linear')}">03:00</div>
 <div class="dg" style="font-size:104px;opacity:0;{A('d1','linear')}">03:01</div></div>
 <div class="dg" style="font-size:118px;opacity:0;{A('d2','linear')}">24/7</div>
 <div class="dg" style="font-size:160px;opacity:0;{A('vain')}">VA</div></div>

<!-- S1 hook (fully visible at t=0) -->
<div class="sc s1">
 <div class="c hk" style="top:690px;font-size:128px">3 Uhr nachts.</div>
 <div class="c" style="top:860px"><span class="pill hk" style="font-size:98px;padding:12px 40px 20px">Wer antwortet?</span></div>
 <div class="c en" style="top:1065px">It's 3 AM. Who answers?</div>
 <div class="glass" style="left:110px;top:1190px;width:860px;padding:30px 40px;opacity:0;{A('msg')}">
  <div class="mono">✉ NEUE NACHRICHT · 03:01</div>
  <div style="font-family:Inter;font-weight:700;font-size:44px;color:#fff;margin-top:14px;line-height:1.2">„Habt ihr morgen einen Termin frei?“</div></div>
 <div class="c" style="top:1480px;opacity:0;{A('wait')}"><span class="chip">Warte auf die Antwort ↓</span></div>
</div>

<!-- S2 team asleep -->
<div class="sc s2">
 <div class="c ttl" style="top:560px">Dein Team<br><span style="color:#7DD3FC">schläft.</span></div>
 <div class="c en" style="top:830px">Your team is asleep.</div>
 <div class="glass" style="left:90px;top:960px;width:900px;height:470px">
  <div class="mono" style="position:absolute;left:44px;top:34px">TEAM · <span style="color:#FFC15E">OFFLINE ●</span></div>
  {''.join(f'<div class="av" style="left:{70+i*275}px;{A(f"av{i}")}"></div><span class="z" style="left:{220+i*275}px;top:140px;animation-delay:-{i*0.4:.1f}s">z</span>' for i in range(3))}
  <div style="position:absolute;left:44px;bottom:36px"><span class="ok" style="background:#B45309;box-shadow:none;{A('off')}">KEINE ANTWORT</span></div>
 </div>
</div>

<!-- S3 agent replies -->
<div class="sc s3">
 <div class="c ttl" style="top:520px">Dein KI-Agent</div>
 <div class="c" style="top:660px"><span class="pill hk" style="font-size:112px">nicht.</span></div>
 <div class="c en" style="top:850px">Your AI agent isn't.</div>
 <div class="glass" style="left:70px;top:960px;width:940px;height:600px">
  <div class="mono" style="position:absolute;left:44px;top:32px">AGENT_01 · <span style="color:#4ADE80">ONLINE ●</span></div>
  <div class="bub bu" style="top:100px;{A('b1')}">Habt ihr morgen<br>einen Termin frei?</div>
  <div class="bub ba" style="top:290px;opacity:0;animation:typing {T}s ease forwards,typingout {T}s linear forwards">• • •</div>
  <div class="bub ba" style="top:290px;{A('b2')}">Ja! Morgen 10:00 ist frei.<br>Soll ich buchen?</div>
  <div style="position:absolute;left:44px;bottom:34px"><span class="ok" style="{A('ok3')}">SOFORT ✓</span></div>
 </div>
</div>

<!-- S4 around the clock -->
<div class="sc s4">
 <div class="c ttl" style="top:250px">Rund um<br><span style="color:#FFC15E">die Uhr.</span></div>
 <div class="c en" style="top:520px">Around the clock.</div>
 <div class="orb">
  {''.join(f'<div class="k" style="left:{x}px;top:{y}px"><div class="glass node" style="{A(f"n{i}")}">{n}</div></div>' for i,(n,(x,y)) in enumerate([("Antworten",(0,-370)),("Termine",(330,0)),("FAQ",(0,370)),("Sprachen",(-330,0))]))}
 </div>
</div>

<!-- S5 we build -->
<div class="sc s5">
 <div class="c ttl" style="top:500px;font-size:112px">Wir bauen<br><span style="color:#7DD3FC">solche Agenten.</span></div>
 <div class="c en" style="top:760px">We build agents like this.</div>
 {''.join(f'<div class="glass card" style="top:{900+i*200}px;{A(f"c{i}")}"><i class="ic{" b" if i==1 else ""}"></i><div><div class="mono">{m}</div><b>{n}</b></div></div>' for i,(m,n) in enumerate([("01 · AI","KI-Agenten"),("02 · GAMES","Spiele"),("03 · IT","Software")]))}
 <div class="c" style="top:1530px;opacity:0;{A('biz')}"><span class="chip">für dein Business</span></div>
</div>

<!-- S6 brand -->
<div class="sc s6"><div style="position:absolute;inset:0;animation:s6out {T}s linear forwards">
 <div class="c hk" style="top:700px;font-size:104px;opacity:0;{A('bw')}">VA Corporation</div>
 <div class="c en" style="top:835px;font-size:42px;opacity:0;{A('bt','cubic-bezier(.2,.8,.2,1)')}">AI agents · Games · Software</div>
 <div class="c" style="top:960px;opacity:0;{A('cta')}"><span class="pill hk" style="font-size:104px;padding:16px 60px 26px">Folgt uns</span><div class="en" style="margin-top:18px;font-size:38px">Follow us</div></div>
 <div class="c" style="top:1270px;opacity:0;{A('url')}"><span class="glass" style="position:relative;display:inline-block;padding:24px 46px;font-weight:800;font-size:64px;color:#fff">va-corporation.github.io</span></div>
</div></div>

<div class="flash"></div><div class="scan"></div>
</div></div>
<style>{kf}</style></body></html>"""
pathlib.Path(__file__).with_name("2026-11-24-de.html").write_text(html, encoding="utf-8")
print("ok", len(html))
