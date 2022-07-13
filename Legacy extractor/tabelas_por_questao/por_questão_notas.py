import os
from radon.raw import analyze
#reduz a lista de exercícios de uma turma, deixando apenas aquelas da sessão desejada, no caso, sessão 1
#a sessão 1 trabalha com os primeiros contatos do aluno com o codebench, e o primeiro módulo dos assuntos, ao todo são 7 módulos
#reduz o tamanho da lista para a as listas da sessão desejada
def listsession(lista,turma,sessao):
	aux=[]
	for l in lista:
		arq=open('/home/user/teste/classes/2018-2/'+turma+'/assessments/'+l)
		arq.readline()
		a=arq.readline()
		if sessao=='s1':
			if '1' in a or ('0' in a and ('2' not in a and '3'not in a and '4'not in a and '5'not in a and '6'not in a and '7' not in a)):
				aux=aux+[l]
		else:
			if sessao[-1] in a:
				aux=aux+[l]
	return aux
#a partir da lista reduzida pela função listsession,reduzimos as listas do codemirror,codes,grades do aluno
#ou seja, serão mantidas apenas os que pertencem a sessão da lista de exercícios que foi escolhida
def session(grades,lista,turma):
	aux1=[]
	for l in lista:
		cont=0
		aux=len(l)-5
		while(cont<len(grades)):
			if(l[:aux]==grades[cont][:aux]):
				aux1=aux1+[grades[cont]]
			cont+=1		
	return aux1
#retorna a média das notas da lista de 'homework', e a nota do 'exam'
def score(grades,lista,turma,aluno):	
	homework,exam,tamanho,tamanho2=0.0,0.0,0,0
	for l in lista:
		aux2=len(l)-5
		arq=open('/home/user/teste/classes/2018-2/'+turma+'/assessments/'+l)
		b=arq.read()
		if('homework' in b):
			cont=0
			tamanho+=1
			while(cont<len(grades)):
				if(l[:aux2]==grades[cont][:aux2]):
					arq2=open('/home/user/teste/classes/2018-2/'+turma+'/users/'+aluno+'/grades/'+grades[cont])
					cont=len(grades)
					aux=arq2.readline()
					homework+=float(aux[19:-1])
				cont+=1		
		elif('exam' in b):
			cont=0
			tamanho2+=1
			while(cont<len(grades)):
				if(l[:aux2]==grades[cont][:aux2]):
					arq2=open('/home/user/teste/classes/2018-2/'+turma+'/users/'+aluno+'/grades/'+grades[cont])
					cont=len(grades)
					aux=arq2.readline()					
					exam+=float(aux[19:-1])
				cont+=1
	if(tamanho==0):
		tamanho=1	
	if(tamanho2==0):
		tamanho2=1		
	return[round(exam/tamanho2,2),round(homework/tamanho,2)]
#retorna uma lista em  formato pronto para uso em .csv
def geral(data,s):
	classes=os.listdir('/home/user/teste/classes/2018-2')
	classes.sort()
	if len(classes[0])>3:
		classes=classes[1:]
	for turma in classes:
		listadealunos=os.listdir('/home/user/teste/classes/2018-2/'+turma+'/users/')
		listadealunos.sort()
		lista=os.listdir('/home/user/teste/classes/2018-2/'+turma+'/assessments/')
		lista.sort()
		lista=listsession(lista,turma,s)
		for aluno in listadealunos:
			grades=os.listdir('/home/user/teste/classes/2018-2/'+turma+'/users/'+aluno+'/grades/')
			grades.sort()
			grades=session(grades,lista,turma)
			print(aluno)
			data+=[[aluno]+score(grades,lista,turma,aluno)]
			
	return data
			
import pandas
sessao=['s1','s2','s3','s4','s5','s6','s7']
for s in sessao:
	data=[['Id','exam_grade_codebench','exercises_list_grade']]
	data=geral(data,s)
	df = pandas.DataFrame(data)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-2/notas/'+s+'.csv', header=None, index=None)
