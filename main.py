from src.data.DataConverter import DataConverter
from src.data.DataFeature import DataFeature

def prepareData(timeFrame='5Min', symbol='EURUSD'):
    dataConverter = DataConverter({"symbol": symbol, "timeFrame": timeFrame}, path = 'R_DATA/')
    dataConverter.convertTickToM1(startYear=2020, endYear=2026)
    dataConverter.convertMonthToYear(startYear=2020, endYear=2026)
    dataConverter.createDataFile(startYear=2020, endYear=2024, file_type = "Train")
    dataConverter.createDataFile(startYear=2024, endYear=2026, file_type = "Validation")

def createFeature(timeFrame='5Min', symbol='EURUSD'):
    dataFeature = DataFeature(root_path = 'data', symbol = symbol, timeFrame = timeFrame)
    dataFeature.create_feature(type="Train")
    dataFeature.create_feature(type="Validation")

if __name__ == '__main__':
    createFeature(timeFrame='1Min', symbol='EURUSD')
    ### OK