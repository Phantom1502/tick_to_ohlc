import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import joblib
import os

class PriceFeature:
    def __init__(self, input_path, output_path, price_scaler = 'price_scaler.pkl'):
        data = pd.read_csv(input_path, index_col="Datetime", parse_dates=True)
        data.drop(['Volume'], axis=1, inplace=True)

        data['EMA_2'] = data['Close'].ewm(span=2, adjust=False).mean()
        data['EMA_3'] = data['Close'].ewm(span=3, adjust=False).mean()
        data['EMA_5'] = data['Close'].ewm(span=5, adjust=False).mean()
        data['EMA_8'] = data['Close'].ewm(span=8, adjust=False).mean()
        data['EMA_13'] = data['Close'].ewm(span=13, adjust=False).mean()
        data['EMA_21'] = data['Close'].ewm(span=21, adjust=False).mean()
        data['EMA_33'] = data['Close'].ewm(span=33, adjust=False).mean()
        data['EMA_54'] = data['Close'].ewm(span=54, adjust=False).mean()
        data['EMA_87'] = data['Close'].ewm(span=87, adjust=False).mean()
        data['EMA_141'] = data['Close'].ewm(span=141, adjust=False).mean()

        data = PriceFeature.normalize(data, price_scaler)

        data.to_csv(output_path)
        self.data = data

    def plot(self):
        data = self.data[:2000]
        plt.figure(figsize=(15, 6))

        plt.plot(data.index, data["EMA_13"], label="EMA_13", linestyle="dashed", alpha=0.7)
        plt.plot(data.index, data["EMA_141"], label="EMA_141", linestyle="dotted", alpha=0.7)
        plt.plot(data.index, data["C"], label="Close", linestyle="solid", alpha=0.7)

        plt.xlabel("Datetime")
        plt.ylabel("Sin values")
        plt.title("Visualization of Time Features")
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid()
        plt.show()

    @staticmethod
    def create_scaler(df, price_scaler = 'price_scaler.pkl'):
        # Normalize OHLC
        scaler = MinMaxScaler()
        scaler.fit(df[['Close']].values)

        # Lưu scaler
        joblib.dump(scaler, price_scaler)

    @staticmethod
    def normalize(df, price_scaler = 'price_scaler.pkl'):
        if not os.path.exists(price_scaler):
            PriceFeature.create_scaler(df, price_scaler)
        # Tải scaler từ file
        scaler = joblib.load(price_scaler)

        # Normalize dữ liệu mới
        # Lấy toàn bộ cột trong DataFrame
        all_columns = df.columns

        # Transform từng cột một
        data_normalized = df.copy()
        for col in all_columns:
            data_normalized[col] = scaler.transform(df[[col]].values)  # Transform từng cột theo scaler của Open
        #data_normalized = scaler.transform(df.values)
        df_normalize = pd.DataFrame(data_normalized)
        df_normalize.rename(columns={
            'Open': 'O',
            'High': 'H',
            'Low': 'L',
            'Close': 'C'
        }, inplace=True)
        #df_normalize['Close'] = df['Close'].reset_index(drop=True)
        return df_normalize