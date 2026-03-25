import yfinance as yf
import pandas as pd
import os
import time
from datetime import datetime

def track_and_save():
    watchlist = {
        "^NSEI": "Nifty 50",
        "^BSESN": "Sensex",
        "BTC-USD": "Bitcoin",
        "RELIANCE.NS": "Reliance"
    }
    
    all_data = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n--- Market Update ({current_time}) ---")
    
    for symbol, name in watchlist.items():
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="1d")
            if not df.empty:
                current_price = df['Close'].iloc[-1]
                open_price = df['Open'].iloc[-1]
                change_pct = ((current_price - open_price) / open_price) * 100
                
                all_data.append({
                    'Time': current_time,
                    'Asset': name,
                    'Price': round(current_price, 2),
                    'Change_Pct': round(change_pct, 2)
                })
                print(f"✅ {name} fetched.")
        except Exception as e:
            print(f"❌ Error in {name}: {e}")

    if all_data:
        new_df = pd.DataFrame(all_data)
        file_name = 'market_history.csv'
        if not os.path.isfile(file_name):
            new_df.to_csv(file_name, index=False)
        else:
            new_df.to_csv(file_name, mode='a', index=False, header=False)
        print(f"💾 Data appended to {file_name}")

# --- LOOP SECTION ---
if __name__ == "__main__":
    print("🚀 Automation Started... Press Ctrl+C to stop (if in terminal).")
    while True:
        track_and_save()
        
        # Kitni der baad dubara check karna hai? 
        # 3600 seconds = 1 Ghanta
        print("Waiting for 1 hour...")
        time.sleep(3600)
