#!/usr/bin/env python3
"""
Imports
"""
import requests

from codebench import CodeBenchData
from db import MysqlDB
from osFiles import OsFiles
from getDataQuestions import TransformData

from utils import keysWordsAssessments, keysWordsUsers
"""
Codebench Class Definition
"""
code = CodeBenchData()
code.doRequest()
"""
Connection with database
"""
db = MysqlDB('localhost', 'root', 'Your Password')
db.connectWithMysql()
database = 'icompML'
db.connectWithDb(database)
"""
Generate all data needed
"""
files = OsFiles.getArqs('data')
for file in files:
    classes = OsFiles.getArqs(f'./data/{file}')
    for clas in classes:
        db.insertInto('classes', {
            "id": int(clas),
            "semester": str(file)
        })
        assessments = OsFiles.getArqs(f'data/{file}/{clas}/assessments')
        for assessment in assessments:
            arq = open(f'data/{file}/{clas}/assessments/{assessment}')
            arq = arq.read()
            arq = [OsFiles.transform2Obj(element) for element in arq.split('\n') if OsFiles.checkIsInside(keysWordsAssessments, element)]
            keys = {'id': int(assessment.split('.data')[0]), 'class_id': int(clas)}
            for key in arq:
                keys.update(key)
            db.insertInto('assessments', keys)
        users = OsFiles.getArqs(f'data/{file}/{clas}/users')
        for user in users:
            arq = open(f'data/{file}/{clas}/users/{user}/user.data').read()
            arq = [OsFiles.transform2Obj(element) for element in arq.split('\n') if OsFiles.checkIsInside(keysWordsUsers, element)]
            keys = {'id': int(user), 'class_id': int(clas)}
            for key in arq:
                keys.update(key)
            db.insertInto('users', keys)
            path = f'data/{file}/{clas}/users/{user}'
            arqs = OsFiles.getArqs(path)
            tD = TransformData(path, arqs, int(user), int(clas), db)
            tD.generateData()
            tD.generateGrades()
            tD.generateFinalGrade() 
