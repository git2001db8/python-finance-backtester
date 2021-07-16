import os
import io
import pandas as pd

df_init = pd.read_csv('python-finance/trades/U6277264_20210713.tlg', sep='|', header=None, skiprows=5, engine='python', skipfooter=1)
df_drop = df_init.drop(columns=[0,1,3,4,5,9,11,13,15])
df_final = df_drop.rename(columns={2:'Symb', 6:'Code', 7:'Date', 8:'Time', 10:'Shares', 12:'Price', 14:'Comm'})
print(df_final)
#df_final.to_csv('Trade.csv')