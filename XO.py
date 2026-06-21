import streamlit as st

# 1. قراءة وتطبيق ملف الـ CSS الخاص بك
try:
    with open("XO.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass  

# 2. تعريف الحالات الابتدائية للعبة في الـ Session State
# 2. تعريف الحالات الابتدائية في الـ Session State
if 'game_started' not in st.session_state:
    st.session_state.game_started = False  # لمعرفة هل بدأوا اللعب أم لا
if 'player_x' not in st.session_state:
    st.session_state.player_x = "Menna"     # الاسم الافتراضي للاعب X
if 'player_o' not in st.session_state:
    st.session_state.player_o = "Malk"      # الاسم الافتراضي للاعب o
if 'board' not in st.session_state:
    st.session_state.board = [''] * 9
if 'turn' not in st.session_state:
    st.session_state.turn = 'Menna'  
if 'winner' not in st.session_state:
    st.session_state.winner = None

def check_winner(board):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # أفقي
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # رأسي
        [0, 4, 8], [2, 4, 6]              # قطري
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != '':
            return board[condition[0]]
    return None

# عنوان اللعبة
st.title("Wlcome Nabil website\nGamePlay(X,o)")

# التحقق من التعادل
check_draw = '' not in st.session_state.board and not st.session_state.winner

# عرض حالة اللعبة للمستخدم وتفعيل البلالين عند الفوز
if st.session_state.winner:
    st.success(f"الفائز هو اللاعب: {st.session_state.winner}! 🎉")
    st.balloons()  # 🎈 هذه الدالة السحرية ستقوم بإطلاق البلالين في الشاشة بأكملها فور الفوز!
elif check_draw:
    st.info("النتيجة: تعادل! 🤝")
else:
    st.write(f"دور اللاعب الحالي: **{st.session_state.turn}**")

# بناء لوحة الـ XO (3 صفوف × 3 أعمدة)
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        button_label = st.session_state.board[idx] if st.session_state.board[idx] != '' else " "
        
        # عند الضغط على المربع
        if cols[col].button(button_label, key=f"btn_{idx}", use_container_width=True):
            if st.session_state.board[idx] == '' and not st.session_state.winner:
                st.session_state.board[idx] = st.session_state.turn
                st.session_state.winner = check_winner(st.session_state.board)
                
                if not st.session_state.winner:
                    st.session_state.turn = 'Malk' if st.session_state.turn == 'Menna' else 'Menna'
                st.rerun()

st.write("---")

# زر إعادة الضبط (Reset)
if st.button("إعادة اللعب 🔄"):
    st.session_state.board = [''] * 9
    st.session_state.turn = 'Menna'
    st.session_state.winner = None
    st.rerun()
