import requests
import time
import json
import os
import sqlite3
import datetime
import shutil


class TelegramBot:
    def __init__(self):
        token = '2144631996:AAE9c1NvWbF-eS1usAdkSO496ETeGGUsT_k'
        self.token = token
        self.url_base = f'https://api.telegram.org/bot{token}/'

    def Iniciar(self):

        update_id = None
        while True:
            atualizacao = self.obter_novas_mensagens(update_id)
            dados = atualizacao["result"]
            #print(dados)
            if dados:
                for dado in dados:
                    self.dado = dado
                    self.download_file()
                    
                    update_id = dado['update_id']
                    try:
                        mensagem = str(dado["message"]["text"])
                    except:
                        break

                    self.download_file()

                    chat_id = dado["message"]["from"]["id"]                    

                    try:
                        banco = sqlite3.connect('users_data.db')
                        cursor = banco.cursor()
                        name = cursor.execute(f"SELECT name FROM usuarios WHERE chat_id={chat_id}").fetchone()[0]
                        money = cursor.execute(f"SELECT money FROM usuarios WHERE chat_id={chat_id}").fetchone()[0]
                        banco.commit()
                        banco.close()
                    except sqlite3.Error as erro:
                        print("Erro ao inserir dados: ", erro)
                        pass

                    # registrar saldo no banco de dados dos usuários
                    self.discount_amount(chat_id, money)

                    

                    
###################################### DEFINED FUNCTION SECTION ########################################                  

    # Obter mensagens
    def obter_novas_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)
    
    def download_file(self):
        print('Solicitção para baixar documento...')
        try:
            file_id = self.dado['message']['document']['file_id']
            file_name = self.dado['message']['document']['file_name']
            print(file_id, file_name)
            loaded_data = json.loads(requests.post(f'https://api.telegram.org/bot{self.token}/getFile?file_id={file_id}').text)
            file_path = loaded_data['result']['file_path']
            file = requests.get(f'https://api.telegram.org/file/bot{self.token}/{file_path}').content
            open(file_name, 'wb').write(file)
            print('Documento foi baixado com sucesso!')
            print(file_name)

            _dados = json.load(open(file_name))
            print("JSON:\n",_dados)
            _codigo = _dados['codigo']
            _nome = _dados['nome']
            _usuario = _dados['usuario']
            _cargo = _dados['cargo']
            _data = _dados['data']
            _rm = _dados['regiao militar']
            _r1,_r2,_r3,_r4,_r5 = _dados['resultado']
            print(_codigo)

            banco = sqlite3.connect('transfers.db')
            cursor = banco.cursor()
            print('a')
            cursor.execute(f"DELETE FROM Dados WHERE Codigo={_codigo}")
            print('b')
            
            cursor.execute(f"INSERT INTO Dados VALUES ({_codigo}, '{_nome}', '{_usuario}', '{_cargo}', '{_data}', {_r1}, {_r2}, {_r3}, {_r4}, {_rm}, {_r5})")
            print('c')
            banco.commit()
            banco.close()
            
        except:
            print('Documento não foi baixado!')
        finally:
            print('Solicitação de documento encerrada!\n')
    
    def generate_pdf(self):
        print('Gerando PDF...')
        

    # Criar uma resposta
    def criar_resposta(self, mensagem, chat_id, money):
        if chat_id:
            return 'Saldo: N$' + str(money) + ',00\n\n/trem - N$1,00\n\n/navio - N$2,00\n\n/aviao - N$8,00'
        elif mensagem.lower() in ('s', 'sim'):
            return ''' Pedido Confirmado! '''
        elif mensagem.lower() in ('n', 'não'):
            return ''' Pedido Confirmado! '''
        else:
            return 'Gostaria de acessar o menu? Digite "menu"'

    # Responder
    def responder(self, resposta, chat_id):
        link_requisicao = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_requisicao)

    def register_account(self, mensagem, chat_id, first_name):
        if mensagem == '/start':
            try:
                os.makedirs('bank_statements/' + str(chat_id))
            except:
                print("Usuário já cadastrado")
            try: 
                banco = sqlite3.connect('users_data.db')
                cursor = banco.cursor()
                cursor.execute(f"DELETE FROM usuarios WHERE chat_id={chat_id}")
                cursor.execute(f"INSERT INTO usuarios VALUES ('{chat_id}','{first_name}', 110)")
                banco.commit()
                banco.close()
                self.responder('Cadastro realizado com sucesso', chat_id)
                print('Cadastro realizado com sucesso!')
            except sqlite3.Error as erro:
                print("Usuário já cadastrado ou Erro ao inserir dados: ", erro)

    def issue_receipt(self, chat_id, amount):
        try:
            dat = str(datetime.datetime.now())[:19]
            dateandtime = f'{dat[8:10]}/{dat[5:7]}/{dat[0:4]} {dat[11:]}'
            banco = sqlite3.connect('transfers.db')
            cursor = banco.cursor()
            cursor.execute(f"INSERT INTO payment VALUES ({chat_id}, {amount}, '{dateandtime}')")
            banco.commit()
            banco.close()
            print('Comprovante gerado com sucesso!')        
        except sqlite3.Error as erro:
            print("Erro ao emitir o comprovante: ", erro)
    
    def discount_amount(self, chat_id, money):
        try:
            banco = sqlite3.connect('users_data.db')
            cursor = banco.cursor()
            cursor.execute(f"UPDATE usuarios SET money={money} WHERE chat_id={chat_id}")
            banco.commit()
            banco.close()
        except sqlite3.Error as erro:
            print("Erro ao registrar saldo: ", erro)
    
    def send_image(self, chat_id, file_location):
        url = self.url_base + "sendPhoto"
        files = {'photo': open(file_location, 'rb')}
        data = {'chat_id' : str(chat_id)}
        r = requests.post(url, files=files, data=data)

    def send_document(self, chat_id, file_location):
        url = self.url_base + "sendDocument"
        files = {'document': open(file_location, 'rb')}
        data = {'chat_id' : str(chat_id)}
        r = requests.post(url, files=files, data=data)

    def send_bank_statement(self, chat_id):
        # in progress
        try:
            banco = sqlite3.connect('transfers.db')
            cursor = banco.cursor()
            extract_table = cursor.execute(f"SELECT amount, date_and_time FROM payment WHERE chat_id={chat_id}").fetchall()
            banco.close()
            for i in range(len(extract_table)):
                mini_list = [f'N$ {extract_table[i][0]},00', extract_table[i][1]]
                extract_table.pop(i)
                extract_table.insert(i, mini_list)
            extract_table.insert(0, ['Valor', 'Data e Hora'])
            from reportlab.platypus import SimpleDocTemplate
            from reportlab.lib.pagesizes import letter
            filename = f'bank_statements/{chat_id}/Extrato - BBV.pdf'
            pdf = SimpleDocTemplate(
                filename,
                pagesize=letter
            )
            from reportlab.platypus import Table
            table = Table(extract_table)
            elems = []
            elems.append(table)
            pdf.build(elems)
            url = self.url_base + "sendDocument"
            files = {'document': open(filename, 'rb')}
            data = {'chat_id' : str(chat_id)}
            r = requests.post(url, files=files, data=data)

        except sqlite3.Error as erro:
            print("Erro ao emitir o extrato: ", erro)

bot = TelegramBot()
bot.Iniciar()
