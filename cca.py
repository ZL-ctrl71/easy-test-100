import streamlit as st
import random
import time
import math
import streamlit.components.v1 as components

# --- 1. ตั้งค่าหน้าจอและดีไซน์ Seamless Theme ---
st.set_page_config(page_title="Math & Physics Universe", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #161625 0%, #0d0d14 100%); color: #ffffff; }
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.08) !important; color: #00ffcc !important;
        border: 2px solid #334455 !important; border-radius: 12px !important;
        font-size: 32px !important; font-weight: bold; text-align: center; height: 65px !important; transition: all 0.3s ease;
    }
    .stTextInput > div > div > input:focus { border-color: #00ffcc !important; box-shadow: 0 0 15px rgba(0, 255, 204, 0.3) !important; }
    h1, h2, h3 { color: #00ffcc !important; }
    .stAlert { background-color: rgba(0, 255, 204, 0.1) !important; color: #00ffcc !important; border: 1px solid rgba(0,255,204,0.3) !important; border-radius: 10px; }
    .stButton > button { border-radius: 10px !important; height: 50px !important; font-size: 16px !important; font-weight: bold !important; transition: 0.2s; }
    .stat-box { background: rgba(0, 0, 0, 0.3); border: 1px solid #333; border-radius: 10px; padding: 10px; text-align: center; margin-bottom: 20px; }
    .solution-box { background: rgba(255, 255, 255, 0.05); border-left: 4px solid #00ffcc; padding: 15px; border-radius: 5px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ระบบจัดการสถานะแอป ---
if 'stage' not in st.session_state: st.session_state.stage = 'setup'
if 'score' not in st.session_state: st.session_state.score = 0
if 'q_count' not in st.session_state: st.session_state.q_count = 0
if 'current_q' not in st.session_state: st.session_state.current_q = None
if 'show_solution' not in st.session_state: st.session_state.show_solution = False
if 'last_answer_correct' not in st.session_state: st.session_state.last_answer_correct = False

# --- รายการเนื้อหาตามระดับความยาก ---
EASY_TOPICS = [
    "คณิต: เศษส่วน (บวก/ลบ)", "คณิต: ทฤษฎีบทพีทาโกรัส", "แคลคูลัส: การหาอนุพันธ์เบื้องต้น",
    "ฟิสิกส์: การเคลื่อนที่แนวตรง", "ฟิสิกส์: กฎของโอห์ม", "ฟิสิกส์: พลังงานจลน์"
]

HARD_TOPICS = [
    "คณิต: สมการกำลังสอง", "คณิต: ตรีโกณมิติ (กฎของโคไซน์)", "คณิต: ลอการิทึม", 
    "คณิต: เมทริกซ์ (ดีเทอร์มิแนนต์ 2x2)", "คณิต: ลำดับเลขคณิต", "คณิต: จำนวนเชิงซ้อน (หาขนาด)",
    "คณิต: ความน่าจะเป็น", "แคลคูลัส: กฎลูกโซ่", "แคลคูลัส: อินทิเกรตจำกัดเขต", 
    "แคลคูลัส: ลิมิต", "ฟิสิกส์: วงจรไฟฟ้าผสม", "ฟิสิกส์: โปรเจกไทล์", 
    "ฟิสิกส์: อนุรักษ์พลังงาน", "ฟิสิกส์: โมเมนตัม (ชนติดกัน)", "ฟิสิกส์: การเคลื่อนที่แบบวงกลม", 
    "ฟิสิกส์: แรงสปริง (กฎของฮุก)", "ฟิสิกส์: แรงลอยตัว", "ฟิสิกส์: กฎของบอยล์ (แก๊สอุดมคติ)",
    "ฟิสิกส์: สมการเลนส์บาง", "ฟิสิกส์: งานและพลังงาน"
]

# --- 3. ฟังก์ชันสุ่มโจทย์ + ระดับความยาก + วิธีทำ ---
def generate_question(selected_topics, difficulty):
    topic = random.choice(selected_topics)
    desc, math_eq, ans, solution = "", "", 0, ""
    
    # ================= หมวดหมู่ง่าย (Easy) =================
    if "เศษส่วน (บวก/ลบ)" in topic:
        den = random.choice([2, 4, 5, 10])
        num1, num2 = random.randint(1, 10), random.randint(1, 10)
        desc = "จงหาผลลัพธ์ของสมการเศษส่วนต่อไปนี้ (ตอบเป็นทศนิยม)"
        math_eq = r"\frac{" + str(num1) + r"}{" + str(den) + r"} + \frac{" + str(num2) + r"}{" + str(den) + r"} = ?"
        ans = (num1 + num2) / den
        solution = f"**วิธีทำ:**<br>1. นำเศษมาบวกกัน: {num1} + {num2} = {num1+num2}<br>2. ได้เศษส่วนคือ {num1+num2}/{den}<br>3. ทศนิยม: {num1+num2} ÷ {den} = {ans:.2f}"
        
    elif "พีทาโกรัส" in topic:
        triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13)]
        a, b, c = random.choice(triples)
        desc = f"สามเหลี่ยมมุมฉาก มีด้านประกอบมุมฉากยาว {a} และ {b} หน่วย จงหาด้านตรงข้ามมุมฉาก (c)"
        math_eq = r"c = \sqrt{a^2 + b^2}"
        ans = c
        solution = f"**วิธีทำ:**<br>1. c² = {a}² + {b}² = {a**2} + {b**2} = {c**2}<br>2. ถอดรากที่สอง จะได้ c = {c}"
        
    elif "อนุพันธ์เบื้องต้น" in topic:
        c, n = random.randint(2, 6), random.randint(2, 4)
        desc = "จงหาค่าอนุพันธ์ ณ จุดที่ x = 1"
        math_eq = r"\frac{d}{dx} (" + str(c) + r"x^{" + str(n) + r"}) = ?"
        ans = c * n
        solution = f"**วิธีทำ:**<br>1. ดิฟได้ {c*n}x^{n-1}<br>2. แทนค่า x = 1 จะได้ {ans}"
        
    elif "การเคลื่อนที่แนวตรง" in topic:
        u, a, t = random.randint(0, 5), random.randint(2, 5), random.randint(2, 5)
        desc = f"รถมีความเร็วต้น {u} m/s ความเร่ง {a} m/s² จงหาความเร็วเมื่อผ่านไป {t} วินาที (m/s)"
        math_eq = r"v = u + at"
        ans = u + (a * t)
        solution = f"**วิธีทำ:**<br>1. v = {u} + ({a} * {t}) = {ans} m/s"

    elif "กฎของโอห์ม" in topic:
        i, r = random.randint(2, 5), random.randint(5, 10)
        desc = f"วงจรมีกระแสไหล {i} A ความต้านทาน {r} Ω จงหาความต่างศักย์ (V)"
        math_eq = r"V = I \times R"
        ans = i * r
        solution = f"**วิธีทำ:**<br>1. V = {i} * {r} = {ans} V"
        
    elif "พลังงานจลน์" in topic:
        m, v = random.choice([2, 4, 6]), random.randint(2, 5)
        desc = f"วัตถุมวล {m} kg ความเร็ว {v} m/s มีพลังงานจลน์เท่าใด? (J)"
        math_eq = r"E_k = \frac{1}{2}mv^2"
        ans = 0.5 * m * (v**2)
        solution = f"**วิธีทำ:**<br>1. Ek = 0.5 * {m} * {v}² = {ans} J"

    # ================= หมวดหมู่ยาก (Hard) - คณิตศาสตร์ & แคลคูลัส =================
    elif "สมการกำลังสอง" in topic:
        r1, r2 = random.randint(1, 6), random.randint(-6, -1)
        b, c = -(r1 + r2), r1 * r2
        b_str = f"+ {b}x" if b > 0 else f"- {abs(b)}x" if b < 0 else ""
        c_str = f"+ {c}" if c > 0 else f"- {abs(c)}"
        desc = "จงหาคำตอบที่เป็น **ค่าบวก** ของสมการกำลังสองต่อไปนี้"
        math_eq = f"x^2 {b_str} {c_str} = 0"
        ans = r1
        solution = f"**วิธีทำ:**<br>1. แยกตัวประกอบได้ (x - {r1})(x - {r2}) = 0<br>2. คำตอบบวกคือ x = {r1}"

    elif "ตรีโกณมิติ" in topic:
        a, b = random.randint(3, 6), random.randint(4, 7)
        desc = f"สามเหลี่ยมมีด้าน a = {a}, b = {b} และมุมกั้น C = 60° จงหาค่าของ c²"
        math_eq = r"c^2 = a^2 + b^2 - 2ab\cos(C)"
        ans = (a**2) + (b**2) - (a*b)
        solution = f"**วิธีทำ:**<br>1. cos(60°) = 0.5<br>2. c² = {a}² + {b}² - 2({a})({b})(0.5) = {ans}"

    elif "ลอการิทึม" in topic:
        base = random.choice([2, 3, 4])
        exponent = random.randint(2, 4)
        val = base ** exponent
        desc = f"จงหาค่าของ x จากสมการต่อไปนี้"
        math_eq = f"\\log_{{{base}}}(x) = {exponent}"
        ans = val
        solution = f"**วิธีทำ:**<br>1. ดันฐานล็อกไปยกกำลัง: x = {base}^{exponent}<br>2. x = {ans}"

    elif "เมทริกซ์" in topic:
        a, b, c, d = random.randint(1, 5), random.randint(1, 5), random.randint(1, 5), random.randint(1, 5)
        desc = "จงหาค่า Determinant ของเมทริกซ์ 2x2 ต่อไปนี้"
        math_eq = f"\\det \\begin{{pmatrix}} {a} & {b} \\\\ {c} & {d} \\end{{pmatrix}}"
        ans = (a*d) - (b*c)
        solution = f"**วิธีทำ:**<br>1. (คูณลง) - (คูณขึ้น) = ({a}*{d}) - ({b}*{c})<br>2. {a*d} - {b*c} = {ans}"

    elif "ลำดับเลขคณิต" in topic:
        a1, d, n = random.randint(2, 10), random.randint(3, 8), random.randint(5, 15)
        desc = f"ลำดับเลขคณิตมีพจน์แรก a₁ = {a1} และผลต่างร่วม d = {d} จงหาพจน์ที่ {n} (aₙ)"
        math_eq = r"a_n = a_1 + (n-1)d"
        ans = a1 + (n - 1) * d
        solution = f"**วิธีทำ:**<br>1. a_{n} = {a1} + ({n}-1){d}<br>2. a_{n} = {a1} + { (n-1)*d } = {ans}"

    elif "จำนวนเชิงซ้อน" in topic:
        pairs = [(3, 4), (6, 8), (5, 12), (8, 15)]
        real, imag = random.choice(pairs)
        desc = "จงหาขนาด (Magnitude) ของจำนวนเชิงซ้อนต่อไปนี้"
        math_eq = f"z = {real} + {imag}i \\implies |z| = ?"
        ans = math.sqrt(real**2 + imag**2)
        solution = f"**วิธีทำ:**<br>1. |z| = √({real}² + {imag}²)<br>2. |z| = √({real**2 + imag**2}) = {ans}"

    elif "ความน่าจะเป็น" in topic:
        desc = "ทอยลูกเต๋า 2 ลูกพร้อมกัน จงหาความน่าจะเป็นที่ผลรวมหน้าลูกเต๋าเท่ากับ 7 (ตอบเป็นทศนิยม)"
        math_eq = r"P(E) = \frac{n(E)}{n(S)}"
        ans = 6 / 36
        solution = f"**วิธีทำ:**<br>1. n(S) = 6*6 = 36<br>2. ผลรวมเป็น 7 มี 6 แบบ: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1)<br>3. 6/36 = 1/6 ≈ {ans:.2f}"

    elif "กฎลูกโซ่" in topic:
        a, b = random.randint(2, 4), random.randint(1, 3)
        desc = "จงหาค่าอนุพันธ์ ณ จุดที่ x = 1"
        math_eq = r"\frac{d}{dx} (" + str(a) + r"x + " + str(b) + r")^2 = ?"
        ans = 2 * (a * 1 + b) * a
        solution = f"**วิธีทำ:**<br>1. d/dx (u)² = 2u * u'<br>2. ได้ 2({a}x + {b}) * {a}<br>3. แทน x=1: 2({a*1 + b}) * {a} = {ans}"

    elif "อินทิเกรตจำกัดเขต" in topic:
        c = random.choice([2, 4, 6])
        desc = "จงหาค่าของการอินทิเกรตจำกัดเขตต่อไปนี้"
        math_eq = f"\\int_{{0}}^{{2}} {c}x \\, dx = ?"
        ans = (c/2) * (2**2) # c/2 * x^2 evaluated at 2
        solution = f"**วิธีทำ:**<br>1. อินทิเกรต {c}x ได้ ({c}/2)x² = {c/2}x²<br>2. แทนขอบเขตบน(2) - ล่าง(0): {c/2}(2)² - 0 = {ans}"

    elif "ลิมิต" in topic:
        a = random.randint(2, 5)
        desc = f"จงหาค่าของลิมิตเมื่อ x เข้าใกล้ {a}"
        math_eq = f"\\lim_{{x \\to {a}}} \\frac{{x^2 - {a**2}}}{{x - {a}}} = ?"
        ans = 2 * a
        solution = f"**วิธีทำ:**<br>1. แยกตัวประกอบตัวเศษ: (x-{a})(x+{a})<br>2. ตัด (x-{a}) กับตัวส่วน<br>3. เหลือลิมิตของ (x+{a}) เมื่อ x->{a} คือ {a}+{a} = {ans}"
        # ================= หมวดหมู่ยาก (Hard) - ฟิสิกส์ =================
    elif "วงจรไฟฟ้าผสม" in topic:
        parallel_pairs = [(3, 6, 2), (4, 4, 2), (6, 12, 4), (10, 10, 5)]
        r2, r3, rp = random.choice(parallel_pairs)
        r1 = random.randint(2, 8)
        desc = f"วงจรมีตัวต้านทาน R1 = {r1} Ω ต่ออนุกรมกับ (R2 = {r2} Ω ขนานกับ R3 = {r3} Ω) จงหาความต้านทานรวม (Ω)"
        math_eq = r"R_{eq} = R_1 + \left( \frac{R_2 R_3}{R_2 + R_3} \right)"
        ans = r1 + rp
        solution = f"**วิธีทำ:**<br>1. ยุบวงจรขนานก่อน: Rp = ({r2}*{r3}) / ({r2}+{r3}) = {rp} Ω<br>2. นำมาบวกกับวงจรอนุกรม: Req = {r1} + {rp} = {ans} Ω"

    elif "โปรเจกไทล์" in topic:
        u = random.choice([10, 20, 30, 40])
        desc = f"วัตถุถูกยิงด้วยความเร็วต้น {u} m/s ทำมุม 45° กับแนวระดับ จงหาระยะตกไกลสุดในแนวแกน x (g = 10 m/s²)"
        math_eq = r"R_x = \frac{u^2 \sin(2\theta)}{g}"
        ans = (u**2) / 10 
        solution = f"**วิธีทำ:**<br>1. แทน θ = 45° จะได้ sin(90°) = 1<br>2. Rx = ({u}²) / 10 = {ans} m"

    elif "อนุรักษ์พลังงาน" in topic:
        heights = [(5, 10), (20, 20), (45, 30), (80, 40)] 
        h, v = random.choice(heights)
        desc = f"ปล่อยมวลตกอิสระจากความสูง {h} เมตร จงหาความเร็วกระทบพื้น (g = 10 m/s²)"
        math_eq = r"mgh = \frac{1}{2}mv^2 \implies v = \sqrt{2gh}"
        ans = v
        solution = f"**วิธีทำ:**<br>1. m ตัด m จะได้ v = √(2gh)<br>2. v = √(2 * 10 * {h}) = {v} m/s"

    elif "โมเมนตัม (ชนติดกัน)" in topic:
        m1, v1 = random.randint(2, 5), random.choice([4, 6, 8, 10])
        m2 = random.randint(2, 5)
        desc = f"วัตถุมวล {m1} kg วิ่งด้วยความเร็ว {v1} m/s ชนกับวัตถุมวล {m2} kg ที่อยู่นิ่ง หลังชนทั้งสองติดไปด้วยกัน จงหาความเร็วหลังชน (m/s)"
        math_eq = r"m_1 u_1 + m_2 u_2 = (m_1 + m_2)v"
        ans = (m1 * v1) / (m1 + m2)
        solution = f"**วิธีทำ:**<br>1. ก่อนชน: ({m1}*{v1}) + 0 = {m1*v1}<br>2. หลังชน: ({m1}+{m2})v = {m1+m2}v<br>3. ความเร็ว v = {m1*v1} / {m1+m2} = {ans:.2f} m/s"

    elif "การเคลื่อนที่แบบวงกลม" in topic:
        m, v, r = random.randint(2, 5), random.choice([2, 4, 6]), random.choice([2, 4])
        desc = f"วัตถุมวล {m} kg เคลื่อนที่แบบวงกลมรัศมี {r} เมตร ด้วยความเร็ว {v} m/s จงหาแรงสู่ศูนย์กลาง (N)"
        math_eq = r"F_c = \frac{mv^2}{r}"
        ans = (m * (v**2)) / r
        solution = f"**วิธีทำ:**<br>1. Fc = ({m} * {v}²) / {r}<br>2. Fc = ({m} * {v**2}) / {r} = {ans} N"

    elif "แรงสปริง (กฎของฮุก)" in topic:
        k = random.choice([100, 200, 500])
        x_cm = random.choice([5, 10, 20])
        x_m = x_cm / 100
        desc = f"สปริงมีค่าคงตัว k = {k} N/m ถูกดึงยืดออก {x_cm} cm จงหาแรงดึงกลับของสปริง (N)"
        math_eq = r"F = kx"
        ans = k * x_m
        solution = f"**วิธีทำ:**<br>1. แปลงระยะเป็นเมตร: x = {x_cm}/100 = {x_m} m<br>2. F = {k} * {x_m} = {ans} N"

    elif "แรงลอยตัว" in topic:
        v_m3 = random.choice([2, 3, 4, 5])
        desc = f"วัตถุปริมาตร {v_m3} m³ จมมิดในน้ำ (ความหนาแน่นน้ำ = 1000 kg/m³, g = 10 m/s²) จงหาแรงลอยตัว (N)"
        math_eq = r"F_b = \rho V g"
        ans = 1000 * v_m3 * 10
        solution = f"**วิธีทำ:**<br>1. Fb = 1000 * {v_m3} * 10 = {ans} N"

    elif "กฎของบอยล์ (แก๊สอุดมคติ)" in topic:
        p1, v1 = random.choice([1, 2, 3]), random.choice([10, 20, 30])
        p2 = p1 * 2
        desc = f"แก๊สมีปริมาตร {v1} L ที่ความดัน {p1} atm หากเพิ่มความดันเป็น {p2} atm โดยอุณหภูมิคงที่ ปริมาตรใหม่จะเป็นเท่าใด (L)"
        math_eq = r"P_1 V_1 = P_2 V_2"
        ans = (p1 * v1) / p2
        solution = f"**วิธีทำ:**<br>1. ({p1})({v1}) = ({p2})(V2)<br>2. V2 = {p1*v1} / {p2} = {ans} L"

    elif "สมการเลนส์บาง" in topic:
        f, s = random.choice([(10, 30), (15, 30), (20, 60)])
        desc = f"วางวัตถุห่างจากเลนส์นูน {s} cm เลนส์มีความยาวโฟกัส {f} cm จงหาระยะภาพ (cm)"
        math_eq = r"\frac{1}{f} = \frac{1}{s} + \frac{1}{s'}"
        ans = (f * s) / (s - f)
        solution = f"**วิธีทำ:**<br>1. 1/{f} = 1/{s} + 1/s'<br>2. 1/s' = 1/{f} - 1/{s} = ({s}-{f}) / {s*f}<br>3. กลับเศษเป็นส่วน: s' = {s*f} / {s-f} = {ans} cm"

    elif "งานและพลังงาน" in topic:
        f_n = random.choice([20, 30, 40, 50])
        s_m = random.choice([5, 10, 15])
        desc = f"ออกแรง {f_n} N ลากกล่องไปตามพื้นราบในทิศเดียวกับการเคลื่อนที่ เป็นระยะทาง {s_m} เมตร จงหางานที่เกิดขึ้น (J)"
        math_eq = r"W = F \cdot s \cdot \cos(\theta)"
        ans = f_n * s_m
        solution = f"**วิธีทำ:**<br>1. ทิศเดียวกันมุม θ = 0° (cos 0° = 1)<br>2. W = {f_n} * {s_m} * 1 = {ans} J"
        
    return {"desc": desc, "math": math_eq, "a": round(float(ans), 2), "topic": topic, "solution": solution}

# --- 4. ระบบตรวจคำตอบ ---
def submit_answer():
    key = f"ans_{st.session_state.q_count}"
    try:
        user_val = float(st.session_state[key])
        if abs(user_val - st.session_state.current_q['a']) < 0.1:
            st.session_state.score += 1
            st.session_state.last_answer_correct = True
        else:
            st.session_state.last_answer_correct = False
    except: 
        st.session_state.last_answer_correct = False

    if "ทบทวน" in st.session_state.mode:
        st.session_state.show_solution = True
    else:
        next_question()

def next_question():
    st.session_state.show_solution = False
    st.session_state.q_count += 1
    if "Fixed" in st.session_state.mode and st.session_state.q_count >= st.session_state.total_q:
        st.session_state.stage = 'result'
    else:
        st.session_state.current_q = generate_question(st.session_state.selected_topics, st.session_state.difficulty)
        st.session_state.q_start_time = time.time()

# --- 5. นาฬิกาจับเวลา (แสดงเฉพาะโหมดสอบ) ---
def render_smart_timer(global_secs, q_secs):
    if "ทบทวน" in st.session_state.mode: return 
    html_code = f"""
    <div style="display: flex; justify-content: space-around; font-family: sans-serif; text-align: center; background: rgba(0,255,204,0.05); border: 1px solid rgba(0,255,204,0.2); padding: 10px; border-radius: 10px; margin-bottom: 15px;">
        <div style="color: #ff4b4b;"> <span style="font-size: 13px; opacity: 0.8;">⏰ เวลารวมเหลือ</span><br> <span style="font-size: 26px; font-weight: bold;" id="g_timer">{global_secs} วิ</span> </div>
        {"<div style='color: #00ffcc;'><span style='font-size: 13px; opacity: 0.8;'>⏱️ เวลาข้อนี้เหลือ</span><br><span style='font-size: 26px; font-weight: bold;' id='q_timer'>" + str(q_secs) + " วิ</span></div>" if q_secs > 0 else ""}
    </div>
    <script>
        var g_left = {global_secs}; var q_left = {q_secs}; var has_q_timer = {str(q_secs > 0).lower()};
        var interval = setInterval(function() {{
            g_left--; document.getElementById('g_timer').innerHTML = g_left + " วิ";
            if (has_q_timer) {{ q_left--; document.getElementById('q_timer').innerHTML = q_left + " วิ"; }}
            if (g_left <= 0 || (has_q_timer && q_left <= 0)) {{
                clearInterval(interval);
                var btns = window.parent.document.getElementsByTagName('button');
                for (var i = 0; i < btns.length; i++) {{
                    if (g_left <= 0 && btns[i].textContent.includes('STOP EXAM')) {{ btns[i].click(); break; }}
                    if (q_left <= 0 && btns[i].textContent.includes('SKIP')) {{ btns[i].click(); break; }}
                }}
            }}
        }}, 1000);
    </script>
    """
    components.html(html_code, height=85)

# ==========================================
# UI: หน้าแรก (Setup)
# ==========================================
if st.session_state.stage == 'setup':
    st.markdown("<h1 style='text-align: center; font-size: 45px;'>การสอบของคนว่าง</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.7; margin-bottom: 30px;'>พัฒนาด้วยใจ: จากกร</p>", unsafe_allow_html=True)
    
    col_diff, col_mode = st.columns(2)
    with col_diff:
        st.session_state.difficulty = st.radio(" ระดับความยาก:", ["ง่ายนิดนึง (พื้นฐาน)", "ยากสุดๆไม่มีลุ้นข้อกานะ (แอดวานซ์)"])
    with col_mode:
        st.session_state.mode = st.radio(" รูปแบบการใช้งาน", ["สอบ Fixed (อันนี้เอาแค่นี้พอได้ทำ)", "สอบ Endless (สำหรับคนว่าง)", " เอาไว้ทบทวน (ไม่จับเวลา+มีเฉลย)"])
    
    is_review = "ทบทวน" in st.session_state.mode
    st.markdown("<hr style='border-color: #333;'>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: st.session_state.total_q = st.number_input("เป้าหมายจำนวนข้อ:", 1, 200, 10, disabled=("Endless" in st.session_state.mode))
    with c2: st.session_state.time_total = st.number_input("เวลารวม (นาที):", 1, 180, 10, disabled=is_review)
    with c3: st.session_state.time_q = st.number_input("เวลาต่อข้อ (วิ) [0=ไม่จำกัด]:", 0, 300, 30, disabled=is_review)

    st.write(" **หลักสูตร:**")
    active_topics = HARD_TOPICS if "ยาก" in st.session_state.difficulty else EASY_TOPICS
    
    # วนลูปเพื่อสร้าง Checkbox แบบ 2 คอลัมน์ให้ดูสวยงามและไม่รก
    cols = st.columns(2)
    selected_topics = []
    for i, t in enumerate(active_topics):
        with cols[i % 2]:
            if st.checkbox(t, value=True):
                selected_topics.append(t)
                
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("START (อ่าเวลาปวดหัว)", use_container_width=True, type="primary"):
        if not selected_topics: st.error("เลือกซักอันแหมะ")
        else:
            st.session_state.selected_topics = selected_topics
            st.session_state.score = 0
            st.session_state.q_count = 0
            st.session_state.show_solution = False
            st.session_state.current_q = generate_question(selected_topics, st.session_state.difficulty)
            st.session_state.test_end_time = time.time() + (st.session_state.time_total * 60)
            st.session_state.q_start_time = time.time()
            st.session_state.stage = 'testing'
            st.rerun()

# ==========================================
# UI: ห้องสอบ / โหมดทบทวน
# ==========================================
elif st.session_state.stage == 'testing':
    if "ทบทวน" not in st.session_state.mode:
        time_left_total = int(st.session_state.test_end_time - time.time())
        if time_left_total <= 0:
            st.session_state.stage = 'result'
            st.rerun()
        q_time_left = st.session_state.time_q - int(time.time() - st.session_state.q_start_time) if st.session_state.time_q > 0 else 0
        render_smart_timer(time_left_total, q_time_left)

    mode_text = f"จาก {st.session_state.total_q} ข้อ" if "Fixed" in st.session_state.mode else "(โหมดทบทวน)" if "ทบทวน" in st.session_state.mode else "(ไร้ขีดจำกัด)"
    st.markdown(f"""
        <div class="stat-box">
            <span style="font-size: 18px; color: #aaa;">ระดับ: </span> <span style="font-size: 20px; color: #fff;">{st.session_state.difficulty}</span>
            <span style="margin: 0 15px; color: #555;">|</span>
            <span style="font-size: 18px; color: #aaa;">กำลังทำข้อที่:</span> <span style="font-size: 24px; font-weight: bold; color: #fff;">{st.session_state.q_count + 1}</span> <span style="font-size: 14px; color: #888;">{mode_text}</span>
            <span style="margin: 0 15px; color: #555;">|</span>
            <span style="font-size: 18px; color: #aaa;">ตอบถูกแล้ว:</span> <span style="font-size: 24px; font-weight: bold; color: #00ffcc;">{st.session_state.score}</span>
        </div>
    """, unsafe_allow_html=True)

    q = st.session_state.current_q
    st.info(f"📌 หมวดหมู่: {q['topic']}")
    st.markdown(f"<div style='text-align:center; font-size: 20px; margin-top:20px;'>{q['desc']}</div>", unsafe_allow_html=True)
    st.latex(q['math'])
    
    if st.session_state.show_solution:
        if st.session_state.last_answer_correct:
            st.success("🎉 ตอบถูกต้อง ยอดเยี่ยมมาก!")
        else:
            st.error(f"❌ ยังไม่ถูกจ้า คำตอบที่ถูกต้องคือ: {q['a']}")
            
        st.markdown(f"<div class='solution-box'>{q['solution']}</div>", unsafe_allow_html=True)
        
        if st.button("▶️ ไปข้อถัดไป (Next)", use_container_width=True, type="primary"):
            next_question()
            st.rerun()
    else:
        st.text_input("พิมพ์คำตอบ (ตัวเลข) แล้วกด Enter:", key=f"ans_{st.session_state.q_count}", on_change=submit_answer)
        
        col_skip, col_stop = st.columns(2)
        with col_skip:
            if st.button("⏭️ SKIP (ยากขนาดนี้ข้ามดีกว่า)", use_container_width=True):
                next_question()
                st.rerun()
        with col_stop:
            if st.button("🛑 STOP EXAM (ได้เท่าไหร่นะ)", use_container_width=True):
                st.session_state.stage = 'result'
                st.rerun()

# ==========================================
# UI: หน้าสรุปผล
# ==========================================
elif st.session_state.stage == 'result':
    st.markdown("<h1 style='text-align: center; font-size: 60px;'>🎯 EXAM FINISHED!</h1>", unsafe_allow_html=True)
    st.balloons()
    st.markdown(f"""
        <div style="background: rgba(0,255,204,0.1); border: 2px solid #00ffcc; border-radius: 15px; padding: 30px; text-align: center; margin: 20px 0;">
            <h2 style="margin:0; color: #fff;">ผลการทดสอบของคุณ</h2>
            <hr style="border-color: rgba(0,255,204,0.3);">
            <div style="font-size: 20px; color: #aaa;">ระดับความยากที่เล่น: <span style="color: #fff;">{st.session_state.difficulty}</span></div>
            <div style="font-size: 20px; color: #aaa;">ทำไปทั้งหมด <span style="color: #fff; font-weight: bold; font-size: 30px;">{st.session_state.q_count}</span> ข้อ</div>
            <div style="font-size: 20px; color: #aaa; margin-top: 10px;">ตอบถูก <span style="color: #00ffcc; font-weight: bold; font-size: 50px;">{st.session_state.score}</span> ข้อ</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 กลับหน้าหลัก / ทำชุดใหม่", use_container_width=True, type="primary"):
        st.session_state.stage = 'setup'
        st.rerun()
