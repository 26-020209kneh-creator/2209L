import streamlit as st

# ==============================
# 기본 설정
# ==============================

BOARD_SIZE = 15

st.set_page_config(
    page_title="오목 게임",
    page_icon="⚫",
    layout="centered"
)


# ==============================
# 게임 초기화
# ==============================

def reset_game():
    st.session_state.board = [
        [0 for _ in range(BOARD_SIZE)]
        for _ in range(BOARD_SIZE)
    ]

    # 1 = 흑돌
    # 2 = 백돌
    st.session_state.player = 1

    st.session_state.game_over = False
    st.session_state.winner = 0


if "board" not in st.session_state:
    reset_game()


# ==============================
# 승리 판정
# ==============================

def count_direction(row, col, row_direction, col_direction, player):
    count = 0

    r = row + row_direction
    c = col + col_direction

    while (
        0 <= r < BOARD_SIZE
        and 0 <= c < BOARD_SIZE
        and st.session_state.board[r][c] == player
    ):
        count += 1

        r += row_direction
        c += col_direction

    return count


def check_win(row, col, player):

    directions = [
        (0, 1),     # 가로
        (1, 0),     # 세로
        (1, 1),     # 대각선 \
        (1, -1)     # 대각선 /
    ]

    for dr, dc in directions:

        count = 1

        count += count_direction(
            row,
            col,
            dr,
            dc,
            player
        )

        count += count_direction(
            row,
            col,
            -dr,
            -dc,
            player
        )

        if count >= 5:
            return True

    return False


# ==============================
# 무승부 판정
# ==============================

def check_draw():

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):

            if st.session_state.board[row][col] == 0:
                return False

    return True


# ==============================
# 돌 놓기
# ==============================

def put_stone(row, col):

    # 게임이 끝난 경우
    if st.session_state.game_over:
        return

    # 이미 돌이 있는 경우
    if st.session_state.board[row][col] != 0:
        return

    player = st.session_state.player

    # 돌 놓기
    st.session_state.board[row][col] = player

    # 승리 확인
    if check_win(row, col, player):

        st.session_state.game_over = True
        st.session_state.winner = player

        return

    # 무승부 확인
    if check_draw():

        st.session_state.game_over = True
        st.session_state.winner = 0

        return

    # 플레이어 변경
    if player == 1:
        st.session_state.player = 2
    else:
        st.session_state.player = 1


# ==============================
# CSS
# ==============================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #777;
        margin-bottom: 25px;
    }

    .board {
        background-color: #D9A441;
        padding: 10px;
        border-radius: 10px;
    }

    div.stButton > button {
        border-radius: 50%;
        height: 42px;
        min-width: 42px;
        padding: 0;
        font-size: 23px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==============================
# 제목
# ==============================

st.markdown(
    '<div class="main-title">⚫ 오목 게임 ⚪</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">15 × 15 오목판</div>',
    unsafe_allow_html=True
)


# ==============================
# 현재 상태
# ==============================

if st.session_state.game_over:

    if st.session_state.winner == 1:
        st.success("🎉 흑돌이 승리했습니다!")

    elif st.session_state.winner == 2:
        st.success("🎉 백돌이 승리했습니다!")

    else:
        st.warning("🤝 무승부입니다!")

else:

    if st.session_state.player == 1:
        st.info("⚫ 현재 차례: 흑돌")
    else:
        st.info("⚪ 현재 차례: 백돌")


# ==============================
# 오목판
# ==============================

for row in range(BOARD_SIZE):

    cols = st.columns(BOARD_SIZE)

    for col in range(BOARD_SIZE):

        value = st.session_state.board[row][col]

        # 빈칸
        if value == 0:
            symbol = " "

        # 흑돌
        elif value == 1:
            symbol = "⚫"

        # 백돌
        else:
            symbol = "⚪"

        with cols[col]:

            clicked = st.button(
                symbol,
                key=f"cell_{row}_{col}",
                use_container_width=True,
                disabled=(
                    value != 0
                    or st.session_state.game_over
                )
            )

            if clicked:

                put_stone(row, col)

                st.rerun()


# ==============================
# 다시 시작
# ==============================

st.divider()

if st.button(
    "🔄 게임 다시 시작",
    use_container_width=True
):

    reset_game()
    st.rerun()


# ==============================
# 게임 설명
# ==============================

st.divider()

st.subheader("📖 게임 방법")

st.write("""
- 흑돌부터 게임을 시작합니다.
- 흑돌과 백돌이 번갈아 돌을 놓습니다.
- 가로, 세로 또는 대각선으로 돌 5개를 연결하면 승리합니다.
- 모든 칸이 채워질 때까지 승자가 없다면 무승부입니다.
""")


st.caption("Made with Python & Streamlit")

