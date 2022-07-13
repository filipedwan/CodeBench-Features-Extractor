import os
from radon.raw import analyze
#retorna uma lista em  formato pronto para uso em .csv
#retorna os dados de cada aluno
def geral(data):
	classes=os.listdir('/home/user/teste/classes/2018-2')
	classes.sort()
	if len(classes[0])>3:
		classes=classes[1:]
	for turma in classes:
		listadealunos=os.listdir('/home/user/teste/classes/2018-2/'+turma+'/users/')
		listadealunos.sort()
		for aluno in listadealunos:
			arq=open('/home/user/teste/classes/2018-2/'+turma+'/users/'+aluno+'/user.data')
			print(aluno)
			#-1 é não respondeu
			aux=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
			for linha in arq:
				if 'course name' in linha:
					aux[0]=linha[18:-1] 
				elif 'high school name' in linha:
					aux[1]=linha[23:-1]
				elif 'school type' in linha:
					if 'private' in linha:
						aux[2]=1
					elif 'public' in linha:
						aux[2]=0
				elif 'shift' in linha:
					aux[3]=linha[12:-1]
				elif 'graduation year' in linha:
					aux[4]=linha[22:-1]
				elif 'has a PC at home' in linha:
					if 'yes' in linha:
						aux[5]=1
					else:
						aux[5]=0
				elif 'share this PC' in linha:
					if 'yes' in linha:
						aux[6]=1
					else:
						aux[6]=0
				elif 'this PC has access to Internet' in linha:
					if 'yes' in linha:
						aux[7]=1
					else:
						aux[7]=0
				elif 'previous experience of any computer' in linha:
					if 'yes' in linha:
						aux[8]=1
					else:
						aux[8]=0
				elif 'worked or interned' in linha:	
					if 'yes' in linha:
						aux[9]=1
					else:
						aux[9]=0	
				elif 'company name' in linha:
					aux[10]=linha[19:-1]
				elif 'year started working' in linha:
					aux[11]=linha[27:-1]
				elif 'year stopped working' in linha:
					aux[12]=linha[27:-1]
				elif 'started other degree programmes' in linha:
					if 'yes' in linha:
						aux[13]=1
					else:
						aux[13]=0
				elif 'degree course' in linha:
					aux[14]=linha[20:-1]
				elif 'institution name' in linha and 'Universidade' not in linha:
					aux[15]=linha[23:-1]
				elif 'year started this degree' in linha:
					aux[16]=linha[31:-1]
				elif 'year stopped this degree' in linha:
					aux[17]=linha[31:-1]
				elif 'sex' in linha:
					if 'female' in linha:
						aux[18]=0
					else:
						aux[18]=1
				#1=solteiro
				#0=qualquer um que não seja solteiro
				elif 'birth' in linha:
					aux[19]=2019-int(linha[20:-1])
				elif 'civil status' in linha:
					aux[20]=linha[19:-1]
				elif 'have kids' in linha:
					if 'yes' in linha:
						aux[21]=1
					else:
						aux[21]=0 
			data+=[[aluno]+aux]
			
	return data			
import pandas
data=[['Id','couse name','high school name','shcool type','shift','graduation year','has a PC at home','share this PC with other people at home','Internet','previous experience of any computer language','worked or interned before the degree','company name','year started working','year stopped working','started other degree programmes','degree course','institution name','year started this degree','year stoped this degree','sex','age','civil status','have kids']]
data=geral(data)
df = pandas.DataFrame(data)
df.to_csv('/home/user/codigos/tabelas_por_questão/2018-2/user_data/dados.csv', header=None, index=None)
