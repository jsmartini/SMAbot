import alpaca_trade_api as alpaca
from time import sleep
from datetime import timezone as tz

key_id = ""
sec_key = ""

def SMA(api, sym, period_type="1D"):
        #using closing price
        barset = api.get_barset(sym, timeframe=period_type).df
        sum = 0
        i = 0
        for closing_price in barset[sym].close:
            sum += closing_price
            i += 1
        return sum/i

def SMAbot(symbol, SMAweight):

    api = alpaca.REST(key_id, sec_key)

    while True:
        shortSMA = SMA(api, symbol, period_type="15Min")
        longSMA = SMAweight*SMA(api,symbol, period_type="1D")

        if not api.get_clock().is_open:
            clock = api.get_clock()
            toOpen = int(clock.next_open.replace(tzinfo=tz.utc).timestamp()-clock.timestamp.replace(tzinfo=tz.utc).timestamp())
            D = toOpen/3600/24
            H = (D - int(D)) * 24
            M = (H - int(H)) * 60
            print("Market Opening in: {0} D {1} H {2} M".format(int(D), int(H), int(M)))
            sleep(toOpen/60)

        elif shortSMA > longSMA:
            api.submit_order(
                symbol=symbol,
                side = "sell",
                type="market",
                qty=100,
                time_in_force="ioc"
            )
            print("100 {0} SOLD: Weighted SMA Change:{1}".format(symbol, shortSMA-longSMA))

        elif shortSMA < longSMA:
            api.submit_order(
                symbol=symbol,
                side = "buy",
                type="market",
                qty=100,
                time_in_force="ioc"
            )
            print("100 {0} Bought: Weighted SMA Change:{1}".format(symbol, shortSMA-longSMA))

    sleep(60*30) #sleeps 30 minutes
if __name__ == "__main__":
    SMAbot("VBIV", 1.03)
