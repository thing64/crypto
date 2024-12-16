import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas_ta as ta
import time
import os
import math
from my_kraken_api_functions import BUY_req, SELL_req, check_asset_status, check_balance
from collections import deque
from cmath import pi
from datetime import datetime



really_buy = True # Set this to True or False based on your criteria for buying







data = check_balance()

# Get the name of the currently running file
file_name69 = os.path.basename(__file__)

# Extract ZUSD and SOL values
usd_balance = float(data['result'].get('ZUSD', '0'))
PEPE_holding = float(data['result'].get('SOL', '0'))

# Determine the full path to the REAL_MONEY_COIN_WALLET.json file
wallet_file_path = os.path.join(os.path.dirname(__file__), 'REAL_MONEY_COIN_WALLET.json')      
# Now you can open the file
with open(wallet_file_path, 'r') as wallet_file:
    wallet_data = json.load(wallet_file)

    
wallet_data['walletBTC']['USD'] = usd_balance
wallet_data['walletBTC']['BTC'] = PEPE_holding

wallet_file_path = os.path.join(os.path.dirname(__file__), 'REAL_MONEY_COIN_WALLET.json')

with open(wallet_file_path, 'w') as wallet_file:
    json.dump(wallet_data, wallet_file, indent=4)



source = 'dataBTC.json'
# source = 'dataSOL.json'
# Determine the full path to the data.json file
data_file_path = os.path.join(os.path.dirname(__file__), source)

# use all data
with open(data_file_path, 'r') as file:
    # Read all lines from the file
    lines = file.readlines()
    # Count the number of lines
    maximun = len(lines)
x_value = maximun


def wallet_update():
    # Determine the full path to the wallet.json file
    wallet_file_path = os.path.join(os.path.dirname(__file__), 'REAL_MONEY_COIN_WALLET.json')
    
    # Get the absolute path of the currently executing script
    current_file_path = os.path.abspath(__file__)
    
    # Extract the file name from the path
    file_name = os.path.basename(current_file_path)
    
    # Now you can open the file
    with open(wallet_file_path, 'r') as wallet_file:
        wallet_data = json.load(wallet_file)
    
    usd_balance = float(wallet_data['walletBTC']['USD'])
    btc_balance = float(wallet_data['walletBTC']['BTC'])
    
    # print("An error: USD Balance:", usd_balance)
    # print("An error: BTC Balance:", btc_balance)
    
    
    status = check_asset_status()
    
    "holding_asset or not_holding"
    
    is_holding_usd = status == "not_holding"
    is_holding_PEPE = status == "holding_asset"
    # print("An error: PEPE_holding first")
    PEPE_holding = btc_balance
    
    return usd_balance,btc_balance,is_holding_usd,is_holding_PEPE,PEPE_holding,file_name

plt.style.use("dark_background")
def williams_alligator(high, low, close, jaw_length=13, teeth_length=8, lips_length=5):
    # Calculate the three SMAs
    jaw = pd.Series(high.rolling(window=jaw_length).mean(), name='Jaw')
    teeth = pd.Series(high.rolling(window=teeth_length).mean(), name='Teeth')
    lips = pd.Series(high.rolling(window=lips_length).mean(), name='Lips')
    return jaw, teeth, lips
def main():
    def update_data(frame):
  
        # Define the file path
        file_path = source
        
        # Initialize lists to store data
        timestamps = deque(maxlen=x_value)
        high_prices = deque(maxlen=x_value)
        low_prices = deque(maxlen=x_value)
        closing_prices = deque(maxlen=x_value)
        volumes = deque(maxlen=x_value)

        # Clear lists
        timestamps.clear()
        closing_prices.clear()
        high_prices.clear()
        low_prices.clear()
        volumes.clear()
        
        # Read JSON data from the file
        with open(file_path, "r") as file:
            for line in file:
                try:
                    # Parse JSON data
                    data = json.loads(line)
                    
                    # Extract relevant information
                    k_data = data["data"]["k"]
                    timestamp = pd.to_datetime(k_data["t"], unit="ms")
                    # time_str = timestamp.strftime("%H:%M:%S")  # Format time as HH:MM:SS
                    time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")  # Format time as YYYY-MM-DD HH:MM:SS
                    close_price = float(k_data["c"])
                    high_price = float(k_data["h"])
                    low_price = float(k_data["l"])
                    volume = float(k_data["v"])
                    
                    # Append to lists
                    timestamps.append(time_str)
                    closing_prices.append(close_price)
                    high_prices.append(high_price)
                    low_prices.append(low_price)
                    volumes.append(volume)
                except json.JSONDecodeError as e:
                    # print("An error: Error decoding JSON:", e)
                    # print("An error: Retrying after 2 seconds...")
                    time.sleep(2)  # Add a delay before retrying
                except KeyError as e:
                    # print("An error: Key not found:", e)
                    hello = 0
            
        # Create DataFrame
        df = pd.DataFrame({
            "Timestamp": timestamps,
            "High": high_prices,
            "Low": low_prices,
            "Close": closing_prices,
            "Volume": volumes
        })
        check = []
        # Calculate EMA
        ema = ta.ema(df["Close"], length=200)
        ema_9 = ta.ema(df["Close"], length=9)
        ema_x = ta.ema(df["Close"], length=600)
        check.append(ema)
        check.append(ema_9)
        check.append(ema_x)

        # Calculate MACD
        macd = ta.macd(df["Close"], fast=3, slow=10, signal=9)
        check.append(macd)
        macd_sma = None
        if macd is not None:
            # Step 2: Calculate the SMA of the MACD line
            macd_sma = ta.ema(macd['MACD_3_10_9'], length=100)  # Adjust length as needed
            check.append(macd_sma)
        
        # Calculate Bollinger Bands
        bollinger_bands = ta.bbands(df['Close'], length=20)
        check.append(bollinger_bands)
        
        # Calculate Acceleration Oscillator (AO)
        # ao = ta.ao(df['High'], df['Low']) 
        # Calculate Acceleration Oscillator (AC)
        ao = ta.ao(df["High"], df["Low"], s=5, len=34)  # You can adjust the smoothing and length parameters

        check.append(ao)
        
        # Calculate Stochastic Oscillator
        stoch = ta.stoch(high=df["High"], low=df["Low"], close=df["Close"], length=14, smooth_k=1, smooth_d=3)
        check.append(stoch)
        # print(stoch)
        
        # # Calculate Supertrends with different parameters
        # su3 = ta.supertrend(df['High'], df['Low'], df['Close'], length=11, multiplier=2)
        # check.append(su3)
        
        # Calculate Williams Alligator indicator
        jaw, teeth, lips = williams_alligator(df['High'], df['Low'], df['Close'])
        check.append(jaw)
        check.append(teeth)
        check.append(lips)
        
        # Calculate ATR
        atr = ta.atr(df['High'], df['Low'], df['Close'], length=14)  # You can adjust the length as needed
        check.append(atr)
        
        # Calculate RSI
        rsi = ta.rsi(df['Close'])    
        check.append(rsi)
        sma_rsi = ta.sma(rsi, length=14)
        if not any(item is None for item in check):
            upper_band = bollinger_bands['BBU_20_2.0']
            lower_band = bollinger_bands['BBL_20_2.0']
            middle_band = bollinger_bands['BBM_20_2.0']
            df['MACD_3_10_9'] = macd['MACD_3_10_9']
            df['MACDs_3_10_9'] = macd['MACDs_3_10_9']
            # df['SUPERT_11_2.0'] = su3['SUPERT_11_2.0']
            df['EMA'] = ema
            df['EMA_09'] = ema_9
            df['EMA_X'] = ema_x
            df['RSI'] = rsi
            df['JAW'] = jaw
            df['TEETH'] = teeth
            df['LIPS'] = lips
            df['SMA_RSI'] = sma_rsi
            df['Upper Band'] = upper_band
            df['Lower Band'] = lower_band
            df['Middle Band'] = middle_band
            df['AO'] = ao
            df['STOCHk_14_3_1'] = stoch['STOCHk_14_3_1']
            df['STOCHd_14_3_1'] = stoch['STOCHd_14_3_1']
            df['MACD_SMA'] = macd_sma
            # Step 1: Calculate ATR
            df['ATR'] = atr

            # Multiply ATR by a multiplier of 10
            multiplier = 3
            df['Adjusted_ATR'] = df['ATR'] * multiplier


            # Combine ATR and closing prices
            combined_data = df['Adjusted_ATR'] + df['Close']
            
            # Calculate the difference between combined_data and Close
            difference = combined_data - df['Close']
            
            difference2 = ta.ema(difference, length=60)
            
            difference = ta.ema(difference, length=10)
            
            
            # Initialize lists to store scatter plot points
            scatter_buy_and_sell = []
            
            scatter_x = []
            scatter_y = []
            counter = len(df['Close'])
            counter_temp = 0
            df_temp = df.copy()
            # for i in range(3, counter + 1):
            # Iterate over increasing number of rows
            for i in range(len(df_temp)):
                if counter_temp > 3:
                    latest_close = df_temp['Close'].iloc[i]
                    latest_rsi = df_temp['RSI'].iloc[i]
                    latest_macd = macd['MACD_3_10_9'].iloc[i]
                    latest_macds = macd['MACDs_3_10_9'].iloc[i]
                    latest_ema_100 = df_temp['EMA'].iloc[i]
                    latest_ema_x = df_temp['EMA_X'].iloc[i]
                    latest_ema_9 = df_temp['EMA_09'].iloc[i]
                    latest_sma_rsi = df_temp['SMA_RSI'].iloc[i]
                    latest_macd_sma = df_temp['MACD_SMA'].iloc[i]
                    # latest_super_11 = df['SUPERT_11_2.0'].iloc[-1]
                    latest_ao = df_temp['AO'].iloc[i]
                    
                    latest_upper_band = df_temp['Upper Band'].iloc[i]
                    latest_lower_band = df_temp['Lower Band'].iloc[i]
                    latest_middle_band = df_temp['Middle Band'].iloc[i]
                    latest_jaw = df_temp['JAW'].iloc[i]
                    latest_teeth = df_temp['TEETH'].iloc[i]
                    latest_lips = df_temp['LIPS'].iloc[i]
                    latest_atr = df_temp['ATR'].iloc[i]

                    
                    
                    second_latest_ema_100 = df_temp['EMA'].iloc[i-1]
                    second_latest_sma_rsi = df_temp['SMA_RSI'].iloc[i-1]
                    second_last_macd = df_temp['MACD_3_10_9'].iloc[i-1]
                    second_last_macds = df_temp['MACDs_3_10_9'].iloc[i-1]
                    second_latest_rsi = df_temp['RSI'].iloc[i-1]
                    second_latest_ema_9 = df_temp['EMA_09'].iloc[i-1]
                    second_latest_lower_band = df_temp['Lower Band'].iloc[i-1]
                    second_latest_upper_band = df_temp['Upper Band'].iloc[i-1]
                    second_latest_ao = df_temp['AO'].iloc[i-1]
                    second_latest_close = df_temp['Close'].iloc[i-1]
                    second_latest_middle_band = df_temp['Middle Band'].iloc[i-1]
                    second_latest_atr = df_temp['ATR'].iloc[i-1]
                    second_latest_ema_x = df_temp['EMA_X'].iloc[i-1]
                    
                    third_latest_ema_9 = df_temp['EMA_09'].iloc[i-2]
                    
                    rounded_down = (second_latest_rsi // 10) * 10 # rounded_down: last tens
                    rounded_up = ((second_latest_rsi + 9) // 10) * 10# Round up to the nearest tens

            
                    macd_slope = latest_macd - second_last_macd
                    macds_slope = latest_macds / second_last_macds
                    middle_slope = latest_middle_band-second_latest_middle_band
                    rsi_smi_slope = latest_sma_rsi - second_latest_sma_rsi
                    latest_ema_9_slope = latest_ema_9 - second_latest_ema_9
                    lower_band_slope = latest_lower_band - second_latest_lower_band
                    ema_100_slope = latest_ema_100 - second_latest_ema_100
                    ema_x_slope = latest_ema_x - second_latest_ema_x
                    upper_band_slope = latest_upper_band - second_latest_upper_band
                    ao_slope = latest_ao - second_latest_ao
                    second_latest_ema_9_slope = second_latest_ema_9 - third_latest_ema_9
                    close_slope = latest_close - second_latest_close
                    atr_slope = latest_atr - second_latest_atr
                    rsi_slope = latest_rsi - second_latest_rsi
                    
                    rsi_mean = df_temp['RSI'].mean()

                    #--use this (one currently using for buyer algo)
                    # if ema_100_slope > 0 and latest_jaw < latest_teeth < latest_lips and (latest_ao <1.98 and macd['MACDs_3_10_9'].iloc[i]>macd_sma.iloc[i] and latest_ao > 0 and latest_ema_9_slope > 0 and latest_rsi < rsi_mean+pi+4 and latest_rsi > latest_sma_rsi) and (second_latest_ao <1.98 and macd['MACDs_3_10_9'].iloc[i-1]>macd_sma.iloc[i-1] and second_latest_ao > 0 and second_latest_ema_9_slope > 0 and second_latest_rsi < 70 and second_latest_rsi > second_latest_sma_rsi):
                    
                    #this is from graph_only_kraken__________=======
                    if latest_jaw < latest_teeth < latest_lips and (latest_ao <1.98 and macd['MACDs_3_10_9'].iloc[i]>macd_sma.iloc[i] and latest_ao > 0 and latest_ema_9_slope > 0 and latest_rsi < rsi_mean+pi+4 and latest_rsi > latest_sma_rsi) and (second_latest_ao <1.98 and macd['MACDs_3_10_9'].iloc[i-1]>macd_sma.iloc[i-1] and second_latest_ao > 0 and second_latest_ema_9_slope > 0 and second_latest_rsi < 70 and second_latest_rsi > second_latest_sma_rsi):
                    
                    #this is for 60min interval
                    # if ema_100_slope > 0 and latest_jaw < latest_teeth < latest_lips and (latest_ao <1.98 and macd['MACDs_3_10_9'].iloc[i]>macd_sma.iloc[i] and latest_ao > 0 and latest_ema_9_slope > 0 and latest_rsi < rsi_mean+pi+4 and latest_rsi > latest_sma_rsi) and (second_latest_ao <1.98 and macd['MACDs_3_10_9'].iloc[i-1]>macd_sma.iloc[i-1] and second_latest_ao > 0 and second_latest_ema_9_slope > 0 and second_latest_rsi < 70 and second_latest_rsi > second_latest_sma_rsi):
                    
                        # print("***************BUY CONDITION MET***************")
                        # Append timestamp and closing price to the scatter plot lists
                        # signal = df_temp["Timestamp"].iloc[i].copy()
                        
                        
                        scatter_buy_and_sell.append({
                            'date': df_temp["Timestamp"].iloc[i],
                            'signal_type': 'buy',
                            "latest_close": latest_close})
                        
                        scatter_x.append(df_temp["Timestamp"].iloc[i])
                        scatter_y.append(latest_close)
                    # -------------------------------------------------------------
                
                counter_temp+=1
                
                
            # Initialize lists to store scatter plot points
            scatter_x_sell = []
            scatter_y_sell = []
            counter = len(df['Close'])
            counter_temp = 0
            df_temp = df.copy()
            
            for i in range(len(df_temp)):
                if counter_temp > 3:
                    latest_close = df_temp['Close'].iloc[i]
                    latest_rsi = df_temp['RSI'].iloc[i]
                    latest_macd = macd['MACD_3_10_9'].iloc[i]
                    latest_macds = macd['MACDs_3_10_9'].iloc[i]
                    latest_ema_100 = df_temp['EMA'].iloc[i]
                    latest_ema_9 = df_temp['EMA_09'].iloc[i]
                    latest_ema_x = df_temp['EMA_X'].iloc[i]
                    latest_sma_rsi = df_temp['SMA_RSI'].iloc[i]
                    latest_macd_sma = df_temp['MACD_SMA'].iloc[i]
                    # latest_super_11 = df_temp['SUPERT_11_2.0'].iloc[-1]
                    
                    latest_upper_band = df_temp['Upper Band'].iloc[i]
                    latest_lower_band = df_temp['Lower Band'].iloc[i]
                    latest_middle_band = df_temp['Middle Band'].iloc[i]

                    
                    
                    
                    second_latest_sma_rsi = df_temp['SMA_RSI'].iloc[i-1]
                    second_last_macd = df_temp['MACD_3_10_9'].iloc[i-1]
                    second_last_macds = df_temp['MACDs_3_10_9'].iloc[i-1]
                    second_latest_rsi = df_temp['RSI'].iloc[i-1]
                    second_latest_ema_9 = df_temp['EMA_09'].iloc[i-1]
                    second_latest_lower_band = df_temp['Lower Band'].iloc[i-1]
                    
                    second_latest_middle_band = df_temp['Middle Band'].iloc[i-1]
                    rounded_down = (second_latest_rsi // 10) * 10 # rounded_down: last tens
                    
            
            
                    macd_slope = latest_macd - second_last_macd
                    macds_slope = latest_macds / second_last_macds
                    middle_slope = latest_middle_band-second_latest_middle_band
                    rsi_smi_slope = latest_sma_rsi - second_latest_sma_rsi
                    rsi_slope = latest_rsi - second_latest_rsi
                    # SELL LOGICCCCC    Inside the update_data function
                    # if (latest_middle_band > latest_close and latest_ema_9 < latest_middle_band) or (second_latest_rsi > 70 and latest_rsi < rounded_down):
                    
                    ##this is the one to use_______=====
                    # if (second_latest_rsi > 70+math.pi and latest_rsi < rounded_down):   
                    
                    #from graph_only_kraken
                    # if (second_latest_rsi > 70+math.pi and latest_rsi < rounded_down) or latest_sma_rsi > 60 and rsi_smi_slope<0:
                    
                    #this is for 60 min interval
                    if second_latest_sma_rsi > 70-math.pi and latest_rsi < rounded_down:
                    
                    # if latest_rsi-second_latest_rsi < 0:
                    # if latest_macd < latest_macds:
                        # Append timestamp and closing price to the scatter plot lists
                        # signal = df_temp["Timestamp"].iloc[i]
                        for _ in range(2):
                            scatter_buy_and_sell.append({
                                'date': df_temp["Timestamp"].iloc[i],
                                'signal_type': 'sell',
                                "latest_close": latest_close
                            })
                            
                        
                        scatter_x_sell.append(df_temp["Timestamp"].iloc[i])
                        scatter_y_sell.append(latest_close)
            
                counter_temp+=1
                
            # print(scatter_buy_and_sell)


            latest_close = df['Close'].iloc[-2]
            latest_rsi = df['RSI'].iloc[-2]
            latest_macd = macd['MACD_3_10_9'].iloc[-2]
            latest_macds = macd['MACDs_3_10_9'].iloc[-2]
            latest_ema_100 = df['EMA'].iloc[-2]
            latest_ema_9 = df['EMA_09'].iloc[-2]
            latest_upper_band = df['Upper Band'].iloc[-2]
            latest_lower_band = df['Lower Band'].iloc[-2]
            latest_middle_band = df['Middle Band'].iloc[-2]
            latest_ao = df['AO'].iloc[-1]
            latest_stochk = df['STOCHk_14_3_1'].iloc[-1]
            latest_stochd = df['STOCHd_14_3_1'].iloc[-1]
            
            second_last_macd = df['MACD_3_10_9'].iloc[-3]
            second_last_macds = df['MACDs_3_10_9'].iloc[-3]
            second_latest_rsi = df['RSI'].iloc[-3]
            second_latest_ema_9 = df['EMA_09'].iloc[-3]
        
            macd_slope = latest_macd - second_last_macd
            macds_slope = latest_macds / second_last_macds
            

            # Get min and max values of Close column
            min_price = df['Close'].min()
            max_price = df['Close'].max()
            # Update the closing price plot
            ax1.clear()
            ax1.plot(df["Timestamp"], df["Close"], color="white", label="Closing Price:"+str(latest_close))
            ax1.plot(df["Timestamp"], df["EMA"], color="midnightblue", label="EMA (100)"+str(latest_ema_100))
            # ax1.plot(df["Timestamp"], df["EMA_09"], color="blue", label="EMA (9)"+str(latest_ema_9))
            ax1.plot(df["Timestamp"], df["EMA_X"], color="purple", label="EMA (X)"+str(latest_ema_x))
            
            
            ax1.scatter(scatter_x, scatter_y, color='green', marker='^', label='Buy Signal', s=200)
            # Plot the scatter plot points again to overlay them on the closing price plot
            ax1.scatter(scatter_x_sell, scatter_y_sell, color='red', marker='o', label='sell Signal', s=200)
            # ax1.plot(df['SUPERT_11_2.0'], label='Supertrend 11,2', alpha=1)  # Adjust alpha here


            ax1.set_ylim(min_price, max_price)


            
            # Plot combined data on ax1
            ax1.plot(combined_data, color='b', label='ATR/Close')
        
            cum = difference - difference2
            cum+=ao
            # Plot combined data on ax1
            ax1.plot(combined_data+cum, color='purple', label='(ATR/Close+cum')

            
            ax1.set_xlabel("Time")
            ax1.set_ylabel("Price (USD)")
            ax1.set_title(file_name69)
            ax1.legend()
            ax1.grid(True)
            ax1.tick_params(axis='x', rotation=45)
            ax1.xaxis.set_major_locator(plt.MaxNLocator(10))  # Set maximum number of ticks to 10

            # Update the EMA plot
            ax2.clear()
            ax2.plot(df["Timestamp"], df['RSI'], color="green", label="RSI"+str(latest_rsi))
            ax2.plot(df['SMA_RSI'], label='SMA_RSI')
            ax2.axhline(y=70, color='r', linestyle='--', label='Overbought (70)')
            ax2.axhline(y=30, color='g', linestyle='--', label='Oversold (30)')
            ax2.set_xlabel("Time")
            ax2.set_ylabel("RSI")
            ax2.legend()
            ax2.grid(True)
            ax2.tick_params(axis='x', rotation=45)
            ax2.xaxis.set_major_locator(plt.MaxNLocator(10)) 


            # Update the EMA plot
            ax3.clear()
            ax3.plot(df.index, df['AO'], color='blue', label='Acceleration Oscillator (AO)')
            # Create a bar chart for AO with green bars for positive values and red bars for negative values
            ax3.bar(df.index, ao, color=['green' if ao_val > 0 else 'red' for ao_val in ao])

            # # plt.bar(df.index, ao, color='blue', alpha=0.5)
            ax3.axhline(y=0, color='r', linestyle='--', label='0Line')

            
            ax3.set_xlabel("Time")
            ax3.set_ylabel("RSI")
            ax3.legend()
            ax3.grid(True)
            ax3.tick_params(axis='x', rotation=45)
            ax3.xaxis.set_major_locator(plt.MaxNLocator(10))  # Set maximum number of ticks to 10

            # Update the EMA plot
            ax4.clear()
            ax4.plot(df['ATR'], label='ATR')
            ax4.set_xlabel("Time")
            ax4.set_ylabel("ATR")
            ax4.legend()
            ax4.grid(True)
            ax4.tick_params(axis='x', rotation=45)
            ax4.xaxis.set_major_locator(plt.MaxNLocator(10))  # Set maximum number of ticks to 10
        
            # Update the EMA plot
            ax5.clear()
            # Plot difference on ax4
            cum = difference - difference2
            cum+=ao
            ax5.bar(df.index, cum, color=['green' if cum_val > 0 else 'red' for cum_val in cum])

            
            ax5.set_ylabel('Difference')
            ax5.tick_params('y', colors='r')
            ax5.xaxis.set_major_locator(plt.MaxNLocator(10))  # Set maximum number of ticks to 10
        
            
            usd_balance,btc_balance,is_holding_usd,is_holding_PEPE,PEPE_holding,file_name = wallet_update()
            
            
            # Ensure both lists have at least one element before accessing their last items
            if scatter_buy_and_sell:  # Checks if both lists are non-empty      
                # print("ouefvas")
                scatter_buy_and_sell.sort(key=lambda x: x['date'])
                # print(scatter_buy_and_sell)
                if scatter_buy_and_sell[-1]['signal_type'] == 'buy':
                    # print("buy")
                    if usd_balance > 0 and is_holding_usd:
                        btc_to_buy = usd_balance / latest_close
                        # print("An error: PEPE_holding BUYING")
                        PEPE_holding += btc_to_buy
                        usd_balance -= btc_to_buy * latest_close  # Update USD balance
                        is_holding_usd = False
                        is_holding_PEPE = True
                        usd_balance = 0
                        if really_buy:
                            BUY_req()
                            print("***************BUY CONDITION MET***************")
                            
                            print("scatter_buy_and_sell:", scatter_buy_and_sell)
                        print(f"Bought {btc_to_buy} BTC at ${latest_close} per BTC", file_name)
                    
                elif scatter_buy_and_sell[-1]['signal_type'] == 'sell':
                    # print("sell")
                    if PEPE_holding > 0 and is_holding_PEPE:
                        usd_to_receive = PEPE_holding * latest_close
                        usd_balance += usd_to_receive
                        is_holding_usd = True
                        is_holding_PEPE = False
                        print(f"Sold {PEPE_holding} BTC at ${latest_close} per BTC. Received ${usd_to_receive} USD", file_name)
                        if really_buy:
                            SELL_req()
                            print("***************SELL CONDITION MET***************")
                        
                            print("scatter_buy_and_sell:", scatter_buy_and_sell)
                        # print("An error: PEPE_holding SELLING")
                        PEPE_holding = 0
                        
            else:
                # print("One or both lists are empty.")
                # Handle the empty list case here as needed
                pass

          
            # Determine the full path to the REAL_MONEY_COIN_WALLET.json file
            wallet_file_path = os.path.join(os.path.dirname(__file__), 'REAL_MONEY_COIN_WALLET.json')      
            # Now you can open the file
            with open(wallet_file_path, 'r') as wallet_file:
                wallet_data = json.load(wallet_file)

                
            wallet_data['walletBTC']['USD'] = usd_balance
            wallet_data['walletBTC']['BTC'] = PEPE_holding
            
            wallet_file_path = os.path.join(os.path.dirname(__file__), 'REAL_MONEY_COIN_WALLET.json')
            
            with open(wallet_file_path, 'w') as wallet_file:
                json.dump(wallet_data, wallet_file, indent=4)
        
        else:
            # print("An error: Calculation failed or returned None. Restarting update_data...")
            time.sleep(2)  # Add a delay before restarting
            update_data(frame)  # Restart the update_data function

    try:
        # Set up the figure and subplots
        fig, (ax1, ax2, ax3,ax4,ax5) = plt.subplots(5, 1, figsize=(11, 8), sharex=True)

        # Set up the animation
        refresh_interval = 3000  # milliseconds (3 seconds)
        ani = animation.FuncAnimation(fig, update_data, interval=refresh_interval)  # Update every 3 seconds

        # Display the plot
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e} Restarting...")
        time.sleep(2)  # Add a delay before Restarting

        main()  # Restart the main function

if __name__ == "__main__":
    main()
