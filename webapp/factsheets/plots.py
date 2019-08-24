import numpy as np
import pandas as pd
import plotly.graph_objects as go
from factsheets import dataio



def plot_returns(fund_name):
    # read data and format
    fund = dataio.read_fund('fund_name')
    returns = fund.get('returns', None)
    df_returns = pd.DataFrame(returns)
    df_returns['month_year'] = df_returns.apply(lambda row: str(row.month) + '/' + str(row.year)[2:], axis=1)
    df_returns.sort_values(by=['year', 'month'], ascending=[True, True], inplace=True)
    df_returns['return'] = df_returns['return'].astype(float)

    # calculate geometric return
    geo_returns = []
    returns = df_returns['return'].tolist()
    for i, ret in enumerate(returns):
        returns_ = returns[0:i+1]
        returns_ = [(e / 100.) + 1 for e in returns_]
        geo_return = np.product(returns_)
        geo_returns.append(geo_return)
    geo_returns = ['$%s' % '%0.2f' % e for e in geo_returns]
    df_returns['geo_return'] = geo_returns

    # plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_returns['month_year'],
        y=df_returns['geo_return']))

    fig.update_layout(
        title=go.layout.Title(
            text="Investment Growth"
        ),
        width=900
    )

    fig.update_xaxes(nticks=5)
    dataio.create_returns_plot(fund_name)