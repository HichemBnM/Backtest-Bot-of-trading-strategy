import pandas as pd
import numpy as np
import ta

df = pd.read_excel("btc_data.xlsx")
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
df.set_index('Date', inplace=True)
df = df.sort_index()

df['EMA_13_D'] = df['Close'].ewm(span=13).mean()
df['EMA_13_D_prev'] = df['EMA_13_D'].shift(1)

df['EMA_13_W'] = df['Close'].resample('W').last().ewm(span=13).mean().reindex(df.index, method='ffill')
df['EMA_13_W_prev'] = df['EMA_13_W'].shift(1)

macd = ta.trend.MACD(df['Close'])
df['MACD_HIST_D'] = macd.macd_diff()
df['MACD_HIST_D_prev'] = df['MACD_HIST_D'].shift(1)

macd_weekly = ta.trend.MACD(df['Close'].resample('W').last())
macd_hist_w = macd_weekly.macd_diff().reindex(df.index, method='ffill')
df['MACD_HIST_W'] = macd_hist_w
df['MACD_HIST_W_prev'] = df['MACD_HIST_W'].shift(1)

df['ATR'] = ta.volatility.AverageTrueRange(
    high=df['Close'], low=df['Close'], close=df['Close'], window=14
).average_true_range()

def get_score(row):
    score = 0
    if row['EMA_13_D'] > row['EMA_13_D_prev']: score += 1
    if row['MACD_HIST_D'] > row['MACD_HIST_D_prev']: score += 1
    if row['EMA_13_W'] > row['EMA_13_W_prev']: score += 1
    if row['MACD_HIST_W'] > row['MACD_HIST_W_prev']: score += 1
    return score

df['Score'] = df.apply(get_score, axis=1)


trades = []
in_trade = False
entry_price = stop_price = shares = 0
bank = 500000000  # Starting capital

for i in range(1, len(df)):
    today = df.iloc[i]
    yesterday = df.iloc[i - 1]

    if not in_trade and yesterday['Score'] < 4 and today['Score'] == 4:
        entry_price = today['Close']
        atr = today['ATR']
        stop_price = entry_price - 2 * atr
        risk_per_share = entry_price - stop_price

        if risk_per_share < 1e-6:
            continue

        shares = int((0.01 * bank) / risk_per_share)  
        in_trade = True
        entry_date = df.index[i]

    elif in_trade and today['Score'] <= 2:
        exit_price = today['Close']
        pl = (exit_price - entry_price) * shares
        bank += pl
        entry_dt = pd.to_datetime(entry_date)
        exit_dt = df.index[i]
        days_held = (exit_dt - entry_dt).days

        trades.append({
            "Entry Date": entry_date,
            "Exit Date": exit_dt,
            "Entry Price": entry_price,
            "Exit Price": exit_price,
            "Shares": shares,
            "P/L": pl,
            "Days Held": days_held,
            "Exit Reason": "Score Drop"
        })

        in_trade = False

    elif in_trade and today['Close'] < stop_price:
        exit_price = stop_price
        pl = (exit_price - entry_price) * shares
        bank += pl
        exit_dt = df.index[i]
        days_held = (exit_dt - pd.to_datetime(entry_date)).days

        trades.append({
            "Entry Date": entry_date,
            "Exit Date": exit_dt,
            "Entry Price": entry_price,
            "Exit Price": exit_price,
            "Shares": shares,
            "P/L": pl,
            "Days Held": days_held,
            "Exit Reason": "Stop Loss"
        })

        in_trade = False

results = pd.DataFrame(trades)

win_days = results[results['P/L'] > 0]['Days Held']
loss_days = results[results['P/L'] <= 0]['Days Held']
avg_days_win = win_days.mean() if not win_days.empty else 0
avg_days_loss = loss_days.mean() if not loss_days.empty else 0

summary = {
    "Total Trades": len(results),
    "Win Rate": (results['P/L'] > 0).mean(),
    "Average P/L": results["P/L"].mean(),
    "Total P/L": results["P/L"].sum(),
    "Average Win": results[results['P/L'] > 0]["P/L"].mean(),
    "Average Loss": results[results['P/L'] <= 0]["P/L"].mean(),
    "Avg Days Held (Win)": avg_days_win,
    "Avg Days Held (Loss)": avg_days_loss,
    "CAGR": ((bank / 50000) ** (1 / (len(df) / 252)) - 1) * 100,
    "Starting Bank": 50000,
    "Ending Bank": bank
}

summary_df = pd.DataFrame([summary])
print(summary_df.T)
import openpyxl
print("openpyxl is working!")
import os   
summary_df = pd.DataFrame([summary])
summary_df.to_excel("summary.xlsx", index=False, engine='openpyxl')    

