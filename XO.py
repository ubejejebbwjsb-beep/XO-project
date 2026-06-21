import streamlit as st

# 1. قراءة وتطبيق ملف الـ CSS الخاص بك
try:
    with open("XO.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass  

# 2. تعريف الحالات الابتدائية في الـ Session State
if 'game_started' not in st.session_state:
    st.session_state.game_started = False  
if 'player_x' not in st.session_state:
    st.session_state.player_x = "Menna"     
if 'player_o' not in st.session_state:
    st.session_state.player_o = "Malk"      
if 'board' not in st.session_state:
    st.session_state.board = [''] * 9
if 'turn' not in st.session_state:
    st.session_state.turn = 'X'  
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'winning_indices' not in st.session_state:
    st.session_state.winning_indices = []  # لحفظ أرقام المربعات الثلاثة الفائزة

def check_winner(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # أفقي
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # رأسي
        [0, 4, 8], [2, 4, 6]              # قطري
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != '':
            return board[condition[0]], condition  # نُعيد الرمز والمربعات الثلاثة الفائزة
    return None, []

# ==========================================
# الشاشة الأولى: صفحة تسجيل الدخول
# ==========================================
if st.session_state.game_started == False:
    st.title("💎💎  Welcome to Nabil's Website 💎💎")
    st.subheader("تسجيل دخول اللاعبين")
    
    game_image_url = "https://images.unsplash.com/photo-1611891404113-68d2f790bd9c?w=500" 
    st.image(game_image_url, caption="جاهز للتحدي؟ 🔥", use_container_width=True)
    
    name_x = st.text_input("اسم اللاعب الأول (X):", value=st.session_state.player_x)
    name_o = st.text_input("اسم اللاعب الثاني (O):", value=st.session_state.player_o)
    
    if st.button("إبدأ اللعب الآن 🚀", use_container_width=True):
        if name_x.strip() == "" or name_o.strip() == "":
            st.error("من فضلك أدخل أسماء اللاعبين أولاً!")
        else:
            st.session_state.player_x = name_x
            st.session_state.player_o = name_o
            st.session_state.game_started = True  
            st.rerun()

# ==========================================
# الشاشة الثانية: صفحة اللعبة
# ==========================================
else:
    players = {'X': st.session_state.player_x, 'O': st.session_state.player_o}
    st.title("GamePlay (X, O)")
    
    check_draw = '' not in st.session_state.board and not st.session_state.winner

    if st.session_state.winner:
        winner_name = players[st.session_state.winner]
        st.success(f"الفائز هو اللاعب: {winner_name} ({st.session_state.winner})! 🎉")
        st.balloons()  
    elif check_draw:
        st.info("النتيجة: تعادل! 🤝")
    else:
        current_player_name = players[st.session_state.turn]
        st.write(f"دور اللاعب الحالي: **{current_player_name} ({st.session_state.turn})**")

    # بناء لوحة الـ XO
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            idx = row * 3 + col
            button_label = st.session_state.board[idx] if st.session_state.board[idx] != '' else " "
            
            # حيلة ذكية: إذا كان هذا المربع من ضمن المربعات الفائزة، نضع له كود مخصص لتلوينه
            if idx in st.session_state.winning_indices:
                button_label = f"✨ {button_label} ✨"
                # حقن ستايل CSS مخصص لتلوين المربع الفائز باللون الأخضر النيون المضيء
                st.markdown(f"""
                <style>
                div[data-testid="stHorizontalBlock"] button[key="btn_{idx}"] {{
                    background: linear-gradient(135deg, #00ff87, #60efff) !important;
                    color: #1e1e2f !important;
                    border-color: #ffffff !important;
                    box-shadow: 0 0 20px rgba(0, 255, 135, 0.8) !important;
                }}
                </style>
                """, unsafe_allow_html=True)

            if cols[col].button(button_label, key=f"btn_{idx}", use_container_width=True):
                if st.session_state.board[idx] == '' and not st.session_state.winner:
                    st.session_state.board[idx] = st.session_state.turn
                    
                    winner, winning_combo = check_winner(st.session_state.board)
                    if winner:
                        st.session_state.winner = winner
                        st.session_state.winning_indices = winning_combo # حفظ المربعات الفائزة
                    
                    if not st.session_state.winner:
                        st.session_state.turn = 'O' if st.session_state.turn == 'X' else 'X'
                    st.rerun()

    st.write("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("إعادة اللعب 🔄", use_container_width=True):
            st.session_state.board = [''] * 9
            st.session_state.turn = 'X'
            st.session_state.winner = None
            st.session_state.winning_indices = []  # تصفير المربعات الفائزة
            st.rerun()
            
    with col2:
        if st.button("تغيير اللاعبين وتسجيل الخروج 👥", use_container_width=True):
            st.session_state.board = [''] * 9
            st.session_state.turn = 'X'
            st.session_state.winner = None
            st.session_state.winning_indices = []  
            st.session_state.game_started = False  
            st.rerun()
