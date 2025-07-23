import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt

st.header("문서/규칙/관계 네트워크 시각화")
# 예시: API에서 문서 간 관계 데이터 불러오기
# nodes, edges = ...
G = nx.Graph()
G.add_edge("규칙A", "PDF문서1")
G.add_edge("사례1", "규칙A")
net = Network(notebook=False, height='600px')
net.from_nx(G)
net.save_graph('network.html')
st.components.v1.html(open('network.html').read(), height=600)

st.header("문서 유형별/기간별 통계")
# 예시: API로 통계 데이터 DataFrame
df = pd.DataFrame([{"type": "규칙", "count": 20}, {"type": "PDF", "count": 5}])
plt.bar(df["type"], df["count"])
st.pyplot(plt)

