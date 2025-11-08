# app.py ― 澪 -Mio-｜脳科学×数秘術で導く“幸せの方程式”
import streamlit as st
import sqlite3
import uuid
import random
import os
import datetime
from datetime import datetime as dt, timedelta
from typing import Optional

# ===== ページ設定（最初に必ず置く） =====
st.set_page_config(
    page_title="澪 -Mio-｜脳科学×数秘術で導く“幸せの方程式”",
    page_icon="🔯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===== 基本設定 =====
APP_TITLE = "澪 -Mio-｜脳科学×数秘術で導く“幸せの方程式”"
LINE_URL = "https://lin.ee/f3iQlQY"  # ← あなたのLINE公式URLに差し替え
LOCK_DAYS = 7
ASSETS_DIR = "assets/tarot"
MIO_MESSAGE = "焦らず、心を整える時間を。"

# ===== DB設定 =====
def init_db():
    conn = sqlite3.connect("mio_locks.db", check_same_thread=False)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_lock (
            anon_id TEXT PRIMARY KEY,
            first_seen TIMESTAMP NOT NULL
        )
    """)
    conn.commit()
    return conn

DB = init_db()

# ===== localStorage（匿名ID） =====
try:
    from streamlit_javascript import st_javascript
except Exception:
    st.warning("ブラウザ識別の初期化中です。")

if "anon_id" not in st.session_state:
    st.session_state.anon_id = str(uuid.uuid4())

# ===== タイトル表示 =====
st.markdown(
    f"<h2 style='text-align:center; color:#b58f5a;'>"
    f"{APP_TITLE}</h2>", unsafe_allow_html=True
)
st.caption("“運命は、偶然じゃなく構造でできている。”<br>3分でわかる、あなたの幸福な数字。", unsafe_allow_html=True)

# ===== 入力フォーム =====
with st.form("mio_form"):
    birthday = st.date_input("生年月日", min_value=dt(1890,1,1), max_value=dt.today())
    悩み = st.selectbox("今の悩み", ["恋愛", "仕事", "人間関係", "お金", "健康"])
    性別 = st.radio("性別", ["女性", "男性", "その他"])
    agree = st.checkbox("この診断は一度のみであることに同意します")
    submitted = st.form_submit_button("🔮 幸福数字を診断する")

# ===== 数秘計算関数 =====
def calc_result(birthday, 性別, 悩み):
    seed = int(birthday.strftime("%Y%m%d")) + len(悩み) + len(性別)
    random.seed(seed)
    num = random.randint(1, 22)
    tarot_list = [
        "愚者", "魔術師", "女教皇", "女帝", "皇帝", "教皇", "恋人", "戦車", "力", "隠者", "運命の輪",
        "正義", "吊るされた男", "死神", "節制", "悪魔", "塔", "星", "月", "太陽", "審判", "世界"
    ]
    stone_list = [
        "アメジスト", "ローズクォーツ", "ラピスラズリ", "ルチルクォーツ", "オニキス",
        "アクアマリン", "トパーズ", "ムーンストーン", "ガーネット", "サファイア",
        "エメラルド", "ルビー", "アメトリン", "ターコイズ", "シトリン",
        "ヘマタイト", "スモーキークォーツ", "カーネリアン", "ペリドット", "クリスタル",
        "モリオン", "ラブラドライト"
    ]
    return {"カード": tarot_list[num-1], "守護石": stone_list[num-1]}

# ===== 結果表示＋LINE誘導 =====
if submitted and agree:
    result = calc_result(birthday, 性別, 悩み)
    st.markdown(
        f"<h4 style='text-align:center;'>✨ あなたの幸福カード ✨</h4>"
        f"<p style='text-align:center; font-size:20px;'>"
        f"『{result['カード']}』<br>"
        f"<span style='font-size:16px; color:#b58f5a;'>守護石：{result['守護石']}</span></p>",
        unsafe_allow_html=True
    )

    # ---- LINEポップアップ ----
    import time
    if "mio_line_popup_shown" not in st.session_state:
        st.session_state.mio_line_popup_shown = False

    def show_line_popup():
        with st.container():
            st.markdown(f"""
            <div style='position:fixed; inset:0; background:rgba(0,0,0,.4); 
            display:flex; align-items:center; justify-content:center; z-index:9999;'>
              <div style='background:#fff9f1; border-radius:16px; padding:24px; width:90%; 
              max-width:480px; box-shadow:0 0 24px rgba(0,0,0,.15); text-align:center;'>
                <h3 style='color:#caa24a;'>LINEで守護石リストを受け取る</h3>
                <p style='color:#666;'>あなた専用の開運アドバイスを無料で送ります。</p>
                <a href='{LINE_URL}' target='_blank'
                style='display:inline-block; background:#06C755; color:white; padding:10px 20px; 
                border-radius:8px; text-decoration:none;'>LINEで受け取る</a><br><br>
                <button onclick="window.parent.postMessage('close_mio_popup','*')"
                style='padding:8px 16px; background:#fff; border:1px solid #ccc; 
                border-radius:8px;'>閉じる</button>
              </div>
            </div>
            <script>
              window.addEventListener('message', (e) => {{
                if(e.data==='close_mio_popup'){{
                  const popup=document.querySelector('div[style*="position:fixed"]');
                  if(popup) popup.remove();
                }}
              }});
            </script>
            """, unsafe_allow_html=True)

    if not st.session_state.mio_line_popup_shown:
        time.sleep(0.3)
        show_line_popup()
        st.session_state.mio_line_popup_shown = True

elif submitted and not agree:
    st.warning("同意チェックを入れてください。")


