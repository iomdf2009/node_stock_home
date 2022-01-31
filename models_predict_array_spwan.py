import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sys
import os



sys.path.append(sys.path[0] + "\models_predict_array.py")
# print("sys.path = ", sys.path)
# print("os.getcwd() = ", os.getcwd())

import models_predict_array

# models_cwd = os.getcwd() + "\\models\\"
# models_dirList = os.listdir(models_cwd)
#
#
# print("dirList :: \n", models_dirList)


col_array = sys.argv[3].split(',')

# for i in range(len(col_array)):
#     print("col_array["+ str(i) +"] : " + col_array[i])

ma = models_predict_array.Model_array(sys.argv[1], sys.argv[2], *col_array)
# ma = Model_array("035720", "1633828014471")
# ma.models_array_insert("5MA", "20MA", "60MA", "PVT")

ma.close_Match_NorData()

ma.lastData_filter(ma.stock_id, ma.file_name, *col_array)

print("last_Data.shape : ", ma.lastData.shape)
print(ma.lastData)

# ma.load_Model()
# print(ma.gru_Models)


predict_numpy = ma.model_Predict_Array(sys.argv[1], sys.argv[4], ma.lastData)

predict_df = pd.DataFrame(predict_numpy, columns=col_array)

# print("predict_df = \n", predict_df)
# print("predict_df.describe() \n", predict_df.describe())



conv_pred_df = ma.norclose_Convert_close(predict_df)

ma.conv_DataFrame_to_Chart(conv_pred_df)

