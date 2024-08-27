from datetime import datetime
from modelos.generico import *
from os import path, system, listdir
import json
from time import sleep
import sys
# import pandas as pd
import pyodbc
import csv
import shutil

# pandas, numpy, openpyxl
# pip install pandas
# pip install numpy
# pip install openpyxl

def obter_caminho_diretorio():
    # Se o script estiver rodando como um executável
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        # Se rodando como script Python
        base_path = path.abspath(".")

    return base_path

def obter_caminho_absoluto(relativo):
    # Se o script estiver rodando como um executável
    if hasattr(sys, '_MEIPASS'):
        # Caminho para o diretório temporário onde o PyInstaller descompacta os arquivos
        base_path = sys._MEIPASS
    else:
        # print(' Caminho para o diretório onde o script Python está localizado')
        base_path = path.abspath(".")

    return path.join(base_path, relativo)


diretorio = path.dirname(path.abspath(__file__))

def diretorio_arquivo(pasta, arquivo):
    return obter_caminho_absoluto(path.join(pasta, arquivo))


def arquivo_existe(local_arquivo):
# Verifica se o arquivo existe
# Entrada: local_arquivo (nome completo do arquivo)
# Retorna: True ou Falso
    return path.isfile(local_arquivo)


def mover_arquivo(origem, destino):
    shutil.move(origem, destino)

def mover_arquivo_executado(nome_arquivo):
    origem = diretorio_arquivo("executar", nome_arquivo)
    destino = diretorio_arquivo("executado", nome_arquivo)
    mover_arquivo(origem, destino)

def gravar_texto(local, texto):
# MÉTODO PADRÃO PARA GRAVAR (CRIA\EDITA) UM ARQUIVO TEXTO
# Entrada:  Local (Recebe o local com o nome.tipo do arquivo)
#           Texto (Conteúdo do arquivo)
    with open(local, "w") as arquivo:
        arquivo.write(texto)


def retorno_data_hora():
    agora = datetime.now()
    return f'{str(agora).ljust(19)}'
    # return f'{str(agora.day).ljust(2)}/{str(agora.month).ljust(2)}/{str(agora.year).ljust(2)} '


def gravar_log_aplicacao(texto):
# Gravar log de execuçções sobre a rotina da ferramenta
# Entrada: texto
# Retorno: grava o arquivo log.txt na raiz da solução
    textoLog = f'\nEm: {retorno_data_hora()} Descricao: {texto}'
    print(texto)

    agora = datetime.now()

    localLog = diretorio_arquivo('logs',f'log{str(agora.year)}_{str(agora.month)}_{str(agora.day)}.txt')

    # localLog = f'logs\log{str(agora.year)}_{str(agora.month)}_{str(agora.day)}.txt'

    with open(localLog, "a", encoding='utf8') as arquivo:
        arquivo.write(textoLog)


def VerificarDiretorio(pasta):
    try:
        diretorio = path.join(obter_caminho_diretorio(), pasta)        
        return listdir(diretorio)
    except FileNotFoundError:
        print(f'Ocorreu um erro em VerificarDiretorio: {diretorio}')
        return []

def leitor_de_arquivo(arquivo):
# Executa a leitura de arquivo
# Entrada: arquivo (Nome completo do arquivo com o endereço)
# Retorno: texto (Conteúdo do arquivo)
    texto = ''
    try:
        with open(arquivo) as conteudo:
            texto = conteudo.read()
            conteudo.close()
    except:
        return ''
    
    return texto

def RecuperarScript(arquivo):
    texto = ''
    try:
        with open(arquivo) as conteudo:
            texto = conteudo.read()
            conteudo.close()
    except:
        return ''
    
    return texto


def leitor_arquivo_json(localarquivo, node):
# Leitor de arqquivo json
# Entrada:  localarquivo
#           node (exmeplo de node: 'dados')
# Retorna: array
    try:
        with open(localarquivo, "r", encoding='utf8') as arquivo:    
            dados = json.load(arquivo)
            return dados.get(node, [])
    except FileExistsError:
        print("ocorreu um erro")
        return[]


def Executar(database, strcon, comando):

    mensagem = ''

    try:
        conexao = pyodbc.connect(strcon)
        cursor = conexao.cursor()
        cursor.execute(comando)
        cursor.commit()
    
    except pyodbc.Error as e:
        mensagem += f'\r\n \r\nBASE: {database}\r\n Erro:\r\n{e.args[1]}'                
    except pyodbc.InterfaceError as e:
        mensagem += f'\r\n \r\nBASE: {database}\r\n Erro pyodbc.InterfaceError:\r\n{e}'        
    except pyodbc.DatabaseError as e:
        mensagem += f'\r\n \r\nBASE: {database}\r\n Erro pyodbc.DatabaseError:\r\n{e}'
        
    finally:                    
        if 'The login failed. (4060)' not in mensagem:            
            cursor.close()        
            del cursor
            conexao.close()
        else:
            mensagem += f'\r\n \r\nATENÇÃO:\r\nNão existe a base {database} no servidor 67'

    return mensagem

def executar_script(selecao):    
    # ITEM SELECIONADO VALIDO
    if len(selecao) > 0:       

        arquivos = VerificarDiretorio('executar')
        if len(arquivos) > 0:
            arquivos.sort()
        else:
            print("Nenhum arquivo encontrado para execução.")

        # #carregar um array de scripts
        for arquivo in arquivos:
            #ler arquivo do diretório
            caminho_arquivo = diretorio_arquivo('executar',arquivo)

            comando = RecuperarScript(caminho_arquivo)
            
            for item in selecao:
                gravar_log_aplicacao(f'Executando o arquivo "{arquivo}" no ambiente {item.ambiente} base: {item.base}')
                
                try:
                    Executar(item.base, item.conetar, comando)                    
                except:
                    gravar_log_aplicacao(f'Erro ao executar o arquivo "{arquivo}" no ambiente {item.ambiente} base: {item.base}')

        # mover_arquivo_executado(arquivo)

    else:
        OpcaoInvalida()

def finalizar():
    gravar_log_aplicacao(nomeclatura["finalizando"])
    sleep(2)
    system('cls')    

def atualizar_bases():
    gravar_log_aplicacao(nomeclatura["atualizar_bases"])
    sleep(2)
    system('cls')    

def OpcaoInvalida():
    sleep(2)
    gravar_log_aplicacao(nomeclatura["opcao_invalida"])
    input(nomeclatura["voltar_menu"])
    aplicativo()

def ocorreu_erro():
    gravar_log_aplicacao(nomeclatura["erro"])
    input(nomeclatura["voltar_menu"])
    aplicativo()


def perguntar():
    sleep(2)
    novaExecucao = input(nomeclatura["retornar_menu"] + " (S/N)")

    if novaExecucao == "s" or novaExecucao == "S":
        aplicativo()
    else:
        finalizar()

def carregar_bases():        
    if len(Conexao.lista) == 0:       
        
        config_path = diretorio_arquivo('configuracao','config.json')

        bases = leitor_arquivo_json(config_path, "dados")

        with open(bases["arquivo_bases"],"r") as arquivo:
            
            arquivo_csv = csv.reader(arquivo, delimiter=",")

            for indice, item in enumerate(arquivo_csv):
                if indice > 0:
                    Conexao(item[1], item[2], item[3], item[4], item[5], item[6])

def aplicativo():
    system('cls')    

    global nomeclatura
    nome_path = diretorio_arquivo('configuracao','config.json')

    nomeclatura = leitor_arquivo_json(nome_path, "dados")
    
#CRIAR LISTA DE CONEXOES, CASO NÃO EXISTA
    gravar_log_aplicacao(nomeclatura["lista_codigo"])

#Carregar lista de bases
    carregar_bases()    

#EXIBIR LISTA DE OPÇÕES EM TELA
    lista_ambientes = list(set([conexao.ambiente for conexao in Conexao.lista]))

    for indice, acao in enumerate(sorted(lista_ambientes)):
        print( f'{indice} = {acao}')

    # print(" ")
    # print("A = " + nomeclatura["atualizar_bases"])
    print("L = Listar bases")
    print("T = " + nomeclatura["todos"])
    print("S = " + nomeclatura["para_sair"])    
    
    item_selecionado = ''
    item_selecionado = str(input(nomeclatura["codigo_desejado"]))

#EXECUTAR AÇÃO SELECIONADA   
    try:        
        # SAIR        
        if item_selecionado == "S" or item_selecionado == "s":
            finalizar() 
        # elif item_selecionado == "A" or item_selecionado == "a":
        #     atualizar_bases()
        elif item_selecionado == "L" or item_selecionado == "l":
            Conexao.listar_conexoes()
            perguntar()
        elif item_selecionado == "T" or item_selecionado == "t":
            executar_script(Conexao.lista)
        else: 
            ambiente = lista_ambientes[int(item_selecionado)]

            gravar_log_aplicacao(f"Item selecionado: {ambiente}")

            selecao = list(filter(lambda x: x.ambiente == ambiente, Conexao.lista))
            executar_script(selecao)

            gravar_log_aplicacao("Concluído")
            perguntar()
            return
        
    except:  
        ocorreu_erro()


