import requests
import time
import json
import os
import sqlite3
import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np

def respostas(_codigo):
    try:
        _banco = sqlite3.connect('transfers.db')
        _cursor = _banco.cursor()
        _Rs = _cursor.execute(f"SELECT R1, R2, R3, R4, R5 FROM Dados WHERE Codigo={_codigo}").fetchall()
        _banco.close()
        _Rs=_Rs[0]
        return _Rs

    except sqlite3.Error as erro:
        print("Erro ao emitir o extrato: ", erro)
        return 0,0,0,0,0

def respostas_regiao(_regiao):
    try:
        w_banco = sqlite3.connect('transfers.db')
        w_cursor = w_banco.cursor()
        w_Rs = w_cursor.execute(f"SELECT R1, R2, R3, R4, R5 FROM Dados WHERE Regiao={_regiao}").fetchall()
        w_banco.close()
        _R1, _R2, _R3, _R4, _R5 = 0,0,0,0,0
        for i in range(len(w_Rs)):
            _R1 += w_Rs[i][0]
            _R2 += w_Rs[i][1]
            _R3 += w_Rs[i][2]
            _R4 += w_Rs[i][3]
            _R5 += w_Rs[i][4]
        _R1 = round(_R1/len(w_Rs),2)
        _R2 = round(_R2/len(w_Rs),2)
        _R3 = round(_R3/len(w_Rs),2)
        _R4 = round(_R4/len(w_Rs),2)
        _R5 = round(_R5/len(w_Rs),2)
        _list = [_R1, _R2, _R3, _R4, _R5]
        for ob in _list:
            ob = round(ob,2) 
        return _list
    except:
        return [0,0,0,0,0]

def pdf_regiao(_regiao):

    _resultado = respostas_regiao(_regiao)
    
    pdf.set_font('times','B',12)
    pdf.cell(0,10,f'{_regiao}ª REGIÃO MILITAR', border=True, align='C', ln=1)
    pdf.set_font('times','',12)

    r_resultado = _resultado
    _resultado = _resultado.append(sum(_resultado[0:5]))
    count = 0
    for _resultado in resultados:
        r_resultado[count] = round(r_resultado[count],2)
        pdf.cell(0,10, f'{_resultado}: {r_resultado[count]}', ln=1)
        count += 1

def respostas_geral():
    _r = [0,0,0,0,0]
    for i in range(12):
        r = respostas_regiao(i+1)
        _r[0] += r[0]
        _r[1] += r[1]
        _r[2] += r[2]
        _r[3] += r[3]
        _r[4] += r[4]
    _r[0] = round(_r[0]/12,2)
    _r[1] = round(_r[1]/12,2)
    _r[2] = round(_r[2]/12,2)
    _r[3] = round(_r[3]/12,2)
    _r[4] = round(_r[4]/12,2)
    return _r

print('Aguarde, por favor...')

data = '27/08/2021'
empresa = 'EME'
codigo = 20000
regiao = 7

resultados = ['1 - DEFINIÇÃO DE POLÍTICA','2 - CONTROLES 1-6 IMPLEMENTADOS', '3 - IMPLEMENTAÇÃO DOS CONTROLES', '4 - AUTOMAÇÃO DOS CONTROLES', '5 - CONTROLES RELATADOS', 'NÍVEL DE MATURIDADE']
r_resultado = [0.6,0.2,0.4,0.3,0.5,2.0]
r_resultado_ = [0.6,0.2,0.4,0.3,0.5]
g_resultado = ['1','2','3','4','5']

r_resultado_ = respostas_geral()
soma = 0
for j in r_resultado_:
    soma += j
r_resultado = r_resultado_ + [round(soma,2)]

#   Gerando Gráfico ////////////////////////////////////////////

ypos = np.arange(len(g_resultado))
plt.xticks(ypos,g_resultado)
plt.bar(ypos,r_resultado_)
plt.savefig('images/aba.png')

#  Gerando PDF /////////////////////////////////////////////////

pdf = FPDF('P','mm','A4')
pdf.set_auto_page_break(auto=True, margin = 15)
pdf.add_page()

#pdf.image('images/logo.png',95,8,18)
pdf.image('images/logo.png',10,8,18)
pdf.image('images/exercito.png',190,8,10)
pdf.ln(20)

pdf.image('images/aba.png',100,65,100)

pdf.set_font('times','B',12)
pdf.cell(0,10,'RELATÓRIO CENTRAL', border=True, align='C', ln=1)
pdf.set_font('times','',12)
pdf.cell(0,10, f'Empresa/OM: {empresa} | Data: {data}', ln=1)
#pdf.cell(0,10, f'Empresa/OM: {empresa} | Código: {codigo} | Data: {data}', ln=1)

pdf.ln(10)

pdf.set_font('times','B',12)
pdf.cell(0,10,'RESULTADOS', border=True, align='C', ln=1)
pdf.set_font('times','',12)

count = 0
for _resultado in resultados:
    pdf.cell(0,10, f'{_resultado}: {r_resultado[count]}', ln=1)
    count += 1

pdf.ln(10)

pdf.set_font('times','B',12)
pdf.cell(0,10,'VISÃO GERAL', border=True, align='C', ln=1)
pdf.set_font('times','',12)

texto = "Os conceitos de cada Região Militar se encontram nas descrições abaixo."

pdf.multi_cell(0,10,texto)

for i in range(12):
    pdf_regiao(i+1)

pdf.output('Relatório Geral.pdf')

print('"Relatório Geral.pdf" gerado com sucesso!')


