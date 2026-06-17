import os
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta
from quotexapi.stable_api import Quotex

# السحب والاتصال التلقائي ببيانات الحساب
EMAIL = os.getenv("QUOTEX_EMAIL", "maikhaled918273@gmail.com")
PASSWORD = os.getenv("QUOTEX_PASS", "010011012")
ASSET = os.getenv("ASSET", "USDBRL_OTC")

print(f"🚀 بدء السحب لزوج: {ASSET}")
client = Quotex(email=EMAIL, password=PASSWORD)
status, error = client.connect()

if not status:
    print(f"❌ خطأ اتصال: {error}")
    exit(1)

end_time = datetime.now()
start_time = end_time - timedelta(days=30)
candles = client.get_candles(ASSET, int(start_time.timestamp()), int(end_time.timestamp()), 60)

if not candles:
    print("❌ لا توجد بيانات")
    client.close()
    exit(1)

df = pd.DataFrame(candles)
df['time'] = pd.to_datetime(df['time'], unit='s')
df['time_egypt'] = df['time'] + pd.Timedelta(hours=3)
df['time_hm'] = df['time_egypt'].dt.strftime('%H:%M')
df.ta.zigzag(append=True)

perfect_signals = []
grouped = df.groupby('time_hm')

for time_hm, group in grouped:
    if len(group) < 4: continue
    total = 0
    c_w0, c_w1, p_w0, p_w1 = 0, 0, 0, 0
    
    for idx, row in group.iterrows():
        total += 1
        if row['close'] > row['open']: c_w0 += 1
        else:
            n = idx + 1
            if n in df.index and df.loc[n, 'close'] > df.loc[n, 'open']: c_w1 += 1
            
        if row['close'] < row['open']: p_w0 += 1
        else:
            n = idx + 1
            if n in df.index and df.loc[n, 'close'] < df.loc[n, 'open']: p_w1 += 1

    if ((c_w0 + c_w1) / total) * 100 == 100:
        perfect_signals.append(f"⏰ {time_hm}  →  🟢 CALL (تكرار {total} مرات)")
    elif ((p_w0 + p_w1) / total) * 100 == 100:
        perfect_signals.append(f"⏰ {time_hm}  →  🔴 PUT  (تكرار {total} مرات)")

with open("all_perfect_signals.txt", "w") as f:
    f.write(f"=== {ASSET} PERFECT SIGNALS (EGYPT TIME) ===\n\n")
    for sig in sorted(perfect_signals):
        f.write(f"{sig}\n")

print("✅ تم استخراج الملف بنجاح.")
client.close()
