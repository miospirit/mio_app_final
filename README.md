# 澪 -Mio-（Final Edition）

特徴:
- 明朝体＋金文字＋パステル背景
- 脳科学×行動経済学のトーンで出力
- LINE誘導（CTA）整理済み
- タロット画像のプレースホルダー同梱（assets/tarot）

## 起動手順（Windows）
```powershell
cd "<あなたのパス>\mio_app_final"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```
ブラウザで http://localhost:8501 を開きます。

## 画像差し替え
`assets/tarot/` 内の `月.png` などを同名PNGで入れ替えるだけでOKです。
推奨: 600x1000px 縦長。
