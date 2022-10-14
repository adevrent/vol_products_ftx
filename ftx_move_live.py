import pandas as pd
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import datetime
from scipy import stats
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar

# Construct DataFrame

df = pd.read_csv("/home/sscf/vol_products_ftx/user_data/Binance_BTCUSDT_d.csv")
df = df.drop(columns = ["unix", "symbol", "Volume BTC", "tradecount", "high", "low", "Volume USDT"])
df["date"] = pd.to_datetime(df["date"])
df["MOVE"] = np.absolute(df["close"] - df["open"])  # Calculate abs value of close - open
df["MOVE_perc"] = df["MOVE"] / df["open"]  # Calculate the percent value also.
df["perc_change"] = (df["close"] - df["open"]) / df["open"]
df["10dvol"] = df["perc_change"].rolling(10).std()  # Calculate rolling 10 day vol.
df["10dvol"] = df["10dvol"].shift(periods = 1)  # Take previous day's vol.
df["10dvol"] = df["10dvol"].fillna(0)  # Replace NaN values with 0.

# Holidays

cal = calendar()
holidays = cal.holidays(start = df["date"].min(),
                        end = df["date"].max())

# Economic news release dates since 01.01.2021

man_pmi = ["2022-10-03", "2022-09-01", "2022-08-01", "2022-07-01", "2022-06-01", "2022-05-02", "2022-04-01", "2022-03-01", "2022-02-01", "2022-01-04", "2021-12-01", "2021-11-01",
           "2021-10-01", "2021-09-01", "2021-08-02", "2021-07-01", "2021-06-01", "2021-05-03", "2021-04-01", "2021-03-01", "2021-02-01", "2021-01-05"]
employment = ["2022-10-07", "2022-09-02", "2022-08-05", "2022-08-05", "2022-07-08", "2022-06-03", "2022-05-06", "2022-04-01", "2022-03-04", "2022-02-04", "2022-01-07",
              "2021-12-03" , "2021-11-05" , "2021-10-08" , "2021-09-03" , "2021-08-06" , "2021-07-02" , "2021-06-04" , "2021-05-07" , "2021-04-02" , "2021-03-05" , "2021-02-05",
              "2021-01-08"]
gdp = ["2022-07-28", "2022-04-28", "2022-01-27", "2021-10-28", "2021-07-29", "2021-04-29", "2021-01-28"]
cpi = ["2022-09-13", "2022-08-10", "2022-07-13", "2022-06-10", "2022-05-11", "2022-04-12", "2022-03-10", "2022-02-10", "2022-01-12", "2021-12-10", "2021-11-10", "2021-10-13",
       "2021-09-14", "2021-08-11", "2021-07-13", "2021-06-10", "2021-05-12", "2021-04-13", "2021-03-10", "2021-02-10", "2021-01-13"]
pce = ["2022-09-30", "2022-08-26", "2022-07-29",
       "2022-06-30", "2022-05-27", "2022-04-29", "2022-03-31", "2022-02-25", "2022-01-28", "2021-12-23", "2021-11-24", "2021-10-29", "2021-10-01", "2021-08-27", "2021-07-30",
       "2021-06-25", "2021-05-28", "2021-04-30", "2021-03-26", "2021-02-26", "2021-01-29"]
fomc = ["2022-09-21", "2022-07-27", "2022-06-15", "2022-05-04", "2022-03-16", "2022-01-26", "2021-12-15", "2021-11-03", "2021-09-22", "2021-07-28", "2021-06-16", "2021-04-28",
        "2021-03-17", "2021-01-27"]

# Aggregated lists:

inflation = list(set(cpi + pce))
prio1 = list(set(inflation + fomc + gdp))
prio2 = list(set(man_pmi + employment))
release_day = list(set(prio1 + prio2))
none_day = list(set(df["date"]) - set(prio1 + prio2))
all_days = list(set(df["date"]))

######################################################################################################
######################################################################################################
#INPUTS

strike_price = 19395
list_name = holidays

######################################################################################################
######################################################################################################

sliced_df = pd.DataFrame(df["MOVE_perc"].loc[df["date"].isin(list_name)])

sliced_df["0_1"] = np.array((sliced_df["MOVE_perc"] >= 0.00) & (sliced_df["MOVE_perc"] < 0.01))
sliced_df["1_2"] = np.array((sliced_df["MOVE_perc"] >= 0.01) & (sliced_df["MOVE_perc"] < 0.02))
sliced_df["2_3"] = np.array((sliced_df["MOVE_perc"] >= 0.02) & (sliced_df["MOVE_perc"] < 0.03))
sliced_df["3_4"] = np.array((sliced_df["MOVE_perc"] >= 0.03) & (sliced_df["MOVE_perc"] < 0.04))
sliced_df["4_5"] = np.array((sliced_df["MOVE_perc"] >= 0.04) & (sliced_df["MOVE_perc"] < 0.05))
sliced_df["5_6"] = np.array((sliced_df["MOVE_perc"] >= 0.05) & (sliced_df["MOVE_perc"] < 0.06))
sliced_df["6_7"] = np.array((sliced_df["MOVE_perc"] >= 0.06) & (sliced_df["MOVE_perc"] < 0.07))
sliced_df["7_8"] = np.array((sliced_df["MOVE_perc"] >= 0.07) & (sliced_df["MOVE_perc"] < 0.08))
sliced_df["8_9"] = np.array((sliced_df["MOVE_perc"] >= 0.08) & (sliced_df["MOVE_perc"] < 0.09))
sliced_df["9_10"] = np.array((sliced_df["MOVE_perc"] >= 0.09) & (sliced_df["MOVE_perc"] < 0.10))
sliced_df["10_11"] = np.array((sliced_df["MOVE_perc"] >= 0.10) & (sliced_df["MOVE_perc"] < 0.11))
sliced_df["11_12"] = np.array((sliced_df["MOVE_perc"] >= 0.11) & (sliced_df["MOVE_perc"] < 0.12))
sliced_df["12_13"] = np.array((sliced_df["MOVE_perc"] >= 0.12) & (sliced_df["MOVE_perc"] < 0.13))
sliced_df["13_14"] = np.array((sliced_df["MOVE_perc"] >= 0.13) & (sliced_df["MOVE_perc"] < 0.14))
sliced_df["14_15"] = np.array((sliced_df["MOVE_perc"] >= 0.14) & (sliced_df["MOVE_perc"] < 0.15))
sliced_df["15_16"] = np.array((sliced_df["MOVE_perc"] >= 0.15) & (sliced_df["MOVE_perc"] < 0.16))
sliced_df["16_17"] = np.array((sliced_df["MOVE_perc"] >= 0.16) & (sliced_df["MOVE_perc"] < 0.17))
sliced_df["17_18"] = np.array((sliced_df["MOVE_perc"] >= 0.17) & (sliced_df["MOVE_perc"] < 0.18))
sliced_df["18_19"] = np.array((sliced_df["MOVE_perc"] >= 0.18) & (sliced_df["MOVE_perc"] < 0.19))
sliced_df["19_20"] = np.array((sliced_df["MOVE_perc"] >= 0.19) & (sliced_df["MOVE_perc"] < 0.20))


sliced_df_0_1 = sliced_df["MOVE_perc"].loc[sliced_df["0_1"] == True]
sliced_df_1_2 = sliced_df["MOVE_perc"].loc[sliced_df["1_2"] == True]
sliced_df_2_3 = sliced_df["MOVE_perc"].loc[sliced_df["2_3"] == True]
sliced_df_3_4 = sliced_df["MOVE_perc"].loc[sliced_df["3_4"] == True]
sliced_df_4_5 = sliced_df["MOVE_perc"].loc[sliced_df["4_5"] == True]
sliced_df_5_6 = sliced_df["MOVE_perc"].loc[sliced_df["5_6"] == True]
sliced_df_6_7 = sliced_df["MOVE_perc"].loc[sliced_df["6_7"] == True]
sliced_df_7_8 = sliced_df["MOVE_perc"].loc[sliced_df["7_8"] == True]
sliced_df_8_9 = sliced_df["MOVE_perc"].loc[sliced_df["8_9"] == True]
sliced_df_9_10 = sliced_df["MOVE_perc"].loc[sliced_df["9_10"] == True]
sliced_df_10_11 = sliced_df["MOVE_perc"].loc[sliced_df["10_11"] == True]
sliced_df_11_12 = sliced_df["MOVE_perc"].loc[sliced_df["11_12"] == True]
sliced_df_12_13 = sliced_df["MOVE_perc"].loc[sliced_df["12_13"] == True]
sliced_df_13_14 = sliced_df["MOVE_perc"].loc[sliced_df["13_14"] == True]
sliced_df_14_15 = sliced_df["MOVE_perc"].loc[sliced_df["14_15"] == True]
sliced_df_15_16 = sliced_df["MOVE_perc"].loc[sliced_df["15_16"] == True]
sliced_df_16_17 = sliced_df["MOVE_perc"].loc[sliced_df["16_17"] == True]
sliced_df_17_18 = sliced_df["MOVE_perc"].loc[sliced_df["17_18"] == True]
sliced_df_18_19 = sliced_df["MOVE_perc"].loc[sliced_df["18_19"] == True]
sliced_df_19_20 = sliced_df["MOVE_perc"].loc[sliced_df["19_20"] == True]

len_total = (len(sliced_df_0_1) + len(sliced_df_1_2) + len(sliced_df_2_3) + len(sliced_df_3_4) + len(sliced_df_4_5) + len(sliced_df_5_6)+
             len(sliced_df_6_7) + len(sliced_df_7_8) + len(sliced_df_8_9) + len(sliced_df_9_10) + len(sliced_df_10_11) + len(sliced_df_11_12)+
             len(sliced_df_12_13) + len(sliced_df_13_14) + len(sliced_df_14_15) + len(sliced_df_15_16) + len(sliced_df_16_17) + len(sliced_df_17_18)+
             len(sliced_df_18_19) + len(sliced_df_19_20))

len_array =  np.array((len(sliced_df_0_1), len(sliced_df_1_2), len(sliced_df_2_3), len(sliced_df_3_4), len(sliced_df_4_5), len(sliced_df_5_6),
             len(sliced_df_6_7), len(sliced_df_7_8) + len(sliced_df_8_9), len(sliced_df_9_10), len(sliced_df_10_11), len(sliced_df_11_12),
             len(sliced_df_12_13), len(sliced_df_13_14), len(sliced_df_14_15), len(sliced_df_15_16), len(sliced_df_16_17), len(sliced_df_17_18),
             len(sliced_df_18_19), len(sliced_df_19_20)))

p_array = (len_array / len_total).round(4)

print("Probability of greater than 0% move: ",
      str(sum(p_array[0:20]* 100).round(2))+ "% ", 
      "(between ",
      str(round(strike_price * 0)),"$ and ",str(round(strike_price * 0.01)),"$)")
print("Probability of greater than 1% move: ",
      str(sum(p_array[1:20]* 100).round(2))+ "% ", 
      "(between ",
      str(round(strike_price * 0.01)),"$ and ",str(round(strike_price * 0.02)),"$)")
print("Probability of greater than 2% move: ",
      str(sum(p_array[2:20]* 100).round(2))+ "% ", 
      "(between ",
      str(round(strike_price * 0.02)),"$ and ",str(round(strike_price * 0.03)),"$)")
print("Probability of greater than 3% move: ",
      str(sum(p_array[3:20]* 100).round(2))+ "% ", 
      "(between ",
      str(round(strike_price * 0.03)),"$ and ",str(round(strike_price * 0.04)),"$)")
print("Probability of greater than 4% move: ",
      str(sum(p_array[4:20]* 100).round(2))+ "% ", 
      "(between ",
      str(round(strike_price * 0.04)),"$ and ",str(round(strike_price * 0.05)),"$)")
print("Probability of greater than 5% move: ",
      str(sum(p_array[5:20]* 100).round(2))+ "% ", 
      "(between ",
      str(round(strike_price * 0.05)),"$ and ",str(round(strike_price * 0.06)),"$)")
print("Probability of greater than 6% move: ",
      str(sum(p_array[6:20]* 100).round(2))+ "% ", 
      "(between ",
      str(round(strike_price * 0.06)),"$ and ",str(round(strike_price * 0.07)),"$)")
print("Probability of greater than 7% move: ",
      str(sum(p_array[7:20]* 100).round(2))+ "% ", 
      "(between ",
      str(round(strike_price * 0.07)),"$ and ",str(round(strike_price * 0.08)),"$)")
print("Probability of greater than 8% move: ",
      str(sum(p_array[8:20]* 100).round(2))+ "% ", 
      "(between ",
      str(round(strike_price * 0.08)),"$ and ",str(round(strike_price * 0.09)),"$)")
print("Probability of greater than 9% move: ",
      str(sum(p_array[9:20]* 100).round(2))+ "% ", 
      "(between ",
      str(round(strike_price * 0.09)),"$ and ",str(round(strike_price * 0.10)),"$)")
print("Probability of greater than 10% move: ",
      str(sum(p_array[10:20]* 100).round(2))+ "% ", 
      "(between ",
      str(round(strike_price * 0.10)),"$ and ",str(round(strike_price * 0.11)),"$)")
print("Probability of greater than 11% move: ",
      str(sum(p_array[11:20]* 100).round(2))+ "% ", 
      "(between ",
      str(round(strike_price * 0.11)),"$ and ",str(round(strike_price * 0.12)),"$)")
print("Probability of greater than 12% move: ",
      str(sum(p_array[12:20]* 100))+ "% ", 
      "(between ",
      str(round(strike_price * 0.12)),"$ and ",str(round(strike_price * 0.13)),"$)")
print("Probability of greater than 13% move: ",
      str(sum(p_array[13:20]* 100))+ "% ", 
      "(between ",
      str(round(strike_price * 0.13)),"$ and ",str(round(strike_price * 0.14)),"$)")
print("Probability of greater than 14% move: ",
      str(sum(p_array[14:20]* 100))+ "% ", 
      "(between ",
      str(round(strike_price * 0.14)),"$ and ",str(round(strike_price * 0.15)),"$)")
print("Probability of greater than 15% move: ",
      str(sum(p_array[15:20]* 100))+ "% ", 
      "(between ",
      str(round(strike_price * 0.15)),"$ and ",str(round(strike_price * 0.16)),"$)")
print("Probability of greater than 16% move: ",
      str(sum(p_array[16:20]* 100))+ "% ", 
      "(between ",
      str(round(strike_price * 0.16)),"$ and ",str(round(strike_price * 0.17)),"$)")
print("Probability of greater than 17% move: ",
      str(sum(p_array[17:20]* 100))+ "% ", 
      "(between ",
      str(round(strike_price * 0.17)),"$ and ",str(round(strike_price * 0.18)),"$)")
print("Probability of greater than 18% move: ",
      str(sum(p_array[18:20]* 100))+ "% ", 
      "(between ",
      str(round(strike_price * 0.18)),"$ and ",str(round(strike_price * 0.19)),"$)")
print("Probability of greater than 19% move: ",
      str(sum(p_array[19:20]* 100))+ "% ", 
      "(between ",
      str(round(strike_price * 0.19)),"$ and ",str(round(strike_price * 0.20)),"$)")