import os
def geral(data):
	classes=os.listdir('/home/user/teste/classes/2018-2')
	classes.sort()
	if len(classes[0])>3:
		classes=classes[1:]
	for turma in classes:
		listadealunos=os.listdir('/home/user/teste/classes/2018-2/'+turma+'/users/')
		listadealunos.sort()
		for aluno in listadealunos:
			grades=os.listdir('/home/user/teste/classes/2018-2/'+turma+'/users/'+aluno+'/grades/')
			grades.sort()
			nota=0.0
			if 'final_grade.data' in grades:
					arq=open('/home/user/teste/classes/2018-2/'+turma+'/users/'+aluno+'/grades/final_grade.data')
					nota=float(arq.readline())
			print(aluno)
			data+=[[aluno]+[round(nota,2)]]
			
	return data
import pandas
data=[['Id','Media_final']]
data=geral(data)	
df = pandas.DataFrame(data)
df.to_csv('/home/user/codigos/tabelas_por_questão/2018-2/media_final/dados.csv', header=None, index=None)
