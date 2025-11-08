# app.py — 澪 -Mio-｜脳科学×数秘術で導く“幸せの方程式”
import streamlit as st
import sqlite3
import uuid
import random
import os
import datetime
from datetime import datetime as dt, timedelta
from typing import Optional

# ===== 基本設定 =====
APP_TITLE = "澪 -Mio-｜脳科学×数秘術で導く“幸せの方程式”"
import os

# ✅ Secrets対応のLINE_URL設定（Streamlit Cloud用）
LINE_URL = st.secrets.get("LINE_URL", os.environ.get("LINE_URL", "https://lin.ee/f3iQlQY"))

LOCK_DAYS = 7
ASSETS_DIR = "assets/tarot"
MIO_MESSAGE = "焦らず、心を整える時間を。"

# ===== DB =====
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
    st_javascript = None

def get_or_set_anon_id() -> str:
    """localStorageに 'mio_anon_id' を保存。なければ生成して保存。"""
    if st_javascript is not None:
        existing = st_javascript("JSON.stringify(localStorage.getItem('mio_anon_id'));")
        if existing and existing not in ("null", "undefined"):
            return existing.strip('"')
        new_id = str(uuid.uuid4())
        st_javascript(f"localStorage.setItem('mio_anon_id', '{new_id}'); null;")
        return new_id
    if "fallback_anon_id" not in st.session_state:
        st.session_state.fallback_anon_id = str(uuid.uuid4())
    return st.session_state.fallback_anon_id

def is_locked(anon_id: str) -> tuple[bool, Optional[dt]]:
    cur = DB.cursor()
    cur.execute("SELECT first_seen FROM user_lock WHERE anon_id=?", (anon_id,))
    row = cur.fetchone()
    if not row:
        return False, None
    first_seen = dt.fromisoformat(row[0])
    if dt.utcnow() < first_seen + timedelta(days=LOCK_DAYS):
        return True, first_seen
    return False, first_seen

def lock_user(anon_id: str):
    cur = DB.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO user_lock (anon_id, first_seen) VALUES (?, ?)",
        (anon_id, dt.utcnow().isoformat()),
    )
    DB.commit()

# ===== 占いロジック =====
MAJOR_ARCANA = [
    "愚者","魔術師","女教皇","女帝","皇帝","教皇","恋人","戦車",
    "力","隠者","運命の輪","正義","吊るされた男","死神","節制",
    "悪魔","塔","星","月","太陽","審判","世界"
]

def calc_life_path_number(date_str: str) -> int:
    nums = [int(x) for x in date_str if x.isdigit()]
    s = sum(nums)
    while s > 9:
        s = sum([int(d) for d in str(s)])
    return 9 if s == 0 else s

def num_profile(n: int, concern: str) -> str:
    core = {
        1: "自己決定と推進力。自分の意志で未来を切り拓くタイプ。",
        2: "共感と調和。関係性の質が幸福感を左右します。",
        3: "創造と表現。アイデアを形にするほど輝く人。",
        4: "安定と積み上げ。構造化で安心を得るタイプ。",
        5: "自由と変化。新規刺激が活力の源泉に。",
        6: "献身と美。整える・整えられる循環で満たされます。",
        7: "洞察と探求。本質を見る“探究者”。",
        8: "実行と成果。数値化と達成で自己効力感が高まる。",
        9: "受容と手放し。循環を意識すると心が軽くなる。",
    }
    behav = {
        1: "行動経済学的に“1”は選好の一貫性を重視し、初手の意思決定が以降の選択を牽引しがち。",
        2: "“2”は損失回避よりも相互利益を優先し、協調的選択を好む傾向。",
        3: "“3”は選択肢が具体化されるほど実行率が上がる（実行意図の効果）。",
        4: "“4”は選択肢が過多だと満足度が下がる“選択のパラドクス”の影響を受けやすい。",
        5: "“5”は新奇性バイアスを味方にできるが、リスク評価の枠組み設計が鍵。",
        6: "“6”は社会的証明で動機づけが高まるため、安心感の設計が有効。",
        7: "“7”は選択肢が多いほど決断が遅くなる傾向。",
        8: "“8”は成果の可視化で行動強化（即時フィードバックが有効）。",
        9: "“9”は選択肢の統合提示で決断がスムーズ（まとめ提案が効く）。",
    }
    neuro = {
        1: "前頭前野の“自己主導”回路が強く、意思決定のスイッチが入ると持続。",
        2: "島皮質・前帯状皮質の“共感”ネットワークが働きやすい。",
        3: "連想ネットワーク優位。右脳の発想を前頭前野が素早く整えるタイプ。",
        4: "ワーキングメモリを節約する『ルーティン化』が安心へ直結。",
        5: "報酬予測誤差に敏感。小さな成功体験を連打すると伸びる。",
        6: "他者文脈のシミュレーションが得意。役割を得ると安定。",
        7: "前頭前野優位で“分析で安心を得る”。静かな時間が思考を深める。",
        8: "ドーパミン系の活用が鍵。数値目標と締め切りで火力UP。",
        9: "デフォルトモードネットワークの“統合”が働きやすい。手放しで進む。",
    }
    concern_tip = {
        "恋愛": "安全に愛されたい/愛したい気持ちを尊重。相手の反応より自分の感覚を信じて。",
        "仕事": "評価より“納得”が集中を生む。プロセス整備で実力が出やすい。",
        "金運": "増やす前に漏れを止める設計が効く。固定費の可視化から。",
        "人間関係": "境界線の最適化が質を上げる。距離と頻度を設計しよう。",
        "その他": "“安心・安全”を最優先。体感に沿った選択が最短距離。",
    }
    return (
        f"✦ あなたの幸福コード：{n}（{core.get(n,'')}）\n\n"
        f"{behav.get(n,'')}\n"
        f"{neuro.get(n,'')}\n\n"
        f"◆ 今のテーマ：{concern} — {concern_tip.get(concern, concern_tip['その他'])}"
    )

def draw_tarot() -> str:
    return random.choice(MAJOR_ARCANA)

def tarot_meaning(name: str) -> str:
    meanings = {
        "愚者": "新しい旅立ち、自由、直感。常識に縛られず、心の赴くままに。",
        "魔術師": "可能性の開花。意志と行動を一致させる時。",
        "女教皇": "直観と静謐。心の声に耳を澄ませて。",
        "女帝": "豊かさと受容。愛と実りを受け取る準備を。",
        "皇帝": "責任と支配。自分のルールを定める強さを。",
        "教皇": "信頼と秩序。導きを受け入れる時。",
        "恋人": "選択と絆。心が本当に求める方へ。",
        "戦車": "前進と勝利。自分を信じて突き進む。",
        "力": "優しさと勇気。恐れずに心を開くことで道が拓く。",
        "隠者": "内省と探求。答えは外ではなく内にある。",
        "運命の輪": "転機と流れ。偶然に見える必然を受け入れて。",
        "正義": "均衡と判断。冷静さと誠実さを大切に。",
        "吊るされた男": "視点の転換。今は静かに見つめる時。",
        "死神": "終わりと再生。手放しが次の始まりを呼ぶ。",
        "節制": "調和と再構築。流れに任せながら整えていく。",
        "悪魔": "執着と誘惑。手放す勇気が自由を呼ぶ。",
        "塔": "崩壊と覚醒。古い構造を壊すことで新しい光が差す。",
        "星": "希望と癒し。未来を信じる気持ちが現実を変える。",
        "月": "心の奥にある“不安”こそ、変化の前触れ。",
        "太陽": "喜びと明快。行動するほど光が増すサイン。",
        "審判": "再生と赦し。過去を受け入れ、新しい自分へ。",
        "世界": "完成と統合。一区切りつき、次の物語へ向かう。",
    }
    return meanings.get(name, "意味の核心は“今のあなたの体感”にあります。胸が静かになる方を選んで。")

def wave_color(n: int, card: str) -> str:
    by_num = {1:"レッド",2:"ピンク",3:"オレンジ",4:"ブラウン",5:"ターコイズ",6:"エメラルド",7:"ブラウン",8:"ゴールド",9:"パープル"}
    by_card = {"月":"ブルー","太陽":"イエロー","星":"シルバー","世界":"ホワイト"}
    return by_card.get(card, by_num.get(n, "ホワイト"))

def stone_suggestion(color: str) -> str:
    stones = {
        "ブラウン":"スモーキークォーツ",
        "ブルー":"ラピスラズリ／アクアマリン",
        "ホワイト":"ホワイトカルサイト／クリスタル",
        "イエロー":"シトリン",
        "シルバー":"ムーンストーン",
        "レッド":"ガーネット",
        "ピンク":"ローズクォーツ",
        "オレンジ":"カーネリアン",
        "ターコイズ":"ターコイズ",
        "エメラルド":"アベンチュリン",
        "ゴールド":"タイガーアイ",
        "パープル":"アメジスト",
    }
    return stones.get(color, "アメジスト")

def tarot_image_path(name: str):
    p = os.path.join(ASSETS_DIR, f"{name}.png")
    return p if os.path.exists(p) else None

# ===== UI =====
st.set_page_config(page_title=APP_TITLE, page_icon="🌙", layout="centered")

# === CSS ===
st.markdown("""
<style>
.stApp {
  background: linear-gradient(160deg, #fde7f3 0%, #eef4ff 55%, #e8fff3 100%);
  color: #1a1a1a;
  font-family: "Hiragino Mincho ProN", "Yu Mincho", "MS PMincho", serif;
}
h1,h2,h3,.gold {
  color: #D4AF37;
  text-shadow: 0 1px 1px rgba(0,0,0,.25);
  letter-spacing: .02em;
}
.subtitle { color:#3a3a3a; }
hr { border: none; height: 1px;
     background: linear-gradient(90deg, transparent, rgba(0,0,0,.2), transparent); }
.mio-card {
  background: rgba(255,255,255,0.9);
  border: 1px solid rgba(0,0,0,0.08);
  box-shadow: 0 6px 20px rgba(0,0,0,.08);
  border-radius: 14px;
  padding: 18px 20px;
}
.stButton>button {
  background: linear-gradient(135deg, #1f2a44, #2f3c66);
  color: #fff !important;
  border-radius: 10px;
  border: 1px solid rgba(0,0,0,0.1);
}
.stButton>button:hover { filter: brightness(1.1); }
</style>
""", unsafe_allow_html=True)

# === Header ===
st.markdown(f"""
<div style="text-align:center;">
  <h1 class="gold" style="margin-bottom:6px;">{APP_TITLE}</h1>
  <div class="subtitle" style="opacity:.95; font-size:16px; line-height:1.7;">
    “運命は、偶然じゃなく構造でできている。<br>
    あなたの心理と数字を、深層心理で読み解きます。”
  </div>
  <div style="margin-top:8px;">3分でわかる、あなたの幸福な数字。</div>
</div>
<hr>
""", unsafe_allow_html=True)

# ===== ロック確認 =====
anon_id = get_or_set_anon_id()
locked, first_seen = is_locked(anon_id)
if locked:
    until = (first_seen + timedelta(days=LOCK_DAYS)).strftime("%Y-%m-%d")
    st.warning(f"この診断は一度のみです。再診断は {until} 以降に可能です。")
    st.markdown(f"▶️ 続きはLINEで深掘り鑑定： [公式LINEへ]({LINE_URL})")
    st.stop()

# ===== 入力フォーム =====
with st.form("mio_form", clear_on_submit=False):
    col1, col2 = st.columns(2)
    with col1:
        bdate = st.date_input(
            "生年月日",
            value=datetime.date(1990, 1, 1),
            min_value=datetime.date(1890, 1, 1),
            max_value=datetime.date.today(),
            format="YYYY-MM-DD"
        )
        gender = st.selectbox("性別", ["女性", "男性", "その他", "回答しない"])
    with col2:
        concern = st.selectbox("今の悩み", ["恋愛", "仕事", "金運", "人間関係", "その他"])
        acting = st.selectbox("行動タイプ", ["すぐ動く", "考えてから動く", "状況で変わる"])

    agree = st.checkbox("この診断は一度のみであることに同意します")
    submitted = st.form_submit_button("🔮 幸福数字を診断する")

# ===== 診断処理 =====
if submitted:
    if not agree:
        st.error("一度のみの実施に同意してください。"); st.stop()
    if not bdate:
        st.error("生年月日を入力してください。"); st.stop()

    lock_user(anon_id)

    lp = calc_life_path_number(bdate.strftime("%Y-%m-%d"))
    card = draw_tarot()
    color = wave_color(lp, card)
    stone = stone_suggestion(color)

    st.success("診断が完了しました。")

    st.markdown("### ✦ あなたの“幸福数字”")
    st.markdown(f"<div class='mio-card'>{num_profile(lp, concern)}</div>", unsafe_allow_html=True)

    st.markdown("### ✦ 今のあなたを象徴するタロット")
    img = tarot_image_path(card)
    if img:
        st.image(img, caption=card, use_column_width=True)
    st.markdown(
        f"<div class='mio-card'>🔮 今のあなたを象徴するタロットカードは【{card}】<br>"
        f"{tarot_meaning(card)}<br>澪からのメッセージ：「{MIO_MESSAGE}」</div>",
        unsafe_allow_html=True
    )

    st.markdown("### ✦ あなたの波動カラー")
    st.markdown(
        f"<div class='mio-card'><b>{color}</b> — その色を身につける/眺める/飾るだけで、心のノイズが減り、選択が澄みます。</div>",
        unsafe_allow_html=True
    )

    st.markdown("### ✦ おすすめ守護石")
    st.markdown(
        f"<div class='mio-card'>おすすめの守護石：{stone}</div>",
        unsafe_allow_html=True
    )

    # --- LINE誘導 ---
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="text-align:center; font-size:18px;">
          <b>“あなた専用の鑑定文”を無料でお届けします。</b><br>
          診断結果の続きを知りたい方は、LINEで <b>【診断】</b> と送ってください。<br><br>
          <a href="{LINE_URL}" target="_blank"
             style="padding:12px 22px; border-radius:10px; background:#1f274e;
                    color:white; text-decoration:none; font-weight:bold;
                    border:1px solid rgba(255,255,255,0.3);
                    box-shadow:0 4px 12px rgba(0,0,0,0.25);">
            🌙 公式LINEで受け取る
          </a>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
    "<div style='text-align:center; font-size:13px; margin-top:25px; color:#555;'>"
    "※ この診断は一度のみとなります。詳細の深掘り・追加鑑定はLINEでご案内しています。<br>"
    "※ LINEが開かない場合は、右上の三本線をタップして「ブラウザで開く」を押すと開けます。"
    "</div>",
    unsafe_allow_html=True
)

