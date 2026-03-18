import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# =====================
# HÀM TÍNH TOÁN
# =====================
def tinh_rsi(df, so_ngay=14):
    delta   = df["Close"].diff()
    tang    = delta.clip(lower=0)
    giam    = -delta.clip(upper=0)
    tb_tang = tang.rolling(so_ngay).mean()
    tb_giam = giam.rolling(so_ngay).mean()
    rs      = tb_tang / tb_giam
    return 100 - 100 / (1 + rs)

def tinh_macd(df):
    ema12     = df["Close"].ewm(span=12, adjust=False).mean()
    ema26     = df["Close"].ewm(span=26, adjust=False).mean()
    macd      = ema12 - ema26
    signal    = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal
    return macd, signal, histogram

def tinh_tat_ca(df):
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    df["RSI"]  = tinh_rsi(df)
    df["MACD"], df["Signal"], df["Histogram"] = tinh_macd(df)
    return df

def phan_tich_volume(df):
    vol_ht = df["Volume"].iloc[-1]
    vol_tb = df["Volume"].rolling(20).mean().iloc[-1]
    gia_tang = df["Close"].iloc[-1] > df["Close"].iloc[-2]
    vol_lon  = vol_ht > vol_tb
    if gia_tang and vol_lon:
        ket_qua = "✅ Giá tăng + Volume lớn — Tích cực"
    elif gia_tang and not vol_lon:
        ket_qua = "⚠️ Giá tăng + Volume yếu — Cẩn thận"
    elif not gia_tang and vol_lon:
        ket_qua = "🔴 Giá giảm + Volume lớn — Áp lực bán mạnh"
    else:
        ket_qua = "⚡ Giá giảm + Volume yếu — Chưa rõ"
    return ket_qua, vol_ht, vol_tb

def phan_tich_xu_huong(df):
    gia_moi  = df["Close"].iloc[-1]
    rsi_moi  = df["RSI"].iloc[-1]
    ma20_moi = df["MA20"].iloc[-1]
    ma50_moi = df["MA50"].iloc[-1]
    tang_5   = (gia_moi - df["Close"].iloc[-5]) / df["Close"].iloc[-5] * 100
    if rsi_moi > 70 and tang_5 > 5:
        xu_huong = "🔥 Tăng nóng ngắn hạn — Rủi ro cao"
    elif gia_moi > ma20_moi and ma20_moi > ma50_moi and rsi_moi < 70:
        xu_huong = "📈 Tăng bền vững — Tích cực"
    elif gia_moi < ma20_moi and ma20_moi < ma50_moi:
        xu_huong = "📉 Giảm bền vững — Thận trọng"
    else:
        xu_huong = "↔️ Chưa rõ xu hướng"
    return xu_huong, tang_5

def tinh_khang_cu_ho_tro(df):
    gia_moi      = df["Close"].iloc[-1]
    khang_cu_20  = df["High"].rolling(20).max().iloc[-1]
    ho_tro_20    = df["Low"].rolling(20).min().iloc[-1]
    khang_cu_50  = df["High"].rolling(50).max().iloc[-1]
    ho_tro_50    = df["Low"].rolling(50).min().iloc[-1]
    cach_khang_cu = (khang_cu_20 - gia_moi) / gia_moi * 100
    cach_ho_tro   = (gia_moi - ho_tro_20)   / gia_moi * 100
    if cach_khang_cu < 2:
        nhan_xet = "⚠️ Gần kháng cự — Khó tăng thêm"
    elif cach_ho_tro < 2:
        nhan_xet = "✅ Gần hỗ trợ — Ít rủi ro giảm thêm"
    else:
        nhan_xet = "⚡ Đang giữa vùng"
    return khang_cu_20, ho_tro_20, khang_cu_50, ho_tro_50, cach_khang_cu, cach_ho_tro, nhan_xet

# =====================
# GIAO DIỆN STREAMLIT
# =====================
st.set_page_config(page_title="Tool Chứng Khoán", page_icon="📈", layout="wide")
st.title("📈 Tool Phân Tích Chứng Khoán")

# Nhập mã + chọn thời gian
col_input, col_period = st.columns([3, 1])
with col_input:
    ma = st.text_input("🔍 Mã cổ phiếu", placeholder="VD: 7203.T, AAPL, BTC-USD")
with col_period:
    period = st.selectbox("📅 Thời gian", ["3mo", "6mo", "1y", "2y"])

nut_phan_tich = st.button("🔍 Phân tích", type="primary")

if nut_phan_tich and ma:
    with st.spinner(f"⏳ Đang tải {ma.upper()}..."):
        try:
            ticker = yf.Ticker(ma.upper())
            df     = ticker.history(period=period)
            info   = ticker.info

            if df.empty:
                st.error(f"❌ Không tìm thấy mã {ma.upper()}")
            else:
                # Tính toán
                df = tinh_tat_ca(df)
                ten = info.get("longName", ma.upper())

                # Thông tin cơ bản
                gia_hien_tai  = df["Close"].iloc[-1]
                gia_cao_nhat  = df["Close"].max()
                gia_thap_nhat = df["Close"].min()
                gia_dau       = df["Close"].iloc[0]
                phan_tram     = (gia_hien_tai - gia_dau) / gia_dau * 100
                rsi_moi       = df["RSI"].iloc[-1]
                macd_moi      = df["MACD"].iloc[-1]
                sig_moi       = df["Signal"].iloc[-1]
                ma20_moi      = df["MA20"].iloc[-1]
                ma50_moi      = df["MA50"].iloc[-1]

                # Gọi hàm phân tích
                vol_ket_qua, vol_ht, vol_tb = phan_tich_volume(df)
                xu_huong, tang_5            = phan_tich_xu_huong(df)
                khang_cu_20, ho_tro_20, khang_cu_50, ho_tro_50, \
                cach_khang_cu, cach_ho_tro, nhan_xet_kc = tinh_khang_cu_ho_tro(df)

                # ── Tiêu đề
                st.subheader(f"📊 {ten}")
                st.divider()

                # ── 4 ô thông tin
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("💰 Giá hiện tại", f"{gia_hien_tai:,.2f}")
                c2.metric("📈 Cao nhất",     f"{gia_cao_nhat:,.2f}")
                c3.metric("📉 Thấp nhất",    f"{gia_thap_nhat:,.2f}")
                c4.metric("📊 Thay đổi",     f"{phan_tram:+.2f}%")

                st.divider()

                # ── Tín hiệu kỹ thuật
                st.subheader("📊 Tín hiệu kỹ thuật")
                c5, c6, c7 = st.columns(3)

                # RSI
                if rsi_moi > 70:
                    c5.error(f"RSI: {rsi_moi:.1f}\n⚠️ Quá mua")
                elif rsi_moi < 30:
                    c5.success(f"RSI: {rsi_moi:.1f}\n✅ Quá bán")
                else:
                    c5.info(f"RSI: {rsi_moi:.1f}\n⚡ Trung lập")

                # MACD
                if macd_moi > sig_moi:
                    c6.success("MACD\n📈 Tích cực")
                else:
                    c6.error("MACD\n📉 Tiêu cực")

                # MA
                if gia_hien_tai > ma20_moi and ma20_moi > ma50_moi:
                    c7.success("MA\n📈 Xu hướng tăng")
                elif gia_hien_tai < ma20_moi and ma20_moi < ma50_moi:
                    c7.error("MA\n📉 Xu hướng giảm")
                else:
                    c7.info("MA\n↔️ Đi ngang")

                st.divider()

                # ── 3 chỉ số mới
                st.subheader("📦 Phân tích nâng cao")
                c8, c9, c10 = st.columns(3)

                c8.info(f"**Khối lượng**\n{vol_ket_qua}\n\nHT: {vol_ht:,.0f}\nTB20: {vol_tb:,.0f}")
                c9.info(f"**Xu hướng**\n{xu_huong}\n\nTăng 5 ngày: {tang_5:+.2f}%")
                c10.info(f"**Kháng cự / Hỗ trợ**\n{nhan_xet_kc}\n\nKháng cự: {khang_cu_20:,.2f} (cách {cach_khang_cu:.1f}%)\nHỗ trợ: {ho_tro_20:,.2f} (cách {cach_ho_tro:.1f}%)")

                st.divider()

                # ── Biểu đồ
                st.subheader("📈 Biểu đồ")
                fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

                ax1.plot(df.index, df["Close"], label="Giá",  color="blue",   linewidth=1.5)
                ax1.plot(df.index, df["MA20"],  label="MA20", color="orange", linestyle="--")
                ax1.plot(df.index, df["MA50"],  label="MA50", color="red",    linestyle="--")
                ax1.set_title(ten)
                ax1.legend()
                ax1.grid(True)

                ax2.plot(df.index, df["RSI"], color="purple", linewidth=1.5)
                ax2.axhline(y=70, color="red",   linestyle="--", label="Quá mua (70)")
                ax2.axhline(y=30, color="green", linestyle="--", label="Quá bán (30)")
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
                st.pyplot(fig)        # ✅ dùng st.pyplot thay plt.show()
                plt.close()

        except Exception as e:
            st.error(f"❌ Lỗi: {e}")