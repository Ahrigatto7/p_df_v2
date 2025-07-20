import streamlit as st

def render():
    st.markdown(
        """
        <style>
        .db-main-title {font-size: 2.3rem; font-weight:700; letter-spacing:-1px;}
        .metric-card {background:#fff; box-shadow:0 2px 8px #0001; border-radius:14px; padding:22px 12px 10px 18px; margin-bottom:10px;}
        </style>
        """, unsafe_allow_html=True)
    st.markdown('<div class="db-main-title">📊 대시보드</div>', unsafe_allow_html=True)
    st.caption("주요 통계와 최근 활동을 한눈에 확인")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card">총 문서<br><span style="font-size:2.0rem;font-weight:800;color:#3D5AFE">163</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">신규 업로드<br><span style="font-size:2.0rem;font-weight:800;color:#00BFAE">7</span></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">검색 수<br><span style="font-size:2.0rem;font-weight:800;color:#FF5C8D">36</span></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card">프롬프트<br><span style="font-size:2.0rem;font-weight:800;color:#7C4DFF">12</span></div>', unsafe_allow_html=True)
    st.markdown("---")

    # 아래에 최근 작업 로그, 간단 그래프 등도 추가 가능
    st.subheader("최근 작업 내역")
    st.write("• 문서 'A' 업로드 (2024-07-20)")
    st.write("• RAG 검색 3회 (2024-07-19)")
    # ... 필요에 따라 시각화/차트 등

