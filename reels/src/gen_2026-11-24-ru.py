#!/usr/bin/env python3
"""Generator for reels/src/2026-11-24-ru.html  (Solar Dawn, deep_house, "Хватит делать это руками")."""
import random, pathlib
T = 10.0
rng = random.Random(2411)

def p(t):  # seconds -> keyframe percent
    return f"{t / T * 100:.2f}%"

def scene(name, a, b, enter="translateY(90px)", leave="translateX(-220px)"):
    if a == 0:
        return (f"@keyframes {name}{{0%{{opacity:1;transform:none}}{p(b-0.12)}{{opacity:1;transform:none}}"
                f"{p(b+0.1)}{{opacity:0;transform:scale(1.18)}}100%{{opacity:0;transform:scale(1.18)}}}}\n")
    if b >= T:
        return (f"@keyframes {name}{{0%,{p(a-0.02)}{{opacity:0;transform:scale(.9)}}{p(a+0.22)}{{opacity:1;transform:none}}"
                f"100%{{opacity:1;transform:none}}}}\n")
    return (f"@keyframes {name}{{0%,{p(a-0.02)}{{opacity:0;transform:{enter}}}{p(a+0.22)}{{opacity:1;transform:none}}"
            f"{p(b-0.14)}{{opacity:1;transform:none}}{p(b+0.08)}{{opacity:0;transform:{leave}}}100%{{opacity:0;transform:{leave}}}}}\n")

def slam(name, t, frm="scale(1.6)", dur=0.26):
    return (f"@keyframes {name}{{0%,{p(t)}{{opacity:0;transform:{frm}}}{p(t+dur)}{{opacity:1;transform:none}}100%{{opacity:1;transform:none}}}}\n")

def grow(name, t, dur, prop="width", a="0", b="100%"):
    return f"@keyframes {name}{{0%,{p(t)}{{{prop}:{a}}}{p(t+dur)}{{{prop}:{b}}}100%{{{prop}:{b}}}}}\n"

kf = ""
cuts = [0.7, 1.4, 2.1, 3.6, 5.1, 6.6, 8.2]
S = [(0, 2.1), (2.1, 3.6), (3.6, 5.1), (5.1, 6.6), (6.6, 8.2), (8.2, T)]
for i, (a, b) in enumerate(S, 1):
    kf += scene(f"s{i}", a, b)

# hook interrupts
for i, t in enumerate([0.7, 0.85, 1.0]):
    kf += slam(f"x{i}", t, "scale(2.2) rotate(-14deg)", 0.22)
kf += slam("agentchip", 1.4, "translateY(60px) scale(1.4)")
kf += slam("wait", 1.4, "scale(1.5)")
# flashes at 1.4, 2.1, 3.6, 5.1, 6.6, 8.2 (never at t=0)
fl = "@keyframes flash{0%{opacity:0}"
for t, o in [(1.4, .55), (2.1, .7), (3.6, .45), (5.1, .45), (6.6, .55), (8.2, .95)]:
    fl += f"{p(t-0.01)}{{opacity:0}}{p(t+0.02)}{{opacity:{o}}}{p(t+0.25)}{{opacity:0}}"
fl += "100%{opacity:0}}\n"
kf += fl
# camera punch on cuts
cam = "@keyframes cam{0%{transform:scale(1.07)}" + f"{p(0.32)}{{transform:scale(1)}}"
for t in [1.4, 2.1, 3.6, 5.1, 6.6, 8.2]:
    cam += f"{p(t-0.01)}{{transform:scale(1)}}{p(t+0.05)}{{transform:scale(1.05)}}{p(t+0.32)}{{transform:scale(1)}}"
cam += "100%{transform:scale(1)}}\n"
kf += cam
# progress dots
for i, (a, b) in enumerate([(2.1, 3.6), (3.6, 5.1), (5.1, 6.6)], 1):
    kf += (f"@keyframes d{i}{{0%,{p(a-0.01)}{{background:rgba(15,27,61,.18);transform:scale(1)}}{p(a+0.15)}{{background:#2F5BEA;transform:scale(1.35)}}"
           f"{p(b-0.01)}{{background:#2F5BEA;transform:scale(1.35)}}{p(b+0.1)}{{background:#F07A1A;transform:scale(1)}}100%{{background:#F07A1A;transform:scale(1)}}}}\n")
kf += f"@keyframes dots{{0%,{p(2.05)}{{opacity:0}}{p(2.25)}{{opacity:1}}{p(7.9)}{{opacity:1}}{p(8.2)}{{opacity:0}}100%{{opacity:0}}}}\n"
# scene 2 chat
kf += slam("b1", 2.3, "translateX(-80px) scale(.8)")
kf += slam("typing", 2.65, "scale(.6)", 0.15)
kf += f"@keyframes typingout{{0%,{p(2.95)}{{opacity:1}}{p(3.0)}{{opacity:0}}100%{{opacity:0}}}}\n"
kf += slam("b2", 3.0, "translateX(80px) scale(.8)", 0.22)
kf += slam("ok2", 3.2, "scale(2)")
# scene 3 sheet
for r in range(6):
    kf += grow(f"r{r}", 3.75 + r * 0.16, 0.22)
kf += f"@keyframes cur{{0%,{p(3.7)}{{transform:translateY(0)}}{p(4.75)}{{transform:translateY(480px)}}100%{{transform:translateY(480px)}}}}\n"
kf += slam("ok3", 4.75, "scale(2)")
# scene 4 report
for i, h in enumerate([38, 52, 46, 70, 84, 96]):
    kf += grow(f"h{i}", 5.25 + i * 0.1, 0.35, "height", "0%", f"{h}%")
kf += f"@keyframes line{{0%,{p(5.5)}{{stroke-dashoffset:1400}}{p(6.2)}{{stroke-dashoffset:0}}100%{{stroke-dashoffset:0}}}}\n"
kf += slam("ok4", 6.15, "scale(2)")
# scene 5 orbit
kf += slam("n5", 6.75, "scale(.3)", 0.35)
kf += slam("meta", 7.35, "scale(1.4)")
# scene 6 brand
kf += f"@keyframes vain{{0%,{p(8.2)}{{opacity:0;transform:scale(.3)}}{p(8.5)}{{opacity:1;transform:scale(1.12)}}{p(8.65)}{{opacity:1;transform:none}}{p(9.72)}{{opacity:1;transform:none}}100%{{opacity:0;transform:none}}}}\n"
kf += slam("bw", 8.35, "scale(1.5)")
kf += slam("bt", 8.5, "translateY(40px)")
kf += slam("cta", 8.65, "scale(1.6)")
kf += slam("url", 8.8, "scale(1.4)")
# loop: brand text eases away at the very end, back to the hook look
kf += f"@keyframes s6out{{0%,{p(9.72)}{{opacity:1}}100%{{opacity:.0}}}}\n"
# global sun path
kf += ("@keyframes sunmove{0%{transform:translate(0,0) scale(1)}" + f"{p(2.0)}{{transform:translate(0,0) scale(1)}}"
       f"{p(2.35)}{{transform:translate(330px,-210px) scale(.42)}}{p(6.5)}{{transform:translate(330px,-210px) scale(.42)}}"
       f"{p(6.85)}{{transform:translate(0,600px) scale(.62)}}{p(8.05)}{{transform:translate(0,600px) scale(.62)}}"
       f"{p(8.35)}{{transform:translate(0,0) scale(1)}}100%{{transform:translate(0,0) scale(1)}}}}\n")

# particles
dots = ""
for i in range(150):
    x, y = rng.randint(0, 1080), rng.randint(-200, 2100)
    s = rng.choice([3, 4, 5, 6, 8])
    c = rng.choice(["", "", " b", " w"])
    d = rng.uniform(1.2, 2.6)
    dots += f'<i class="dot{c}" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;animation-duration:{d:.2f}s;animation-delay:-{rng.uniform(0,2):.2f}s"></i>'
rays = "".join(f'<i class="ray" style="transform:rotate({a}deg)"></i>' for a in range(0, 360, 20))

html = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;overflow:hidden;font-family:'Montserrat',sans-serif;background:#CFE8FF}}
.st{{position:relative;width:1080px;height:1920px;overflow:hidden;background:linear-gradient(180deg,#8CCBFF 0%,#CFE8FF 46%,#FFE4C2 100%)}}
.cam{{position:absolute;inset:0;animation:cam {T}s cubic-bezier(.2,.8,.2,1) forwards}}
.blob{{position:absolute;border-radius:50%;filter:blur(110px)}}
.g1{{left:-240px;top:-160px;width:760px;height:760px;background:#FFC15E;opacity:.55;animation:drift 6s ease-in-out infinite alternate}}
.g2{{left:520px;top:1180px;width:820px;height:820px;background:#2F5BEA;opacity:.22;animation:drift 7s ease-in-out infinite alternate-reverse}}
.g3{{left:-200px;top:1450px;width:700px;height:600px;background:#FFC15E;opacity:.45;animation:drift 5s ease-in-out infinite alternate}}
@keyframes drift{{to{{transform:translate(110px,-120px) scale(1.12)}}}}
.grid{{position:absolute;left:-420px;bottom:-300px;width:1920px;height:900px;transform:perspective(900px) rotateX(72deg);
 background-image:linear-gradient(rgba(47,91,234,.5) 2px,transparent 2px),linear-gradient(90deg,rgba(47,91,234,.42) 2px,transparent 2px);background-size:110px 110px;
 -webkit-mask-image:linear-gradient(to top,#000 10%,transparent 80%);animation:gridmove 2.5s linear infinite}}
@keyframes gridmove{{to{{background-position:0 110px}}}}
.dust{{position:absolute;inset:0;animation:rise {T}s linear forwards}}@keyframes rise{{to{{transform:translateY(-260px)}}}}
.dot{{position:absolute;border-radius:50%;background:#F5A623;box-shadow:0 0 10px #FFC15E;animation:tw 2s ease-in-out infinite alternate}}
.dot.b{{background:#2F5BEA;box-shadow:0 0 10px rgba(47,91,234,.7)}}.dot.w{{background:#fff;box-shadow:0 0 12px #fff}}
@keyframes tw{{to{{opacity:.15}}}}
/* sun */
.sunG{{position:absolute;left:540px;top:400px;width:0;height:0;z-index:5;animation:sunmove {T}s cubic-bezier(.7,0,.3,1) forwards}}
.rays{{position:absolute;left:0;top:0;animation:spin 16s linear infinite}}
.ray{{position:absolute;left:-6px;top:-560px;width:12px;height:560px;transform-origin:6px 560px;background:linear-gradient(to top,rgba(255,247,222,.0),rgba(255,224,150,.75) 45%,transparent);filter:blur(4px)}}
.ray{{left:-6px;top:-560px}}
.sunO{{position:absolute;left:-210px;top:-210px;width:420px;height:420px;border-radius:50%;background:radial-gradient(circle at 40% 34%,#FFF7DE 0%,#FFD37A 38%,#FFC15E 60%,#F07A1A 100%);
 box-shadow:0 0 150px 60px rgba(255,170,60,.6),0 0 0 14px rgba(255,247,222,.55);animation:pulse .43s ease-in-out infinite alternate}}
@keyframes pulse{{to{{box-shadow:0 0 210px 90px rgba(255,170,60,.72),0 0 0 22px rgba(255,247,222,.65)}}}}
.ring{{position:absolute;left:-290px;top:-290px;width:580px;height:580px;border-radius:50%;border:5px solid rgba(47,91,234,.8);border-left-color:transparent;border-bottom-color:rgba(6,182,212,.7);animation:spin 2.6s linear infinite}}
.ring.b{{left:-345px;top:-345px;width:690px;height:690px;border:3px dashed rgba(240,122,26,.6);animation:spin 9s linear infinite reverse}}
.sunVA{{position:absolute;left:-210px;top:-210px;width:420px;height:420px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:160px;color:#3A1A00;opacity:0;animation:vain {T}s cubic-bezier(.2,.9,.3,1.3) forwards}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.scan{{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(15,27,61,.035) 0 2px,transparent 2px 5px);z-index:60;pointer-events:none}}
.flash{{position:absolute;inset:0;background:radial-gradient(circle at 50% 40%,#FFFDF5,#FFE9B8 60%,#FFD37A);opacity:0;z-index:70;animation:flash {T}s linear forwards}}
.sc{{position:absolute;inset:0;z-index:10}}
.s1{{animation:s1 {T}s cubic-bezier(.7,0,.3,1) forwards}}.s2{{opacity:0;animation:s2 {T}s cubic-bezier(.2,.8,.2,1) forwards}}
.s3{{opacity:0;animation:s3 {T}s cubic-bezier(.2,.8,.2,1) forwards}}.s4{{opacity:0;animation:s4 {T}s cubic-bezier(.2,.8,.2,1) forwards}}
.s5{{opacity:0;animation:s5 {T}s cubic-bezier(.2,.8,.2,1) forwards}}.s6{{opacity:0;animation:s6 {T}s cubic-bezier(.2,.8,.2,1) forwards}}
.c{{position:absolute;left:0;width:1080px;text-align:center}}
.hk{{font-weight:900;color:#0F1B3D;letter-spacing:-.02em;line-height:1;text-shadow:0 6px 30px rgba(255,255,255,.7)}}
.pill{{display:inline-block;background:#0F1B3D;color:#FFC15E;padding:10px 46px 22px;border-radius:40px;box-shadow:0 20px 60px rgba(15,27,61,.35),0 0 0 4px rgba(255,193,94,.6)}}
.en{{font-family:'Inter',sans-serif;font-weight:700;color:#1E3A8A;font-size:44px;letter-spacing:.01em}}
.mono{{font-family:'DejaVu Sans Mono',monospace;font-size:26px;letter-spacing:.14em;color:#1E3A8A;font-weight:700}}
.glass{{position:absolute;background:rgba(255,255,255,.55);backdrop-filter:blur(14px);border:2px solid rgba(255,255,255,.9);border-radius:30px;box-shadow:0 24px 70px rgba(15,27,61,.18)}}
.task{{width:300px;height:190px;padding:26px 24px}}
.task b{{display:block;font-size:36px;font-weight:800;color:#0F1B3D;line-height:1.1;margin-top:16px}}
.x{{position:absolute;right:-18px;top:-26px;background:#C2410C;color:#fff;font-weight:900;font-size:24px;letter-spacing:.06em;padding:10px 16px;border-radius:14px;box-shadow:0 10px 30px rgba(194,65,12,.4);opacity:0}}
.chip{{display:inline-block;background:#2F5BEA;color:#fff;font-weight:800;font-size:46px;padding:18px 44px;border-radius:60px;box-shadow:0 18px 50px rgba(47,91,234,.45)}}
.dots{{position:absolute;top:150px;left:0;width:1080px;display:flex;justify-content:center;gap:26px;z-index:40;animation:dots {T}s linear forwards}}
.dots i{{display:block;width:28px;height:28px;border-radius:50%;background:rgba(15,27,61,.18);border:3px solid rgba(255,255,255,.9)}}
.num{{font-weight:900;font-size:220px;color:#2F5BEA;line-height:1;text-shadow:0 0 60px rgba(47,91,234,.35)}}
.ttl{{font-weight:900;font-size:110px;color:#0F1B3D;letter-spacing:-.02em;line-height:1.02}}
.ok{{display:inline-block;background:#15803D;color:#fff;font-weight:900;font-size:40px;letter-spacing:.06em;padding:14px 34px;border-radius:20px;box-shadow:0 14px 40px rgba(21,128,61,.4);opacity:0}}
.bub{{position:absolute;padding:28px 36px;border-radius:34px;font-family:'Inter';font-weight:700;font-size:40px;line-height:1.2;opacity:0}}
.bu{{left:110px;background:#fff;color:#0F1B3D;border-bottom-left-radius:8px;box-shadow:0 14px 40px rgba(15,27,61,.15)}}
.ba{{right:110px;background:#2F5BEA;color:#fff;border-bottom-right-radius:8px;box-shadow:0 14px 40px rgba(47,91,234,.4)}}
.row{{height:58px;margin:18px 0;border-radius:12px;background:rgba(15,27,61,.08);overflow:hidden;position:relative}}
.row i{{position:absolute;left:0;top:0;bottom:0;width:0;border-radius:12px;background:linear-gradient(90deg,#2F5BEA,#06B6D4)}}
.bar{{position:absolute;bottom:0;width:90px;height:0;border-radius:14px 14px 4px 4px;background:linear-gradient(to top,#2F5BEA,#06B6D4)}}
.bar.o{{background:linear-gradient(to top,#F07A1A,#FFC15E)}}
.node{{position:absolute;width:250px;height:110px;margin:-55px 0 0 -125px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:36px;color:#0F1B3D}}
.orb{{position:absolute;left:540px;top:1000px;width:0;height:0;animation:spin 6s linear infinite}}
.orb .k{{position:absolute;animation:spin 6s linear infinite reverse}}
</style></head><body><div class="st"><div class="cam">
<div class="blob g1"></div><div class="blob g2"></div><div class="blob g3"></div>
<div class="grid"></div><div class="dust">{dots}</div>
<div class="sunG"><div class="rays">{rays}</div><div class="ring b"></div><div class="ring"></div><div class="sunO"></div><div class="sunVA">VA</div></div>

<div class="dots"><i style="animation:d1 {T}s linear forwards"></i><i style="animation:d2 {T}s linear forwards"></i><i style="animation:d3 {T}s linear forwards"></i></div>

<!-- S1 hook -->
<div class="sc s1">
 <div class="c hk" style="top:660px;font-size:150px">ХВАТИТ</div>
 <div class="c hk" style="top:815px;font-size:124px">ДЕЛАТЬ ЭТО</div>
 <div class="c" style="top:955px"><span class="pill hk" style="font-size:146px;color:#FFC15E;text-shadow:0 0 30px rgba(255,193,94,.5)">РУКАМИ</span></div>
 <div class="c en" style="top:1170px">Stop doing this by hand</div>
 <div class="glass task" style="left:60px;top:1300px;transform:rotate(-5deg)"><span class="mono">ЗАДАЧА 01</span><b>Ответить клиенту</b><span class="x" style="animation:x0 {T}s cubic-bezier(.2,.9,.3,1.3) forwards">ВРУЧНУЮ ✕</span></div>
 <div class="glass task" style="left:390px;top:1340px;transform:rotate(2deg)"><span class="mono">ЗАДАЧА 02</span><b>Заполнить таблицу</b><span class="x" style="animation:x1 {T}s cubic-bezier(.2,.9,.3,1.3) forwards">ВРУЧНУЮ ✕</span></div>
 <div class="glass task" style="left:720px;top:1300px;transform:rotate(5deg)"><span class="mono">ЗАДАЧА 03</span><b>Собрать отчёт</b><span class="x" style="animation:x2 {T}s cubic-bezier(.2,.9,.3,1.3) forwards">ВРУЧНУЮ ✕</span></div>
 <div class="c" style="top:1580px;opacity:0;animation:agentchip {T}s cubic-bezier(.2,.9,.3,1.3) forwards"><span class="chip">→ это сделает ИИ-агент</span></div>
 <div class="c mono" style="top:1700px;font-size:30px;opacity:0;animation:wait {T}s cubic-bezier(.2,.9,.3,1.3) forwards">3 ЗАДАЧИ · СМОТРИ ДО #3</div>
</div>

<!-- S2 chat -->
<div class="sc s2">
 <div class="c" style="top:300px"><span class="num">#1</span></div>
 <div class="c ttl" style="top:540px">Ответы<br>клиентам</div>
 <div class="c en" style="top:790px">Customer replies</div>
 <div class="glass" style="left:70px;top:900px;width:940px;height:640px">
  <div class="mono" style="position:absolute;left:40px;top:30px">ЧАТ · <span style="color:#15803D">АГЕНТ ОНЛАЙН ●</span></div>
  <div class="bub bu" style="top:110px;animation:b1 {T}s cubic-bezier(.2,.9,.3,1.3) forwards">Вы сегодня работаете?</div>
  <div class="bub ba" style="top:270px;opacity:0;animation:typing {T}s ease forwards,typingout {T}s linear forwards">• • •</div>
  <div class="bub ba" style="top:270px;animation:b2 {T}s cubic-bezier(.2,.9,.3,1.3) forwards">Да! Отвечаю сразу —<br>в любое время.</div>
  <div style="position:absolute;left:40px;bottom:40px"><span class="ok" style="animation:ok2 {T}s cubic-bezier(.2,.9,.3,1.3) forwards">АВТО ✓</span></div>
 </div>
</div>

<!-- S3 sheet -->
<div class="sc s3">
 <div class="c" style="top:300px"><span class="num">#2</span></div>
 <div class="c ttl" style="top:540px">Таблицы<br>и данные</div>
 <div class="c en" style="top:790px">Spreadsheets &amp; data</div>
 <div class="glass" style="left:70px;top:900px;width:940px;height:640px;padding:90px 50px 0">
  <div class="mono" style="position:absolute;left:50px;top:32px">ТАБЛИЦА · АВТОЗАПОЛНЕНИЕ</div>
  {''.join(f'<div class="row"><i style="animation:r{r} {T}s cubic-bezier(.2,.8,.2,1) forwards;max-width:{rng.randint(70,100)}%"></i></div>' for r in range(6))}
  <div style="position:absolute;left:30px;top:96px;width:8px;height:58px;background:#F07A1A;border-radius:4px;box-shadow:0 0 18px #F07A1A;animation:cur {T}s cubic-bezier(.7,0,.3,1) forwards"></div>
  <div style="position:absolute;right:40px;bottom:30px"><span class="ok" style="animation:ok3 {T}s cubic-bezier(.2,.9,.3,1.3) forwards">ГОТОВО ✓</span></div>
 </div>
</div>

<!-- S4 report -->
<div class="sc s4">
 <div class="c" style="top:300px"><span class="num">#3</span></div>
 <div class="c ttl" style="top:540px">Отчёты<br>сами собой</div>
 <div class="c en" style="top:790px">Reports that build themselves</div>
 <div class="glass" style="left:70px;top:900px;width:940px;height:640px">
  <div class="mono" style="position:absolute;left:50px;top:32px">ОТЧЁТ · ЕЖЕДНЕВНО</div>
  <div style="position:absolute;left:70px;right:70px;top:110px;bottom:120px">
   {''.join(f'<div class="bar{" o" if i==5 else ""}" style="left:{i*135}px;animation:h{i} {T}s cubic-bezier(.2,.8,.2,1) forwards"></div>' for i in range(6))}
   <svg width="800" height="410" style="position:absolute;left:0;top:0;overflow:visible"><polyline points="45,250 180,200 315,225 450,130 585,80 720,20" fill="none" stroke="#0F1B3D" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1400" stroke-dashoffset="1400" style="animation:line {T}s cubic-bezier(.2,.8,.2,1) forwards"/></svg>
  </div>
  <div style="position:absolute;left:50px;bottom:34px"><span class="ok" style="animation:ok4 {T}s cubic-bezier(.2,.9,.3,1.3) forwards">ОТЧЁТ ГОТОВ ✓</span></div>
 </div>
</div>

<!-- S5 agent orbit -->
<div class="sc s5">
 <div class="c ttl" style="top:250px;font-size:104px">Всё это —<br><span style="color:#2F5BEA">ИИ-агент</span></div>
 <div class="c en" style="top:500px">All of it — one AI agent</div>
 <div class="orb">
  {''.join(f'<div class="k" style="left:{x}px;top:{y}px"><div class="glass node" style="opacity:0;animation:n5 {T}s cubic-bezier(.2,.9,.3,1.3) forwards">{n}</div></div>' for n,(x,y) in [("ЧАТ",(0,-360)),("ТАБЛИЦЫ",(360,0)),("ОТЧЁТЫ",(0,360)),("ВИДЕО",(-360,0))])}
 </div>
 <div class="c" style="top:1500px;opacity:0;animation:meta {T}s cubic-bezier(.2,.9,.3,1.3) forwards"><span class="chip" style="font-size:42px">Мы создаём их для бизнеса</span><div class="en" style="margin-top:22px;font-size:38px">We build them for businesses</div></div>
</div>

<!-- S6 brand -->
<div class="sc s6"><div style="position:absolute;inset:0;animation:s6out {T}s linear forwards">
 <div class="c hk" style="top:700px;font-size:104px;opacity:0;animation:bw {T}s cubic-bezier(.2,.9,.3,1.3) forwards">VA Corporation</div>
 <div class="c en" style="top:835px;font-size:42px;color:#0F1B3D;opacity:0;animation:bt {T}s cubic-bezier(.2,.8,.2,1) forwards">AI agents · Games · Software</div>
 <div class="c" style="top:960px;opacity:0;animation:cta {T}s cubic-bezier(.2,.9,.3,1.3) forwards"><span class="pill hk" style="font-size:104px;padding:16px 60px 26px">Подпишись</span><div class="en" style="margin-top:18px;font-size:38px">Follow us</div></div>
 <div class="c" style="top:1260px;opacity:0;animation:url {T}s cubic-bezier(.2,.9,.3,1.3) forwards"><span class="glass" style="position:relative;display:inline-block;padding:24px 46px;font-weight:800;font-size:64px;color:#0F1B3D;letter-spacing:-.01em">va-corporation.github.io</span></div>
</div></div>

<div class="flash"></div><div class="scan"></div>
</div></div>
<style>{kf}</style></body></html>"""
pathlib.Path(__file__).with_name("2026-11-24-ru.html").write_text(html, encoding="utf-8")
print("ok", len(html))
