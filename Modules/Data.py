from Modules.Symbols import symbols as sb

import yfinance as yf




def get_key(value):
    
    key_wanted = None
    for key, values_in_dict in sb.items():
        if values_in_dict == value:
            key_wanted = key
            break

    if key_wanted is not None:
        return key_wanted

def temps_reel_data(symbols):
    
    for elem in symbols:
        
        print(f"\n{get_key(elem)} : 0000-00000-0000-000--00")