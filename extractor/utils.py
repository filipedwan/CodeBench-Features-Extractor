#!/usr/bin/env python3
import datetime
import numpy as np
import itertools

prediction_columns = [
    'logins',
    'comments',
    'blank_line',
    'lloc',
    'count_if',
    'count_loop',
    'count_var',
    'syntax_grade',
    'log_rows',
    'deleted_coef',
    'writed_coef',
    'pasted_coef',
    'focus_time',
    'writed_time',
    'early_often',
    'error_coef',
    'submit_coef',
    'jadud',
    'amount_of_change',
    'procastination',
    'correct',
    'incorrect',
    'blank',
    'homework_grade',
    'exam_grade'
]

codebench_dataset = f'http://codebench.icomp.ufam.edu.br/dataset/'
codebench_base_zip = f'{codebench_dataset}files'

keysWordsAssessments = [
    'weight', 
    'type', 
    'start', 
    'end', 
    'total_exercises', 
    'course id', 
    'course name'
]
keysWordsUsers = [
    'course id', 
    'course name'
]

def convert_2d_list(array):
    return list(itertools.chain.from_iterable(array))


def convertToDate(string):
    newArr = string.split()
    date, hours = newArr[0], newArr[1]
    [year, month, day], [hour, minutes, second] = date.split('-'), hours.split(':')
    return datetime.datetime(
                    int(year), 
                    int(month), 
                    int(day), 
                    int(hour), 
                    int(minutes), 
                    int(second.split('.')[0])
                )

def convertArrToDateArray(array):
    for i in range(len(array)):
        array[i] = convertToDate(array[i])
    return array

def convertToSeconds(s, t, f, type=True):
    diff_seconds = (datetime.datetime.strptime(t, f) - datetime.datetime.strptime(s, f)).total_seconds()
    if (diff_seconds > 300 and type):
        return 0
    return diff_seconds

def condition(line):
    return ('=' in line) and ('==' not in line) and ('>' not in line) and ('<' not in line) and ('!' not in line) and ('#' not in line)

def conditionExecution(line):
    return '-- EXECUTION TIME:' not in line and  '-- OUTPUT:' not in line and 'Traceback (most recent call last)' not in line and 'File "XXXX"' not in line

def checkIfIsHour(time):
    try:
        data = convertToDate(time)
        return True
    except:
        return False

def transformVariables(string):
    removeKeys = ['(', ')', '{', '}', '[', ']']
    for key in removeKeys:
        string = string.replace(key, '')
    return string

def inTime(start, end, line):
    time = line.split('#')[0]
    if (checkIfIsHour(time)):
        time = convertToDate(time)
        return time >= start and time <= end
    else:
        return False

def prazo(start, end, f):
    return int((datetime.datetime.strptime(end,f)-datetime.datetime.strptime(start,f)).total_seconds() / (24 * 60 * 60))

def processArrayProcastination(vetor):
    vetor = [vetor[i] * (i + 1) for i in range(len(vetor))]
    return sum(vetor) 

def countDiffs(keysCodeAfter, keysCodeBefore):
    diffs = 0
    usedKeys = []
    for key in keysCodeBefore:
        usedKeys.append(key)
        try:
            seq1 = keysCodeBefore[key]
        except:
            seq1 = ''
        try:
            seq2 = keysCodeAfter[key]   
        except:
            seq2 = ''
        diffs = diffs + sum(1 for a, b in zip(seq1, seq2) if a != b) + abs(len(seq1) - len(seq2))
    for key in keysCodeAfter:
        if (key not in usedKeys):
            diffs = diffs + len(keysCodeAfter[key])
    return diffs

def filterGrade(arq):
    arq = [' '.join(element.split()[1:]) for element in arq if 'grade' in element or 'correct' in element or 'blank' in element]
    return [element.split(':')[-1].strip().replace('\n', '') for element in arq] 

def transformArray(array):
    helper_dict = {}
    for arr in array:
        for i in range(len(arr)):
            try:
                helper_dict.update({i: helper_dict[i] + [float(arr[i])]})
            except:
                helper_dict.update({i: [float(arr[i])]})
    avgArray = []
    for key in helper_dict:
        if (key in (7, 9, 10, 11, 15, 16, 17, 18)):
            avgArray.append(np.sum(helper_dict[key]))
            continue
        elif (key in (14, 19, 20)):
            avgArray.append(np.average(helper_dict[key]) ** 0.5)
            continue
        avgArray.append(np.average(helper_dict[key]))
    return avgArray

def transformGradesArray(array):
    correct = incorrect = blank = 0
    h_grade, e_grade = [0], [0]
    for arr in array:
        correct = correct + int(arr[1])
        incorrect = incorrect + int(arr[2])
        blank = blank + int(arr[3])
        if 'homework' in arr:
            h_grade.append(float(arr[0]))
        else:
            e_grade.append(float(arr[0]))
    if len(h_grade) > 1:
        h_grade = h_grade[1:]
    if len(e_grade) > 1:
        e_grade = e_grade[1:]
    return [correct, incorrect, blank, round(np.average(h_grade), 2), round(np.average(e_grade), 2)]

def finalMetricsTransformation(metrics, grade_metrics):
    correct, incorrect, blank = grade_metrics[0], grade_metrics[1], grade_metrics[2]
    questions = correct + incorrect + blank
    metrics[7] = metrics[7] / (2 * questions)
    if (metrics[7] > 1):
        metrics[7] = 1
    grade_metrics[0] = correct / questions
    grade_metrics[1] = incorrect / questions
    grade_metrics[2] = blank / questions
    deleted, writed, pasted = metrics[9], metrics[10], metrics[11]
    if (deleted + writed + pasted == 0):
        pasted = 1
    metrics[9] = deleted / (deleted + writed + pasted)
    metrics[10] = writed / (deleted + writed + pasted)
    metrics[11] = pasted / (deleted + writed + pasted)
    tested, submited, wrong_submit, syntax_error = metrics[15], metrics[16], metrics[17], metrics[18]
    if (tested + submited > 0):
        metrics[15] = (syntax_error) / (tested + submited)
    else:
        metrics[15] = 1
    if (submited > 0):
        metrics[16] = (submited - wrong_submit) / (submited)
    else:
        metrics[16] = 0
    metrics = metrics[:17] + metrics[19:]
    return metrics, grade_metrics
