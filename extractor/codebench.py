#!/usr/bin/env python3
"""
Imports
"""
import tarfile

from utils import codebench_dataset, codebench_base_zip
from osFiles import OsFiles

class CodeBenchData():
    def __init__(self):
        self.baseUrl = codebench_dataset
        self.zipUrl = codebench_base_zip
        self.chunk_size = 128


    def checkClass(self):
        arqs = OsFiles.getArqs('data/')
        arqs = [arq for arq in arqs if '-' in arq and '.' not in arq]
        return len(arqs) > 0


    def doRequest(self):
        if(self.checkClass()):
            return
        arqs = OsFiles.getArqs('data/')
        arqs = [file for file in arqs if 'data.tar.gz' in file]
        if (len(arqs) == 1):
            arqs = OsFiles.getArqs('data/')
            arqs = [file for file in arqs if 'cb_dataset' in file]
            if (not arqs):
                self.unzipData()
                self.doRequest()
            else:
                self.unzipAll(arqs)
                self.deleteZips()
                return
        response = requests.get(codebench_dataset).text
        response = [line.strip() for line in response.split('\n') if 'cb_dataset_v' in line]
        response = [line.split('files/')[-1].split('"')[0] for line in response]
        response.sort()
        response = response[-1]
        self.downloadZip(response)
        self.doRequest()


    def deleteZips(self):
        arqs = OsFiles.getArqs('data/')
        arqs = [file for file in arqs if '.tar.gz' in file]
        for arq in arqs:
            OsFiles.deleteArq(f'data/{arq}')


    def downloadZip(self, path, save_path='data/data.tar.gz'):
        current_url = f'{self.zipUrl}/{path}'
        r = requests.get(current_url, stream=True)
        with open(save_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=self.chunk_size):
                fd.write(chunk)
        return True
    

    def unzipData(self, path='data/data.tar.gz'):
        if path.endswith("tar.gz"):
            tar = tarfile.open(path, "r:gz")
            tar.extractall('data/')
            tar.close()
        elif path.endswith("tar"):
            tar = tarfile.open(path, "r:")
            tar.extractall('data/')
            tar.close()


    def unzipAll(self, arqs):
        for arq in arqs:
            self.unzipData(f'data/{arq}')

