import sys
import os

import tensorflow as tf
os.chdir("C:\\Users\\HJH_notePC\\Desktop\\node_stock_home")
print("os.getcwd() : ",os.getcwd())
sys.path.append(os.getcwd() + "\\stock_gru_model.py")
print("sys.path : \n", sys.path)
print("os.getcwd() : ", os.getcwd())
import stock_gru_model

# process_class = stock_gru_model.Stock_gruModel(sys.argv[1], sys.argv[2]);
# print("process_class.stock_id :: ", process_class.stock_id)
# print("process_class.file_name :: ", process_class.file_name)

models_cwd = os.getcwd() + "\\models\\"
uploads_cwd = os.getcwd() + "\\uploads\\"
models_dirList = os.listdir(models_cwd)

print("dirList :: \n", models_dirList)



for i in range(len(models_dirList)):
    load_Models = []
    model_cols = []
    uploads_filename = None
    dir_In_list = os.listdir(models_cwd + models_dirList[i])

    for j in range(len(dir_In_list)):
        load_Models.append(tf.keras.models.load_model(models_cwd + models_dirList[i] + "/" + dir_In_list[j]))
        model_cols.append(str(dir_In_list[j]).split('_')[0])

        # print("model_cols[" + str(j) + "] :: " + model_cols[j])

        uploads_filename = os.listdir(uploads_cwd + models_dirList[i])[1].split('_')[2].split('.')[0]
        # print("uploads_filename :: ", uploads_filename)

    print(models_dirList[i], " dir_In_list :: \n", dir_In_list)
    print("model_cols :: ", model_cols)
    print("uploads_filename :: ", uploads_filename)
    print("load_Models :: ", load_Models)

    train_model_datas = stock_gru_model.Stock_gruModel(models_dirList[i], uploads_filename)

    for k in range(len(load_Models)):

        train_model_datas.scaler_and_normalization(*model_cols, y_data_col=model_cols[k])
        # print(str(models_dirList[i]) +" : "+ str(uploads_filename) + " : train_model_datas.x_scal_numpy :: \n", train_model_datas.x_scal_dataframe)
        # print(str(models_dirList[i]) + " : " + str(uploads_filename) + " : train_model_datas.y_scal_numpy :: \n",
        #       train_model_datas.y_scal_dataframe)
        train_model_datas.timeSeriesDataCreation(train_model_datas.x_scal_dataframe, train_model_datas.y_scal_dataframe)
        # print(str(models_dirList[i]) +" : "+ str(uploads_filename) + " : train_model_datas.x_scal_numpy :: \n", train_model_datas.x_scal_numpy)
        # print(str(models_dirList[i]) +" : "+ str(uploads_filename) + " : train_model_datas.y_scal_numpy :: \n", train_model_datas.y_scal_numpy)

        train_model_datas.train_test_Seperation(train_model_datas.x_scal_numpy, train_model_datas.y_scal_numpy)

        # print(load_Models[k])
        md_earlyStop = tf.keras.callbacks.EarlyStopping(monitor="val_loss", restore_best_weights=True, patience=5)
        load_Models[k].fit(train_model_datas.x_train, train_model_datas.y_train,
                        validation_data=(train_model_datas.x_test, train_model_datas.y_test),
                        epochs=30, callbacks=md_earlyStop)

        load_Models[k].save(models_cwd + "/" + str(models_dirList[i]) + "/" + str(model_cols[k]) + "_" + str(models_dirList[i]) + "_GRU_model.h5")


    load_Models = []
    model_cols = []
    uploads_filename = None


