
import numpy as np
import pandas as pd
import sys
import math


class Ma_analysis:

    dataFrame = None

    def __init__(self, file_path, upload_path):
        file_path = file_path

        self.setread_csv(file_path)

        print(self.dataFrame.head())
        print("analysis_data.dataFrame.columns = \n", self.dataFrame.columns)

        none_NaN_dataFrame = self.drop_nan(self.dataFrame)
        self.upload_to_csv(none_NaN_dataFrame, upload_path)


    def setread_csv(self, path):
        try:
            stock_df = pd.read_csv(path)
            # print(type(stock_df))
            # print(stock_df.head())

            self.dataFrame = stock_df


        except Exception as err:
            print(str(err))

    def dataFrame_Filter(self, dataframe, column):
        #[Date, Start, high, low, close, percent, 5MA, 20MA, 60MA, volume, 5VOL, 20VOL, 60VOL, PVT, CCI, Sonar, RSI]

        temp_df = []
        temp_df = dataframe[column]

        print(type(temp_df))
        print(len(temp_df))
        print(temp_df.head())
        print(temp_df.tail())

        return temp_df

    def join_MA(self, original_df, join_df):

        concat_MA_df = pd.concat([original_df, join_df], axis=1)

        return concat_MA_df

    def upload_to_csv(self, dataframe, path):
        dataframe.to_csv(path, sep=',', na_rep='NaN')
        print("uploaded dataFrame. ", path)

        return True


    def drop_nan(self, dataframe):
        print(dataframe.describe())

        for col in dataframe.columns:
            # print(col)
            print(col, dataframe.loc[dataframe[col] == 0].shape[0])

        print("0 ---> replace =>np.NaN")
        dataframe = dataframe.replace(0, np.NaN)

        for col in dataframe.columns:
            # print(col)
            print(col, dataframe.loc[dataframe[col] == 0].shape[0])

        print("NaN summary()")
        print(dataframe.isna().sum())
        print("NaN Drop.....")
        dataframe = dataframe.dropna()

        print("----result----")
        print(dataframe.isna().sum())

        dataframe = dataframe.reset_index(drop=True)

        return dataframe


file_path = sys.argv[1]

analysis_data = Ma_analysis(file_path, sys.argv[2])


