import csv
import subprocess
import os
import time

with open('certificado_modelo_ministrante.tex') as arq:
    tx = arq.read()
with open('lista.csv') as f:
    leitor = csv.reader(f)
    next(leitor)
    for linha in leitor:
        ID = linha[0]
        data = linha[1]
        Cr = linha[2]
        Cg = linha[3]
        saida = tx%(ID,Cr,data,Cg)
        arq_name = 'Certificados/'+ID+'.tex'
        TexFile = open(arq_name,'w')
        TexFile.write(saida)
        TexFile.close()
        subprocess.Popen(['pdflatex',arq_name],shell=False)
        print('Processo finalizado para {0}'.format(ID))
        time.sleep(.8)
        os.system('rm *.aux *.log')
        os.system('mv *.pdf Certificados')
