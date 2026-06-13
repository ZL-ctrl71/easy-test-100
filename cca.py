import streamlit as st
import random
import time
import math
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="ระบบห้องสอบคณิตศาสตร์จำลอง", layout="centered")

st.title("⏱️ ห้องสอบคณิตศาสตร์จำลอง (Advanced Mode)")
st.write("---")

# 📚 คลังสุ่มโจทย์แบบยืดหยุ่นและขยายขอบเขตคำตอบ (0.1 - 100)
def generate_math_question(allowed_modes):
    mode = random.choice(allowed_modes)
    
    if mode == 'สมการกำลังสอง':
        x1 = random.randint(2, 40)
        x2 = random.randint(41, 99)
        b = x1 + x2
        c = x1 * x2
        ans = max(x1, x2) 
        return f"จงหาค่า $x$ ที่เป็นจำนวนเต็มบวกที่มากที่สุดจากสมการ: $x^2 - {b}x + {c} = 0$", str(ans), 'สมการกำลังสอง'

    elif mode == 'พีทาโกรัส':
        a = random.randint(5, 60)
        b = random.randint(5, 60)
        c_exact = math.sqrt(a**2 + b**2)
        
        ask_type = random.choice(['find_c', 'find_side'])
        if ask_type == 'find_c':
            ans = round(c_exact, 1)
            ans_str = str(int(ans)) if ans.is_integer() else str(ans)
            return f"สามเหลี่ยมมุมฉากรูปหนึ่ง มีด้านประกอบมุมฉากยาว {a} และ {b} หน่วย จงหาความยาวของด้านตรงข้ามมุมฉาก ($c$) (หากมีทศนิยม ให้ตอบเป็นทศนิยม 1 ตำแหน่ง)", ans_str, 'พีทาโกรัส'
        else:
            c_rounded = round(c_exact, 1)
            ans = round(b, 1)
            ans_str = str(int(ans)) if ans.is_integer() else str(ans)
            return f"สามเหลี่ยมมุมฉากรูปหนึ่ง มีด้านตรงข้ามมุมฉาก ($c$) ยาวประมาณ {c_rounded} หน่วย และมีด้านประกอบมุมฉากด้านหนึ่งยาว {a} หน่วย จงหาความยาวของด้านประกอบมุมฉากอีกด้านหนึ่ง (ตอบเป็นจำนวนเต็ม)", ans_str, 'พีทาโกรัส'

    elif mode == 'ตรีโกณมิติ':
        k1 = random.randint(10, 90)
        k2 = random.randint(5, 45)
        
        if k1 % 2 != 0:
            k1 += 1
            
        # 🔥 [แก้ไขจุดสำคัญ] ปรับโค้ดให้แสดงผลเศษส่วนแบบ บน-ล่าง ด้วย \frac{}{} เพื่อให้อ่านง่าย ไม่สับสนแล้วครับน้า
        trig_variants = [
            (f"จงหาค่าของ: ${k1}\\sin(30^\\circ) + {k2}\\tan(45^\\circ)$", str(int(k1*0.5 + k2*1))),
            (f"จงหาค่าของ: ${k1}\\cos(60^\\circ) + {k2}$", str(int(k1*0.5 + k2))),
            (f"จงหาค่าของ: ${k1}\\sin(30^\\circ) - {k2}$", str(int(k1*0.5 - k2))),
            (f"ถ้า $\\sin(\\theta) = \\frac{{3}}{{5}}$ และเป็นมุมแหลม จงหาค่าของ: ${k1}\\cos(\\theta)$", str(int(k1 * 0.8))),
            (f"ถ้า $\\tan(\\theta) = \\frac{{3}}{{4}}$ และเป็นมุมแหลม จงหาค่าของ: ${k1}\\sin(\\theta)$", str(int(k1 * 0.6)))
        ]
        q_text, ans = random.choice(trig_variants)
        return q_text, ans, 'ตรีโกณมิติ'

def get_unique_question(allowed_modes):
    if len(st.session_state.used_questions) > 40:
        st.session_state.used_questions = []

    while True:
        q_text, q_ans, q_mode = generate_math_question(allowed_modes)
        if q_text not in st.session_state.used_questions:
            st.session_state.used_questions.append(q_text)
            return q_text, q_ans, q_mode

# 🛠️ ตั้งค่าตัวแปรเริ่มต้น
if 'exam_active' not in st.session_state:
    st.session_state.exam_active = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total' not in st.session_state:
    st.session_state.total = 0
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""
if 'force_stop' not in st.session_state:
    st.session_state.force_stop = False
if 'history' not in st.session_state:
    st.session_state.history = []
if 'used_questions' not in st.session_state:
    st.session_state.used_questions = []

# --- หน้าแรก: เมนูตั้งค่าก่อนเริ่มสอบ ---
if not st.session_state.exam_active:
    st.info("⚙️ ตั้งค่ารูปแบบการทดสอบของคุณ")
    
    st.write("📂 **เลือกหมวดโจทย์ที่ต้องการทดสอบ:**")
    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1:       chk_eq = st.checkbox("สมการกำลังสอง", value=True)
    with c_m2:       chk_py = st.checkbox("พีทาโกรัส", value=True)
    with c_m3:       chk_tr = st.checkbox("ตรีโกณมิติ", value=True)
    
    allowed_modes = []
    if chk_eq: allowed_modes.append('สมการกำลังสอง')
    if chk_py: allowed_modes.append('พีทาโกรัส')
    if chk_tr: allowed_modes.append('ตรีโกณมิติ')

    col_setup1, col_setup2 = st.columns(2)
    with col_setup1:
        total_time_options = {"⏱️ 30 วินาที": 30, "⏱️ 60 วินาที (มาตรฐาน)": 60, "⏱️ 120 วินาที": 120, "⏱️ 300 วินาที": 300}
        selected_total = st.selectbox("⏳ เวลารวมในการสอบ:", options=list(total_time_options.keys()), index=1)
        st.session_state.chosen_total_time = total_time_options[selected_total]
    with col_setup2:
        per_q_options = {"⚡ 5 วินาที": 5, "⚡ 10 วินาที": 10, "⚡ 15 วินาที": 15, "⚡ 20 วินาที": 20, "♾️ ไม่จำกัดเวลา": 99999}
        selected_per_q = st.selectbox("🚨 เวลาจำกัดต่อ 1 ข้อ:", options=list(per_q_options.keys()), index=1)
        st.session_state.chosen_per_question_time = per_q_options[selected_per_q]

    st.write("")
    if not allowed_modes:
        st.error("❌ กรุณาเลือกหมวดโจทย์อย่างน้อย 1 หมวดก่อนเริ่มสอบครับ")
    else:
        if st.button("🚀 เริ่มการทดสอบ", use_container_width=True):
            st.session_state.exam_active = True
            st.session_state.score = 0
            st.session_state.total = 0
            st.session_state.force_stop = False
            st.session_state.history = []
            st.session_state.used_questions = []
            st.session_state.allowed_modes = allowed_modes
            st.session_state.start_time = time.time()       
            st.session_state.q_start_time = time.time()     
            st.session_state.q_text, st.session_state.q_ans, st.session_state.q_mode = get_unique_question(allowed_modes)
            st.session_state.feedback = ""
            st.rerun()

# --- หน้าจอรายงานผลลัพธ์ ---
elif time.time() - st.session_state.start_time >= st.session_state.chosen_total_time or st.session_state.force_stop:
    st.write("## 📊 สรุปผลรายงานการทดสอบ")
    st.write("---")
    
    c_res1, c_res2 = st.columns(2)
    c_res1.metric(label="คะแนนที่ได้ (ข้อที่ถูก)", value=f"{st.session_state.score} ข้อ")
    c_res2.metric(label="ทำไปทั้งหมด", value=f"{st.session_state.total} ข้อ")
    
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.write("### 📈 สถิติเวลาที่ใช้รายข้อ (วินาที)")
        chart_data = df.set_index('ข้อที่')[['เวลาที่ใช้ (วิ)']]
        st.line_chart(chart_data, color="#FF4B4B")
        
        st.write("### 🔍 สรุปสถิติตามหมวดโจทย์")
        summary_df = df.groupby('หมวดโจทย์').agg(
            ข้อที่เจอ=('ข้อที่', 'count'),
            ตอบถูก=('ผลลัพธ์', lambda x: (x == '✅ ถูก').sum())
        ).reset_index()
        summary_df['เปอร์เซ็นต์ความถูกต้อง'] = (summary_df['ตอบถูก'] / summary_df['ข้อที่เจอ'] * 100).round(1).astype(str) + '%'
        st.table(summary_df)
    else:
        st.info("ไม่มีข้อมูลสถิติเนื่องจากยังไม่ได้ตอบโจทย์ข้อใดเลย")

    if st.button("🔄 กลับไปหน้าแรก", use_container_width=True):
        st.session_state.exam_active = False
        st.session_state.force_stop = False
        st.rerun()

# --- หน้าจอระหว่างทำข้อสอบ ---
else:
    st_autorefresh(interval=1000, key="exam_timer")

    elapsed_total = time.time() - st.session_state.start_time
    total_time_left = max(0, int(st.session_state.chosen_total_time - elapsed_total))
    elapsed_q = time.time() - st.session_state.q_start_time
    q_time_left = max(0, int(st.session_state.chosen_per_question_time - elapsed_q))

    if st.session_state.chosen_per_question_time != 99999 and q_time_left <= 0:
        st.session_state.history.append({
            'ข้อที่': st.session_state.total + 1,
            'หมวดโจทย์': st.session_state.q_mode,
            'เวลาที่ใช้ (วิ)': st.session_state.chosen_per_question_time,
            'ผลลัพธ์': '⏳ หมดเวลา'
        })
        st.session_state.total += 1
        st.session_state.feedback = f"💨 หมดเวลาทำข้อที่แล้ว! (ระบบข้ามให้อัตโนมัติ เฉลยคือ: {st.session_state.q_ans})"
        st.session_state.q_start_time = time.time() 
        st.session_state.q_text, st.session_state.q_ans, st.session_state.q_mode = get_unique_question(st.session_state.allowed_modes)
        st.rerun()
        
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("⏳ เวลารวมที่เหลือ", f"{total_time_left} วิ")
        if st.session_state.chosen_per_question_time == 99999:
            c2.metric("🚨 เวลาข้อนี้", "ไม่จำกัด")
        else:
            c2.metric("🚨 เวลาข้อนี้เหลือ", f"{q_time_left} วิ")
        c3.metric("🎯 คะแนนปัจจุบัน", f"{st.session_state.score} ข้อ")

        st.write("---")
        st.write(f"### 📝 โจทย์ข้อที่ {st.session_state.total + 1} [{st.session_state.q_mode}]:")
        st.write(st.session_state.q_text)
        st.write("---")

        if st.session_state.feedback:
            if "ถูกต้อง" in st.session_state.feedback: st.success(st.session_state.feedback)
            else: st.error(st.session_state.feedback)

        with st.form(key="math_form", clear_on_submit=True):
            user_input = st.text_input("พิมพ์คำตอบของคุณตรงนี้ แล้วกด Enter:", key="ans_field")
            submit_btn = st.form_submit_button("ส่งคำตอบ 🎯", use_container_width=True)

            if submit_btn and user_input:
                time_spent = round(time.time() - st.session_state.q_start_time, 1)
                st.session_state.total += 1
                
                if user_input.strip() == st.session_state.q_ans:
                    st.session_state.score += 1
                    st.session_state.feedback = f"🎉 ข้อล่าสุดถูกต้อง! (+1 คะแนน)"
                    res_status = '✅ ถูก'
                else:
                    st.session_state.feedback = f"❌ ข้อล่าสุดผิดครับ! (เฉลยคือ: {st.session_state.q_ans})"
                    res_status = '❌ ผิด'
                
                st.session_state.history.append({
                    'ข้อที่': st.session_state.total,
                    'หมวดโจทย์': st.session_state.q_mode,
                    'เวลาที่ใช้ (วิ)': time_spent,
                    'ผลลัพธ์': res_status
                })
                
                st.session_state.q_start_time = time.time()
                st.session_state.q_text, st.session_state.q_ans, st.session_state.q_mode = get_unique_question(st.session_state.allowed_modes)
                st.rerun()

        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button("⏭️ ข้ามข้อนี้(ยากจังเลย)", use_container_width=True):
                time_spent = round(time.time() - st.session_state.q_start_time, 1)
                st.session_state.history.append({
                    'ข้อที่': st.session_state.total + 1,
                    'หมวดโจทย์': st.session_state.q_mode,
                    'เวลาที่ใช้ (วิ)': time_spent,
                    'ผลลัพธ์': '⏭️ ข้าม'
                })
                st.session_state.total += 1
                st.session_state.feedback = "⏭️ คุณกดข้ามข้อที่แล้ว"
                st.session_state.q_start_time = time.time()
                st.session_state.q_text, st.session_state.q_ans, st.session_state.q_mode = get_unique_question(st.session_state.allowed_modes)
                st.rerun()
        
        with c_btn2:
            if st.button("🛑 หยุดทำข้อสอบ", use_container_width=True):
                st.session_state.force_stop = True
                st.rerun()