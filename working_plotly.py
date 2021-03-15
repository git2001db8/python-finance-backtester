import os
import pandas
import plotly.graph_objects as go
from plotly.subplots import make_subplots

specific = ['AMD']

for filename in os.listdir('python-finance/datasets/'):
    # print(filename)
    symbol = filename.split('.')[0]
    print(symbol)
    if symbol in specific:
        df = pandas.read_csv('python-finance/datasets/{}'.format(filename), parse_dates=True, index_col=0)

print(df)
df_ohlc = df['Adj Close'].resample('1W').ohlc()
df_volume = df['Volume'].resample('1W').sum()
df_resample = df_ohlc.join(df_volume)
df_resample.reset_index(level=0, inplace=True)
print(df_resample)


#fig = make_subplots(specs=[[{"secondary_y": True}]])
# fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.02)
# fig.add_trace(go.Candlestick(x=df_resample['Date'], open=df_resample['open'], high=df_resample['high'], low=df_resample['low'], close=df_resample['close']), row=1, col=1)
# fig.add_trace(go.Bar(x=df_resample['Date'], y=df_resample['Volume']), row=2, col=1)
# fig.update(layout_xaxis_rangeslider_visible=False)
# fig.layout.yaxis2.showgrid=False
# fig.show()

trace1 = go.Candlestick(x=df_resample['Date'], open=df_resample['open'], high=df_resample['high'], low=df_resample['low'], close=df_resample['close'])
trace2 = go.Bar(x=df_resample['Date'], y=df_resample['Volume'], yaxis="y2")
data = [trace1, trace2]
layout = go.Layout(
    yaxis2=dict(
        domain=[0, 0.2]
    ),
    legend=dict(
        traceorder="reversed"
    ),
    yaxis=dict(
        domain=[0.25, 1]
    )
)
fig = go.Figure(data=data, layout=layout)
fig.update(layout_xaxis_rangeslider_visible=False)
fig.show()