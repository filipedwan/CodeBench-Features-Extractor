#!/usr/bin/env python3
import mysql.connector

class MysqlDB:
    def __init__(self, host='localhost', user='', password=''):
        self.user = user
        self.host = host
        self.password = password
        self.db = None
    
    def connectWithMysql(self):
        self.db = mysql.connector.connect(host=self.host, user=self.user, password=self.password)

    def connectWithDb(self, database=''):
        self.database = database
        self.db = mysql.connector.connect(host=self.host, 
                                          user=self.user, 
                                          password=self.password, 
                                          database=self.database)    
        self.cursor = self.db.cursor()

    def createDatabase(self, database=''):
        self.database = database
        self.db.cursor().execute(f'CREATE DATABASE IF NOT EXISTS {self.database}')

    def createTable(self, table='', keys={}, pKey='id', ref={}, rKey='id'):
        string = f'CREATE TABLE IF NOT EXISTS {table} ('
        for key in keys:
            string = string + f'{key} {keys[key]},'
        string = f'{string[:-1]}, primary key({pKey}))'
        for key in ref:
            string = f'{string[:-1]}, foreign key({key}) references {ref[key]}({rKey}))'
        self.db.cursor().execute(string)

    def insertInto(self, table, values):
        string = f'INSERT INTO {table} ('
        for value in values:
            string = string + f'{value},'
        string = f'{string[:-1]}) VALUES('
        vals = ()
        for value in values:
            vals = vals + (values[value], )
            string = string + '%s' + ','
        string = f'{string[:-1]})'
        try:
            self.db.cursor().execute(string, vals)
            self.db.commit()
        except:
            return None
            
    def updateInto(self, table="", values={}, filter={}):
        string = f'UPDATE {table} SET '
        vals = ()
        for value in values:
            string = string + f'{value}=%s,'
            vals = vals + (values[value], )
        string = f'{string[:-1]} WHERE '
        for value in filter:
            string = string + f'{value}=%s AND '
            vals = vals + (filter[value], )
        string = f'{string[:-5]}'
        try:
            self.db.cursor().execute(string, vals)
            self.db.commit()
        except:
            print("Something went wrong")

    def getAndResults(self, table, values, order=''):
        string = f'SELECT * FROM {table}'
        for value in values:
            if ('WHERE' not in string and values != {}):
                string = string + ' WHERE'
            string = f'{string} {value}={values[value]} AND'
        if (values != {}):
            string = ' '.join(string.split()[:-1])
        if (len(order) > 0):
            string = f'{string} ORDER BY {order}'
        return self.getAndResultsByQuery(string)

    def getAndResultsByQuery(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
        

"""
db = mysqlDB('localhost', 'root', 'abc123')
db.connectWithMysql()
database = 'icompML'
#db.createDatabase(database)
db.connectWithDb(database)
db.createTable('users', {
    'id': 'int not null auto_increment',
    'user_id': 'int not null',
    'class_id': 'int not null',
    'year': 'int not null'
})
db.createTable('classes', {
    'id': 'int not null',
    'semester': 'varchar(6) not null'
})
db.createTable('sessions', {
    'id': 'int not null auto_increment',
    'user_id': 'int not null',
    'session_number': 'int not null',
    'pb': 'decimal(2, 2) not null'
}, fKey='user_id', tableRef='users', keyRef='id')
db.createTable('assessments', {
    'id': 'INT NOT NULL',
    'class_id': 'INT NOT NULL',
    'type': 'VARCHAR(20) NOT NULL',
    'start': "DATETIME NOT NULL",
    "end": "DATETIME NOT NULL",
    "weight": "INT NOT NULL",
    "total_exercises": "INT NOT NULL"
}, fKey="class_id", tableRef="classes", keyRef="id")
db.createTable('users', {
    'id': 'INT NOT NULL',
    'class_id': 'INT NOT NULL',
    'course_id': 'INT NOT NULL',
    'course_name': "VARCHAR(50) NOT NULL"
}, fKey="class_id", tableRef="classes", keyRef="id")
db.createTable('users', {
    'id': 'INT NOT NULL',
    'class_id': 'INT NOT NULL',
    'course_id': 'INT NOT NULL',
    'course_name': "VARCHAR(50) NOT NULL"
}, fKey="class_id", tableRef="classes", keyRef="id", pKey="id, class_id")
db.createTable('questions', {
    'id': 'INT NOT NULL',
    'assessment_id': 'INT NOT NULL',
    'class_id': 'INT NOT NULL',
    'user_id': 'INT NOT NULL',
    'logins': 'INT NOT NULL DEFAULT 0',
    'comments': 'INT NOT NULL DEFAULT 0',
    'blank_line': 'INT NOT NULL DEFAULT 0',
    'lloc': 'INT NOT NULL DEFAULT 0',
    'sloc': 'INT NOT NULL DEFAULT 0',
    'count_if': 'INT NOT NULL DEFAULT 0',
    'count_loop': 'INT NOT NULL DEFAULT 0',
    'count_var': 'INT NOT NULL DEFAULT 0',
    'syntax_grade': 'INT NOT NULL DEFAULT 0',
    'log_rows': 'INT NOT NULL DEFAULT 0',
    'count_delete': 'INT NOT NULL DEFAULT 0',
    'writed': 'INT NOT NULL DEFAULT 0',
    'pasted': 'INT NOT NULL DEFAULT 0',
    'focus_time': 'FLOAT NOT NULL DEFAULT 0',
    'writed_time': 'FLOAT NOT NULL DEFAULT 0',
    'deleted_time': 'FLOAT NOT NULL DEFAULT 0',
    'pasted_time': 'FLOAT NOT NULL DEFAULT 0',
    'procastination': 'INT NOT NULL DEFAULT 0',
    'tested': 'INT NOT NULL DEFAULT 0',
    'submited': 'INT NOT NULL DEFAULT 0',
    'is_rigth': 'INT(1) NOT NULL DEFAULT 0',
    'wrong_submit': 'INT NOT NULL DEFAULT 0',
    'grade': 'INT(3) NOT NULL DEFAULT 0',
    'syntax_error': 'INT NOT NULL DEFAULT 0',
    'jadud': 'INT NOT NULL DEFAULT 0',
    'amount_of_change': 'INT NOT NULL DEFAULT 0'
}, ref={
        'assessment_id': 'assessments', 
        'class_id': 'classes',
        'user_id': 'users'
        }, 
    rKey="id", 
    pKey="id, assessment_id, class_id, user_id")
db.createTable('grades', {
    'assessment_id': 'INT NOT NULL',
    'class_id': 'INT NOT NULL',
    'user_id': 'INT NOT NULL',
    'grade': 'FLOAT NOT NULL',
    'correct': 'INT NOT NULL',
    'incorrect': 'INT NOT NULL',
    'blank': 'INT NOT NULL'
}, ref={
        'assessment_id': 'assessments', 
        'class_id': 'classes',
        'user_id': 'users'
        }, 
    rKey="id", 
    pKey="assessment_id, class_id, user_id")
db.createTable('final_grade', {
    'class_id': 'INT NOT NULL',
    'user_id': 'INT NOT NULL',
    'grade': 'FLOAT NOT NULL'
}, ref={
        'class_id': 'classes',
        'user_id': 'users'
        }, 
    rKey="id", 
    pKey="class_id, user_id")
db.createTable('predictions', {
    'user_id': 'INT NOT NULL',
    'class_id': 'INT NOT NULL',
    'session': 'INT NOT NULL DEFAULT 1',
    'logins': 'DOUBLE NOT NULL DEFAULT 0',
    'comments': 'DOUBLE NOT NULL DEFAULT 0',
    'blank_line': 'DOUBLE NOT NULL DEFAULT 0',
    'lloc': 'DOUBLE NOT NULL DEFAULT 0',
    'sloc': 'DOUBLE NOT NULL DEFAULT 0',
    'count_if': 'DOUBLE NOT NULL DEFAULT 0',
    'count_loop': 'DOUBLE NOT NULL DEFAULT 0',
    'count_var': 'DOUBLE NOT NULL DEFAULT 0',
    'syntax_grade': 'DOUBLE NOT NULL DEFAULT 0',
    'log_rows': 'DOUBLE NOT NULL DEFAULT 0',
    'count_delete': 'DOUBLE NOT NULL DEFAULT 0',
    'writed': 'DOUBLE NOT NULL DEFAULT 0',
    'pasted': 'DOUBLE NOT NULL DEFAULT 0',
    'focus_time': 'DOUBLE NOT NULL DEFAULT 0',
    'writed_time': 'DOUBLE NOT NULL DEFAULT 0',
    'deleted_time': 'DOUBLE NOT NULL DEFAULT 0',
    'pasted_time': 'DOUBLE NOT NULL DEFAULT 0',
    'procastination': 'DOUBLE NOT NULL DEFAULT 0',
    'tested': 'DOUBLE NOT NULL DEFAULT 0',
    'submited': 'DOUBLE NOT NULL DEFAULT 0',
    'is_rigth': 'DOUBLE NOT NULL DEFAULT 0',
    'wrong_submit': 'DOUBLE NOT NULL DEFAULT 0',
    'syntax_error': 'DOUBLE NOT NULL DEFAULT 0',
    'jadud': 'DOUBLE NOT NULL DEFAULT 0',
    'amount_of_change': 'DOUBLE NOT NULL DEFAULT 0',
    'correct': 'DOUBLE NOT NULL DEFAULT 0',
    'incorrect': 'DOUBLE NOT NULL DEFAULT 0',
    'blank': 'DOUBLE NOT NULL DEFAULT 0',
    'homework_grade': 'DOUBLE NOT NULL DEFAULT 0',
    'exam_grade': 'DOUBLE NOT NULL DEFAULT 0',
    'passed_probability': 'FLOAT NOT NULL DEFAULT 0',
    'grade_regression': 'FLOAT NOT NULL DEFAULT 0'
}, ref={
        'class_id': 'classes',
        'user_id': 'users'
        }, 
    rKey="id", 
    pKey="class_id, user_id, session")
"""
