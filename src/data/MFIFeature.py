import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import joblib
import os

class MFIFeature:
    def __init__(self, input_path, output_path):
        data = pd.read_csv(input_path, index_col="Datetime", parse_dates=True)
        data['MFI_2'] = MFIFeature.calculate_mfi(data, period=2)
        data['MFI_3'] = MFIFeature.calculate_mfi(data, period=3)
        data['MFI_5'] = MFIFeature.calculate_mfi(data, period=5)
        data['MFI_8'] = MFIFeature.calculate_mfi(data, period=8)
        data['MFI_13'] = MFIFeature.calculate_mfi(data, period=13)
        data['MFI_21'] = MFIFeature.calculate_mfi(data, period=21)
        data['MFI_34'] = MFIFeature.calculate_mfi(data, period=34)
        data['MFI_55'] = MFIFeature.calculate_mfi(data, period=55)
        data['MFI_89'] = MFIFeature.calculate_mfi(data, period=89)
        data['MFI_144'] = MFIFeature.calculate_mfi(data, period=144)
        data.drop(['Close', 'Open', 'High', 'Low', 'Volume'], axis=1, inplace=True)

        data.to_csv(output_path)

        self.data = data

    def plot(self):
        data = self.data[:2000]
        plt.figure(figsize=(15, 6))

        plt.plot(data.index, data["MFI_34"], label="MFI_34", linestyle="dashed", alpha=0.7)
        plt.plot(data.index, data["MFI_144"], label="MFI_144", linestyle="dotted", alpha=0.7)

        plt.xlabel("Datetime")
        plt.ylabel("Sin values")
        plt.title("Visualization of Time Features")
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid()
        plt.show()

    @staticmethod
    def calculate_mfi(df, period=14):
        typical_price = (df['High'] + df['Low'] + df['Close']) / 3
        money_flow = typical_price * df['Volume']

        positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
        negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0)

        avg_positive_flow = positive_flow.rolling(window=period, min_periods=1).sum()
        avg_negative_flow = negative_flow.rolling(window=period, min_periods=1).sum()

        money_flow_ratio = avg_positive_flow / avg_negative_flow
        mfi = (100.0 - (100.0 / (1 + money_flow_ratio))) / 100.0  # Normalize to 0-1

        return mfi

    @staticmethod
    def calculate_rsi(df, period=14):
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=period, min_periods=1).mean()
        avg_loss = loss.rolling(window=period, min_periods=1).mean()

        rs = avg_gain / avg_loss
        rsi = (100.0 - (100.0 / (1 + rs)))/100.0 # normalize to 0 1

        return rsi