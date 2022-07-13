import re
import os
from radon.raw import analyze
import numpy
#reduz a lista de exercícios de uma turma, deixando apenas aquelas da sessão desejada, no caso, sessão 1
#a sessão 1 trabalha com os primeiros contatos do aluno com o codebench, e o primeiro módulo dos assuntos, ao todo são 7 módulos
#reduz o tamanho da lista para a as listas da sessão desejada
def listsession(lista,turma,sessao):
	aux=[]
	for l in lista:
		arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/assessments/'+l)
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
def session(codemirror,codes,grades,executions,lista,turma):
	aux1,aux2,aux3,aux4=[],[],[],[]
	for l in lista:
		aux=len(l)-5
		contador=0
		while(contador<len(codemirror)):
			ax=''
			for elemento in codemirror[contador]:
				if elemento!='_':
					ax+=elemento
				else:
					break
			if(l[:aux]==ax):
				aux1=aux1+[codemirror[contador]]
			contador+=1
		contador=0
		while(contador<len(codes)):
			ax=''
			for elemento in codes[contador]:
				if elemento!='_':
					ax+=elemento
				else:
					break
			if(l[:aux]==ax):
				aux2=aux2+[codes[contador]]
			contador+=1
		contador=0
		while(contador<len(executions)):
			ax=''
			for elemento in executions[contador]:
				if elemento!='_':
					ax+=elemento
				else:
					break
			if(l[:aux]==ax):
				aux4=aux4+[executions[contador]]
			contador+=1
		cont=0
		while(cont<len(grades)):
			ax=''
			for elemento in grades[cont]:
				if elemento!='.':
					ax+=elemento
				else:
					break
			if(l[:aux]==ax):
				aux3=aux3+[grades[cont]]
			cont+=1			
	return [aux1,aux2,aux3,aux4]




#retorna a razão das questões que geraram mais de 50 linhas log, por todas as questões feitas pelo aluno.
def plagio(lista,codemirror,turma,aluno):
	num1,num2=0,0
	lista2=[]
	for elemento in codemirror:
		digitados,colados=0,0
		log=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/codemirror/'+elemento)
		for linhas in log:
			if('input' in linhas):
				digitados+=1
			elif('paste' in linhas):
				flag=0
				b=''
				for l in linhas:
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
	for l in lista:
		arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/assessments/'+l)
		b=arq.read()
		aux=len(l)-5
		if('homework' in b):
			cont=0
			while(cont<len(codemirror)):
				if(l[:aux]==codemirror[cont][:aux]):
					linhaslog=0
					num2+=1
					digitados,colados=0,0
					log=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/codemirror/'+codemirror[cont])
					for linhas in log:
						linhaslog+=1
						if('input' in linhas):
							digitados+=1
						elif('paste' in linhas):
							flag=0
							b=''
							for l in linhas:
								if(flag==0 and l=='['):
									flag=1
								elif(flag==1 and l!=']'):
									b+=l
								elif(flag==1 and l==']'):
									break
							colados=len(b)-2	
					if(linhaslog>50):
						num1+=1
						if(digitados>0):
							if (colados/digitados)>(mean+2*sd):
								num1-=1
						else:
							if colados>0:
								num1-=1
				cont+=1	
	if(num2>0):
		return round(num1/num2,2)
	else:
		return 0.0





#retorna a média das notas da lista de 'homework', e a nota do 'exam'
def score(grades,lista,turma,aluno):	
	homework,exam,tamanho,tamanho1=0,0,0,0
	for l in lista:
		aux=len(l)-5
		arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/assessments/'+l)
		b=arq.read()
		if('homework' in b):
			cont=0
			tamanho+=1
			while(cont<len(grades)):
				if(l[:aux]==grades[cont][:aux]):
					arq2=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/grades/'+grades[cont])
					aux=arq2.readline()
					homework+=float(aux[19:-1])
					cont=len(grades)
				cont+=1		
		elif('exam' in b):
			cont=0
			tamanho+=1
			while(cont<len(grades)):
				if(l[:aux]==grades[cont][:aux]):
					arq2=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/grades/'+grades[cont])
					aux=arq2.readline()					
					exam+=float(aux[19:-1])
					cont=len(grades)
				cont+=1
	if(tamanho==0):
		tamanho=1	
	if tamanho1==0:
		tamanho1=1		
	return[round(exam/tamanho1,2),round(homework/tamanho,2)]
#retorna uma média de logins por lista de 'homework', são somados todos os logins do aluno durante os prazos da lista divido pela quantidade de listas
def logins(lista,turma,aluno):
	cont,cont2=0,0
	for l in lista:
		arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/assessments/'+l)
		b=arq.read()
		arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/assessments/'+l)
		arq.readline()
		arq.readline()
		arq.readline()
		arq.readline()
		start=arq.readline()[12:18]
		end=arq.readline()[10:26]
		if('homework' in b):
			cont2+=1
			arq2=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/logins.log')
			for linhas in arq2:
				if(linhas[:19]>=start and linhas[:19]<=end):
					if('login' in linhas):
						cont+=1
	if cont2==0:
		return 0.0	
	return int(cont/cont2)
#retorna a razão dos caracteres apagados pelas quantidades de lista de 'homework', e a razão entre todas as linhas de log geradas nas questões da lista
#pela quantidade de questões que o aluno fez.
def deleteaux(lista,turma,aluno,codemirror):
	delete,linhalog=[],[]
	cont=0
	while(cont<len(codemirror)):
		linhaslog_cont,delete_cont=0,0
		log=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/codemirror/'+codemirror[cont])
		for linha in log:
			linhaslog_cont+=1
			if('delete' in linha or 'backspace' in linha):
				delete_cont+=1
		delete+=[delete_cont]
		linhalog+=[linhaslog_cont]
		cont+=1	
	elements = numpy.array(delete)
	mean = numpy.mean(elements, axis=0)
	sd = numpy.std(elements, axis=0)
	final_list = [x for x in delete if (x > mean - 2 * sd)]
	final_list = [x for x in final_list if (x < mean + 2 * sd)]
	delete=final_list
	meandel = numpy.mean(delete, axis=0)
	elements = numpy.array(linhalog)
	mean = numpy.mean(elements, axis=0)
	sd = numpy.std(elements, axis=0)
	final_list = [x for x in linhalog if (x > mean - 2 * sd)]
	final_list = [x for x in final_list if (x < mean + 2 * sd)]
	linhalog=final_list
	meanlog = numpy.mean(linhalog, axis=0)
	if len(linhalog)>0:
		if len(delete)>0:
			return [round(meandel,2),round(meanlog,2)]
		else:			
			return [0.0,round(meanlog,2)]
	else:
		if len(delete)>0:
			return [round(meandel,2),0.0]
		else:
			return [0.0,0.0]
#retorna a razão entre os teste realizados, pela quantidade de questões de todas as listas de 'homework'
def test(lista,turma,aluno,executions):
	teste=[]
	for execucao in executions:
		test_cont=0
		execution=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/executions/'+execucao)
		for linha in execution:
			if '== TEST' in linha:
				test_cont+=1
		teste+=[test_cont]
	elements = numpy.array(teste)
	mean = numpy.mean(elements, axis=0)
	sd = numpy.std(elements, axis=0)
	final_list = [x for x in teste if (x > mean - 2 * sd)]
	final_list = [x for x in final_list if (x < mean + 2 * sd)]
	teste=final_list
	meantest = numpy.mean(teste, axis=0)	
	if len(teste)>0:
		return round(meantest,2)
	return 0.0
#razão entre caracteres colados pelos digitados
def copy(turma,aluno,codemirror):
	lista=[]
	for log in codemirror:
		arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/codemirror/'+log)
		digitados,colados=0,0
		for linhas in arq:
			if('input' in linhas):
				digitados+=1
			elif('paste' in linhas):
				flag=0
				b=''
				for l in linhas:
					if(flag==0 and l=='['):
						flag=1
					elif(flag==1 and l!=']'):
						b+=l
					elif(flag==1 and l==']'):
						break
				colados+=len(b)-2
		if digitados>0:
			lista+=[colados/digitados]
		else:
			lista+=[colados]	
	elements = numpy.array(lista)
	mean = numpy.mean(elements, axis=0)
	sd = numpy.std(elements, axis=0)
	final_list = [x for x in lista if (x > mean - 2 * sd)]
	final_list = [x for x in final_list if (x < mean + 2 * sd)]
	lista=final_list
	meancopy = numpy.mean(lista, axis=0)			
	if len(lista)>0:
		return round(meancopy,2)
	return -1.0
#tempo que o aluno fica na IDE durante o prazo das listas de 'homework', se uma ação demorasse mais de 5 min, então o tempo na IDE não era contabilizado.
#focus blur(foco na ide, e sai da ide)
def tempo(lista,turma,aluno,codemirror):
	tempo=0
	from datetime import datetime
	s = '0-0-0 0:0:0.0'
	t = '0-0-0 0:0:0.0'
	f = '%Y-%m-%d %H:%M:%S.%f'
	for l in lista:
		arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/assessments/'+l)
		b=arq.read()
		aux=len(l)-5
		if('homework' in b):
			cont=0
			while(cont<len(codemirror)):
				if(l[:aux]==codemirror[cont][:aux]):
					log=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/codemirror/'+codemirror[cont])
					flag=0
					for linhas in log:
						if ('-' in linhas) and (':' in linhas) and  ('.' in linhas) and ('#' in linhas) and (int(linhas[7:9])<=31):
							
							
							if 'focus' in linhas and flag==0:
								s=linhas[:21]		
								flag=1
							elif flag==1 and 'blur' in linhas:
								t=linhas[:21]
								if s!=t and (datetime.strptime(t, f) - datetime.strptime(s, f)).total_seconds()<300:
									tempo+=(datetime.strptime(t, f) - datetime.strptime(s, f)).total_seconds()
								flag=0
								s = '0-0-0 0:0:0.0'
								t = '0-0-0 0:0:0.0'
							elif flag==1 and 'blur' not in linhas:
								t=linhas[:21]
								if s!=t and (datetime.strptime(t, f) - datetime.strptime(s, f)).total_seconds()<300:
									tempo+=(datetime.strptime(t, f) - datetime.strptime(s, f)).total_seconds()
								s=t
								t = '0-0-0 0:0:0.0'	
						
				cont+=1
	return round(tempo/60,2)
#mudar pra velocidade de codificação
#retorna a velocidade de digitação do aluno
#se uma digitação demora mais de 5s ela é descartada
#foi feito uma lista de velocidade, que cada elemento representava a razão de números 'input' pelo tempo
#o valor retornado é uma espécie de média de digitação de todos os caracteres 'input'
#existem sequências com apenas 2 'input', era contabilizado em velocidade, com isso tirei os outliers
#o valor retornado era a soma dos elementos na lista_final, após remoção dos outliers, dividido pela quantidade de termos na lista
def velocidade(lista,turma,aluno,codemirror):
	from datetime import datetime
	s = '0-0-0 0:0:0.0'
	t = '0-0-0 0:0:0.0'
	f = '%Y-%m-%d %H:%M:%S.%f'
	velocidade=[]
	for l in lista:
		arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/assessments/'+l)
		b=arq.read()
		aux=len(l)-5
		if('homework' in b):
			cont=0
			while(cont<len(codemirror)):
				if(l[:aux]==codemirror[cont][:aux]):
					digita=0
					flag=0
					firstime=0
					log=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/codemirror/'+codemirror[cont])
					for linhas in log:
						if '-' in linhas and ':' in linhas and  '.' in linhas and '#' in linhas and int(linhas[7:9])<=31:

							if ('input' in linhas and flag==0 ):
								s=linhas[:21]
								digita+=1
								flag=1
							elif('input' in linhas and flag==1):	
								if(firstime==0):
									digita+=1
									firstime=1
									t=linhas[:21]
									if (datetime.strptime(t, f) - datetime.strptime(s, f)).total_seconds()>5:
										digita=1
										firstime=0
										s=linhas[:21]
										t = '0-0-0 0:0:0.0'
								elif(datetime.strptime(linhas[:21], f) - datetime.strptime(t, f)).total_seconds()<=5:
									t=linhas[:21]
									digita+=1
								else:
									if(s!=t and digita>=5):									
										velocidade+=[digita/(datetime.strptime(t, f) - datetime.strptime(s, f)).total_seconds()]
									digita=1								
									s=linhas[:21]
									firstime=0
									t = '0-0-0 0:0:0.0'
							elif('input' not in linhas and flag==1):
								flag=0
								if(t[0]!='0' and s!=t and digita>=5):
									velocidade+=[digita/(datetime.strptime(t, f) - datetime.strptime(s, f)).total_seconds()]
								digita=0
								firstime=0 
								t = '0-0-0 0:0:0.0'

				cont+=1
	elements = numpy.array(velocidade)
	mean = numpy.mean(elements, axis=0)
	sd = numpy.std(elements, axis=0)
	final_list = [x for x in velocidade if (x > mean - 2 * sd)]
	final_list = [x for x in final_list if (x < mean + 2 * sd)]
	if(len(final_list)>0):
		return round(sum(final_list)/len(final_list),2)
	else:
		return 0.0
#retorna as tentativas,loc,sloc,blank lines,comments,submissões com erros de Syntax e as submissões totais
#quem não fez nada tem total erro de syntax
def code(codes,turma,aluno):
	hulp=[0,0,0,0]
	SyntaxErro=0
	for code in codes:
		arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/codes/'+code)
		while True:
			try:						
				a=analyze(arq.read())
				hulp[0]=hulp[0]+a[3]
				hulp[1]=hulp[1]+a[5]
				hulp[2]=hulp[2]+a[1]
				hulp[3]=hulp[3]+a[2]
				break
			except Exception as e:
				SyntaxErro+=1
	return [hulp]
def jadud(executions,turma,aluno):
	jadud=[]
	for execucao in executions:
		aux=0
		a=''
		b=''
		flag2=0
		arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/executions/'+execucao)
		for linha in arq:
			if 'Error:' in linha and flag2==0:
				a=linha
				flag2=1
			elif flag2==1 and '*-*-*-*-*' in linha:
				flag2=2
			elif 'Error:' in linha and flag2==2:
				b=linha
				aux+=8
				caracter1=''
				caracter2=''
				for letra in a:
					caracter1+=letra
					if letra==':':
						break
				for let in b:
					caracter2+=let
					if let==':':
						break
				if caracter1==caracter2:
					aux+=3
					if a==b:
						aux+=2
				a=b
				flag2=1
			elif flag2==2 and '*-*-*-*-*' in linha:
				flag2=0
		jadud+=[aux]
	elements = numpy.array(jadud)
	mean = numpy.mean(elements, axis=0)
	sd = numpy.std(elements, axis=0)
	final_list = [x for x in jadud if (x > mean - 2 * sd)]
	final_list = [x for x in final_list if (x < mean + 2 * sd)]
	meanjadud=numpy.mean(final_list, axis=0)
	if len(final_list)>0:
		return round(meanjadud,2)
	else:
		return -1.0
def watson(executions,turma,aluno):
	from datetime import datetime
	import numpy
	f = '%Y-%m-%d %H:%M:%S'
	watson=[]
	for execucao in executions:
			aux=0
			flag2=0
			s = '0-0-0 0:0:0.0'
			t = '0-0-0 0:0:0.0'
			time=[]
			arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/executions/'+execucao)
			for linha in arq:
				if ('== TEST' in linha or '== SUBMITION' in linha)and flag2==0:
					s=linha[-22:-3]
					flag2=1
				elif ('== TEST' in linha or '== SUBMITION' in linha)and flag2==1:
					t=linha[-22:-3]
					if (datetime.strptime(t, f) - datetime.strptime(s, f)).total_seconds()<600:
						time+=[(datetime.strptime(t, f) - datetime.strptime(s, f)).total_seconds()]
					s=t
			elements = numpy.array(time)
			mean = numpy.mean(elements, axis=0)
			sd = numpy.std(elements, axis=0)
			final_list = [x for x in time if (x > mean - 2 * sd)]
			final_list = [x for x in final_list if (x < mean + 2 * sd)]
			elements = numpy.array(final_list)
			mean = numpy.mean(elements, axis=0)
			sd = numpy.std(elements, axis=0)
			a=''
			b=''
			flag2=0
			arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/executions/'+execucao)
			for linha in arq:
				if '== TEST' in linha or '== SUBMITION'and flag2==0:
					s=linha[-22:-3]
					flag2=1
				elif flag2==1 and 'Error:' in linha:
					a=linha
					flag2=2
				elif '*-*-*-*-*' in linha and flag2==1:
					flag2=0
				elif '*-*-*-*-*' in linha and flag2==2:
					flag2=3
				elif '== TEST' in linha or '== SUBMITION'and flag2==3:
					t=linha[-22:-3]
					flag2=4
				elif flag2==4 and 'Error:' in linha:
					#falha,falha	
					aux+=4					
					b=linha
					caracter1=''
					caracter2=''
					for letra in a:
						caracter1+=letra
						if letra==':':
							break
					for let in b:
						caracter2+=let
						if let==':':
							break
					if caracter1==caracter2:
						aux+=4
						if a==b:
							aux+=2
					if (datetime.strptime(t, f) - datetime.strptime(s, f)).total_seconds()<mean-sd:
						aux+=1
					elif (datetime.strptime(t, f) - datetime.strptime(s, f)).total_seconds()>mean+sd:
						aux+=25
					elif (datetime.strptime(t, f) - datetime.strptime(s, f)).total_seconds()<mean+sd:
						aux+=15
					a=linha
					s=t
					flag2=2
				elif flag2==4 and '*-*-*-*-*' in linha:
					#falha,sucesso
					if (datetime.strptime(t, f) - datetime.strptime(s, f)).total_seconds()<mean-sd:
						aux+=1
					elif (datetime.strptime(t, f) - datetime.strptime(s, f)).total_seconds()>mean+sd:
						aux+=25
					else:
						aux+=15
					flag2=0
			watson+=[aux]	
	
	elements = numpy.array(watson)
	mean = numpy.mean(elements, axis=0)
	sd = numpy.std(elements, axis=0)
	final_list = [x for x in watson if (x > mean - 2 * sd)]
	final_list = [x for x in final_list if (x < mean + 2 * sd)]
	meanwatson=numpy.mean(final_list, axis=0)
	if len(final_list)>0:
		return round(meanwatson,2)
	else:
		return -1.0
def syntax_erro(executions,turma,aluno):
	lista=[]
	submit,submit_erro=0,0	
	for execucao in executions:
		arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/executions/'+execucao)
		flag=0
		for linha in arq:
			if '== SUBMITION' in linha and flag!=2:
				submit+=1
				flag=1
			elif '-- ERROR:' in linha and flag==1:
				submit_erro+=1
				flag=0
			elif '*-*-*-*-' in linha and flag==1:
				flag==0
			elif '100%' in linha and flag==1:
				flag=2
	if submit>0:
		return [round(submit_erro/submit,2),round(submit,2)]
	else:
		return [1.0,0.0]
def cont_code(codes,turma,aluno):
	if_elif_else,while_for,variable=[],[],[]
	for questao in codes:
		cont=0
		while(cont<len(codes)):
			cont_if_elif_else,cont_while_for=0,0
			aux_variable=[]
			arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/codes/'+codes[cont])
			for linha in arq:
				if 'if' in linha or 'elif' in linha or 'else' in linha:
					cont_if_elif_else+=1
				elif 'while' in linha or 'for' in linha:
					cont_while_for+=1
				else:
					if ('=' in linha) and ('==' not in linha) and ('>' not in linha) and ('<' not in linha) and ('!' not in linha) and ('#' not in linha):
						cont2=0
						aux=''
						while(cont2<len(linha)):
							if linha[cont2]!=' ':
								if linha[cont2]!='=':
									aux+=linha[cont2]
								else:		
									cont2=len(linha)
							cont2+=1
						if '[' in aux:
							cont2=0
							aux2=''
							while(cont2<len(aux)):
								if aux[cont2]!=' ':
									if aux[cont2]!='[':
										aux2+=aux[cont2]
									else:		
										if aux2 not in aux_variable:
											aux_variable+=[aux2]
										cont2=len(aux)
								cont2+=1
						elif ',' in aux:
							cont2=0
							aux2=''
							while(cont2<len(aux)):
								if aux[cont2]!=' ':
									if aux[cont2]!=',':
										aux2+=aux[cont2]
									else:		
										if aux2 not in aux_variable:
											aux_variable+=[aux2]
										aux2=''
								cont2+=1
						else:
							if aux not in aux_variable:
								aux_variable+=[aux]
							aux=''
			aux_variable_help=[]				
			for elemento in aux_variable:
				if '\t' in elemento:
					aux=''
					for caracter in elemento:
						if caracter!='\t':
							aux+=caracter
					if aux not in aux_variable_help:
						aux_variable_help+=[aux]
					
				else:
					aux_variable_help+=[elemento]
			cont+=1
			variable+=[len(aux_variable_help)]
			if_elif_else+=[cont_if_elif_else]
			while_for+=[cont_while_for]
	elements = numpy.array(variable)
	mean = numpy.mean(elements, axis=0)
	sd = numpy.std(elements, axis=0)
	final_list = [x for x in variable if (x > mean - 2 * sd)]
	final_list = [x for x in final_list if (x < mean + 2 * sd)]
	variable=final_list
	mean_variable=numpy.mean(variable, axis=0)
	elements = numpy.array(if_elif_else)
	mean = numpy.mean(elements, axis=0)
	sd = numpy.std(elements, axis=0)
	final_list = [x for x in if_elif_else if (x > mean - 2 * sd)]
	final_list = [x for x in final_list if (x < mean + 2 * sd)]
	if_elif_else=final_list
	mean_condition=numpy.mean(if_elif_else, axis=0)
	elements = numpy.array(while_for)
	mean = numpy.mean(elements, axis=0)
	sd = numpy.std(elements, axis=0)
	final_list = [x for x in while_for if (x > mean - 2 * sd)]
	final_list = [x for x in final_list if (x < mean + 2 * sd)]
	while_for=final_list
	mean_cicle=numpy.mean(while_for, axis=0)
	if len(if_elif_else)>0:
		if len(while_for)>0:
			if len(variable)>0:
				return [round(mean_condition,2),round(mean_cicle,2),round(mean_variable,2)]
			else:
				return [round(mean_condition,2),round(mean_cicle,2),0.0]
		else:
			if len(variable)>0:
				return [round(mean_condition,2),0.0,round(mean_variable,2)]
			else:
				return [round(mean_condition,2),0.0,0.0] 
	else:
		if len(while_for)>0:
			if len(variable)>0:
				return [0.0,round(mean_cicle,2),round(mean_variable,2)]
			else:
				return [0.0,round(mean_cicle,2),0.0]
		else:
			if len(variable)>0:
				return [0.0,0.0,round(mean_variable,2)]
			else:
				return [0.0,0.0,0.0] 

def MF(turma,aluno):
	media=0.0
	notas=os.listdir('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/grades')
	for elemento in notas:
		if 'final' in elemento:	
			arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/grades/'+elemento)
			media=float(arq.readline())
	return round(media,2)
def submission_exercise(turma,aluno,executions):
	lista=[]	
	for execucao in executions:
		submit=0
		arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/executions/'+execucao)
		flag=0
		for linha in arq:
			if '== SUBMITION' in linha and flag!=2:
				submit+=1
				flag=1
			elif '100%' in linha and flag==1:
				flag=2
			elif '*-*-*-' in linha and flag!=2:
				flag=0
		lista+=[submit]
	elements = numpy.array(lista)
	mean = numpy.mean(elements, axis=0)
	sd = numpy.std(elements, axis=0)
	final_list = [x for x in lista if (x > mean - 2 * sd)]
	final_list = [x for x in final_list if (x < mean + 2 * sd)]
	lista=final_list
	mean=numpy.mean(lista, axis=0)
	if len(lista)>0:
		return round(mean,2)
	else:
		return 0.0
def success_average(turma,aluno,executions):
	lista=[]
	for elemento in executions:
		submit,correct,flag=0,0,0
		arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/executions/'+elemento)
		for l in arq:
			if '== SUBMITION' in l and flag!=2:
				submit+=1
				flag=1
			elif '100%' in l and flag==1:
				correct=1
				flag=2
			elif '*-*-*-' in l and flag!=2:
				flag=0
		if submit>0:
			lista+=[correct/submit]
		else:
			lista+=[0]
	elements = numpy.array(lista)
	mean = numpy.mean(elements, axis=0)
	sd = numpy.std(elements, axis=0)
	final_list = [x for x in lista if (x > mean - 2 * sd)]
	final_list = [x for x in final_list if (x < mean + 2 * sd)]
	lista=final_list
	mean=numpy.mean(lista, axis=0)
	if len(lista)>0:
		return round(mean,2)
	else:
		return 0.0

def error(turma,aluno,codes,codemirror,lista):
	cont=0
	lista2=[]
	for l in lista:
		aux=len(l)-5
		arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/assessments/'+l)
		for linha in arq:
			if 'total_exercises' in linha:
				
				cont+=int(linha[22:-1])
	for code in codes:
			arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/codes/'+code)
			aux=2
			while True:
				try:						
					analyze(arq.read())
					break
				except Exception as e:
					aux=1
			if aux==2:
				for elemento in codemirror:
					if elemento[:-4]==code[:-3]:
						arq=open('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/codemirror/'+elemento)
						for linhas in arq:
							if 'Congratulations' in linhas:
								aux=3
								break
			lista2+=[aux]
	lista3=[0]*(cont-len(lista2))
	lista2=lista2+lista3
	
	return round(numpy.mean(numpy.array(lista2),axis=0),2)
#retorna uma lista em  formato pronto para uso em .csv
def geral(data,s):
	classes=os.listdir('/home/samuel/teste/classes/2018-2')
	classes.sort()
	if len(classes[0])>3:
		classes=classes[1:]
	for turma in classes:
		listadealunos=os.listdir('/home/samuel/teste/classes/2018-2/'+turma+'/users/')
		listadealunos.sort()
		lista=os.listdir('/home/samuel/teste/classes/2018-2/'+turma+'/assessments/')
		lista.sort()
		lista=listsession(lista,turma,s)
		for aluno in listadealunos:
			codemirror=os.listdir('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/codemirror/')
			codemirror.sort()
			executions=os.listdir('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/executions/')
			executions.sort()
			grades=os.listdir('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/grades/')
			grades.sort()
			codes=os.listdir('/home/samuel/teste/classes/2018-2/'+turma+'/users/'+aluno+'/codes/')
			codes.sort()
			[codemirror,codes,grades,executions]=session(codemirror,codes,grades,executions,lista,turma)
			#usar para 2016-1			
			#aux=[]
			#if aluno=='1201':
			#	for elemento in executions:
			#		if elemento!='181_1218.log':
			#			aux+=[elemento]
			#	executions=aux
			delete,system_acess,linhaslog,correto,teste=0,0,0,0,0
			exam,homework=0.0,0.0
			[cont_condition,cont_cicle,cont_variable]=cont_code(codes,turma,aluno)
			hulp=[0,0,0,0]
			[syntax,submit]=syntax_erro(executions,turma,aluno)
			print(aluno)
			[hulp]=code(codes,turma,aluno)
			hulp=[submit]+hulp
			teste=test(lista,turma,aluno,executions)
			[delete,linhaslog]=deleteaux(lista,turma,aluno,codemirror)
			system_acess=logins(lista,turma,aluno)
			hulp=hulp+[system_acess]
			if(len(grades)>0):
				[exam,homework]=score(grades,lista,turma,aluno)
				hulp=hulp+[exam]
			else:
				hulp=hulp+[0.0]
				grades=[0]
			data=data+[[aluno]+hulp+[delete]+[linhaslog]+[submission_exercise(turma,aluno,executions)]+[success_average(turma,aluno,executions)]+[teste]+[homework]+[round(plagio(lista,codemirror,turma,aluno)*homework,2)]+[copy(turma,aluno,codemirror)]+[syntax]+[tempo(lista,turma,aluno,codemirror)]+[velocidade(lista,turma,aluno,codemirror)]+[jadud(executions,turma,aluno)]+[watson(executions,turma,aluno)]+[cont_condition]+[cont_cicle]+[cont_variable]+[error(turma,aluno,codes,codemirror,lista)]+[MF(turma,aluno)]]
	return data
import pandas
sessao=['s1','s2','s3','s4','s5','s6','s7']
for s in sessao:
	data=[['Id','attempts','comments','blank_line','lloc','sloc','system_access','exam_grade_codebench','delete_average','average_log_rows','submission_per_exercise','sucess_average','test_average','exercises_list_grade','exercises_list_grade_check_plagiarism','copy_paste_proportion','sintaxe_error','IDE_usage','keystroke_latency','jadud','watson','cont_condition','cont_cicle','cont_variable','error','Media_final']]
	data=geral(data,s)
	df = pandas.DataFrame(data)
	df.to_csv('/home/samuel/codigos/tabelas_por_lista/2018-2/'+s+'.csv', header=None, index=None)
