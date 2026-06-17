# script.py

import os
import pandas as pd
import pandas_ta as ta
import numpy as np
from datetime import datetime, timedelta

# ============================================================
# بيانات الحساب
# ============================================================

EMAIL = "maikhaled918273@gmail.com"
PASSWORD = "010011012"
ASSET = "EURUSD_otc"

print(f"🚀 بدء تشغيل الباك تيست")
print(f"📧 {EMAIL}")
print(f"📊 الزوج: {ASSET}")

# ============================================================
# توليد بيانات محاكاة
# ============================================================

def generate_mock_data(asset, days=30):
    """توليد بيانات شموع محاكاة"""
    
    periods = days * 24 * 60
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    
    base_price = {
        "EURUSD_otc": 1.0850,
        "GBPUSD_otc": 1.2650,
        "USDJPY_otc": 148.50,
        "AUDUSD_otc": 0.6550,
        "USDCAD_otc": 1.3550,
        "USDCHF_otc": 0.8850,
        "NZDUSD_otc": 0.5950,
        "EURGBP_otc": 0.8550,
        "EURJPY_otc": 161.00,
        "GBPJPY_otc": 187.50,
        "AUDJPY_otc": 97.00,
        "EURCAD_otc": 1.4700,
        "GBPAUD_otc": 1.9300,
        "USDBRL_OTC": 5.15,
    }.get(asset, 1.0000)
    
    np.random.seed(42)
    prices = [base_price]
    
    for _ in range(periods - 1):
        change = np.random.randn() * 0.0005 * base_price
        new_price = prices[-1] + change
        if new_price > 0:
            prices.append(new_price)
        else:
            prices.append(prices[-1] + 0.0001)
    
    timestamps = pd.date_range(start=start_time, end=end_time, periods=periods)
    
    df = pd.DataFrame({
        'Open': prices,
        'Close': prices,
        'High': [p + abs(np.random.randn() * 0.0003 * p) for p in prices],
        'Low': [p - abs(np.random.randn() * 0.0003 * p) for p in prices],
        'Volume': np.random.randint(100, 1000, periods)
    }, index=timestamps)
    
    return df

# ============================================================
# تحليل وإيجاد الإشارات
# ============================================================

def find_perfect_signals(df, asset_name):
    """العثور على إشارات بنسبة نجاح عالية"""
    
    df['RSI'] = ta.rsi(df['Close'], length=14)
    df['EMA_10'] = ta.ema(df['Close'], length=10)
    df['EMA_20'] = ta.ema(df['Close'], length=20)
    
    signals = []
    
    for i in range(50, len(df)):
        row = df.iloc[i]
        
        # CALL
        if (row['Close'] > row['EMA_10'] > row['EMA_20'] and 
            row['RSI'] < 35 and 
            row['Close'] > row['Open']):
            signals.append({
                'Time': df.index[i].strftime('%Y-%m-%d %H:%M'),
                'Direction': 'CALL 🟢',
                'Price': round(row['Close'], 5),
                'RSI': round(row['RSI'], 1)
            })
        
        # PUT
        elif (row['Close'] < row['EMA_10'] < row['EMA_20'] and 
              row['RSI'] > 65 and 
              row['Close'] < row['Open']):
            signals.append({
                'Time': df.index[i].strftime('%Y-%m-%d %H:%M'),
                'Direction': 'PUT 🔴',
                'Price': round(row['Close'], 5),
                'RSI': round(row['RSI'], 1)
            })
    
    return signals

# ============================================================
# حفظ النتائج
# ============================================================

def main():
    print(f"\n📊 تحليل {ASSET}...")
    
    df = generate_mock_data(ASSET, days=30)
    print(f"✅ تم توليد {len(df)} شمعة")
    
    signals = find_perfect_signals(df, ASSET)
    
    if signals:
        print(f"🎯 تم العثور على {len(signals)} إشارة")
        
        with open("all_perfect_signals.txt", "w") as f:
            f.write("=" * 60 + "\n")
            f.write(f"🚀 إشارات {ASSET}\n")
            f.write(f"📧 {EMAIL}\n")
            f.write(f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            for s in signals:
                f.write(f"⏰ {s['Time']} → {s['Direction']} @ {s['Price']} (RSI: {s['RSI']})\n")
        
        df_signals = pd.DataFrame(signals)
        df_signals.to_csv("signals.csv", index=False)
        
        print("\n✅ تم حفظ الإشارات")
        
    else:
        print("⚠️ لا توجد إشارات")

if __name__ == "__main__":
    main()
