import os
from radon.raw import analyze
import numpy
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
		while(contador<len(codemirror)):
			if(l[:len(l)-5]==codemirror[contador][:len(l)-5]):
				aux1=aux1+[codemirror[contador]]
			contador+=1		
	return aux1
#diz se a questão gerou mais 50 linhas de log ou não
def plagio(codemirror,turma,aluno,data):
	linhas=[]
	lista2=[]
	for elemento in codemirror:
		digitados,colados=0,0
		log=open('/home/user/teste/classes/2018-2/'+turma+'/users/'+aluno+'/codemirror/'+elemento)
		for linha in log:
			if('input' in linha):
				digitados+=1
			elif('paste' in linha):
				flag=0
				b=''
				for l in linha:
					if(flag==0 and l=='['):
						flag=1
					elif(flag==1 and l!=']'):
						b+=l
					elif(flag==1 and l==']'):
						break
				colados=len(b)-2
		if digitados==0:
			lista2+=[colados]
		else:
			lista2+=[colados/digitados]	
	elements = numpy.array(lista2)
	mean = numpy.mean(elements, axis=0)
	sd = numpy.std(elements, axis=0)
	final_list = [x for x in lista2 if (x > mean - 2 * sd)]
	final_list = [x for x in final_list if (x < mean + 2 * sd)]
	mean = numpy.mean(final_list, axis=0)
	sd = numpy.std(final_list, axis=0)
	for questão in data[0][1:]:
		cont=0
		flag=0
		while(cont<len(codemirror)):
			aux=0
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
				digitados,colados=0,0
				arq=open('/home/user/teste/classes/2018-2/'+turma+'/users/'+aluno+'/codemirror/'+codemirror[cont])
				cont=len(codemirror)
				for linha in arq:
					aux+=1
					if('input' in linha):
						digitados+=1
					elif('paste' in linha):
						flag2=0
						b=''
						for l in linha:
							if(flag2==0 and l=='['):
								flag2=1
							elif(flag2==1 and l!=']'):
								b+=l
							elif(flag2==1 and l==']'):
								break
						colados=len(b)-2	
				if aux>50:		
					if(digitados>0):
						if (colados/digitados)>(mean+2*sd):
							linhas+=[0]
						else:
							linhas+=[1]
					else:
						linhas+=[0]
				else:
					linhas+=[0]
			cont+=1
		if(flag==0):
			linhas+=[-1]
	return linhas
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
			data+=[[aluno]+plagio(codemirror,turma,aluno,data)]
			
	return data
			
import pandas
sessao=['s1','s2','s3','s4','s5','s6','s7']
for s in sessao:
	data=[['Id']]
	data=geral(data,s)
	df = pandas.DataFrame(data)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-2/plagio/'+s+'.csv', header=None, index=None)
