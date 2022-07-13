import os
from radon.raw import analyze
#retorna os elementos da lista sem repetição
def norep(lista):
	if len(lista)>0:
		if lista[0] in lista[1:]:
			return norep(lista[1:])
		else:
			return [lista[0]]+norep(lista[1:])
	else:
		return []
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
#retorna o 'data' com as questão que serão aplicadas
def questao(data,classes,s):
	listaux=[]
	for turma in classes:
		lista=os.listdir('/home/user/teste/classes/2018-2/'+turma+'/assessments/')
		lista.sort()
		lista=listsession(lista,turma,s)
		aux=[]
		for l in lista:
			arq=open('/home/user/teste/classes/2018-2/'+turma+'/assessments/'+l)
			b=arq.read()
			arq=open('/home/user/teste/classes/2018-2/'+turma+'/assessments/'+l)
			if('homework' in b):
				flag=0
				for linhas in arq:
					if 'total_exercises' in linhas:
						if int(linhas[22:-1])>0:
							flag=1
					elif(flag==1 and 'exercise' in linhas):
						aux+=[linhas[18:-1]]
		listaux+=[aux]
	contador=0
	listaux2=[]
	while(contador<len(listaux)):
		listaux2+=listaux[contador]
		contador+=1
	listaux2=norep(listaux2)
	aux=[]
	for elemento in listaux2:
		flag=0
		contador=len(listaux)-1
		while(contador>=0):
			if (elemento not in listaux[contador]):
				contador=0
				flag=1
			contador-=1
		if flag==0:
			aux+=[elemento]
	data[0]+=aux							
	return data
#a partir da lista reduzida pela função listsession,reduzimos as listas do codemirror,codes,scores do aluno
#ou seja, serão mantidas apenas os que pertencem a sessão da lista de exercícios que foi escolhida
def session(codemirror,lista,turma):
	aux1=[]
	for l in lista:
		contador=0
		aux=len(l)-5
		while(contador<len(codemirror)):
			if(l[:aux]==codemirror[contador][:aux]):
				aux1=aux1+[codemirror[contador]]
			contador+=1		
	return aux1
#razão entre caracteres colados e caracters digitados por questão
def copy(codemirror,turma,aluno,data):
	lista=[]
	for questão in data[0][1:]:
		cont=0
		flag=0
		while(cont<len(codemirror)):
			colados,digitado=0,0
			aux2=''
			flag2=0
			for elemento in codemirror[cont]:		
				if elemento=='_':
					flag2=1
				elif flag2==1:
					if elemento!='.':				
						aux2+=elemento
					else:
						flag2=2
			if(questão==aux2):
				flag=1
				arq=open('/home/user/teste/classes/2018-2/'+turma+'/users/'+aluno+'/codemirror/'+codemirror[cont])
				cont=len(codemirror)
				for linha in arq:
					if 'inpute' in linha:
						digitado+=1
					elif 'paste' in linha:
						flag2=0
						b=''
						for l in linha:
							if(flag2==0 and l=='['):
								flag2=1
							elif(flag2==1 and l!=']'):
								b+=l
							elif(flag2==1 and l==']'):
								break
						colados+=len(b)-2	
				#perguntar do filipe
				if(digitado==0):
					digitado=1
				lista+=[round(colados/digitado,2)]
			cont+=1
		if(flag==0): 
			lista+=[-1.0]
	return lista
#retorna uma lista em  formato pronto para uso em .csv
def geral(data,s):
	classes=os.listdir('/home/user/teste/classes/2018-2')
	classes.sort()
	if len(classes[0])>3:
		classes=classes[1:]
	data=questao(data,classes,s)
	for turma in classes:
		listadealunos=os.listdir('/home/user/teste/classes/2018-2/'+turma+'/users/')
		listadealunos.sort()
		lista=os.listdir('/home/user/teste/classes/2018-2/'+turma+'/assessments/')
		lista.sort()
		lista=listsession(lista,turma,s)
		for aluno in listadealunos:
			codemirror=os.listdir('/home/user/teste/classes/2018-2/'+turma+'/users/'+aluno+'/codemirror/')
			codemirror.sort()
			codemirror=session(codemirror,lista,turma)
			print(aluno)
			data+=[[aluno]+copy(codemirror,turma,aluno,data)]
			
	return data
			
import pandas
sessao=['s1','s2','s3','s4','s5','s6','s7']
for s in sessao:
	data=[['Id']]
	data=geral(data,s)
	df = pandas.DataFrame(data)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-2/copy/'+s+'.csv', header=None, index=None)
