import streamlit as st
import random

# 1. 페이지 및 세션 초기화
st.set_page_config(page_title="Streamlit Blackjack", page_icon="🃏")

if "points" not in st.session_state:
    st.session_state.points = 1000
if "deck" not in st.session_state:
    st.session_state.deck = []
if "player_hand" not in st.session_state:
    st.session_state.player_hand = []
if "dealer_hand" not in st.session_state:
    st.session_state.dealer_hand = []
if "game_status" not in st.session_state:
    st.session_state.game_status = "BET"  # BET, PLAYING, GAME_OVER
if "bet" not in st.session_state:
    st.session_state.bet = 0

# 2. 로직 함수
suits = ["♠️", "♥️", "♦️", "♣️"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

def calculate_score(hand):
    score = 0
    aces = 0
    for card in hand:
        # 공백을 기준으로 카드의 랭크(숫자/문자)만 정확하게 가져옵니다.
        val = card.split()[0]
        if val in ["J", "Q", "K"]:
            score += 10
        elif val == "A":
            aces += 1
            score += 11
        else:
            score += int(val)
            
    # 에이스(A) 처리: 21 초과 시 11점을 1점으로 계산
    while score > 21 and aces > 0:
        score -= 10
        aces -= 1
    return score

def start_new_game(bet_amount):
    deck = [f"{r} {s}" for s in suits for r in ranks]
    random.shuffle(deck)
    st.session_state.deck = deck
    st.session_state.bet = bet_amount
    st.session_state.points -= bet_amount
    st.session_state.player_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
    st.session_state.dealer_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
    st.session_state.game_status = "PLAYING"

# 3. 화면 레이아웃
st.title("🃏 스트림릿 블랙잭")
st.sidebar.metric("보유 포인트", f"{st.session_state.points} P")

# [단계 1] 베팅 화면
if st.session_state.game_status == "BET":
    st.subheader("게임 시작 전 베팅해 주세요.")
    
    # 포인트가 부족한 경우 처리
    if st.session_state.points <= 0:
        st.error("포인트를 모두 잃었습니다!")
        if st.button("포인트 충전하기 (1,000 P) 💵"):
            st.session_state.points = 1000
            st.rerun()
    else:
        bet_input = st.number_input(
            "베팅금액", 
            min_value=10, 
            max_value=st.session_state.points, 
            value=min(100, st.session_state.points), 
            step=10
        )
        if st.button("게임 시작 🎲"):
            start_new_game(bet_input)
            st.rerun()

# [단계 2] 진행 및 결과 화면
elif st.session_state.game_status in ["PLAYING", "GAME_OVER"]:
    player_score = calculate_score(st.session_state.player_hand)
    dealer_score = calculate_score(st.session_state.dealer_hand)

    # 딜러 영역
    st.subheader("🤵 딜러 패")
    if st.session_state.game_status == "PLAYING":
        st.write(f"[ {st.session_state.dealer_hand[0]} , 🂠 ]")
    else:
        st.write(f"{'  '.join(st.session_state.dealer_hand)} (점수: {dealer_score})")

    st.divider()

    # 플레이어 영역
    st.subheader("👤 플레이어 패")
    st.write(f"{'  '.join(st.session_state.player_hand)} (점수: {player_score})")

    # 액션 버튼 (Hit / Stand)
    if st.session_state.game_status == "PLAYING":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Hit (카드 받기) 🎴"):
                st.session_state.player_hand.append(st.session_state.deck.pop())
                if calculate_score(st.session_state.player_hand) > 21:
                    st.session_state.game_status = "GAME_OVER"
                st.rerun()
        with col2:
            if st.button("Stand (차례 넘기기) ✋"):
                # 딜러는 17 이상이 될 때까지 계속 카드를 받음
                while calculate_score(st.session_state.dealer_hand) < 17:
                    st.session_state.dealer_hand.append(st.session_state.deck.pop())
                st.session_state.game_status = "GAME_OVER"
                st.rerun()

    # 결과 판정
    if st.session_state.game_status == "GAME_OVER":
        st.divider()
        if player_score > 21:
            st.error("버스트(Bust)! 21을 초과하여 패배했습니다.")
        elif dealer_score > 21:
            st.success(f"딜러 버스트! 딜러가 21을 초과하여 승리했습니다. (+{st.session_state.bet * 2} P)")
            st.session_state.points += st.session_state.bet * 2
            st.balloons()
        elif player_score > dealer_score:
            st.success(f"승리했습니다! (+{st.session_state.bet * 2} P)")
            st.session_state.points += st.session_state.bet * 2
            st.balloons()
        elif player_score < dealer_score:
            st.error("딜러의 점수가 더 높아 패배했습니다.")
        else:
            st.warning("무승부(Push)입니다. 베팅금을 돌려받습니다.")
            st.session_state.points += st.session_state.bet

        if st.button("다시 하기 🔄"):
            st.session_state.game_status = "BET"
            st.rerun()
