import requests, time

def volume_explosion():
    print("Base — Volume Explosion Detector (1000%+ spike in <60 sec)")
    # pairAddress → (timestamp, volume_24h)
    history = {}

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/pairs/base", timeout=10)
            now = time.time()

            for pair in r.json().get("pairs", []):
                addr = pair["pairAddress"]
                vol24 = pair.get("volume", {}).get("h24", 0) or 0

                if addr not in history:
                    history[addr] = (now, vol24)
                    continue

                last_time, last_vol = history[addr]

                # Only check pairs younger than 10 min and with previous data
                age = now - pair.get("pairCreatedAt", 0) / 1000
                if age > 600:  # older than 10 min → ignore
                    continue

                time_diff = now - last_time
                if time_diff < 60 and last_vol > 5000:  # had real volume before
                    multiplier = vol24 / last_vol if last_vol > 0 else 999
                    if multiplier >= 10:  # 1000%+ in under 60 sec
                        token = pair["baseToken"]["symbol"]
                        print(f"VOLUME EXPLOSION ×{multiplier:.1f}\n"
                              f"{token} just went nuclear\n"
                              f"Volume 24h: ${vol24:,.0f} (was ${last_vol:,.0f})\n"
                              f"Age: {age:.0f}s | Price: ${float(pair['priceUsd'] or 0):.10f}\n"
                              f"https://dexscreener.com/base/{addr}\n"
                              f"→ This is the exact moment the rocket lights\n"
                              f"→ You are literally watching ignition\n"
                              f"{'FIRE'*25}")

                history[addr] = (now, vol24)

            time.sleep(3.8)
        except:
            time.sleep(3)

if __name__ == "__main__":
    volume_explosion()
