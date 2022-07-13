#!/usr/bin/env python3
"""
imports
"""
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import shap

from db import mysqlDB
from utils import prediction_columns, transformArray, transformGradesArray, convert_2d_list, finalMetricsTransformation

from imblearn.under_sampling import TomekLinks
#from imblearn.over_sampling import SMOTE

from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold

#from tensorflow.compat.v1.keras.backend import get_session
#from tensorflow.keras.utils import to_categorical
#from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
#tf.compat.v1.disable_v2_behavior()
"""
Db Connection
"""
db = mysqlDB('localhost', 'root', 'abc123')
db.connectWithMysql()
database = 'icompML'
db.connectWithDb(database)
"""
Get Data
"""
users, columns = db.getAndResults('final_grade', {}), [i[0] for i in db.cursor.description]
"""
Some definitions
"""
sc = MinMaxScaler()
split = StratifiedKFold(n_splits=10, random_state=42, shuffle=True)
tl = TomekLinks(return_indices=True, sampling_strategy='majority')
y = 0
sessions = [1, 2, 3, 4, 5, 6, 7]

for session in sessions:
    data = [['user_id', 'class_id'] + prediction_columns + ['label', 'final_grade']]
    for user in users:
        if (list(user)[-1] >= 5 ):
            y = 1
        else:
            y = 0
        inTuple = '(1)'
        if session > 1:
            inTuple = f'{tuple(sessions[:session])}'
        AVG, SUM = 'AVG', 'SUM'
        query_columns = (f'{AVG}(logins) as logins,' + 
                        f'{SUM}(comments) as comments,' +
                        f'{SUM}(blank_line) as blank_line,' +
                        f'{SUM}(lloc) as lloc,' +
                        f'{SUM}(count_if) as count_if,' +
                        f'{SUM}(count_loop) as count_loop,' + 
                        f'{SUM}(count_var) as count_var,' +
                        f'{SUM}(syntax_grade) as syntax_grade,' +
                        f'{SUM}(log_rows) as log_rows,' + 
                        f'{SUM}(count_delete) as count_delete,' +
                        f'{SUM}(writed) as writed,' +
                        f'{SUM}(pasted) as pasted,' + 
                        f'{SUM}(focus_time) / 60 as focus_time,' +
                        f'{SUM}(writed_time) / 60 as writed_time,' +
                        f'{SUM}(early_often) as early_often,' +
                        f'{SUM}(tested) as tested,' + 
                        f'{SUM}(submited) as submited,' +
                        f'{SUM}(wrong_submit) as wrong_submit,' +
                        f'{SUM}(syntax_error) as syntax_error,'+
                        f'{SUM}(jadud) as jadud,' + 
                        f'{SUM}(amount_of_change) as amount_of_change,' + 
                        f'{SUM}(procastination) as procastination')


        query = f'SELECT {query_columns} FROM questions INNER JOIN assessments WHERE assessments.id = questions.assessment_id AND assessments.session in {inTuple} AND questions.user_id = {user[1]} and questions.class_id = {user[0]} AND assessments.type = "homework" and datediff(assessments.end, assessments.start) <= 14 group by questions.assessment_id'
        metrics, columns = db.getAndResultsByQuery(query), [i[0] for i in db.cursor.description]
        
        if len(metrics) == 0:
            continue
        
        metrics = [list(metric) for metric in metrics]
        metrics = transformArray(metrics)

        query_columns = (f'{AVG}(grades.grade) as grade,'+
                         f'{SUM}(grades.correct) as correct,' +
                         f'{SUM}(grades.incorrect) as incorrect,' +
                         f'{SUM}(grades.blank) as blank,' +
                         f'assessments.type as type')
        
        query = f'SELECT {query_columns} FROM grades INNER JOIN assessments WHERE assessments.id = grades.assessment_id AND assessments.session in {inTuple} AND grades.user_id = {user[1]} and grades.class_id = {user[0]} group by assessments.type'
        grade_metrics, columns = db.getAndResultsByQuery(query), [i[0] for i in db.cursor.description]
        
        if len(grade_metrics) == 0:
            continue
        
        grade_metrics = [list(metric) for metric in grade_metrics]
        grade_metrics = transformGradesArray(grade_metrics)
        metrics, grade_metrics = finalMetricsTransformation(metrics, grade_metrics)
        data.append([user[1], user[0]] + metrics + grade_metrics + [y, user[-1]])
    pd.DataFrame(data).to_csv(f'session{session}.csv', header=None, index=None)
    # df = pd.DataFrame(data[1:])
    # X, y = df.iloc[:,2:-2].values, df.iloc[:, -2].values
    # users_indexes, y_grades = df.iloc[:, :2].values, df.iloc[:, -1].values
    # X = sc.fit_transform(X)
    # vetor_X_train, vetor_y_train, vetor_X_test = [], [], [] 
    # y_test, y_grades_train, users_test = [], [], []
    # for train_index, val_index in split.split(X, y):
    #     vetor_X_train.append(X[train_index])
    #     vetor_X_test.append(X[val_index])
    #     vetor_y_train.append(y[train_index])
    #     y_grades_train.append(y_grades[train_index])
    #     users_test.append(users_indexes[val_index])
    #     y_test.append(y[val_index])
    # contador, predictions, y_test = 0, [], convert_2d_list(y_test)
    # while (contador < len(vetor_X_train)):
    #     X_train, X_test, y_train = vetor_X_train[contador], vetor_X_test[contador], vetor_y_train[contador]
    #     X_train, y_train, id_tl = tl.fit_sample(X_train, y_train)
    #     #X_train, y_train = smote.fit_sample(X_train, y_train)
        
    #     estimator = RandomForestClassifier(
    #                                     bootstrap=True, 
    #                                     criterion="gini", 
    #                                     max_features=0.3, 
    #                                     min_samples_leaf=11, 
    #                                     min_samples_split=8, 
    #                                     n_estimators=100
    #                                     )

    #     #estimator = KerasClassifier(build_fn=baseline_model, epochs=400, batch_size=30)
    #     estimator.fit(X_train, y_train)
    #     predictions.append(estimator.predict(X_test))
    #     y_prob = estimator.predict_proba(X_test)

    #     explainer = shap.TreeExplainer(estimator)
    #     shap_values = explainer.shap_values(X_test,check_additivity=False)

    #     estimator = RandomForestRegressor(
    #                                     bootstrap=True, 
    #                                     criterion="mse", 
    #                                     max_features=0.3, 
    #                                     min_samples_leaf=11, 
    #                                     min_samples_split=8, 
    #                                     n_estimators=100
    #                                     )

    #     y_train = y_grades_train[contador]
    #     y_train = [y_train[i] for i in range(len(y_train)) if i in id_tl]

    #     estimator.fit(X_train, y_train)
    #     grades_predictions = estimator.predict(X_test)
        
    #     for i in range(len(users_test[contador])):
    #         keys = {
    #             'user_id': int(users_test[contador][i][0]),
    #             'class_id': int(users_test[contador][i][1]),
    #             'session': session,
    #             'passed_probability': float(y_prob[i][1]),
    #             'grade_regression': float(grades_predictions[i]),
    #         }
    #         current_shap_values = shap_values[-1][i]
    #         for j in range(len(current_shap_values)):
    #             keys.update({prediction_columns[j]: current_shap_values[j]})
    #         if (db.insertInto('predictions', keys) is None):
    #             continue
    #     del estimator
    #     contador = contador + 1
    # predictions = convert_2d_list(predictions)
    # print(classification_report(y_test, predictions))


