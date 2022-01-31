import tensorflow as tf
import numpy as np
import pandas as pd

import os
import sys

import sklearn.model_selection
import sklearn.preprocessing

import matplotlib.pyplot as plt



class Stock_gruModel:

  stock_id = None
  file_name = None
  stock_dataset = None
  stock_dataset_loc = None
  x_scal_dataframe = None
  y_scal_dataframe = None
  x_scal_numpy = None
  y_scal_numpy = None
  x_train , x_test = None, None
  y_train, y_test = None, None
  md_earlyStop = None

  scaler = sklearn.preprocessing.MinMaxScaler()

  def __init__(self, stock_id, file_name):
    self.setStock_id(stock_id)
    self.setFile_name(file_name)
    self.setread_csv()

  def setFile_name(self, file_name):
    self.file_name = file_name
    print("self.file_name = ", self.file_name)

  def setStock_id(self, stock_id):
    self.stock_id = stock_id
    print("self.stock_id = ", self.stock_id)

  def setread_csv(self):
    current_cwd = os.getcwd()
    # print("current_cwd : ", current_cwd)
    try:
      # os.chdir("./uploads")
      self.stock_dataset = pd.read_csv("./uploads/" + self.stock_id + "/" + self.stock_id + "_" + self.file_name + ".csv_df.csv", sep=',')
      self.stock_dataset_loc = self.stock_dataset.columns[1:]
      self.stock_dataset = self.stock_dataset[self.stock_dataset_loc]

      # os.chdir("../")
      # current_cwd = os.getcwd()
      print("\n\nstock_dataset_loc Parameter inserted.")
      print("\n\nstock_dataset Parameter inserted.")
      print("stock_dataset_loc = \n", self.stock_dataset_loc)
      print("self.stock_dataset.head() = \n", self.stock_dataset.head())
      print("\nself.stock_dataset.describe() = \n", self.stock_dataset.describe())

    except Exception as err:
      print(str(err))

  def sendTo_csv(self, dataframe, file_name):
    dataframe.to_csv("../" + file_name)
    print("")

  def analysis_to_chart(self, column):
    plt.figure(figsize=(10, 10))
    try:
      temp = self.stock_dataset[column]
    except Exception as err:
      print(str(err) , "not in column")
      return 0

    plt.title(str(self.stock_id) + " to Chart")
    plt.xlabel("Date")
    plt.ylabel(str(column))
    plt.plot(temp, label=column)
    plt.legend(loc="best")
    plt.show()

  def scaler_and_normalization(self, *x_data_col, y_data_col):
    x_dataframe_col = []
    for i in range(len(x_data_col)):
      x_dataframe_col.append(x_data_col[i])

    y_dataframe_col = [y_data_col]


    try:
      scaler_np = self.scaler.fit_transform(self.stock_dataset[x_dataframe_col])
      print("type(scaler_np) = \n", type(scaler_np))
      print("scaler_np.shape = ", scaler_np.shape)
      # print("scaler_np[0:10]= \n", scaler_np[0:10])

      self.x_scal_dataframe = pd.DataFrame(scaler_np, columns=x_dataframe_col)
      # print("x_scal_dataframe.head() = \n", self.x_scal_dataframe.head())
      print("\nx_scal_dataframe member variable inserted.\n")
      print("type(x_scal_dataframe) = ", type(self.x_scal_dataframe))
      print("x_scal_dataframe.shape = ", self.x_scal_dataframe.shape)
      self.y_scal_dataframe = pd.DataFrame(self.x_scal_dataframe[y_data_col], columns=y_dataframe_col)
      # print("y_scal_dataframe.head() = \n", self.y_scal_dataframe.head())
      print("\ny_scal_dataframe member variable inserted.\n")
      print("type(y_scal_dataframe) = ", type(self.y_scal_dataframe))
      print("y_scal_dataframe.shape = ", self.y_scal_dataframe.shape)

    except Exception as err:
      print(str(err), "Not in column")

  def timeSeriesDataCreation(self, x_dataframe, y_dataframe, window=30):
    X = []
    Y = []

    try:

      for i in range(len(x_dataframe)-window):
        x = x_dataframe[i : i+window] # 0:30, 1:31, 2:32 ...
        # print("x = \n", x)
        X.append(x)
        y = y_dataframe[i+window : (i+window)+1]
        # print("y = \n", y)
        Y.append(y)

      self.x_scal_numpy = np.array(X)
      print("\nx_scal_numpy member variable inserted\n")
      print("type(x_scal_numpy) = ", type(self.x_scal_numpy))
      print("x_scal_numpy.shape = ", self.x_scal_numpy.shape)
      # print("x_scal_numpy[0] = ", self.x_scal_numpy[0])

      self.y_scal_numpy = np.array(Y).reshape(-1, 1)
      print("\ny_scal_numpy member variable inserted\n")
      print("type(y_scal_numpy) = ", type(self.y_scal_numpy))
      print("y_scal_numpy.shape = ", self.y_scal_numpy.shape)
      # print("y_scal_numpy[0] = ", self.y_scal_numpy[0])

    except Exception as err:
      print(str(err))

  def train_test_Seperation(self, x_data_array, y_data_array, test_size=0.2, shuffle=False):

    try:

      print("\nx_train, x_test member variable Create.\n")
      self.x_train, self.x_test = sklearn.model_selection.train_test_split(x_data_array, test_size=test_size, shuffle=shuffle)
      print("type(x_train) = ", type(self.x_train))
      print("type(x_test) = ", type(self.x_test))
      print("x_train.shape = ", self.x_train.shape)
      print("x_test.shape = ", self.x_test.shape)

      print("\ny_train, y_test member variable Create.\n")
      self.y_train, self.y_test = sklearn.model_selection.train_test_split(y_data_array, test_size=test_size, shuffle=shuffle)
      print("type(y_train) = ", type(self.y_train))
      print("type(y_test) = ", type(self.y_test))
      print("y_train.shape = ", self.y_train.shape)
      print("y_test.shape = ", self.y_test.shape)

    except Exception as err:
      print(str(err))

  def stock_GRU_ModelCreation(self, x_train, y_train, units=128, optimizer=tf.keras.optimizers.Adam(), loss="mse", metrics=["mae"], md_earlyStop=True, dropout=0.0):
    try:

      _input = tf.keras.layers.Input(shape=x_train[0].shape)
      print("input ==> x_train[0].shape = ", x_train[0].shape)
      gru_cell = tf.keras.layers.GRU(units=units, activation='tanh', dropout=dropout)(_input)


      _output = tf.keras.layers.Dense(units=y_train.shape[1], activation='linear')(gru_cell)

      gru_model = tf.keras.models.Model(inputs=_input, outputs=_output)

      gru_model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
      if(md_earlyStop == True):
        print("\nmd_earlyStop member variable create.\n")
        self.md_earlyStop = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                             patience=5,
                                                             restore_best_weights=True)

      gru_model.summary()

      return gru_model

    except Exception as err:
      print(str(err))




class Stock_gruModel_next:


  def model_next(self, stock_id, stock_fileid, *pred_x_column, pred_y_column, # 000000, 0000000000000, wantpredict_column
                 window=30,
                 test_size=0.2,
                 shuffle=False,
                 units=128,
                 optimizer=tf.keras.optimizers.Adam(),
                 loss='mse',
                 metrics=["mae"],
                 epochs = 30,
                 md_earlyStop=True):

    stock_class = Stock_gruModel(stock_id, stock_fileid)

    # stock_class.analysis_to_chart(pred_y_column)

    stock_class.scaler_and_normalization(*pred_x_column, y_data_col=pred_y_column)

    # stock_class.sendTo_csv(stock_class.x_scal_dataframe, "confirm.csv")

    stock_class.timeSeriesDataCreation(stock_class.x_scal_dataframe,
                                              stock_class.y_scal_dataframe,
                                              window=window)

    stock_class.train_test_Seperation(stock_class.x_scal_numpy, stock_class.y_scal_numpy,
                                      test_size=test_size,
                                      shuffle=shuffle)

    stock_GRU_model = stock_class.stock_GRU_ModelCreation(stock_class.x_train, stock_class.y_train,
                                                          units=units,
                                                          optimizer=optimizer,
                                                          loss=loss,
                                                          metrics=metrics,
                                                          md_earlyStop=md_earlyStop,
                                                          dropout=0.0)

    hist = stock_GRU_model.fit(stock_class.x_train, stock_class.y_train,
                                         epochs=epochs,
                                         validation_data=(stock_class.x_test, stock_class.y_test),
                                         callbacks=stock_class.md_earlyStop)

    stock_GRU_model.save("./models/" + str(stock_id) + "/" + str(pred_y_column) + "_" + str(stock_id) + "_GRU_model.h5")

    print("\nmodel_saved\n", "./models/" + str(stock_id) + "/" + str(pred_y_column) + "_" + str(stock_id) + "_GRU_model.h5")

    print("current_cwd = ", os.getcwd())
    return 0

  def model_predict(self, stock_id, stock_fileid, *pred_x_column, pred_y_column, chart=True):
    try:
      print("\ncurrent_cwd = ", os.getcwd())

      pred_model = tf.keras.models.load_model("./models/" + stock_id + "/" + pred_y_column +"_"+ stock_id +"_GRU_model.h5")

      temp_class = Stock_gruModel(stock_id, stock_fileid)
      temp_class.scaler_and_normalization(*pred_x_column, y_data_col=pred_y_column)
      temp_class.timeSeriesDataCreation(temp_class.x_scal_dataframe, temp_class.y_scal_dataframe)
      temp_class.train_test_Seperation(temp_class.x_scal_numpy, temp_class.y_scal_numpy)

      pred = pred_model.predict(temp_class.x_test)
      # print(pred)

      if(chart == True):
        plt.figure(figsize=(12,6))
        plt.title("y_test, prediction matching")
        plt.xlabel("period")
        plt.ylabel(pred_y_column)
        plt.plot(temp_class.y_test, label="y_test")
        plt.plot(pred, label="prediction")
        plt.legend(loc="best")

        plt.savefig("./charts/" + str(stock_id) + "/" + str(pred_y_column) + "_" + str(stock_id) + "_charts.png")
        # plt.show()
      else:
        pass


    except Exception as err:
      print(str(err))


# stock_model = Stock_gruModel("035720", "1633505417210")
# # stock_model.analysis_to_chart("20MA")
# stock_model.scaler_and_normalization("5MA", "20MA", "60MA", "close", "PVT", "CCI", "Sonar", "RSI", y_data_col="close")
# stock_model.timeSeriesDataCreation(stock_model.x_scal_dataframe, stock_model.y_scal_dataframe)
# stock_model.train_test_Seperation(stock_model.x_scal_numpy, stock_model.y_scal_numpy)
# stock_gru_md = stock_model.stock_GRU_ModelCreation(stock_model.x_train, stock_model.y_train, units=256)
# stock_gru_md.fit(stock_model.x_train, stock_model.y_train, epochs=30, validation_data=(stock_model.x_test, stock_model.y_test), callbacks=stock_model.md_earlyStop)

