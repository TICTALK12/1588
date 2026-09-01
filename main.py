import streamlit as st
import random
import time

# 1. 페이지 및 세션 초기화
st.set_page_config(page_title="Streamlit Royal Casino", page_icon="🎰", layout="wide")

if "points" not in st.session_state:
    st.session_state.points = 1000
if "current_page" not in st.session_state:
    st.session_state.current_page = "HOME"

# 블랙잭 세션 상태
if "deck" not in st.session_state:
    st.session_state.deck = []
if "player_hand" not in st.session_state:
    st.session_state.player_hand = []
if "dealer_hand" not in st.session_state:
    st.session_state.dealer_hand = []
if "game_status" not in st.session_state:
    st.session_state.game_status = "BET"
if "bj_bet" not in st.session_state:
    st.session_state.bj_bet = 0

# 2. 사이드바 (내비게이션 및 포인트 관리)
with st.sidebar:
    st.title("🎰 ROYAL CASINO")
    st.divider()
    
    st.metric(label="💰 보유 포인트", value=f"{st.session_state.points:,} P")
    
    if st.button("💵 포인트 무료 충전 (1,000 P)", use_container_width=True):
        st.session_state.points += 1000
        st.toast("1,000 포인트가 충전되었습니다!", icon="🎉")
        st.rerun()
        
    st.divider()
    st.subheader("📌 바로가기")
    if st.button("🏠 메인 로비", use_container_width=True):
        st.session_state.current_page = "HOME"
        st.rerun()
    if st.button("🎰 슬롯머신 (Slot Machine)", use_container_width=True):
        st.session_state.current_page = "SLOT"
        st.rerun()
    if st.button("🃏 블랙잭 (Blackjack)", use_container_width=True):
        st.session_state.current_page = "BLACKJACK"
        st.rerun()
    if st.button("🎡 룰렛 (Roulette)", use_container_width=True):
        st.session_state.current_page = "ROULETTE"
        st.rerun()

# -----------------------------------------------------------------------------
# PAGE 1: 메인 로비 (HOME)
# -----------------------------------------------------------------------------
if st.session_state.current_page == "HOME":
    st.title("🏛️ Streamlit Royal Casino 에 오신 것을 환영합니다!")
    st.write("원하시는 게임을 선택하여 포인트를 더 높여보세요!")
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🎰 슬롯머신 (Slot)")
        st.markdown("""
        - **규칙**: 레버를 돌려 3개의 심볼을 맞추는 클래식 슬롯!
        - **배당**: 
            - 3개 일치: **10배** (잭팟 🥳)
            - 2개 일치: **2배**
        - **특징**: 빠르게 즐길 수 있는 스피디한 게임!
        """)
        if st.button("🎰 슬롯머신 플레이", type="primary", use_container_width=True):
            st.session_state.current_page = "SLOT"
            st.rerun()

    with col2:
        st.subheader("🃏 블랙잭 (Blackjack)")
        st.markdown("""
        - **규칙**: 딜러와 카드 합 **21**을 겨루는 클래식 카드 게임!
        - **배당**: 승리 시 베팅금의 **2배**
        - **특징**: Hit/Stand 전략을 활용해 딜러를 이겨보세요.
        """)
        if st.button("🃏 블랙잭 플레이", type="primary", use_container_width=True):
            st.session_state.current_page = "BLACKJACK"
            st.rerun()
            
    with col3:
        st.subheader("🎡 룰렛 (Roulette)")
        st.markdown("""
        - **규칙**: 회전하는 휠에서 공이 멈출 숫자와 색상을 맞추는 게임!
        - **배당**: 
            - 홀수/짝수, Red/Black: **2배**
            - 특정 숫자 맞추기 (0~36): **36배**
        - **특징**: 짜릿한 한 방 잭팟을 노려보세요!
        """)
        if st.button("🎡 룰렛 플레이", type="primary", use_container_width=True):
            st.session_state.current_page = "ROULETTE"
            st.rerun()

# -----------------------------------------------------------------------------
# PAGE 2: 슬롯머신 (SLOT MACHINE)
# -----------------------------------------------------------------------------
elif st.session_state.current_page == "SLOT":
    st.title("🎰 클래식 슬롯머신 (Slot Machine)")
    st.write("슬롯을 돌려 동일한 문양을 맞춰보세요!")
    st.divider()

    symbols = ["🍒", "🍋", "🔔", "💎", "7️⃣"]

    if st.session_state.points <= 0:
        st.error("포인트를 모두 잃었습니다! 사이드바에서 포인트를 충전해주세요.")
    else:
        slot_bet = st.number_input(
            "베팅 금액",
            min_value=10,
            max_value=st.session_state.points,
            value=min(100, st.session_state.points),
            step=10,
            key="slot_bet_input"
        )

        if st.button("🎰 슬롯 돌리기!", type="primary", use_container_width=True):
            st.session_state.points -= slot_bet
            
            # 슬롯 애니메이션 연출
            slot_placeholder = st.empty()
            with st.spinner("슬롯 돌아가는 중... 🎰"):
                for _ in range(12):
                    temp_spin = [random.choice(symbols) for _ in range(3)]
                    slot_placeholder.markdown(f"# [ {' | '.join(temp_spin)} ]")
                    time.sleep(0.08)

            # 최종 슬롯 결과
            result = [random.choice(symbols) for _ in range(3)]
            slot_placeholder.markdown(f"# [ {' | '.join(result)} ]")

            # 당첨 정산
            if result[0] == result[1] == result[2]:
                winnings = slot_bet * 10
                st.session_state.points += winnings
                st.balloons()
                st.success(f"🎉🎉 🎉 JACKPOT! 3개 일치! (+{winnings:,} P)")
            elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
                winnings = slot_bet * 2
                st.session_state.points += winnings
                st.info(f"✨ 2개 일치! (+{winnings:,} P)")
            else:
                st.error(f"아쉽게도 꽝입니다! (-{slot_bet:,} P)")

            st.info(f"현재 남은 포인트: {st.session_state.points:,} P")

# -----------------------------------------------------------------------------
# PAGE 3: 블랙잭 (BLACKJACK)
# -----------------------------------------------------------------------------
elif st.session_state.current_page == "BLACKJACK":
    st.title("🃏 블랙잭 (Blackjack)")
    
    suits = ["♠️", "♥️", "♦️", "♣️"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def calculate_score(hand):
        score = 0
        aces = 0
        for card in hand:
            val = card.split()[0]
            if val in ["J", "Q", "K"]:
                score += 10
            elif val == "A":
                aces += 1
                score += 11
            else:
                score += int(val)
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
        return score

    def start_new_game(bet_amount):
        deck = [f"{r} {s}" for s in suits for r in ranks]
        random.shuffle(deck)
        st.session_state.deck = deck
        st.session_state.bj_bet = bet_amount
        st.session_state.points -= bet_amount
        st.session_state.player_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
        st.session_state.dealer_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
        st.session_state.game_status = "PLAYING"

    if st.session_state.game_status == "BET":
        st.subheader("게임 시작 전 베팅해 주세요.")
        if st.session_state.points <= 0:
            st.error("포인트를 모두 잃었습니다! 사이드바에서 포인트를 충전해주세요.")
        else:
            bet_input = st.number_input(
                "베팅금액", 
                min_value=10, 
                max_value=st.session_state.points, 
                value=min(100, st.session_state.points), 
                step=10
            )
            if st.button("게임 시작 🎲", type="primary"):
                start_new_game(bet_input)
                st.rerun()

    elif st.session_state.game_status in ["PLAYING", "GAME_OVER"]:
        player_score = calculate_score(st.session_state.player_hand)
        dealer_score = calculate_score(st.session_state.dealer_hand)

        st.subheader("🤵 딜러 패")
        if st.session_state.game_status == "PLAYING":
            st.write(f"[ {st.session_state.dealer_hand[0]} , 🂠 ]")
        else:
            st.write(f"{'  '.join(st.session_state.dealer_hand)} (점수: {dealer_score})")

        st.divider()

        st.subheader("👤 플레이어 패")
        st.write(f"{'  '.join(st.session_state.player_hand)} (점수: {player_score})")

        if st.session_state.game_status == "PLAYING":
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Hit (카드 받기) 🎴", use_container_width=True):
                    st.session_state.player_hand.append(st.session_state.deck.pop())
                    if calculate_score(st.session_state.player_hand) > 21:
                        st.session_state.game_status = "GAME_OVER"
                    st.rerun()
            with col2:
                if st.button("Stand (차례 넘기기) ✋", use_container_width=True):
                    while calculate_score(st.session_state.dealer_hand) < 17:
                        st.session_state.dealer_hand.append(st.session_state.deck.pop())
                    st.session_state.game_status = "GAME_OVER"
                    st.rerun()

        if st.session_state.game_status == "GAME_OVER":
            st.divider()
            if player_score > 21:
                st.error("버스트(Bust)! 21을 초과하여 패배했습니다.")
            elif dealer_score > 21:
                st.success(f"딜러 버스트! 딜러가 21을 초과하여 승리했습니다. (+{st.session_state.bj_bet * 2:,} P)")
                st.session_state.points += st.session_state.bj_bet * 2
                st.balloons()
            elif player_score > dealer_score:
                st.success(f"승리했습니다! (+{st.session_state.bj_bet * 2:,} P)")
                st.session_state.points += st.session_state.bj_bet * 2
                st.balloons()
            elif player_score < dealer_score:
                st.error("딜러의 점수가 더 높아 패배했습니다.")
            else:
                st.warning("무승부(Push)입니다. 베팅금을 돌려받습니다.")
                st.session_state.points += st.session_state.bj_bet

            if st.button("다시 하기 🔄", type="primary"):
                st.session_state.game_status = "BET"
                st.rerun()

# -----------------------------------------------------------------------------
# PAGE 4: 룰렛 (ROULETTE)
# -----------------------------------------------------------------------------
elif st.session_state.current_page == "ROULETTE":
    st.title("🎡 유러피언 룰렛 (Roulette)")
    st.write("원하는 방식(색상, 홀/짝, 단일 숫자)으로 베팅해 보세요!")
    st.divider()

    RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
    BLACK_NUMBERS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

    if st.session_state.points <= 0:
        st.error("포인트를 모두 잃었습니다! 사이드바에서 포인트를 충전해주세요.")
    else:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            bet_type = st.radio(
                "베팅 유형 선택",
                ["색상 (Red/Black)", "홀수 / 짝수 (Odd/Even)", "단일 숫자 (0~36)"],
                horizontal=True
            )
            
            selected_option = None
            multiplier = 2
            
            if bet_type == "색상 (Red/Black)":
                selected_option = st.selectbox("색상을 선택하세요 (배당: 2배)", ["🔴 Red", "⚫ Black"])
                multiplier = 2
            elif bet_type == "홀수 / 짝수 (Odd/Even)":
                selected_option = st.selectbox("홀/짝을 선택하세요 (배당: 2배)", ["짝수 (Even)", "홀수 (Odd)"])
                multiplier = 2
            elif bet_type == "단일 숫자 (0~36)":
                selected_option = st.number_input("숫자를 선택하세요 (배당: 36배)", min_value=0, max_value=36, value=7, step=1)
                multiplier = 36

            roulette_bet = st.number_input(
                "베팅 금액",
                min_value=10,
                max_value=st.session_state.points,
                value=min(100, st.session_state.points),
                step=10,
                key="roulette_bet_input"
            )

            spin_button = st.button("🎡 룰렛 돌리기!", type="primary", use_container_width=True)

        with col2:
            st.subheader("🎯 룰렛 정보")
            st.markdown("""
            - 🔴 **Red**: 1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36
            - ⚫ **Black**: 2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35
            - 🟢 **Green**: 0 (단일 숫자로만 당첨 가능)
            """)

        if spin_button:
            st.session_state.points -= roulette_bet
            
            # 애니메이션 연출
            wheel_placeholder = st.empty()
            with st.spinner("룰렛 돌리는 중... 🎡"):
                for _ in range(15):
                    temp_num = random.randint(0, 36)
                    color_tag = "🔴" if temp_num in RED_NUMBERS else ("⚫" if temp_num in BLACK_NUMBERS else "🟢")
                    wheel_placeholder.markdown(f"### 🎡 휠 돌아가는 중: {color_tag} `{temp_num}`")
                    time.sleep(0.1)

            # 최종 당첨 결과
            winning_number = random.randint(0, 36)
            if winning_number in RED_NUMBERS:
                winning_color = "🔴 Red"
            elif winning_number in BLACK_NUMBERS:
                winning_color = "⚫ Black"
            else:
                winning_color = "🟢 Green (0)"

            wheel_placeholder.markdown(f"## 🎯 최종 결과: {winning_color} `{winning_number}`")

            # 당첨 여부 확인
            is_win = False
            
            if bet_type == "색상 (Red/Black)":
                if (selected_option == "🔴 Red" and winning_number in RED_NUMBERS) or \
                   (selected_option == "⚫ Black" and winning_number in BLACK_NUMBERS):
                    is_win = True
            elif bet_type == "홀수 / 짝수 (Odd/Even)":
                if winning_number != 0:
                    if (selected_option == "짝수 (Even)" and winning_number % 2 == 0) or \
                       (selected_option == "홀수 (Odd)" and winning_number % 2 != 0):
                        is_win = True
            elif bet_type == "단일 숫자 (0~36)":
                if selected_option == winning_number:
                    is_win = True

            # 정산
            if is_win:
                payout = roulette_bet * multiplier
                st.session_state.points += payout
                st.balloons()
                st.success(f"🎉 축하합니다! 당첨되었습니다! (+{payout:,} P)")
            else:
                st.error(f"아쉽게도 꽝입니다! (-{roulette_bet:,} P)")
                
            st.info(f"현재 남은 포인트: {st.session_state.points:,} P")
