
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, precision_score, accuracy_score, recall_score, f1_score,mean_absolute_error, mean_squared_error, r2_score, mean_squared_log_error


def train_model(X_train = None, y_train=None, X_val=None, y_val=None, model=None, regression=True):
    if X_train is None:
        raise ValueError("X_train: Expecting a DataFrame/ numpy2d array, got 'None'")
    
    if y_train is None:
        raise ValueError("y_train: Expecting a Series/ numpy1D array, got 'None'")

    if X_val is None:
        raise ValueError("X_val: Expecting a Series/ numpy1D array, got 'None'")
    
    if y_val is None:
        raise ValueError("y_val: Expecting a Series/ numpy1D array, got 'None'")
    
    if model is None:
        raise ValueError("estimator: Expecting estimator, got 'None'")
    
    pred, acc, f1, precision, recall, mae, mse, msle, r2,confusion_mat = 0, 0, 0, 0, 0, 0, 0, 0, 0,None

    if regression:
      model.fit(X_train, y_train)
      pred = model.predict(X_val)
      mae = mean_absolute_error(y_val, pred)
      mse = mean_squared_error(y_val, pred)
      # msle = mean_squared_log_error(y_val, pred)
      r2 = r2_score(y_val, pred)
      print("Mean Absolute Error: ", round(mae, 5))
      print("Mean Squared Error: ", round(mse, 5))
      # print("Mean Squared Log Error: ", round(msle, 5))
      print("R-squared Error:  ", round(r2, 5))
      print("*" * 100)
    else:
      model.fit(X_train, y_train)
      pred = model.predict(X_val)
      acc = accuracy_score(y_val, pred)
      f1 = f1_score(y_val, pred)
      precision = precision_score(y_val, pred)
      recall = recall_score(y_val, pred)
      confusion_mat = confusion_matrix(y_val, pred)
      print("Accuracy is ", round(acc * 100))
      print("F1 score is ", round(f1 * 100))
      print("Precision is ", round(precision * 100))
      print("Recall is ", round(recall * 100))
      print("*" * 100)
      print("confusion Matrix")
      print('                 Score positive    Score negative')
      print('Actual positive    %6d' % confusion_mat[0,0] + '             %5d' % confusion_mat[0,1])
      print('Actual negative    %6d' % confusion_mat[1,0] + '             %5d' % confusion_mat[1,1])
      print('')

def return_csv(model=None, X_train=None, y_train=None, X_val=None,sample_submission_df=None,target_name=None,file_location_name=None):
    if X_train is None:
        raise ValueError("X_train: Expecting a DataFrame/ numpy2d array, got 'None'")
    
    if y_train is None:
        raise ValueError("y_train: Expecting a Series/ numpy1D array, got 'None'")

    if X_val is None:
        raise ValueError("X_val: Expecting a Series/ numpy1D array, got 'None'")

    if model is None:
        raise ValueError("model: Expecting Estimator, got 'None'")
    
    if sample_submission_df is None:
        raise ValueError("sample_submission_df: Expecting String, got 'None'")

    if target_name is None:
        raise ValueError("taget_name: Expecting String, got 'None'")
    
    if file_location_name is None:
        raise ValueError("file_location_name: Expecting String, got 'None'")
    
    model.fit(X_train, y_train)
    pred = model.predict(X_val)
    sub = sample_submission_df
    sub[target_name] = pred
    sub.to_csv(file_location_name, index=False)

