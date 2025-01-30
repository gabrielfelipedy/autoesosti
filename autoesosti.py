from enum import Flag

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException

import PySimpleGUI as sg

import winsound
import time


class Esosti:

    def __init__(self) -> None:

        #construtor da classe

        chrome_options = Options()
        chrome_options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--lang=pr-BR')
        chrome_options.add_argument('--disable-notifications')

        #define atributos de classe

        
        self.navegador = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        #self.navegador = webdriver.Chrome(executable_path="C:\\chromedriver\\chromedriver-win32\\chromedriver.exe")
        
        self.navegador.maximize_window()
        self.navegador.get("https://esosti.trf1.jus.br/")

        print("Classe inicializada com sucesso")

    # ********************************************
    # ******* Método iniciar e utilitários *******
    # ********************************************

    def iniciar(self):
        self.getIDs()
        self.chamado_atendimento()
        self.chamado_retornado()
        self.atualiza_nevegador()

        print("Método iniciar finalizado com sucesso")


    def getIDs(self):
        time.sleep(10)

        try:
            chamados_atendimento = self.navegador.find_element(By.CSS_SELECTOR, "[aria-label='Atividades para Atendimento']")
            id_atendimentos = chamados_atendimento.get_attribute("id")[12:18]
            print(f'ESSE É O ID DO ELEMENTO ATENDIMENTOS: {id_atendimentos}')

            chamados_retornados = self.navegador.find_element(By.CSS_SELECTOR, "[aria-label='Atividades - Atendimento Retornado']")
            id_retornados = chamados_retornados.get_attribute("id")[12:18]
            print(f'ESSE É O ID DO ELEMENTO RETORNADOS: {id_retornados}')

        except (NoSuchElementException, Exception):
            print("Elemento não encontrado")
            self.getIDs()

        self.id1 = id_atendimentos
        self.id2 = id_retornados


    def chamado_atendimento(self):
        id_atendimento = f'rsportletdata_{self.id1}'
        print(id_atendimento)
        try:
            chamado = self.navegador.find_element(By.XPATH, f"//*[@id='{id_atendimento}']/table/tbody/tr[3]/td[4]/a/span")
            #print(chamado)
            winsound.PlaySound('C:\\Windows\\Media\\Ring01.wav', winsound.SND_ALIAS)
            print('Novo chamado para atendimento')

        except NoSuchElementException:
            print('Nenhum novo chamado cadastrado')
        time.sleep(5)

        print("Método chamado atendimento finalizado com sucesso")

    def chamado_retornado(self):
        id_retornado = f'rsportletdata_{self.id2}'
        print(id_retornado)
        try:
            chamado = self.navegador.find_element(By.XPATH, f"//*[@id='{id_retornado}']/table/tbody/tr[3]/td[3]/a/span")
            #print(chamado)
            winsound.PlaySound('C:\\Windows\\Media\\Ring01.wav', winsound.SND_ALIAS)
            print('Novo chamado retornado')
        except NoSuchElementException:
            print('Nenhum novo chamado retornado')
        time.sleep(5)

        print("Método chamado retornado atendente finalizado com sucesso")

    def atualiza_nevegador(self):
        time.sleep(30)
        self.navegador.refresh()
        try:
            self.navegador.switch_to.alert.accept()
        except NoAlertPresentException:
            print('Sem alerta')
        time.sleep(20)

        print("Método atualiza navegador atendente finalizado com sucesso")

    # ********************************************
    # ************* Finaliza aqui ****************
    # ********************************************
    

    def autentica_atendente(self):
        usernm = ...
        passwd = ...

        sg.theme("LightBlue2")

        # cria uma caixa de login para autenticação

        layout = [[sg.Text("Log In", size=(15, 1), font=40)],
                  [sg.Text("Username", size=(15, 1), font=16),
                   sg.InputText(key='-usrnm-', font=16)],
                  [sg.Text("Password", size=(15, 1), font=16), sg.InputText(
                      key='-pwd-', password_char='*', font=16)],
                  [sg.Button('Ok'), sg.Button('Cancel')]]

        window = sg.Window("Log In", layout)

        print("autentique-se")

        #Começa a captura de eventos da caixa de login

        while True:
            event, values = window.read()

            #Se cancelar ou fechar a janela
            if event == "Cancel" or event == sg.WIN_CLOSED:
                break
            elif event == "Ok":
                usernm = values['-usrnm-']
                passwd = values['-pwd-']

            username = self.navegador.find_element(By.ID, "j_username")
            password = self.navegador.find_element(By.ID, "j_password")

            username.send_keys(usernm)
            password.send_keys(passwd)
            window.close()

            select = Select(self.navegador.find_element(By.ID, 'uf'))
            select.select_by_visible_text('SJAP')
            entrar = self.navegador.find_element(By.XPATH, '//*[@id="loginbutton"]')
            entrar.click()
            time.sleep(1)

            #se der erro no login tenta novamente por chamada recursiva
            if self.navegador.current_url == 'https://esosti.trf1.jus.br/itsm/webclient/login/loginerror.jsp':
                self.navegador.get("https://esosti.trf1.jus.br/")
                self.autentica_atendente()

            time.sleep(5)
            #clica na aba correta para visualizar os chamados
            self.navegador.find_element(By.ID, "m1e20cba1-sct_anchor_1").click()
            time.sleep(15)

        print("Método autentica atendente finalizado com sucesso")

# Main
if __name__ == "__main__":

    essoti = Esosti()
    essoti.autentica_atendente()

    while True:
        essoti.iniciar()