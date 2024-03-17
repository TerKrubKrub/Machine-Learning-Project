import matplotlib.pyplot as plt
import pandas as pd

from Algorithms import *
from tabulate import tabulate

scheme_code = input('Enter the MF Scheme code:- ')


@getDataFrame(scheme_code)
def forecasting_mutual_fund(df, details):
    pred_linear, rmse_linear = linear(df.iloc[:-30])
    pred_arima, rmse_arima = arima(df.iloc[:-30])

    data = [
        ['Linear', pred_linear[0], pred_linear[1], pred_linear[2], pred_linear[3], pred_linear[4]
            , min(pred_linear), max(pred_linear)],
        ['ARIMA', pred_arima[0], pred_arima[1], pred_arima[2], pred_arima[3], pred_arima[4],
         min(pred_arima), max(pred_arima)]
    ]
    print("\n  Time Series Forecasting for " + details['scheme_name'] + " (" + str(details['scheme_code']) + ")\n")
    print(tabulate(data, headers=["Algorithm", "Day 1", "Day 2", "Day 3", "Day 4", "Day 5",
                                  "1 Month Low", "1 Month High"], tablefmt='orgtbl'))

    df_30 = df['nav'].iloc[-100:].astype(float)
    Y = [np.nan for i in range(len(df_30) - 30)]

    plt.xlabel('Days [last 100 + 30 forecasted]')
    plt.ylabel('NAV')
    plt.title("Forecasting for " + details['scheme_name'])
    plt.legend()
    s = df_30
    sns.set(style="ticks")
    data_preproc = pd.DataFrame({
        'Trends': s.values,
        'Linear': np.append(Y, pred_linear),
        'ARIMA': np.append(Y, pred_arima),
    })
    sns.lineplot(data=data_preproc)
    plt.show()

forecasting_mutual_fund()
