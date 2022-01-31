import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys
import os



sys.path.append(sys.path[0] + "\stock_gru_model.py")
# print("sys.path = ", sys.path)

import stock_gru_model


class Model_array:
    print("\ncurrent path = ", os.getcwd(), "\n")

    stock_id = None
    file_name = None



    models_array = []
    models_columns = []
    gru_Models = []
    lastData = None
    predict_day = None
    close_df_Map = None



    predict_list = []

    def __init__(self, stock_id, file_name, *args):  # *args = [models_path]
        self.stock_id = stock_id
        self.file_name = file_name

        if (len(args) < 1):
            print(
                "\nclass : Model_array create.\n stock_id : {0}\n file_name : {1} \n  models_array = None".format(
                    self.stock_id, self.file_name))
        else:
            for index in range(len(args)):
                # print("args[index] = ", index)
                self.models_array.append(
                    "./models/" + self.stock_id + "/" + args[index] + "_" + self.stock_id + "_GRU_model.h5")
                self.models_columns.append(args[index])
            print(
                "\nclass : Model_array create.\n stock_id : {0}\n file_name : {1} \n  models_array = {2}".format(
                    self.stock_id, self.file_name, self.models_array))
            print("\nmodel_columns = ", self.models_columns)

    def models_array_insert(self, *args):

        if (len(args) < 1):
            print("\n\n insert Parameters = None")
        else:
            for index in range(len(args)):
                self.models_array.append(
                    "./models/" + self.stock_id + "/" + args[index] + "_" + self.stock_id + "_GRU_model.h5")
                print("\ninserted models_array[{0}]".format(index),
                      "== ./models/" + self.stock_id + "/" + args[index] + "_" + self.stock_id + "_GRU_model.h5")
                self.models_columns.append(args[index])
            print("\n", self.models_array, "\n")
            print("\n", self.models_columns, "\n")

    def lastData_filter(self, stock_id, file_name, *x_data_col, y_pred_column="close"):
        stock_data = stock_gru_model.Stock_gruModel(stock_id, file_name)
        stock_data.scaler_and_normalization(*x_data_col, y_data_col=y_pred_column)
        print("lastData_filter :: stock_data.x_scal_dataframe.columns" , stock_data.x_scal_dataframe.columns)
        # print("lastData_insert :: stock_data.y_scal_dataframe" , stock_data.y_scal_dataframe)
        stock_data.sendTo_csv(stock_data.x_scal_dataframe, "confirm.csv")
        temp_data = np.array(stock_data.x_scal_dataframe)
        temp_last_data = temp_data[-30:-1]
        temp_last_data = np.append(temp_last_data, temp_data[-1].reshape(-1, 7), axis=0)
        self.lastData = temp_last_data


    # def load_Model(self):
    #     models = []
    #
    #     for i in range(len(self.models_array)):
    #         models.append(tf.keras.models.load_model(self.models_array[i]))
    #
    #     self.gru_Models = models
    #     print("gru_Models Parameter create.")

    def model_predict_Oneday(self, stock_id, last_data, pred_y_column):
        try:
            # print("\ncurrent_cwd = ", os.getcwd())

            pred_model = tf.keras.models.load_model(
                "./models/" + stock_id + "/" + pred_y_column + "_" + stock_id + "_GRU_model.h5")
            print("pred_model : ", pred_model.summary())
            # print("temp_class.x_test[-1] = \n", temp_class.x_test[-1])
            # print("temp_class.x_test[-1].shape = ", temp_class.x_test[-1].shape)
            reshaped_temp_x_test = last_data.reshape(-1, 30, 7)
            # print("reshaped_temp_x_test.shape = ", reshaped_temp_x_test.shape)
            # print("reshaped_temp_x_test = ", reshaped_temp_x_test)
            pred = pred_model.predict(reshaped_temp_x_test)
            # print(pred)


            return float(pred)


        except Exception as err:
            print(str(err))

    def model_Predict_Array(self, stock_id, predict_day, last_data):
        self.predict_day = predict_day

        for index in range(int(predict_day)):
            temp_list = []
            for i in range(len(self.models_columns)):
                temp = self.model_predict_Oneday(stock_id, last_data, self.models_columns[i])
                temp_list.append(temp)

            temp_list = np.array(temp_list)
            # print(temp_list.shape)
            print(temp_list)

            last_data = np.append(last_data, temp_list.reshape(-1, 7), axis=0)
            print("\nlast_data.shape = ", last_data.shape)
            # print("\nlast_Data = \n", last_Data)

            last_data = last_data[1:]

            print("\nlast_Data.shape[1:] = ", last_data.shape)
            # print("\last_data[-1:] = \n", last_Data)

            self.predict_list.append(temp_list)

        print("\nma.predict_list.shape = ", np.array(self.predict_list).shape)
        print("\nma.predict_list = \n", np.array(self.predict_list))

        return self.predict_list

    def conv_DataFrame_to_Chart(self, dataframe):
        plt.figure(figsize=(12,6))

        plt.title("predict " + str(self.stock_id) + " " + str(self.predict_day) + " " + str(self.stock_id.split('_')[1]) + str(" charts"))
        plt.xlabel(str(self.stock_id.split('_')[1]))
        plt.ylabel("close")
        plt.plot(dataframe["max_close"], label="max_close")
        plt.plot(dataframe["min_close"], label="min_close")
        # plt.plot(dataframe["max_nor_close"], label="max_nor_close")
        # plt.plot(dataframe["min_nor_close"], label="min_nor_close")
        plt.grid()
        plt.legend(loc="best")
        print("os.getcwd() : ", os.getcwd())
        plt.savefig("./predict_charts/" + str(self.stock_id) + "/predict_" + str(self.stock_id) + "_" + str(self.predict_day) + "datas_charts.png")
        plt.show()


    def close_Match_NorData(self):
        temp_df = stock_gru_model.Stock_gruModel(self.stock_id, self.file_name)
        temp_df.scaler_and_normalization(*self.models_columns, y_data_col="close")
        # print("\n1\n", temp_df.x_scal_dataframe["close"])
        # print("\n2\n", temp_df.stock_dataset["close"])

        self.close_df_Map = pd.concat([temp_df.stock_dataset["close"], temp_df.x_scal_dataframe["close"]],
                                      axis=1,
                                      keys=["close", "nor_close"])
        self.close_df_Map = self.close_df_Map.sort_values(by=["close"], ascending=True)
        print("\n\nclose_df_Map Parameter inserted.")
        print("\nclose_df = \n", self.close_df_Map)

    def norclose_Convert_close(self, pred_df):
        all_df = pd.DataFrame()

        for i in range(len(pred_df)):
            temp1 = self.close_df_Map.loc[self.close_df_Map["nor_close"]>=pred_df["close"][i]][0:1]
            temp1 = temp1.rename(columns={"close": "max_close", "nor_close": "max_nor_close"})
            temp1 = temp1.reset_index(drop=True)
            temp2 = self.close_df_Map.loc[self.close_df_Map["nor_close"]<=pred_df["close"][i]].tail(1)
            temp2 = temp2.rename(columns={"close": "min_close", "nor_close": "min_nor_close"})
            temp2 = temp2.reset_index(drop=True)
            alltemp = pd.concat([temp1, temp2], axis=1, verify_integrity=True)#ignore_index=True, keys=["Max_close", "nor_close1", "Min_Close", "nor_close2"]
            all_df = all_df.append(alltemp)
            all_df = all_df.reset_index(drop=True)

            # print(alltemp)

        print("\n\nall_df : \n", all_df)
        return all_df

