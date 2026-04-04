import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'

# =====================
# 計算関数
# =====================
def calc_rsi(df, period=14):
    delta   = df["Close"].diff()
    gain    = delta.clip(lower=0)
    loss    = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs      = avg_gain / avg_loss
    return 100 - 100 / (1 + rs)

def calc_macd(df):
    ema12     = df["Close"].ewm(span=12, adjust=False).mean()
    ema26     = df["Close"].ewm(span=26, adjust=False).mean()
    macd      = ema12 - ema26
    signal    = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal
    return macd, signal, histogram

def calc_all(df):
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    df["RSI"]  = calc_rsi(df)
    df["MACD"], df["Signal"], df["Histogram"] = calc_macd(df)
    return df

def analyze_volume(df):
    vol_now = df["Volume"].iloc[-1]
    vol_avg = df["Volume"].rolling(20).mean().iloc[-1]
    price_up = df["Close"].iloc[-1] > df["Close"].iloc[-2]
    vol_high = vol_now > vol_avg
    if price_up and vol_high:
        result = "✅ 価格上昇 + 出来高大 — ポジティブ"
    elif price_up and not vol_high:
        result = "⚠️ 価格上昇 + 出来高小 — 注意"
    elif not price_up and vol_high:
        result = "🔴 価格下落 + 出来高大 — 売り圧力強い"
    else:
        result = "⚡ 価格下落 + 出来高小 — 不明確"
    return result, vol_now, vol_avg

def analyze_trend(df):
    price   = df["Close"].iloc[-1]
    rsi     = df["RSI"].iloc[-1]
    ma20    = df["MA20"].iloc[-1]
    ma50    = df["MA50"].iloc[-1]
    chg5    = (price - df["Close"].iloc[-5]) / df["Close"].iloc[-5] * 100
    if rsi > 70 and chg5 > 5:
        trend = "🔥 短期過熱 — リスク高い"
    elif price > ma20 and ma20 > ma50 and rsi < 70:
        trend = "📈 安定上昇 — ポジティブ"
    elif price < ma20 and ma20 < ma50:
        trend = "📉 安定下落 — 注意"
    else:
        trend = "↔️ トレンド不明確"
    return trend, chg5

def calc_support_resistance(df):
    price        = df["Close"].iloc[-1]
    resistance20 = df["High"].rolling(20).max().iloc[-1]
    support20    = df["Low"].rolling(20).min().iloc[-1]
    resistance50 = df["High"].rolling(50).max().iloc[-1]
    support50    = df["Low"].rolling(50).min().iloc[-1]
    dist_res     = (resistance20 - price) / price * 100
    dist_sup     = (price - support20)    / price * 100
    if dist_res < 2:
        comment = "⚠️ レジスタンス付近 — 上値重い"
    elif dist_sup < 2:
        comment = "✅ サポート付近 — 下値リスク小"
    else:
        comment = "⚡ レンジ中間"
    return resistance20, support20, resistance50, support50, dist_res, dist_sup, comment

# =====================
# Streamlit UI
# =====================
st.set_page_config(page_title="株価テクニカル分析", page_icon="📈", layout="wide")
st.title("📈 株価テクニカル分析ツール")

col_input, col_period = st.columns([3, 1])
with col_input:
    ticker_input = st.text_input("🔍 銘柄コード", placeholder="例：7203.T, AAPL, BTC-USD")
with col_period:
    period = st.selectbox("📅 期間", ["3mo", "6mo", "1y", "2y"],
                          format_func=lambda x: {"3mo":"3ヶ月","6mo":"6ヶ月","1y":"1年","2y":"2年"}[x])

btn_analyze = st.button("🔍 分析する", type="primary")

if btn_analyze and ticker_input:
    with st.spinner(f"⏳ {ticker_input.upper()} のデータを取得中..."):
        try:
            ticker = yf.Ticker(ticker_input.upper())
            df     = ticker.history(period=period)
            info   = ticker.info

            if df.empty:
                st.error(f"❌ 銘柄 {ticker_input.upper()} が見つかりません")
            else:
                df  = calc_all(df)
                name = info.get("longName", ticker_input.upper())

                price_now  = df["Close"].iloc[-1]
                price_high = df["Close"].max()
                price_low  = df["Close"].min()
                price_open = df["Close"].iloc[0]
                pct_change = (price_now - price_open) / price_open * 100
                rsi_now    = df["RSI"].iloc[-1]
                macd_now   = df["MACD"].iloc[-1]
                sig_now    = df["Signal"].iloc[-1]
                ma20_now   = df["MA20"].iloc[-1]
                ma50_now   = df["MA50"].iloc[-1]

                vol_result, vol_now, vol_avg = analyze_volume(df)
                trend, chg5                  = analyze_trend(df)
                r20, s20, r50, s50, d_res, d_sup, sr_comment = calc_support_resistance(df)

                # ── 銘柄名
                st.subheader(f"📊 {name}")
                st.divider()

                # ── 基本情報
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("💰 現在値",   f"{price_now:,.2f}")
                c2.metric("📈 期間高値", f"{price_high:,.2f}")
                c3.metric("📉 期間安値", f"{price_low:,.2f}")
                c4.metric("📊 騰落率",   f"{pct_change:+.2f}%")

                st.divider()

                # ── テクニカルシグナル
                st.subheader("📊 テクニカルシグナル")
                c5, c6, c7 = st.columns(3)

                if rsi_now > 70:
                    c5.error(f"RSI: {rsi_now:.1f}\n⚠️ 買われすぎ")
                elif rsi_now < 30:
                    c5.success(f"RSI: {rsi_now:.1f}\n✅ 売られすぎ")
                else:
                    c5.info(f"RSI: {rsi_now:.1f}\n⚡ 中立")

                if macd_now > sig_now:
                    c6.success("MACD\n📈 ポジティブ")
                else:
                    c6.error("MACD\n📉 ネガティブ")

                if price_now > ma20_now and ma20_now > ma50_now:
                    c7.success("移動平均\n📈 上昇トレンド")
                elif price_now < ma20_now and ma20_now < ma50_now:
                    c7.error("移動平均\n📉 下降トレンド")
                else:
                    c7.info("移動平均\n↔️ 横ばい")

                st.divider()

                # ── 高度な分析
                st.subheader("📦 詳細分析")
                c8, c9, c10 = st.columns(3)

                c8.info(f"**出来高分析**\n{vol_result}\n\n現在：{vol_now:,.0f}\n20日平均：{vol_avg:,.0f}")
                c9.info(f"**トレンド**\n{trend}\n\n5日変化：{chg5:+.2f}%")
                c10.info(f"**レジスタンス / サポート**\n{sr_comment}\n\nレジスタンス：{r20:,.2f}（差{d_res:.1f}%）\nサポート：{s20:,.2f}（差{d_sup:.1f}%）")

                st.divider()

                # ── チャート
                st.subheader("📈 チャート")
                fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

                ax1.plot(df.index, df["Close"], label="Price",  color="blue",   linewidth=1.5)
                ax1.plot(df.index, df["MA20"],  label="MA20",   color="orange", linestyle="--")
                ax1.plot(df.index, df["MA50"],  label="MA50",   color="red",    linestyle="--")
                ax1.set_title(name)
                ax1.legend()
                ax1.grid(True)

                ax2.plot(df.index, df["RSI"], color="purple", linewidth=1.5)
                ax2.axhline(y=70, color="red",   linestyle="--", label="Overbought (70)")
                ax2.axhline(y=30, color="green", linestyle="--", label="Oversold (30)")
                ax2.set_title("RSI")
                ax2.set_ylim(0, 100)
                ax2.legend()
                ax2.grid(True)

                ax3.plot(df.index, df["MACD"],   label="MACD",   color="blue")
                ax3.plot(df.index, df["Signal"], label="Signal", color="orange")
                colors = ["green" if x > 0 else "red" for x in df["Histogram"]]
                ax3.bar(df.index, df["Histogram"], color=colors, alpha=0.5)
                ax3.axhline(y=0, color="black", linewidth=0.5)
                ax3.set_title("MACD")
                ax3.legend()
                ax3.grid(True)

                plt.tight_layout()
                st.pyplot(fig)
                plt.close()

        except Exception as e:
            st.error(f"❌ エラー：{e}")
