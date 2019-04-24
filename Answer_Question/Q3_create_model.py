# -*- coding: utf-8 -*-
'''
Created on 2019年3月29日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
from xgboost.compat import SKLEARN_INSTALLED
'''
第三题
(3) 综合考虑运输车辆的安全、效率和节能，并结合自然气象条件与道路状况等情况， 
为运输车辆管理部门建立行车安全的综合评价指标体系与综合评价模型。 
'''
#建模
import sklearn
import pandas as pd

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import LabelEncoder

# load dataset
df= pd.read_csv("../Result/result3/data/A00001_total.csv")
y=df[['acce','daisu_hire','danger_rate','danger_score','dece','max_daisu','off_flip','over_speed','tierd_drive']]
x=df.drop(columns=['acce','daisu_hire','danger_rate','danger_score','dece','max_daisu','off_flip','over_speed','tierd_drive'])
x =pd.get_dummies( x)#热编码
x_len=len(x.columns)
y_len=len(y.columns)
X = x.values.astype(float)
Y = y.values.astype(float)

# # encode class values as integers
# encoder = LabelEncoder()
# encoded_Y = encoder.fit_transform(Y)
# # convert integers to dummy variables (one hot encoding)
# dummy_y = np_utils.to_categorical(encoded_Y)

# define model structure
def baseline_model():
    model = Sequential()
#     model.add(Embedding(500, 250,input_length = x_len, dropout =0.2))
    model.add(Dense(output_dim=20, input_dim=x_len, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(output_dim=y_len, input_dim=20, activation='softmax'))
#     model.add(LSTM(200, dropout_U =0.2, dropout_W =0.2))

#     model.add(Dense(y_len,activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#     model.summary()
    return model
estimator = KerasClassifier(build_fn=baseline_model, nb_epoch=40, batch_size=256)
# splitting data into training set and test set. If random_state is set to an integer, the split datasets are fixed.
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=0)
estimator.fit(X_train, Y_train)

# make predictions
pred = estimator.predict(X_test)

# # inverse numeric variables to initial categorical labels
# init_lables = encoder.inverse_transform(pred)

# k-fold cross-validate
seed = 42
np.random.seed(seed)
kfold = KFold(n_splits=10, shuffle=True, random_state=seed)
results = cross_val_score(estimator, X, Y, cv=kfold)
print(results)