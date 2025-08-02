import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import feedparser
import gradio as gr

def calculate_indicators(df):
    df["SMA_50"] = df["Close"].rolling(window=50).mean()
    df["SMA_200"] = df["Close"].rolling(window=200).mean()
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))
    df["EMA_12"] = df["Close"].ewm(span=12, adjust=False).mean()
    df["EMA_26"] = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = df["EMA_12"] - df["EMA_26"]
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    return df

def generate_verdict(df):
    reasons = []

    if df["RSI"].iloc[-1] < 30:
        reasons.append("🔻 RSI is below 30 (oversold)")
    elif df["RSI"].iloc[-1] > 70:
        reasons.append("🔺 RSI is above 70 (overbought)")

    if df["MACD"].iloc[-1] < df["Signal"].iloc[-1]:
        reasons.append("📉 MACD is below Signal (bearish)")
    elif df["MACD"].iloc[-1] > df["Signal"].iloc[-1]:
        reasons.append("📈 MACD is above Signal (bullish)")

    price = df["Close"].iloc[-1]
    sma50 = df["SMA_50"].iloc[-1]
    sma200 = df["SMA_200"].iloc[-1]

    if price < sma50 < sma200:
        reasons.append("❌ Death cross: price < SMA50 < SMA200")
        verdict = "SELL"
    elif price > sma50 > sma200:
        reasons.append("✅ Golden cross: price > SMA50 > SMA200")
        verdict = "BUY"
    else:
        verdict = "HOLD"

    return verdict, reasons

def plot_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode='lines+markers', name='Close Price', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA_50"], mode='lines', name='SMA 50', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA_200"], mode='lines', name='SMA 200', line=dict(color='green')))
    fig.update_layout(
        title="📊 Stock Price with SMA",
        xaxis_title="Date",
        yaxis_title="Price",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=14)
    )
    return fig

def get_news(stock):
    feed_url = f"https://news.google.com/rss/search?q={stock}+stock"
    feed = feedparser.parse(feed_url)
    if not feed.entries:
        return "No news found."

    news_html = ""
    for entry in feed.entries[:3]:
        news_html += f"<p>🗞 <a href='{entry.link}' target='_blank'>{entry.title}</a></p>"
    return news_html

def analyze_stock(stock):
    if not stock:
        return None, "<span style='color:gray'>Please select a stock.</span>", ""

    ticker = yf.Ticker(stock)
    df = ticker.history(period="6mo")
    if df.empty:
        return None, "<span style='color:red'>No data found.</span>", ""

    df = calculate_indicators(df)
    verdict, reasons = generate_verdict(df)
    chart = plot_chart(df)
    news = get_news(stock)

    color = {"BUY": "#22c55e", "SELL": "#ef4444", "HOLD": "#eab308"}[verdict]
    verdict_html = f"""
        <div style='background-color:{color}20; padding:15px; border-radius:10px;'>
            <h3 style='color:{color}; margin-bottom:10px;'>📌 Recommendation: {verdict}</h3>
            <ul>{"".join(f"<li>{r}</li>" for r in reasons)}</ul>
        </div>
    """

    return chart, verdict_html, news

stocks = ["TCS.NS", "INFY.NS", "RELIANCE.NS", "HDFCBANK.NS", "ITC.NS"]

with gr.Blocks(title="AI Stock Analyzer") as demo:
    gr.Markdown("## 📈 AI Stock Analyzer")
    gr.Markdown("Get AI-powered stock recommendation (Buy/Sell/Hold) based on RSI, MACD, SMA + live news & charts.")


    # your dropdown, button, chart, and recommendation layout continues here...


    with gr.Row():
        with gr.Column(scale=1):
            dropdown = gr.Dropdown(choices=stocks, label="Select Stock", interactive=True)
            submit_btn = gr.Button("🚀 Analyze", variant="primary")
            chart_output = gr.Plot(label="")

        with gr.Column(scale=1):
            recommendation_html = gr.HTML(label="🧠 Recommendation")
            news_output = gr.HTML(label="📰 Top News")

    submit_btn.click(fn=analyze_stock, inputs=dropdown, outputs=[chart_output, recommendation_html, news_output])

demo.launch()
