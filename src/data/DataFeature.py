from src.data.TimeFeature import TimeFeature
from src.data.PriceFeature import PriceFeature
from src.data.MACDFeature import MACDFeature
from src.data.MFIFeature import MFIFeature

class DataFeature:
    def __init__(self, root_path = 'data', symbol = 'EURUSD', timeFrame = '5Min'):
        self.root_path = root_path
        self.symbol = symbol
        self.timeFrame = timeFrame
        
        self.price_scaled_path = f'{root_path}/scaler/{symbol}_{timeFrame}_Scaler.csv'
        self.macd_scaled_path = f'{root_path}/scaler/{symbol}_{timeFrame}_MACD_Scaler.csv'
    
    def create_feature(self, type = "Train"):
        data_path = f'{self.root_path}/ohlc/{self.symbol}_{self.timeFrame}_{type}.csv'
        time_path = f'{self.root_path}/features/{self.symbol}_{self.timeFrame}_{type}_Time.csv'
        price_path = f'{self.root_path}/features/{self.symbol}_{self.timeFrame}_{type}_Price.csv'
        macd_path = f'{self.root_path}/features/{self.symbol}_{self.timeFrame}_{type}_MACD.csv'
        mfi_path = f'{self.root_path}/features/{self.symbol}_{self.timeFrame}_{type}_MFI.csv'
        
        price = TimeFeature(data_path, time_path)
        price = PriceFeature(data_path, price_path, self.price_scaled_path)
        macd = MACDFeature(data_path, macd_path, self.macd_scaled_path)
        mfi = MFIFeature(data_path, mfi_path)
