import MetaTrader5 as mt5

def execute_trade(signal, price, probability):
    if probability < 80:
        print(f"[!] Trade Ignored: Probability {probability}% is too low for Prop Firm Safety.")
        return False

    if not mt5.initialize():
        print("[-] MT5 Initialization Failed")
        return False

    symbol = "XAUUSD" # Sesuaikan dengan simbol di MT5 Anda (Gold)
    lot = 0.1 # Sesuaikan dengan Risk Management Anda
    
    # Tentukan Tipe Order
    order_type = mt5.ORDER_TYPE_BUY if signal == "BUY" else mt5.ORDER_TYPE_SELL
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": mt5.symbol_info_tick(symbol).ask if signal == "BUY" else mt5.symbol_info_tick(symbol).bid,
        "magic": 123456,
        "comment": "NS-X Sentinel Execution",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"[-] Order Failed: {result.comment}")
    else:
        print(f"[SUCCESS] Order {signal} Executed at {price}")
    
    mt5.shutdown()
