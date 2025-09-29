import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

# ---------------------------
# Function to fetch Binance Kline data
# ---------------------------
def get_historical_data(symbol="BTCUSDT", interval="15m", limit=200):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(url, params=params)
    data = response.json()

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "trades",
        "taker_base_vol", "taker_quote_vol", "ignore"
    ])

    # Convert numeric fields
    df[["open","high","low","close","volume"]] = df[["open","high","low","close","volume"]].astype(float)

    # Convert time
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")

    return df

# ---------------------------
# Streamlit App
# ---------------------------
st.set_page_config(page_title="BTCUSDT Candlestick", layout="wide")

st.title("📊 Binance BTCUSDT Candlestick Data")

# User inputs
interval = st.selectbox("Select Interval", ["1m","5m","15m","1h","4h","1d"], index=2)
limit = st.slider("Number of candles", 50, 500, 200)

if st.button("Get Historical Data"):
    df = get_historical_data("BTCUSDT", interval, limit)

    if df.empty:
        st.warning("No data received from Binance API")
    else:
        st.write(f"Showing {len(df)} rows for BTCUSDT ({interval})")
        st.dataframe(df)

        # Plot candlestick chart
        fig = go.Figure(data=[go.Candlestick(
            x=df["open_time"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="BTCUSDT"
        )])

        fig.update_layout(
            title=f"BTCUSDT - {interval} Candlestick Chart",
            xaxis_title="Time",
            yaxis_title="Price (USDT)",
            xaxis_rangeslider_visible=False,
            template="plotly_dark",
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)
