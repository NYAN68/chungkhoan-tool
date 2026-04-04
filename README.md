# 📈 株価テクニカル分析ツール / Stock Technical Analysis Tool

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red?logo=streamlit)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🇯🇵 日本語

### 概要
株価データをリアルタイムで取得し、主要なテクニカル指標を自動計算・可視化するWebアプリです。  
日本株・米国株・仮想通貨に対応しています。

### 主な機能
- **移動平均線（MA20 / MA50）** — トレンド方向の確認
- **RSI（相対力指数）** — 過買い・過売りのシグナル検出
- **MACD** — トレンド転換のシグナル
- **出来高分析** — 価格変動と出来高の関係を評価
- **サポート・レジスタンスライン** — 直近の高値・安値ゾーンを自動検出
- **総合トレンド判定** — 複数指標を組み合わせた自動判断

### 使用技術
| ライブラリ | 用途 |
|---|---|
| `Streamlit` | WebUI フレームワーク |
| `yfinance` | 株価データ取得 |
| `pandas` | データ処理 |
| `matplotlib` | チャート描画 |

### セットアップ
```bash
git clone https://github.com/NYAN68/Kabuka-tekunikaru-bunseki-tool
cd Kabuka-tekunikaru-bunseki-tool
pip install -r requirements.txt
streamlit run tool.py
```

### 使い方
1. テキストボックスに銘柄コードを入力（例：`7203.T`、`AAPL`、`BTC-USD`）
2. 分析期間を選択（3ヶ月 / 6ヶ月 / 1年 / 2年）
3. 「分析」ボタンをクリック → 指標とチャートが自動表示

---

## 🇬🇧 English

### Overview
A web application that fetches real-time stock data and automatically calculates and visualizes key technical indicators.  
Supports Japanese stocks, US stocks, and cryptocurrencies.

### Features
- **Moving Averages (MA20 / MA50)** — trend direction analysis
- **RSI** — overbought / oversold signal detection
- **MACD** — trend reversal signals
- **Volume Analysis** — relationship between price movement and volume
- **Support & Resistance** — automatic detection of recent high/low zones
- **Trend Summary** — combined multi-indicator auto judgment

### Tech Stack
| Library | Purpose |
|---|---|
| `Streamlit` | Web UI framework |
| `yfinance` | Stock data fetching |
| `pandas` | Data processing |
| `matplotlib` | Chart rendering |

### Setup
```bash
git clone https://github.com/NYAN68/Kabuka-tekunikaru-bunseki-tool
cd Kabuka-tekunikaru-bunseki-tool
pip install -r requirements.txt
streamlit run tool.py
```

### Usage
1. Enter a ticker symbol (e.g. `7203.T`, `AAPL`, `BTC-USD`)
2. Select analysis period (3M / 6M / 1Y / 2Y)
3. Click **Analyze** → indicators and charts appear automatically

---

## 📸 スクリーンショット / Screenshots

> *(スクリーンショットをここに追加してください / Add screenshots here)*
><img width="1920" height="1032" alt="image" src="https://github.com/user-attachments/assets/21adc1f0-0580-4be0-aeed-625787e129e9" />
<img width="1920" height="1032" alt="image" src="https://github.com/user-attachments/assets/edbb75f8-44c1-4f29-9312-952491032ed8" />
<img width="1920" height="1032" alt="image" src="https://github.com/user-attachments/assets/0d39d566-d949-4b7a-8836-a6b6b36b4568" />



> 

---

## 👤 Author

**NGUYEN THANH NHAN**  
🔗 [GitHub](https://github.com/NYAN68)
