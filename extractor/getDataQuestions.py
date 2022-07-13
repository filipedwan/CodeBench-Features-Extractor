#!/usr/bin/env python3
import os
from utils import *
from radon.raw import analyze

class TransformData:
    def __init__(self, path='', arqs=[], user=0, clas=0, db=None):
        self.path = path
        self.arqs = arqs
        self.user = user
        self.clas = clas
        self.db = db


    def getLogins(self, keys=None):
        data = self.db.getAndResults('assessments', keys)[0]
        keys.pop('id')
        keys.update({'session': data[-1]})
        data = self.db.getAndResults('assessments', keys, 'start')
        start = data[0][3]
        data = self.db.getAndResults('assessments', keys, 'end')
        end = data[-1][4]
        arq = open(f'{self.path}/logins.log').read()
        arq = [element.split('#')[0] for element in arq.split('\n') if 'login' in element]
        arq = convertArrToDateArray(arq)
        arq = [element for element in arq if element >= start and element <= end]
        return len(arq)


    def getMetricsByCode(self, code=""):
        hulp = {
            'comments': 0,
            'blank_line': 0,
            'lloc': 0,
            'count_if': 0,
            'count_loop': 0,
            'count_var': 0,
            'syntax_grade': 0
        }
        all_variables = []
        arq = open(f'{self.path}/codes/{code}.py')
        try:
            a = analyze(arq.read())
            hulp['comments'] = a[3]
            hulp['blank_line'] = a[5]
            hulp['lloc'] = a[1]
            hulp['syntax_grade'] = 1
        except Exception as e:
            hulp['syntax_grade'] = 0
        arq = open(f'{self.path}/codes/{code}.py')
        for line in arq:
            if (('if' in line or 'else' in line) and ':' in line):
                hulp['count_if'] = hulp['count_if'] + 1
            elif (('while' in line or 'for' in line) and ":" in line):
                hulp['count_loop'] = hulp['count_loop'] + 1
            elif condition(line):
                variables = line.strip().split('=')[0].split(',')
                variables = [transformVariables(variable) for variable in variables]
                for variable in variables:
                    if variable not in all_variables:
                        all_variables.append(variable)
        hulp['count_var'] = len(all_variables)
        return hulp


    def getLogInformations(self, codemirror="", keys={}):
        data = self.db.getAndResults('assessments', keys)[0]
        start, end = data[3], data[4]
        log = open(f'{self.path}/codemirror/{codemirror}.log')
        keys = {
            'log_rows': 0,
            'count_delete': 0,
            'writed': 0,
            'pasted': 0,
            'focus_time': 0,
            'writed_time': 0,
            'deleted_time': 0,
            'pasted_time': 0,
            'early_often': 0,
            'procastination': 0
        }
        f = '%Y-%m-%d %H:%M:%S.%f'
        flag, inputFlag, pasteFlag, deleteFlag = 0, False, False, False
        log = [line for line in log.read().split('\n') if inTime(start, end, line)]
        keys['log_rows'] = len(log)
        vectorPrazo = [a * 0 for a in range(prazo(f'{start}.0', f'{end}.0', f))]
        for linha in log:
            if('#change#' in linha):
                if (keys['procastination'] == 0):
                    time = linha.split('#')[0]
                    keys['procastination'] = keys['procastination'] + convertToSeconds(f'{start}.0', time, f, False)
                currentTime = linha.split('#')[0]
                indice = prazo(f'{start}.0', currentTime, f)
                if (indice < len(vectorPrazo)):
                    vectorPrazo[indice] += 1
                else:
                    keys['early_often'] = keys['early_often'] + 1
            if('delete' in linha or 'backspace' in linha):
                keys['count_delete'] = keys['count_delete'] + 1
                if (not deleteFlag):
                    deleteFlag = True
                    startDelete = linha.split('#')[0]
                elif (flag == 1 and deleteFlag):
                    endDelete = linha.split('#')[0]
                    keys['deleted_time'] = keys['deleted_time'] + convertToSeconds(startDelete, endDelete, f)
                    startDelete = endDelete
            if('input' in linha):
                keys['writed'] = keys['writed'] + 1
                if (not inputFlag):
                    inputFlag = True
                    startInput = linha.split('#')[0]
                elif (flag == 1 and inputFlag):
                    endInput = linha.split('#')[0]
                    writedSeconds = convertToSeconds(startInput, endInput, f)
                    if (writedSeconds < 5):
                        keys['writed_time'] = keys['writed_time'] + writedSeconds
                    startInput = endInput
            if('paste' in linha):
                flagPaste = 0
                b = ''
                for l in linha:
                    if (flagPaste == 0 and l == '['):
                        flagPaste = 1
                    elif (flagPaste == 1 and l != ']'):
                        b += l
                    elif (flagPaste == 1 and l == ']'):
                        break
                keys['pasted'] = keys['pasted'] + len(b)-2
                if (not pasteFlag):
                    pasteFlag = True
                    startPaste = linha.split('#')[0]
                elif (flag == 1 and pasteFlag):
                    endPaste = linha.split('#')[0]
                    keys['pasted_time'] = keys['pasted_time'] + convertToSeconds(startPaste, endPaste, f)
                    startPaste = endPaste
            if 'focus' in linha and flag == 0:
                s = linha.split('#')[0]
                flag = 1
            elif flag == 1:
                t = linha.split('#')[0]
                keys['focus_time'] = keys['focus_time'] + convertToSeconds(s, t, f)
                if ('blur' in linha):
                    flag = 0
                    s = '0-0-0 0:0:0.0'
                    t = '0-0-0 0:0:0.0'
                else:
                    s = t
        if (len(vectorPrazo) > 0):
            keys.update({'early_often': processArrayProcastination(vectorPrazo)})
        return keys


    def getProcastinationInformation(self, codemirror="", keys={}):
        data = self.db.getAndResults('assessments', keys)[0]
        start, end = data[3], data[4]
        log = open(f'{self.path}/codemirror/{codemirror}.log')
        keys = {
            'procastination': 0
        }
        f = '%Y-%m-%d %H:%M:%S.%f'
        log = [line for line in log.read().split('\n') if inTime(start, end, line)]
        for linha in log:
            if('#change#' in linha):
                if (keys['procastination'] == 0):
                    time = linha.split('#')[0]
                    keys['procastination'] = keys['procastination'] + convertToSeconds(f'{start}.0', time, f, False)
                    return keys
        return keys


    def getExecutionsInformations(self, execution="", keys={}):
        data = self.db.getAndResults('assessments', keys)[0]
        start, end = data[3], data[4]
        log = open(f'{self.path}/executions/{execution}.log',
                   encoding='latin-1')
        keys = {
            'tested': 0,
            'submited': 0,
            'is_rigth': 0,
            'wrong_submit': 0,
            'grade': 0,
            'syntax_error': 0,
            'jadud': 0,
            'amount_of_change': 0
        }
        flag, currentError, inTime, codeFlag = 0, None, False, False
        keysCodeBefore, keysCodeAfter, lineCode, afterCodeFlag = {}, {}, 1, False
        for line in log:
            if ('== TEST' in line):
                inTime = False
                date = line.split(' (')[-1].replace(')', '')
                date = convertToDate(date)
                if (date >= start and date <= end):
                    keys['tested'] = keys['tested'] + 1
                    inTime = True
            elif ('== SUBMITION' in line):
                inTime = False
                date = line.split(' (')[-1].replace(')', '')
                date = convertToDate(date)
                if (date >= start and date <= end):
                    keys['submited'] = keys['submited'] + 1
                    flag = 1
                    inTime = True
            elif ('-- ERROR:' in line and inTime):
                keys['syntax_error'] = keys['syntax_error'] + 1
            elif ("-- GRADE:" in line and flag == 1):
                flag = 2
            elif (flag == 2):
                flag = 0
                if ('100%' in line):
                    keys['is_rigth'] = 1
                    keys['wrong_submit'] = keys['submited'] - 1
                    keys['grade'] = 100
                    keys.update({'syntax_grade': 2})
                    return keys
                else:
                    current_grade = int(line.strip().split('%')[0])
                    keys['grade'] = current_grade
            elif ('Error:' in line and inTime):
                if (currentError is None):
                    currentError = line
                else:
                    keys['jadud'] = keys['jadud'] + 3
                    if (line.split(':')[0] == currentError.split(':')[0]):
                        keys['jadud'] = keys['jadud'] + 5
                        if (line == currentError):
                            keys['jadud'] = keys['jadud'] + 3
                    currentError = line
            elif ('-- CODE:' in line and inTime):
                codeFlag = True
                if (keysCodeBefore != {}):
                    afterCodeFlag = True
            elif (codeFlag):
                if (conditionExecution(line)):
                    if (keysCodeAfter == {} and not afterCodeFlag):
                        keysCodeBefore.update({f'line{lineCode}': line})
                        lineCode = lineCode + 1
                    else:
                        keysCodeAfter.update({f'line{lineCode}': line})
                        lineCode = lineCode + 1
                else:
                    codeFlag, afterCodeFlag, lineCode = False, False, 1
            elif (not codeFlag and keysCodeAfter != {} and keysCodeBefore != {}):
                keys['amount_of_change'] = keys['amount_of_change'] + countDiffs(keysCodeAfter, keysCodeBefore)
                keysCodeBefore = keysCodeAfter
                keysCodeAfter = {}
        keys['wrong_submit'] = keys['submited']
        return keys


    def generateData(self):
        arqsCodemirror = os.listdir(f'{self.path}/codemirror')
        keysArrayCodemirror = []
        for codemirror in arqsCodemirror:
            array = codemirror.split('_')
            assessment, question = array[0], array[1].split('.')[0]
            keysArrayCodemirror.append({
                                        'assessment_id': int(assessment),
                                        'id': int(question),
                                        'user_id': self.user,
                                        'class_id': self.clas
                                        })
        for keyArrayCodemirror in keysArrayCodemirror:
            id = f'{keyArrayCodemirror["assessment_id"]}_{keyArrayCodemirror["id"]}'
            keys = {
                'id': keyArrayCodemirror['assessment_id'],
                'class_id': keyArrayCodemirror['class_id']
            }
            logins = self.getLogins(keys)
            keyArrayCodemirror.update({'logins': logins})
            keyArrayCodemirror.update(self.getMetricsByCode(id))
            keyArrayCodemirror.update(self.getLogInformations(id, keys))
            keyArrayCodemirror.update(self.getExecutionsInformations(id, keys))
            
            self.db.insertInto('questions', keyArrayCodemirror)


    def generateGrades(self):
        grades = os.listdir(f'{self.path}/grades/')
        for grade in grades:
            keys = {}
            try:
                assessment = int(grade.split('.')[0])
            except:
                continue
            keys.update({
                        'assessment_id': assessment,
                        'user_id': self.user,
                        'class_id': self.clas
                        })
            arq = open(f'{self.path}/grades/{grade}').read().split('\n')
            [grade, correct, incorret, blank] = filterGrade(arq)
            keys.update({
                        'grade': grade,
                        'correct': correct,
                        'incorrect': incorret,
                        'blank': blank})
            self.db.insertInto('grades', keys)


    def generateFinalGrade(self):
        keys = {}
        keys.update({
                    'user_id': self.user,
                    'class_id': self.clas
                    })
        try:
            grade = open(f'{self.path}/grades/final_grade.data').read()
            keys.update({'grade': grade})
            self.db.insertInto('final_grade', keys)
        except:
            print(f'{self.user} in {self.clas} do not have final grade')


    def updateProcastination(self):
        arqsCodemirror = os.listdir(f'{self.path}/codemirror')
        keysArrayCodemirror = []
        for codemirror in arqsCodemirror:
            array = codemirror.split('_')
            assessment, question = array[0], array[1].split('.')[0]
            keysArrayCodemirror.append({
                                        'assessment_id': int(assessment),
                                        'id': int(question),
                                        'user_id': self.user,
                                        'class_id': self.clas
                                        })
        for keyArrayCodemirror in keysArrayCodemirror:
            filter = keyArrayCodemirror
            id = f'{keyArrayCodemirror["assessment_id"]}_{keyArrayCodemirror["id"]}'
            keys = {
                'id': keyArrayCodemirror['assessment_id'],
                'class_id': keyArrayCodemirror['class_id']
            }
            self.db.updateInto('questions', self.getProcastinationInformation(id, keys), filter)
