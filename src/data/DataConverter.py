import pandas as pd
import os

class DataConverter:
    def __init__(self, data, path = 'DATA/'):
        self.raw_path = f'{path}RAW/{data["symbol"]}/'
        self.month_path = f'{path}MONTH/{data["symbol"]}/'
        self.year_path = f'{path}YEAR/{data["symbol"]}/'
        self.all_path = f'{path}ALL/{data["symbol"]}/'
        
        self.symbol = data["symbol"]
        self.timeFrame = data["timeFrame"]
        
        self.prepareData()
        
    def prepareData(self):
        if not os.path.exists(self.month_path):
            os.makedirs(self.month_path)
        if not os.path.exists(self.year_path):
            os.makedirs(self.year_path)
        if not os.path.exists(self.all_path):
            os.makedirs(self.all_path)
    
    def tickToM1(self, rawfile, M1file, TIME_FRAME = "1Min"):
        if os.path.exists(rawfile):
            # Reading the data
            data = pd.read_csv(rawfile, usecols=[2, 3])

            data = data.rename(columns={"Timestamp": "Datetime"})
            data.set_index('Datetime')
            # data.drop(data.columns[0])
            # print(data.head())
            data.index = pd.to_datetime(data['Datetime'], format='ISO8601')

            # Resample LTP column to 15 mins bars using resample function from pandas
            result = data['Bid'].resample(TIME_FRAME).ohlc()

            # Resample LTQ column to 15 mins bars using resample function from pandas
            result_v = data['Bid'].resample(TIME_FRAME).count()

            # Concatenate resampled data
            resample_data = pd.concat([result, result_v], axis=1,)
            resample_data = resample_data.dropna()

            resample_data = resample_data.rename(columns={
                                                "Timestamp": "Datetime",
                                                "open": "Open",
                                                "high": "High",
                                                "low": "Low",
                                                "close": "Close",
                                                "Bid": "Volume"})

            resample_data.to_csv(M1file)
            
    def monthToYear(self, listMonths, yearpath):
        if (len(listMonths) == 0):
            return
        m_data = []
        for month in listMonths:
            m_data.append(pd.read_csv(month))
        data = pd.concat(m_data)
        data.to_csv(yearpath, index=False)
            
    def convertTickToM1(self, startYear = 2010, endYear = 2025):
        for year in range(startYear, endYear):
            for month in range(1, 13):
                if month < 10:
                    rawfile = f'{self.raw_path}Exness_{self.symbol}_Zero_Spread_{year}_0{month}.csv'
                    month_m1_file = f'{self.month_path}{self.symbol}_{self.timeFrame}_{year}_0{month}.csv'
                else:
                    rawfile = f'{self.raw_path}Exness_{self.symbol}_Zero_Spread_{year}_{month}.csv'
                    month_m1_file = f'{self.month_path}{self.symbol}_{self.timeFrame}_{year}_{month}.csv'

                self.tickToM1(rawfile, month_m1_file, self.timeFrame)
                
    def convertMonthToYear(self, startYear = 2010, endYear = 2025):
        for year in range(startYear, endYear):
            year_path = f'{self.year_path}{self.symbol}_{self.timeFrame}_{year}.csv'
            
            months = []
            for month in range(1, 13):
                if month < 10:
                    month_m1_file = f'{self.month_path}{self.symbol}_{self.timeFrame}_{year}_0{month}.csv'
                else:
                    month_m1_file = f'{self.month_path}{self.symbol}_{self.timeFrame}_{year}_{month}.csv'
                print(month_m1_file)
                if os.path.exists(month_m1_file):
                    months.append(month_m1_file)

            self.monthToYear(months, year_path)
    
    def createDataFile(self, startYear = 2010, endYear = 2025, file_type = "Train"):
        listyears = []
        for year in range(startYear, endYear):
            year_path = f'{self.year_path}{self.symbol}_{self.timeFrame}_{year}.csv'
            if os.path.exists(year_path):
                listyears.append(year_path)
        
        if (len(listyears) == 0):
            return
        m_data = []
        for year in listyears:
            m_data.append(pd.read_csv(year))
        data = pd.concat(m_data)
        
        allpath = f'{self.all_path}{self.symbol}_{self.timeFrame}_{file_type}.csv'
        
        data.to_csv(allpath, index=False)