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

