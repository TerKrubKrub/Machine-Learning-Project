from Algorithms import *

def getDataFrame(scheme_code):
    def decorate(func):
        def decorated(*args,**kwargs):
            df = yf.download(str(scheme_code),period='max')
            print(df)
            df = df.drop(columns=['Open', 'High', 'Low', 'Adj Close', 'Volume'])
            df = df.rename(columns={'Close': 'nav'})
            df.reset_index(inplace=True)
            print(df)

            # Display basic information about the dataset
            print("Number of variables:", df.shape[1])
            print("\nnav Means:")
            print(df['nav'].mean())
            print("\nnav Standard Deviations:")
            print(df['nav'].std())
            print("\nnav Quantiles:")
            print(df['nav'].quantile([0.25, 0.5, 0.75]))

            # Calculate the first quartile (Q1) and third quartile (Q3)
            Q1 = df['nav'].quantile(0.25)
            Q3 = df['nav'].quantile(0.75)

            # Calculate the Interquartile Range (IQR)
            IQR = Q3 - Q1

            # Define the lower and upper bounds for outliers
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            # Identify outliers using boolean indexing
            outliers = (df['nav'] < lower_bound) | (df['nav'] > upper_bound)

            # Display basic information about outliers
            print("\nOutliers:")
            print(df[outliers])

            # Drop outliers from the DataFrame
            df = df[~outliers]
            print("\nDataFrame without Outliers:")
            print(df)

            df['date'] = df['Date'].dt.strftime('%Y-%m-%d')

            info = yf.Ticker(str(scheme_code)).get_info()
            details = {'scheme_name': info['longName'], 'scheme_code': str(scheme_code)}
            return func(df,details)
        return decorated
    return decorate


def data_frame(func):
    def decorated(*args,**kwargs):
        df = yf.download(str(*args) + ".BO", period='max')
        df = df.drop(columns=['Open', 'High', 'Low', 'Adj Close', 'Volume'])
        df = df.rename(columns={'Close': 'nav'})
        df.reset_index(inplace=True)
        df['date'] = df['Date'].dt.strftime('%Y-%m-%d')
        info = yf.Ticker(str(*args) + ".BO").get_info()
        details = {'scheme_name': info['longName'], 'scheme_code': str(*args)}
        return func(df,details)
    return decorated
