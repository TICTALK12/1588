import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="KBO 선수 성적 조회", layout="wide")

# KBO 선수 정보 크롤링 함수
@st.cache_data(ttl=3600)  # 1시간 동안 결과 캐싱
def get_kbo_player_data(player_name):
    # 1. KBO 선수 검색
    search_url = f"https://www.koreabaseball.com/Player/Search.aspx?searchWord={player_name}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    
    # 검색 결과 확인
    rows = soup.select(".tData tbody tr")
    if not rows or "검색 결과가 없습니다" in rows[0].text:
        return None

    # 첫 번째 검색 결과에서 선수 ID 및 기본 정보 추출
    first_row = rows[0].select("td")
    player_id = first_row[0].find("a")["href"].split("playerId=")[-1]
    name = first_row[1].text.strip()
    team = first_row[2].text.strip()
    position = first_row[3].text.strip()

    # 2. 선수 상세 페이지 접속 (프로필 + 성적)
    detail_url = f"https://www.koreabaseball.com/Player/Detail.aspx?playerId={player_id}"
    detail_res = requests.get(detail_url, headers=headers)
    detail_soup = BeautifulSoup(detail_res.text, "html.parser")

    # 프로필 이미지 추출
    img_tag = detail_soup.select_one("#cphContents_cphContents_cphContent_playerProfile_imgProfile")
    img_url = "https:" + img_tag["src"] if img_tag else None

    # 기록 테이블 추출 (타자/투수 성적)
    stat_table = detail_soup.select_one(".tData")
    stats_df = pd.DataFrame()
    
    if stat_table:
        headers_list = [th.text.strip() for th in stat_table.select("thead tr th")]
        data_rows = []
        for tr in stat_table.select("tbody tr"):
            row_data = [td.text.strip() for td in tr.select("td")]
            if len(row_data) == len(headers_list):
                data_rows.append(row_data)
        
        stats_df = pd.DataFrame(data_rows, columns=headers_list)

    return {
        "name": name,
        "team": team,
        "position": position,
        "image": img_url,
        "stats": stats_df
    }

# UI 구성
st.title("⚾ KBO 선수 성적 실시간 조회")

player_input = st.text_input("선수 이름을 입력하세요 (예: 김도영, 구자욱, 손아섭)", value="김도영")

if player_input:
    with st.spinner("KBO 데이터를 가져오는 중..."):
        player = get_kbo_player_data(player_input)

    if player:
        st.success(f"'{player['name']}' 선수를 찾았습니다.")
        st.divider()

        # 프로필 섹션
        col1, col2 = st.columns([1, 3])
        with col1:
            if player["image"]:
                st.image(player["image"], width=160)
        with col2:
            st.subheader(f"{player['name']} 선수 프로필")
            st.write(f"**소속팀:** {player['team']}")
            st.write(f"**포지션:** {player['position']}")

        st.divider()

        # 성적 테이블 섹션
        st.subheader("📊 통산/시즌별 기록")
        if not player["stats"].empty:
            st.dataframe(player["stats"], use_container_width=True)
            
            # 숫자형 변환 및 간이 차트 (타자/투수에 맞춰 컬럼 확인)
            if "AVG" in player["stats"].columns:  # 타자인 경우
                df_chart = player["stats"].copy()
                df_chart = df_chart[df_chart["연도"].str.isdigit()]  # 통산/합계 행 제외
                df_chart["AVG"] = pd.to_numeric(df_chart["AVG"], errors="coerce")
                
                st.subheader("📈 연도별 타율 추이")
                st.line_chart(df_chart, x="연도", y="AVG")
        else:
            st.info("성적 데이터가 없습니다.")
    else:
        st.error("선수를 찾을 수 없습니다. 이름이 정확한지 확인해 주세요.")
