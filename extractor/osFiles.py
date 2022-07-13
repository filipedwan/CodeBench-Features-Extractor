#!/usr/bin/env python3
import os

class OsFiles:
    def __init__(self, path=''):
        self.path = path
    

    def setPath(self, path):
        self.path = path


    staticmethod
    def getArqs(path="./"):
        return os.listdir(path)


    staticmethod
    def deleteArq(path=None):
        if (path is None):
            return
        os.remove(path)


    staticmethod
    def checkIsInside(keys=[], element=None):
        for key in keys:
            if key in element:
                return True
        return False

    staticmethod
    def transform2Obj(string=""):
        new_arr = string.split(":")
        key, value = new_arr[0], ':'.join(new_arr[1:])
        key, value = '_'.join(key.replace('-', '').strip().split()), value.strip()
        try:
            return {key: int(value)}
        except:
            return {key: value}

