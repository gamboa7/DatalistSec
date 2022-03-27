import requests
import time
import json
import os
import sqlite3
import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np

data = '27/08'
empresa = '7º GAC'
codigo = 20001

resultados = ['1 - DEFINIÇÃO DE POLÍTICA','2 - CONTROLES 1-6 IMPLEMENTADOS', '3 - IMPLEMENTAÇÃO DOS CONTROLES', '4 - AUTOMAÇÃO DOS CONTROLES', '5 - CONTROLES RELATADOS', 'NÍVEL DE MATURIDADE']
r_resultado = [0.2,0.5,0.47,0.23,0.61,2.01]
r_resultado_ = [0.2,0.5,0.47,0.23,0.61]
g_resultado = ['1','2','3','4','5']

ypos = np.arange(len(g_resultado))
plt.xticks(ypos,g_resultado)
plt.bar(ypos,r_resultado_)
plt.savefig('bab.png')

pdf = FPDF('P','mm','A4')
pdf.set_auto_page_break(auto=True, margin = 15)
pdf.add_page()

pdf.image('dsldsl.png',90,8,18)
pdf.ln(20)

pdf.image('bab.png',100,65,100)

pdf.set_font('times','B',12)
pdf.cell(0,10,'RELATÓRIO INDIVIDUAL', border=True, align='C', ln=1)
pdf.set_font('times','',12)
pdf.cell(0,10, f'Empresa: {empresa} | Código: {codigo} | Data: {data} | 7ª Região Militar', ln=1)

pdf.ln(10)

pdf.set_font('times','B',12)
pdf.cell(0,10,'RESULTADOS', border=True, align='C', ln=1)
pdf.set_font('times','',12)

count = 0
for _resultado in resultados:
    pdf.cell(0,10, f'{_resultado}: {r_resultado[count]}', ln=1)
    count += 1
for i in range(2):
    pdf.cell(0,10,"",ln=1)

pdf.ln(10)

pdf.set_font('times','B',12)
pdf.cell(0,10,'VISÃO GERAL', border=True, align='C', ln=1)
pdf.set_font('times','',12)

textinho = "- PONTOS CRÍTICOS: Automação do controle\n- Diretriz de implementação: Utilize uma ferramenta para analisar em tempo real seu inventário de ativos, podendo ser físicos ou virtuais.\n- Empresas parceiras: SolarWind Network Performance Monitor e Paessler PRTG Network Monitor."
textinho = '- A empresa não possui uma política formal de segurança da informação, isto é, não há ainda um documento formal que formalize diretrizes e práticas de defesa cibernética.\n - Em média, os controles foram implementados apenas em alguns sistemas.Esse cenário não é seguro, pois os dados da empresa podem estar sendo expostos a ação de hackers através dos sistemas nos quais os controles não foram implementados.\n - A avaliação também mostrou que a maior parte dos controles estão apenas parcialmente automatizados.\n - Os controles têm sido relatados à alta administração na maioria dos sitemas.\n - Por fim, o nível de maturidade é Repetível.'


pdf.multi_cell(0,10,textinho, ln=1)

pdf.add_page()

# Página 2 kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk

pdf.set_font('times','B',12)
pdf.cell(0,10,'CIS 1', border=True, align='C', ln=1)
pdf.set_font('times','',12)

resultados = ['1 - DEFINIÇÃO DE POLÍTICA', '2 - IMPLEMENTAÇÃO DOS CONTROLES', '3 - AUTOMAÇÃO DOS CONTROLES', '4 - CONTROLES RELATADOS']
r_resultado = [0.21,0.43,0.09,0.45,0.61,2.01]
r_resultado_ = [0.21,0.43,0.09,0.45]
g_resultado = ['1','2','3','4']

count = 0
pdf.cell(0,10,"",ln=1)
for _resultado in resultados:
    pdf.cell(0,10, f'{_resultado}: {r_resultado[count]}', ln=1)
    count += 1
pdf.cell(0,10,"",ln=1)

pdf.set_font('times','B',12)
pdf.cell(0,10,'DIRETRIZ DE IMPLEMETAÇÃO', border=True, align='C', ln=1)
pdf.set_font('times','',12)

textinho = "- PONTOS CRÍTICOS: Ferramenta passiva de descoberta de ativos\n- Diretriz de implementação: Utilize uma ferramenta para analisar em tempo real seu inventário de ativos, podendo ser físicos ou virtuais.\n- Empresas parceiras: SolarWind Network Performance Monitor e Paessler PRTG Network Monitor."
pdf.multi_cell(0,10,textinho, ln=1)
'''
plt.clf()
ypos = np.arange(len(g_resultado))
plt.xticks(ypos,g_resultado)
plt.bar(ypos,r_resultado_)
plt.savefig('bab.png')

pdf.image('bab.png',100,25,70)
'''
pdf.output('pdfpdf.pdf')


