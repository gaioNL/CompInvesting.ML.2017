import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df


def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()

def compute_daily_returns(df):
    """Compute and return the daily return values."""
    #daily_returns = df.copy()
    #daily_returns[1:] = (df[1:]/df[:-1].values) -1
    daily_returns = ( df/df.shift(1)) -1
    daily_returns.ix[0,:] = 0
    return daily_returns

    return (df[:-1].values / df[1:] - 1).fillna(0)



def test_run():

    #read data
    dates = pd.date_range('2009-01-01','2012-12-31')

    symbols = ['SPY','XOM']

    df = get_data(symbols,dates)

    plot(df)

    daily_returns = compute_daily_returns(df)
    plot_data(daily_returns,title = "daily_returns" ,ylabel = "daily_returns", xlabel = "dates")    

    #plot histograms
    daily_returns.hist(bins = 20, label ='SPY')
    daily_returns.hist(bins = 20, label ='XOM')
    plt.legend(loc = 'upper right')
    plt.show()

    #plot mean & std
    mean = daily_returns.mean()
    std= daily_returns.std()

    plt.axvline(mean,color = 'w', linestyle = 'dashed', linewidth =2)
    plt.axvline(std,color = 'r', linestyle = 'dashed', linewidth =2)
    plt.axvline(-std,color = 'r', linestyle = 'dashed', linewidth =2)
    plt.show()

    #plot kurtosis
    print daily_returns.kurtosis()


    #SCATTER PLOTS
    #read data
    dates = pd.date_range('2009-01-01','2012-12-31')

    symbols = ['SPY','XOM','GLD']
    df = get_data(symbols,dates)

    plot(df)

    daily_returns = compute_daily_returns(df)
    plot_data(daily_returns,title = "daily_returns" ,ylabel = "daily_returns", xlabel = "dates")

    daily_returns.plot(kind = 'scatter', x='SPY' ,y='XOM')
    beta_XOM,alpha_XOM = np.polyfit(daily_returns['SPY'],daily_returns['XOM'],1)
    plt.plot(daily_returns['SPY'],beta_XOM*daily_returns['SPY']+alpha_XOM,'-',color = 'r')
    plt.show()

    #correlation
    print daily_returns.corr(method = 'Pearson')

if __name__ == "main":
    test_run()