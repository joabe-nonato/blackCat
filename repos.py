from datetime import datetime
from modelos.generico import *
from os import path, system
import json
from time import sleep
from sys import exit

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
    listar_acoes()


def ocorreu_erro():
    gravar_log_aplicacao(nomeclatura["erro"])
    input(nomeclatura["voltar_menu"])
    listar_acoes()


def perguntar():
    sleep(2)
    novaExecucao = input(nomeclatura["retornar_menu"] + " (S/N)")

    if novaExecucao == "s" or novaExecucao == "S":
        listar_acoes()
    else:
        finalizar()


def listar_acoes():
    system('cls')    
    conexoes = leitor_arquivo_json(f"configuracao\conexoes.json", "dados")

    global nomeclatura
    nomeclatura = leitor_arquivo_json(f"configuracao\\nomeclatura.json", "dados")

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
    
    executarEm = ''
    executarEm = str(input(nomeclatura["codigo_desejado"]))

#EXECUTAR AÇÃO SELECIONADA
    lista_execucao = []
    nao_selecionado = True

    print(executarEm)
        
    try:    
    
        # SAIR        
        if executarEm == "S" or executarEm == "s":
            finalizar() 
        # elif executarEm == "A" or executarEm == "a":
        #     atualizar_bases()
        else: 
        # SELECIONAR
            for acao in Conexao.lista:

                if str(acao._id) == executarEm:
                    nao_selecionado = False
                    print(acao.nome)
                    lista_execucao.append(acao)
                    break

                elif executarEm == "T" or executarEm == "t":
                    nao_selecionado = False
                    print(acao.nome)
                    lista_execucao.append(acao)
                    continue


            # SELEÇÃO ERRADA
            if nao_selecionado:
                OpcaoInvalida()
            else:
                
                # EXECUTAR NA BASE
                for executar in lista_execucao:
                    print(executar)

                perguntar()

    except:  
        ocorreu_erro()


