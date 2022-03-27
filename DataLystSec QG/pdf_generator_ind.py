import requests
import time
import json
import os
import sqlite3
import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np

_dados = json.load(open('ind.json'))

data = '27/08'
empresa = '7º GAC'
codigo = 20001

resultados = ['1 - DEFINIÇÃO DE POLÍTICA','2 - CONTROLES 1-6 IMPLEMENTADOS', '3 - IMPLEMENTAÇÃO DOS CONTROLES', '4 - AUTOMAÇÃO DOS CONTROLES', '5 - CONTROLES RELATADOS', 'NÍVEL DE MATURIDADE']
r_resultado = [0.2,0.5,0.47,0.23,0.61,2.01]
r_resultado_ = [0.2,0.5,0.47,0.23,0.61]
g_resultado = ['1','2','3','4','5']

cis1 = ['- Diretriz de implementação: Utilize uma ferramenta para analisar em tempo real seu inventário de ativos, podendo ser físicos ou virtuais.\n- Empresas parceiras: SolarWind Network Performance Monitor e Paessler PRTG Network Monitor.',
        '- Diretriz de implementação: Faça a verificação passive de seu inventário, na qual não é necessário contato em tempo real com os ativos.\n- Empresas parceiras: TripWire Asset Discovery',
        '- Diretriz de implementação: Faça os logs DHCp usando uma ferramenta de automatização do protocolo.\n- Empresas parceiras: NXLog',
        '- Diretriz de implementação: Mantenha um inventário de ativos organizado e, posteriormente, catalogado.\n- Empresas parceiras: TripWire Asset Discovery',
        '- Diretriz de implementação: Faça o registro detalhado de seu inventário com uma ferramenta organizada e bem implementada.\n- Empresas parceiras: TripWire Asset Discovery',
        '- Diretriz de implementação: Verifique com mais detalhes os ativos de seu inventário e veja se estão catalodados corretamente\n- Empresas parceiras: TripWire Asset Discovery',
        '- Diretriz de implementação: Habilite o controle de portas de acesso em ativos\n- Empresas parceiras: ManageEngine'
        ]

cis2 = ['- Diretriz de implementação: Manter controle de acesso de software não autorizado.\n- Empresas parceiras: PlexTrac',
        '- Diretriz de implementação: Verifique com o vendedor se ele está atualizando o próprio software\n- Empresas parceiras: Comunicação do Parceiro',
        '- Diretriz de implementação: Utilizar ferramentas de inventário de software mais específicos para essa tarefa\n- Empresas parceiras: PlexTrac',
        '- Diretriz de implementação: Mantenha um log de softwares utilizados organizado e, posteriormente, catalogado.\n- Empresas parceiras: PlexTrac',
        '- Diretriz de implementação: Os logs de hardware e software devem estar interligados\n- Empresas parceiras: PlexTrac',
        '- Diretriz de implementação: Faça a verificação de softwares não autorizados regularmente\n- Empresas parceiras: PlexTrac',
        '- Diretriz de implementação: Aplique o whitelisting de softwares autorizados regularmente\n- Empresas parceiras: PlexTrac',
        '- Diretriz de implementação: Aplique o whitelisting nas bibliotecas regularmente\n- Empresas parceiras: PlexTrac',
        '- Diretriz de implementação: Aplique o whitelisting nos scripts usados regularmente, é a área mais vulnerável nesse quesito.\n- Empresas parceiras: PlexTrac',
        '- Diretriz de implementação: Segregue os seus ativos de hardware e software, para que não haja nenhum ataque eletrônico na infraestrutura\n- Empresas parceiras: LogTech'
        ]

cis3 = ['- Diretriz de implementação: Aplique regularmente scanners de vulnerabilidade em sua empresa\n- Empresas parceiras: OWASP ZAP',
        '- Diretriz de implementação: Os escaneiamentos devem ser regulares e autenticados\n- Empresas parceiras: OWASP ZAP',
        '- Diretriz de implementação: Faça a proteça de contas voltadas exclusivamente para o monitoramento de softwares\n- Empresas parceiras: OWASP ZAP',
        '- Diretriz de implementação: Manutenha o seu Sistema operacional regularmente com patches\n- Empresas parceiras: Windows Updater',
        '- Diretriz de implementação: Manutenha os seus softwares regularmente com patches\n- Empresas parceiras: CCleaner software updater',
        '- Diretriz de implementação: Faça a comparação back-to-back, ou seja,  de trás para trás, de seus ativos\n- Empresas parceiras: CCleaner Checker',
        '- Diretriz de implementação: Faça uma avaliação de riscos \n- Empresas parceiras: Dripster Risk Manager'
        ]

cis4 = ['- Diretriz de implementação: Faça um inventário de contas de administrador\n- Empresas parceiras: Admyn Tool',
        '- Diretriz de implementação: Faça a mudança rapidamente de senhas padrão de softwares e hardwares. Em 2012, o maior ataque hacker foi feito em larga escala ao atacar senhas padrão de câmeras de segurança, não repita esse erro.\n- Empresas parceiras: DashLane',
        '- Diretriz de implementação: Faça a mudança rapidamente de senhas padrão de softwares e hardwares. Em 2012, o maior ataque hacker foi feito em larga escala ao atacar senhas padrão de câmeras de segurança, não repita esse erro.\n- Empresas parceiras: DashLane'
        ]

cis_r = [cis1, cis2, cis3, cis4]

cis_s = [[0.0,0.0,0.7,0.0,0.0,0.0,0.0],
        [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
        [0.0,0.0,0.0,0.0,0.0,0.0,0.0],
        [0.0,0.5,0.0]]

for k in range(len(cis_s)):
    cis_s[k] = _dados[f'cis{k+1}']

#print(cis_s)

ypos = np.arange(len(g_resultado))
plt.xticks(ypos,g_resultado)
plt.bar(ypos,r_resultado_)
plt.savefig('bab.png')

pdf = FPDF('P','mm','A4')
pdf.set_auto_page_break(auto=True, margin = 15)
pdf.add_page()

pdf.image('images/logo.png',90,8,18)
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


pdf.multi_cell(0,10,textinho)

pdf.add_page()

# Página 2 kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk

for i in range(len(cis_r)):
    pdf.set_font('times','B',12)
    pdf.cell(0,10,f'CIS {i+1}', border=True, align='C', ln=1)
    pdf.set_font('times','',12)
    for j in range(len(cis_r[i])):
        if cis_s[i][j] < 0.25:
            pdf.set_font('times','B',12)
            pdf.cell(0,10,f'Sub-controle {i+1}.{j+1}', ln=1)
            pdf.set_font('times','',12)
            pdf.multi_cell(0,10,f'{cis_r[i][j]}')

resultados = ['1 - DEFINIÇÃO DE POLÍTICA', '2 - IMPLEMENTAÇÃO DOS CONTROLES', '3 - AUTOMAÇÃO DOS CONTROLES', '4 - CONTROLES RELATADOS']
r_resultado = [0.21,0.43,0.09,0.45,0.61,2.01]
r_resultado_ = [0.21,0.43,0.09,0.45]
g_resultado = ['1','2','3','4']

'''
count = 0
pdf.cell(0,10,"",ln=1)
for _resultado in resultados:
    pdf.cell(0,10, f'{_resultado}: {r_resultado[count]}', ln=1)
    count += 1
pdf.cell(0,10,"",ln=1)
'''

'''
pdf.set_font('times','B',12)
pdf.cell(0,10,'DIRETRIZ DE IMPLEMETAÇÃO', border=True, align='C', ln=1)
pdf.set_font('times','',12)

textinho = "- PONTOS CRÍTICOS: Ferramenta passiva de descoberta de ativos\n- Diretriz de implementação: Utilize uma ferramenta para analisar em tempo real seu inventário de ativos, podendo ser físicos ou virtuais.\n- Empresas parceiras: SolarWind Network Performance Monitor e Paessler PRTG Network Monitor."
pdf.multi_cell(0,10,textinho, ln=1)
'''
'''
plt.clf()
ypos = np.arange(len(g_resultado))
plt.xticks(ypos,g_resultado)
plt.bar(ypos,r_resultado_)
plt.savefig('bab.png')

pdf.image('bab.png',100,25,70)
'''
pdf.output('Relatório Individual.pdf')


