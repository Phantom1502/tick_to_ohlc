import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class TimeFeature:
    def __init__(self, input_path, output_path):
        data = pd.read_csv(input_path, index_col="Datetime", parse_dates=True)
        time_df = data[['Close']]
        # Thêm các cột thời gian
        time_df['Minute_of_Hour'] = time_df.index.minute  # Phút trong giờ (0-59)
        time_df['Minute_of_Day'] = time_df.index.hour * 60 + time_df['Minute_of_Hour']     # Giờ trong ngày (0-23)
        time_df['Minute_of_Week'] = time_df.index.weekday * 24 * 60 + time_df['Minute_of_Day']  # Ngày trong tuần (0: Thứ Hai, 6: Chủ Nhật)

        # Tùy chọn: Biểu diễn tuần hoàn
        time_df['Minute_sin'] = np.sin(2 * np.pi * time_df['Minute_of_Hour'] / 60)
        time_df['Minute_cos'] = np.cos(2 * np.pi * time_df['Minute_of_Hour'] / 60)
        time_df['Hour_sin'] = np.sin(2 * np.pi * time_df['Minute_of_Day'] / (24 * 60))
        time_df['Hour_cos'] = np.cos(2 * np.pi * time_df['Minute_of_Day'] / (24*60))
        time_df['Day_sin'] = np.sin(2 * np.pi * time_df['Minute_of_Week'] / (7*24 * 60))
        time_df['Day_cos'] = np.cos(2 * np.pi * time_df['Minute_of_Week'] / (7*24 * 60))
        time_df.drop(['Close', 'Minute_of_Hour', 'Minute_of_Day', 'Minute_of_Week'], axis=1, inplace=True)
        time_df.to_csv(output_path)

        self.data = time_df

    def plot(self):
        data = self.data[:2000]
        plt.figure(figsize=(15, 6))

        plt.plot(data.index, data["Minute_sin"], label="Minute_sin", linestyle="dashed", alpha=0.7)
        plt.plot(data.index, data["Hour_sin"], label="Hour_sin", linestyle="dotted", alpha=0.7)
        plt.plot(data.index, data["Day_sin"], label="Day_sin", linestyle="solid", alpha=0.7)

        plt.xlabel("Datetime")
        plt.ylabel("Sin values")
        plt.title("Visualization of Time Features")
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid()
        plt.show()