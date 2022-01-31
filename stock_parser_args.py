
import numpy as np
import pandas as pd
import sys
import math

class Ma_analysis:

    dataFrame = ''
    # self.dataFrame


    def setread_csv(self, path):
        try:
            stock_df = pd.read_csv(path)
            # print(type(stock_df))
            # print(stock_df.head())

            self.dataFrame = stock_df


        except Exception as err:
            print(str(err))

    def filter_3MA(self, dataframe):

        _3MA_df = []
        for i in range(len(dataframe) - 2):
            _3MA_df.append(dataframe["AdjClose"][i:i + 3].sum() / 3.)
            # print(dataframe["AdjClose"][i:i+3].sum()/3.)

        _3MA_df = pd.DataFrame(_3MA_df, columns=["3MA"], index=range(2, len(_3MA_df) + 2))

        # print(type(_3MA_df))
        # print(len(_3MA_df))
        # print(_3MA_df.head())
        # print(_3MA_df.tail())

        return _3MA_df

    def filter_5MA(self, dataframe):

        _5MA_df = []
        for i in range(len(dataframe) - 4):
            _5MA_df.append(dataframe["AdjClose"][i:i + 5].sum() / 5.)
            # print(dataframe["AdjClose"][i:i+5].sum()/5.)

        _5MA_df = pd.DataFrame(_5MA_df, columns=["5MA"], index=range(4, len(_5MA_df) + 4))

        # print(type(_5MA_df))
        # print(len(_5MA_df))
        # print(_5MA_df.head())
        # print(_5MA_df.tail())

        return _5MA_df

    def filter_20MA(self, dataframe):

        _20MA_df = []
        for i in range(len(dataframe) - 19):
            _20MA_df.append(dataframe["AdjClose"][i:i + 20].sum() / 20.)
            # print(dataframe["AdjClose"][i:i+20].sum()/20.)

        _20MA_df = pd.DataFrame(_20MA_df, columns=["20MA"], index=range(19, len(_20MA_df) + 19))

        # print(type(_20MA_df))
        # print(len(_20MA_df))
        # print(_20MA_df.head())
        # print(_20MA_df.tail())

        return _20MA_df

    def filter_60MA(self, dataframe):

        _60MA_df = []
        for i in range(len(dataframe) - 59):
            _60MA_df.append(dataframe["AdjClose"][i:i + 60].sum() / 60.)
            # print(dataframe["AdjClose"][i:i+60].sum()/60.)

        _60MA_df = pd.DataFrame(_60MA_df, columns=["60MA"], index=range(59, len(_60MA_df) + 59))

        # print(type(_60MA_df))
        # print(len(_60MA_df))
        # print(_60MA_df.head())
        # print(_60MA_df.tail())

        return _60MA_df

    def join_MA(self, original_df, join_df):

        concat_MA_df = pd.concat([original_df, join_df], axis=1)

        return concat_MA_df

    def upload_to_csv(self, dataframe, path):
        dataframe.to_csv(path, sep=',', na_rep='NaN')

        return True

    def filter_UpDown(self, dataframe):
        updown_df = []
        for i in range(len(dataframe) - 1):
            updown_df.append(dataframe["AdjClose"][i + 1] - dataframe["AdjClose"][i])
            # print(dataframe["AdjClose"][i+1]-dataframe["AdjClose"][i])

        updown_df = pd.DataFrame(updown_df, columns=["updown"], index=range(1, len(updown_df) + 1))

        # print(updown_df)
        return updown_df

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

    def filter_3Ma_60MaPercent(self, dataframe):
        #confirm nan
        confirm_nan = dataframe.columns
        for i in confirm_nan:
            # print(dataframe[i].isna().sum())
            if(dataframe[i].isna().sum() >0):
                print("dataset is belong to Nan.... function quit")
                return 1

        percent_df = []

        for j in range(len(dataframe)):
            num1 = float(dataframe["3MA"][j:j+1])
            num2 = float(dataframe["60MA"][j:j+1])
            subnum = num1 - num2
            if(subnum > -1 and subnum< 1):
                subnum = math.ceil(subnum)+1
            if(num2 > -1 and num2 < 1):
                num2 = math.ceil(num2)
            caledNum = num2 / subnum
            percent_df.append(caledNum)

        percent_df = pd.DataFrame(percent_df, columns=["percent3_60"])

        return percent_df

    def filter_20Ma_60MaPercent(self, dataframe):
        #confirm nan
        confirm_nan = dataframe.columns
        for i in confirm_nan:
            # print(dataframe[i].isna().sum())
            if(dataframe[i].isna().sum() >0):
                print("dataset is belong to Nan.... function quit")
                return 1

        percent_df = []

        for j in range(len(dataframe)):
            num1 = float(dataframe["20MA"][j:j+1])
            num2 = float(dataframe["60MA"][j:j+1])
            subnum = num1 - num2
            if(subnum > -1 and subnum< 1):
                subnum = math.ceil(subnum)+1
            if(num2 > -1 and num2 < 1):
                num2 = math.ceil(num2)
            caledNum = num2 / subnum
            percent_df.append(caledNum)

        percent_df = pd.DataFrame(percent_df, columns=["percent20_60"])

        return percent_df




# a = Ma_analysis()
#
# a.setread_csv("./035720noneMA.csv")
#
# # print(type(a.dataFrame))
# # print(a.dataFrame.head())
# # print(a.dataFrame.loc[a.dataFrame["Date"]=="2010-10-19"])
#
# _3ma_df = a.filter_3MA(a.dataFrame)
#
# # print(_3ma_df)
#
# concat_3ma_df = a.join_MA(a.dataFrame, _3ma_df)
#
# # print(concat_3ma_df)
#
# # print(len(a.dataFrame))
#
#
# _5ma_df = a.filter_5MA(a.dataFrame)
#
#
# concat_5ma_df = a.join_MA(a.dataFrame, _5ma_df)
#
# # print(concat_5ma_df)
# # print(concat_5ma_df[0:10])
#
# _20ma_df = a.filter_20MA(a.dataFrame)
#
# concat_20ma_df = a.join_MA(a.dataFrame, _20ma_df)
#
# # print(concat_20ma_df)
# # print(concat_20ma_df.tail())
#
# _60ma_df = a.filter_60MA(a.dataFrame)
#
# concat_60ma_df = a.join_MA(a.dataFrame, _60ma_df)
#
# # print(concat_60ma_df[0:10])
# # print(concat_60ma_df[10:20])
# # print(concat_60ma_df[20:30])
# # print(concat_60ma_df[30:40])
# # print(concat_60ma_df[40:50])
# # print(concat_60ma_df[50:60])
# # print(concat_60ma_df[60:70])
# # print(concat_60ma_df[70:80])
# # print(concat_60ma_df.tail())
# updown_df = a.filter_UpDown(a.dataFrame)
# a.dataFrame = a.join_MA(a.dataFrame, updown_df)
# a.dataFrame = a.join_MA(a.dataFrame, _3ma_df)
# a.dataFrame = a.join_MA(a.dataFrame, _5ma_df)
# a.dataFrame = a.join_MA(a.dataFrame, _20ma_df)
# a.dataFrame = a.join_MA(a.dataFrame, _60ma_df)
#
# a.dataFrame = a.drop_nan(a.dataFrame)
#
# # print(a.dataFrame[0:10])
# # print(a.dataFrame[10:20])
# # print(a.dataFrame[20:30])
# # print(a.dataFrame[30:40])
# # print(a.dataFrame[40:50])
# # print(a.dataFrame[50:60])
# # print(a.dataFrame[60:70])
# # print(a.dataFrame[70:80])
# # print(a.dataFrame.tail())
#
# percent3_60 = a.filter_3Ma_60MaPercent(a.dataFrame)
# percent20_60 = a.filter_20Ma_60MaPercent(a.dataFrame)
#
# # print(percent3_60)
# # print(percent20_60)
# a.dataFrame = a.join_MA(a.dataFrame, percent3_60)
# a.dataFrame = a.join_MA(a.dataFrame, percent20_60)
#
# print(a.dataFrame)
#
# # a.upload_to_csv(a.dataFrame, "./035720pdedited2.csv")





############################################################################################
file_path = sys.argv[1]

analysis_data = Ma_analysis()

analysis_data.setread_csv(file_path)

filter_updown = analysis_data.filter_UpDown(analysis_data.dataFrame)
_3ma_df = analysis_data.filter_3MA(analysis_data.dataFrame)
_5ma_df = analysis_data.filter_5MA(analysis_data.dataFrame)
_20ma_df = analysis_data.filter_20MA(analysis_data.dataFrame)
_60ma_df = analysis_data.filter_60MA(analysis_data.dataFrame)

analysis_data.dataFrame = analysis_data.join_MA(analysis_data.dataFrame, filter_updown)
analysis_data.dataFrame = analysis_data.join_MA(analysis_data.dataFrame, _3ma_df)
analysis_data.dataFrame = analysis_data.join_MA(analysis_data.dataFrame, _5ma_df)
analysis_data.dataFrame = analysis_data.join_MA(analysis_data.dataFrame, _20ma_df)
analysis_data.dataFrame = analysis_data.join_MA(analysis_data.dataFrame, _60ma_df)

analysis_data.dataFrame = analysis_data.drop_nan(analysis_data.dataFrame)

percent3_60 = analysis_data.filter_3Ma_60MaPercent(analysis_data.dataFrame)
percent20_60 = analysis_data.filter_20Ma_60MaPercent(analysis_data.dataFrame)

analysis_data.dataFrame = analysis_data.join_MA(analysis_data.dataFrame, percent3_60)
analysis_data.dataFrame = analysis_data.join_MA(analysis_data.dataFrame, percent20_60)

analysis_data.upload_to_csv(analysis_data.dataFrame, sys.argv[2])

