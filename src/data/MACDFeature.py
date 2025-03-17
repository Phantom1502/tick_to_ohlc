import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import joblib
import os

class MACDFeature:
    def __init__(self, input_path, output_path, macd_scaler='macd_scaler.pkl'):
        data = pd.read_csv(input_path, index_col="Datetime", parse_dates=True)
        MACDFeature.calculate_macd(data, short_window=2, long_window=5, signal_window=3)
        MACDFeature.calculate_macd(data, short_window=3, long_window=8, signal_window=5)
        MACDFeature.calculate_macd(data, short_window=5, long_window=13, signal_window=8)
        MACDFeature.calculate_macd(data, short_window=8, long_window=21, signal_window=13)
        MACDFeature.calculate_macd(data, short_window=13, long_window=34, signal_window=21)
        data.drop(['Close', 'Open', 'High', 'Low', 'Volume'], axis=1, inplace=True)

        scaler = MACDFeature.create_scaler(data, macd_scaler)
        # Lưu lại index trước khi biến đổi
        index = data.index

        # Chuẩn hóa dữ liệu và đặt lại index
        data = pd.DataFrame(scaler.transform(data.values), columns=data.columns, index=index)

        data.to_csv(output_path)

        self.data = data

    def plot(self):
        data = self.data[:2000]
        plt.figure(figsize=(15, 6))

        plt.plot(data.index, data["MACD13_34"], label="MACD13_34", linestyle="dashed", alpha=0.7)
        plt.plot(data.index, data["Histogram13_34"], label="Histogram13_34", linestyle="dotted", alpha=0.7)

        plt.xlabel("Datetime")
        plt.ylabel("Sin values")
        plt.title("Visualization of Time Features")
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid()
        plt.show()
    
    @staticmethod
    def create_scaler(df, macd_scaler='macd_scaler.pkl'):
        if not os.path.exists(macd_scaler):
            # Normalize OHLC
            scaler = StandardScaler()
            scaler.fit(df.values)

            # Lưu scaler
            joblib.dump(scaler, macd_scaler)
            return scaler
        return joblib.load(macd_scaler)

    @staticmethod
    def calculate_macd(df, short_window=12, long_window=26, signal_window=9):
        # Tính EMA ngắn và EMA dài
        df['EMA_short'] = df['Close'].ewm(span=short_window, adjust=False).mean()
        df['EMA_long'] = df['Close'].ewm(span=long_window, adjust=False).mean()

        # Tính MACD
        df[f'MACD{short_window}_{long_window}'] = df['EMA_short'] - df['EMA_long']

        # Tính Signal Line
        df['Signal Line'] = df[f'MACD{short_window}_{long_window}'].ewm(span=signal_window, adjust=False).mean()

        # Tính Histogram (chênh lệch giữa MACD và Signal Line)
        df[f'Histogram{short_window}_{long_window}'] = df[f'MACD{short_window}_{long_window}'] - df['Signal Line']

        # Xóa các cột EMA không cần thiết (nếu muốn gọn gàng)
        df.drop(['EMA_short', 'EMA_long', 'Signal Line'], axis=1, inplace=True)

        return df