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
		aux=len(l)-5
		while(contador<len(codemirror)):
			if(l[:aux]==codemirror[contador][:aux]):
				aux1=aux1+[codemirror[contador]]
			contador+=1		
	return aux1
#retorna a velocidade de codificação do aluno
#se uma digitação demora mais de 5s ela é descartada
#foi feito uma lista de velocidade, que cada elemento representava a razão de números 'input' pelo tempo
#o valor retornado é uma espécie de média de digitação de todos os caracteres 'input'
#existem sequências com apenas 2 'input', era contabilizado em velocidade, com isso tirei os outliers
#o valor retornado era a soma dos elementos na lista_final, após remoção dos outliers, dividido pela quantidade de termos na lista
#o valor retornado era a velocidade de codificação por questão.
def velocidade(codemirror,turma,aluno,data):
	from datetime import datetime
	speed=[]
	f = '%Y-%m-%d %H:%M:%S.%f'
	for questão in data[0][1:]:
		cont=0
		flag=0
		while(cont<len(codemirror)):
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
				velocidade=[]
				flag2=0
				firstime=0
				digita=0
				s = '0-0-0 0:0:0.0'
				t = '0-0-0 0:0:0.0'
				arq=open('/home/user/teste/classes/2018-2/'+turma+'/users/'+aluno+'/codemirror/'+codemirror[cont])
				cont=len(codemirror)
				for linha in arq:
					if ':' in linha and '-' in linha and '.' in linha and '#' in linha and int(linha[7:9])<=31:
							if ('input' in linha and flag2==0):
									s=linha[:21]
									digita+=1
									flag2=1
							elif('input' in linha and flag2==1):	
								if(firstime==0):
									digita+=1
									firstime=1
									t=linha[:21]
									if (datetime.strptime(t, f) - datetime.strptime(s, f)).total_seconds()>5:
										digita=1
										firstime=0
										s=linha[:21]
										t = '0-0-0 0:0:0.0'
								elif(datetime.strptime(linha[:21], f) - datetime.strptime(t, f)).total_seconds()<=5:
									t=linha[:21]
									digita+=1
								else:
									if(s!=t and digita>=5):									
										velocidade+=[digita/(datetime.strptime(t, f) - datetime.strptime(s, f)).total_seconds()]
									digita=1								
									s=linha[:21]
									firstime=0
									t = '0-0-0 0:0:0.0'
							elif('input' not in linha and flag2==1):
								flag2=0
								if(t[0]!='0' and s!=t and digita>=5):
									velocidade+=[digita/(datetime.strptime(t, f) - datetime.strptime(s, f)).total_seconds()]
								digita=0
								firstime=0
								t = '0-0-0 0:0:0.0'
				elements = numpy.array(velocidade)
				mean = numpy.mean(elements, axis=0)
				sd = numpy.std(elements, axis=0)
				final_list = [x for x in velocidade if (x > mean - 2 * sd)]
				final_list = [x for x in final_list if (x < mean + 2 * sd)]
				mean=numpy.mean(final_list)
				if(len(final_list)>0):				
					speed+=[round(mean,2)]
				else:
					speed+=[0.0]
			cont+=1
		if(flag==0):
			speed+=[-1.0]
	return speed
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
			data+=[[aluno]+velocidade(codemirror,turma,aluno,data)]
			
	return data
			
import pandas
sessao=['s1','s2','s3','s4','s5','s6','s7']
for s in sessao:
	data=[['Id']]
	data=geral(data,s)
	df = pandas.DataFrame(data)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-2/keystroke_latency/'+s+'.csv', header=None, index=None)
