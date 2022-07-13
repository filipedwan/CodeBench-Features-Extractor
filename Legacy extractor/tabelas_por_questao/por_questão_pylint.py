import os
from pylint import epylint
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
		arq=open('/home/user/teste/classes/2018-1/'+turma+'/assessments/'+l)
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
		lista=os.listdir('/home/user/teste/classes/2018-1/'+turma+'/assessments/')
		lista.sort()
		lista=listsession(lista,turma,s)
		aux=[]
		for l in lista:
			arq=open('/home/user/teste/classes/2018-1/'+turma+'/assessments/'+l)
			b=arq.read()
			arq=open('/home/user/teste/classes/2018-1/'+turma+'/assessments/'+l)
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
#conta as tentativas do aluno por questão
def distinct_operators(codes,turma,aluno,data):
	ext_depend,function,duplicated,warning,error,mixed,bad,invalid,superfluous=[],[],[],[],[],[],[],[],[]
	trailing,line,no_else,variable,argument,blocks,rate=[],[],[],[],[],[],[]
	for questão in data[0][1:]:
		cont=0
		flag=0
		while(cont<len(codes)):
			ext_depend_cont,function_cont,duplicated_cont,warning_cont,error_cont,mixed_cont,bad_cont,invalid_cont,superfluous_cont=0,0,0,0,0,0,0,0,0
			trailing_cont,line_cont,no_else_cont,variable_cont,argument_cont,blocks_cont,rate_cont=0,0,0,0,0,0,0
			aux2=''
			flag2=0
			for elemento in codes[cont]:		
				if elemento=='_':
					flag2=1
				elif flag2==1:
					if elemento!='.':				
						aux2+=elemento
					else:
						flag2=2
			if(questão==aux2):
				flag=1					
				a, pylint_stderr = epylint.py_run('/home/user/teste/classes/2018-1/'+turma+'/users/'+aluno+'/codes/'+codes[cont]+ ' --reports=y' , return_std=True)
				cont2=0
				flag2=0
				for linha in a:
					if 'External dependencies' in linha:
						flag2=1
					
					elif flag2==1:
						if cont2<3:
							cont2+=1
						elif cont2==3 and linha!=' \n':
							ext_depend_cont+=1
						elif cont2==3 and linha==' \n':
							flag2=0
							cont2=0
					elif '|function' in linha:
						function_cont=int(linha[12:15])
					elif 'nb duplicated lines' in linha:
						duplicated_cont=int(linha[28:31])
					elif '|warning' in linha:
						warning_cont=int(linha[14:19])
					elif '|error' in linha:
						error_cont=int(linha[14:17])
					elif '|mixed-indentation' in linha:
						cont2=0
						cont3=0
						for elemento in linha:
							cont3+=1
							if elemento=='|':
								cont2+=1	
							if cont2==2:
								break
						mixed_cont=int(linha[cont3:cont3+5])
					elif '|bad-whitespace' in linha:
						cont2=0
						cont3=0
						for elemento in linha:
							cont3+=1
							if elemento=='|':
								cont2+=1	
							if cont2==2:
								break
						bad_cont=int(linha[cont3:cont3+5])
					elif '|invalid-name' in linha:
						cont2=0
						cont3=0
						for elemento in linha:
							cont3+=1
							if elemento=='|':
								cont2+=1	
							if cont2==2:
								break
						invalid_cont=int(linha[cont3:cont3+5])
					elif '|superfluous-parens' in linha:
						cont2=0
						cont3=0
						for elemento in linha:
							cont3+=1
							if elemento=='|':
								cont2+=1	
							if cont2==2:
								break
						superfluous_cont=int(linha[cont3:cont3+5])
					elif '|trailing-whitespace' in linha:
						cont2=0
						cont3=0
						for elemento in linha:
							cont3+=1
							if elemento=='|':
								cont2+=1	
							if cont2==2:
								break
						trailing_cont=int(linha[cont3:cont3+5])
					elif '|line-too-long' in linha:
						cont2=0
						cont3=0
						for elemento in linha:
							cont3+=1
							if elemento=='|':
								cont2+=1	
							if cont2==2:
								break
						line_cont=int(linha[cont3:cont3+5])
					elif '|no-else-return' in linha:
						cont2=0
						cont3=0
						for elemento in linha:
							cont3+=1
							if elemento=='|':
								cont2+=1	
							if cont2==2:
								break
						no_else_cont=int(linha[cont3:cont3+5])
					elif '|unused-variable' in linha:
						cont2=0
						cont3=0
						for elemento in linha:
							cont3+=1
							if elemento=='|':
								cont2+=1	
							if cont2==2:
								break
						variable_cont=int(linha[cont3:cont3+5])
					elif '|unused-argument' in linha:
						cont2=0
						cont3=0
						for elemento in linha:
							cont3+=1
							if elemento=='|':
								cont2+=1	
							if cont2==2:
								break
						argument_cont=int(linha[cont3:cont3+5])
					elif '|too-many-nested-blocks' in linha:
						cont2=0
						cont3=0
						for elemento in linha:
							cont3+=1
							if elemento=='|':
								cont2+=1	
							if cont2==2:
								break
						blocks_cont=int(linha[cont3:cont3+5]) 
					elif 'Your code has been rated' in linha:
						aux=linha[29:41]
						aux2=''
						for caracter in aux:
							if caracter!='/':
								aux2+=caracter
							else:
								break
						rate_cont=float(aux2)
						
				ext_depend+=[ext_depend_cont]
				function+=[function_cont]
				duplicated+=[duplicated_cont]
				warning+=[warning_cont]
				error+=[error_cont]
				mixed+=[mixed_cont]
				bad+=[bad_cont]
				invalid+=[invalid_cont]
				superfluous+=[superfluous_cont]
				trailing+=[trailing_cont]
				line+=[line_cont]
				no_else+=[no_else_cont]
				variable+=[variable_cont]
				argument+=[argument_cont]
				blocks+=[blocks_cont]
				rate+=[rate_cont]
				cont=len(codes)	
			cont+=1
		if(flag==0):
			ext_depend+=[-1]
			function+=[-1]
			duplicated+=[-1]
			warning+=[-1]
			error+=[-1]
			mixed+=[-1]
			bad+=[-1]
			invalid+=[-1]
			superfluous+=[-1]
			trailing+=[-1]
			line+=[-1]
			no_else+=[-1]
			variable+=[-1]
			argument+=[-1]
			blocks+=[-1]
			rate+=[-1000]
	return [ext_depend,function,duplicated,warning,error,mixed,bad,invalid,superfluous,trailing,line,no_else,variable,argument,blocks,rate]
#retorna uma lista em  formato pronto para uso em .csv
def geral(s):
	data,data1,data2,data3,data4,data5,data6,data7,data8,data9,data10,data11,data12,data13,data14,data15=[['Id']],[['Id']],[['Id']],[['Id']],[['Id']],[['Id']],[['Id']],[['Id']],[['Id']],[['Id']],[['Id']],[['Id']],[['Id']],[['Id']],[['Id']],[['Id']]
	classes=os.listdir('/home/user/teste/classes/2018-1')
	classes.sort()
	if len(classes[0])>3:
		classes=classes[1:]
	data=questao(data,classes,s)
	data1[0]+=data[0][1:]
	data2[0]+=data[0][1:]
	data3[0]+=data[0][1:]
	data4[0]+=data[0][1:]
	data5[0]+=data[0][1:]
	data6[0]+=data[0][1:]
	data7[0]+=data[0][1:]
	data8[0]+=data[0][1:]
	data9[0]+=data[0][1:]
	data10[0]+=data[0][1:]
	data11[0]+=data[0][1:]
	data12[0]+=data[0][1:]
	data13[0]+=data[0][1:]
	data14[0]+=data[0][1:]
	data15[0]+=data[0][1:]
	print(data14[0])
	for turma in classes:
		listadealunos=os.listdir('/home/user/teste/classes/2018-1/'+turma+'/users/')
		listadealunos.sort()
		lista=os.listdir('/home/user/teste/classes/2018-1/'+turma+'/assessments/')
		lista.sort()
		lista=listsession(lista,turma,s)
		for aluno in listadealunos:
			codes=os.listdir('/home/user/teste/classes/2018-1/'+turma+'/users/'+aluno+'/codes/')
			codes.sort()
			codes=session(codes,lista,turma)
			[ext_depend,function,duplicated,warning,error,mixed,bad,invalid,superfluous,trailing,line,no_else,variable,argument,blocks,rate]=distinct_operators(codes,turma,aluno,data)
			print(aluno)
			data+=[[aluno]+ext_depend]
			data1+=[[aluno]+function]
			data2+=[[aluno]+duplicated]
			data3+=[[aluno]+warning]
			data4+=[[aluno]+error]
			data5+=[[aluno]+mixed]
			data6+=[[aluno]+bad]
			data7+=[[aluno]+invalid]
			data8+=[[aluno]+superfluous]
			data9+=[[aluno]+trailing]
			data10+=[[aluno]+line]
			data11+=[[aluno]+no_else]
			data12+=[[aluno]+variable]
			data13+=[[aluno]+argument]
			data14+=[[aluno]+blocks]
			data15+=[[aluno]+rate]
	return [data,data1,data2,data3,data4,data5,data6,data7,data8,data9,data10,data11,data12,data13,data14,data15]		
import pandas
sessao=['s1','s2','s3','s4','s5','s6','s7']
for s in sessao:
	[data,data1,data2,data3,data4,data5,data6,data7,data8,data9,data10,data11,data12,data13,data14,data15]=geral(s)
	df = pandas.DataFrame(data)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-1/external_dependencies/'+s+'.csv', header=None, index=None)
	df = pandas.DataFrame(data1)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-1/function/'+s+'.csv', header=None, index=None)
	df = pandas.DataFrame(data2)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-1/duplicated_lines/'+s+'.csv', header=None, index=None)
	df = pandas.DataFrame(data3)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-1/warning/'+s+'.csv', header=None, index=None)
	df = pandas.DataFrame(data4)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-1/error_pylint/'+s+'.csv', header=None, index=None)
	df = pandas.DataFrame(data5)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-1/mixed_indentation/'+s+'.csv', header=None, index=None)
	df = pandas.DataFrame(data6)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-1/bad_whitespace/'+s+'.csv', header=None, index=None)
	df = pandas.DataFrame(data7)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-1/invalid_name/'+s+'.csv', header=None, index=None)
	df = pandas.DataFrame(data8)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-1/superfluous_parens/'+s+'.csv', header=None, index=None)
	df = pandas.DataFrame(data9)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-1/trailing_whitespace/'+s+'.csv', header=None, index=None)
	df = pandas.DataFrame(data10)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-1/line_too_long/'+s+'.csv', header=None, index=None)
	df = pandas.DataFrame(data11)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-1/no_else_return/'+s+'.csv', header=None, index=None)
	df = pandas.DataFrame(data12)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-1/unused_variable/'+s+'.csv', header=None, index=None)
	df = pandas.DataFrame(data13)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-1/unused_argument/'+s+'.csv', header=None, index=None)
	df = pandas.DataFrame(data14)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-1/too_many_nested_blocks/'+s+'.csv', header=None, index=None)
	df = pandas.DataFrame(data15)
	df.to_csv('/home/user/codigos/tabelas_por_questão/2018-1/rate_pylint/'+s+'.csv', header=None, index=None)
