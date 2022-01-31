
import sys
import os
import tensorflow as tf
import matplotlib.pyplot as plt
import datetime

sys.path.append(sys.path[0] + "\stock_gru_model.py")
# print("stock_gru_model_spawn :: sys.path = \n", sys.path)
# print("os.getcwd() = ", os.getcwd())

import stock_gru_model

models_cwd = os.getcwd() + "\\models\\"
models_dirList = os.listdir(models_cwd)

# print("sys.argv[0] : ", sys.argv[1])
# print("dirList :: \n", models_dirList)

if str(sys.argv[1]) in models_dirList and len(os.listdir(models_cwd + sys.argv[1])) > 1:

    # print("true\n")
    print("stock_gru_model_spwan : models_cwd :: \n", models_cwd)

    load_model = tf.keras.models.load_model(models_cwd + str(sys.argv[1]) + "\\" + str(sys.argv[4]) + "_" + str(sys.argv[1]) + "_GRU_model.h5")
    print(models_cwd + str(sys.argv[1]) + "\\" + str(sys.argv[4]) + "_" + str(sys.argv[1]) + "_GRU_model.h5")
    print("stock_gru_model_spwan : load_model :: ", load_model)

    train_model_datas = stock_gru_model.Stock_gruModel(sys.argv[1], sys.argv[2])
    param3 = []
    param3 = str.split(sys.argv[3], ",")
    print("stock_gru_model_spwan : param3 :: ", param3)

    train_model_datas.scaler_and_normalization(*param3, y_data_col=sys.argv[4])
    # print(str(models_dirList[i]) +" : "+ str(uploads_filename) + " : train_model_datas.x_scal_numpy :: \n", train_model_datas.x_scal_dataframe)
    # print(str(models_dirList[i]) + " : " + str(uploads_filename) + " : train_model_datas.y_scal_numpy :: \n",
    #       train_model_datas.y_scal_dataframe)
    train_model_datas.timeSeriesDataCreation(train_model_datas.x_scal_dataframe, train_model_datas.y_scal_dataframe)
    # print(str(models_dirList[i]) +" : "+ str(uploads_filename) + " : train_model_datas.x_scal_numpy :: \n", train_model_datas.x_scal_numpy)
    # print(str(models_dirList[i]) +" : "+ str(uploads_filename) + " : train_model_datas.y_scal_numpy :: \n", train_model_datas.y_scal_numpy)

    train_model_datas.train_test_Seperation(train_model_datas.x_scal_numpy, train_model_datas.y_scal_numpy)

    # print(load_Models[k])
    md_earlyStop = tf.keras.callbacks.EarlyStopping(monitor="val_loss", restore_best_weights=True, patience=5)
    load_model.fit(train_model_datas.x_train, train_model_datas.y_train,
                       validation_data=(train_model_datas.x_test, train_model_datas.y_test),
                       epochs=30, callbacks=md_earlyStop)



    pred = load_model.predict(train_model_datas.x_test)
    date_title = datetime.datetime.now()

    plt.figure(figsize=(12, 6))
    plt.title(str(date_title) + " y_test, prediction matching")
    plt.xlabel("period")
    plt.ylabel(sys.argv[4])
    plt.plot(train_model_datas.y_test, label="y_test")
    plt.plot(pred, label="prediction")
    plt.legend(loc="best")

    plt.savefig(os.getcwd() + "/charts/" + str(sys.argv[1]) + "/" + str(sys.argv[4]) + "_" + str(sys.argv[1]) + "_charts.png")
    # plt.show()

    load_model.save(models_cwd + str(sys.argv[1]) + "\\" + str(sys.argv[4]) + "_" + str(sys.argv[1]) + "_GRU_model.h5")

else:



    # stock_model = stock_gru_model.Stock_gruModel_next()
    # stock_model.model_next("035720", "1633509629571", "5MA", "20MA", "60MA", "close", "PVT", "Sonar", "RSI", pred_y_column="close",units= 256)
    # stock_model.model_predict("035720", "1633509629571", "5MA", "20MA", "60MA", "close", "PVT", "Sonar", "RSI", pred_y_column="close")

    pred_h5 = stock_gru_model.Stock_gruModel_next()
    param_3 = []
    param_3 = str.split(sys.argv[3], ',')
    print("param_3 = ", param_3)
    pred_h5.model_next(sys.argv[1], sys.argv[2], *param_3, pred_y_column=sys.argv[4], units=256) #[stock_id], [file_name], [train_columns] [predict_column]
    pred_h5.model_predict(sys.argv[1], sys.argv[2], *param_3, pred_y_column=sys.argv[4]) #[stock_id], [file_name], [train_columns] [predict_column]

