#!/usr/bin/env python3
from db import mysqlDB
from utils import *

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
classes, columns = db.getAndResults('classes', {}), [i[0] for i in db.cursor.description]
keys = {}
for classe in classes:
    assessments, columns = db.getAndResults('assessments', {'class_id': classe[0]}, order='start'), [i[0] for i in db.cursor.description]
    count = 1
    flag = False
    for assessment in assessments:
        if ('homework' in assessment):
            db.updateInto('assessments', {'session': count}, {'id': assessment[0], 'class_id': assessment[1]})
            flag = True
        else:
            if (not flag):
                break
            db.updateInto('assessments', {'session': count}, {'id': assessment[0], 'class_id': assessment[1]})
            count = count + 1
            if (count > 7):
                count = 7
