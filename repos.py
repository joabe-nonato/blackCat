from datetime import datetime
from modelos.generico import *
from os import path, system, listdir
import json
from time import sleep
from sys import exit
import pandas as pd
import pyodbc

def arquivo_existe(local_arquivo):
# Verifica se o arquivo existe
# Entrada: local_arquivo (nome completo do arquivo)
# Retorna: True ou Falso
    return path.isfile(local_arquivo)


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
    localLog = f'logs\log{str(agora.year)}_{str(agora.month)}_{str(agora.day)}.txt'

    with open(localLog, "a", encoding='utf8') as arquivo:
        arquivo.write(textoLog)


def VerificarDiretorio(diretorio):
    try:
        return listdir(diretorio)
    except FileNotFoundError:
        print('Ocorreu um erro em VerificarDiretorio')
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
    
    print('Executar', database, strcon, comando)

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


def retorno_database(filtro, lista_conexao):
    dados = pd.read_csv("dados\\base.csv")
    df = pd.DataFrame(lista_conexao)
    conexao_filtrada = df[df['nome'] == filtro]
    # Verificar se as colunas 'servidor' e 'base' existem no DataFrame
    if 'servidor' not in dados.columns or 'base' not in dados.columns:
        print("As colunas 'servidor' e/ou 'base' não foram encontradas no CSV.")
        return
    # print("XXXXXX:")
    # print(dados.head(), filtro)
    dados_filtrados = dados[dados["servidor"] == filtro]
    # Verificar se há dados após a filtragem
    if dados_filtrados.empty:
        print("Nenhum dado encontrado para o filtro fornecido.")
        return
    # Exibir as primeiras linhas do DataFrame filtrado para verificação
    # print("Primeiras linhas do DataFrame filtrado:")
    # print(dados_filtrados.head())
    arquivos = VerificarDiretorio('executar')
    if len(arquivos) > 0:
        arquivos.sort()
    else:
        print("Nenhum arquivo encontrado para execução.")

    #carregar um array de scripts
    for arquivo in arquivos:
        #ler arquivo do diretório
        comando = RecuperarScript(f'executar\{arquivo}')
    # PERCORRER CONEXOES FILTRADAS
        for indice, conn in conexao_filtrada.iterrows():    
            #PERCORRER BASES DE DADOS FILTRADAS
            for indice, linha in dados_filtrados.iterrows():    
                base_selecionada = linha['base']
                cadeia_conexao = retornar_string_conexao(conn['servidor'],base_selecionada, conn['usuario'], conn['senha'])                       
                
                # print(cadeia_conexao, comando)
                Executar(base_selecionada, cadeia_conexao, comando)


def retornar_string_conexao(servidor, database, username, password):
# RETORNA A STRING DE CONEXÃO SQL
# Entrada: servidor, database, username, password
# Retorno: string de conexão
    return f"Driver=SQL Server;Server={servidor};Database={database};UID={username};PWD={password}"

#   PROGRAMA   ###############   PROGRAMA   ###############   PROGRAMA   ###############   PROGRAMA   ############
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


def aplicativo():
    system('cls')    
    conexoes = leitor_arquivo_json(f"configuracao\\conexoes.json", "dados")

    global nomeclatura
    nomeclatura = leitor_arquivo_json(f"configuracao\\nomeclatura.json", "dados")

    # print("RetornarBaseDados")
    # RetornarBaseDados()

#CRIAR LISTA DE CONEXOES, CASO NÃO EXISTA
    gravar_log_aplicacao(nomeclatura["lista_codigo"])
    
    if len(Conexao.lista) == 0:
        for item in conexoes:
            Conexao(item["nome"], item["servidor"], item["usuario"], item["senha"])

#EXIBIR LISTA DE OPÇÕES EM TELA
    for acao in Conexao.lista:
        print(acao)

    print(" ")
    # print("A = " + nomeclatura["atualizar_bases"])
    # print("L = Listar bases")
    print("T = " + nomeclatura["todos"])
    print("S = " + nomeclatura["para_sair"])    
    
    item_selecionado = ''
    item_selecionado = str(input(nomeclatura["codigo_desejado"]))

#EXECUTAR AÇÃO SELECIONADA
    lista_execucao = []
    nao_selecionado = True

    # print(item_selecionado)
        
    try:    
    
        # SAIR        
        if item_selecionado == "S" or item_selecionado == "s":
            finalizar() 
        # elif item_selecionado == "A" or item_selecionado == "a":
        #     atualizar_bases()
        else: 
        # SELECIONAR
            for acao in Conexao.lista:

                if str(acao._id) == item_selecionado:
                    nao_selecionado = False
                    # print(acao.nome)
                    lista_execucao.append(acao.nome)
                    break

                elif item_selecionado == "T" or item_selecionado == "t":
                    nao_selecionado = False
                    # print(acao.nome)
                    lista_execucao.append(acao.nome)
                    continue


            # SELEÇÃO ERRADA
            if nao_selecionado:
                OpcaoInvalida()
            else:
                
                # EXECUTAR NA BASE
                for filtro in lista_execucao:
                    retorno_database(filtro, conexoes)

                perguntar()

    except:  
        ocorreu_erro()


