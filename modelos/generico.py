
#CONEXÃO
class Conexao:
    lista = []

    def __init__(self, nome, servidor, usuario, senha):
        self.nome = nome
        self.servidor = servidor
        self.usuario = usuario
        self.senha = senha
        Conexao.lista.append(self)
        self._id = (Conexao.lista.index(self) + 1)

    def __str__(self):
        return f'{self._id} = {self.nome}'

#MÉTODOS
    @classmethod
    def listar_conexoes(cls):
        print(f'{"Nome".ljust(5)}')

        for registro in cls.lista:
            print(f'{registro.nome.ljust(30)} ')



#ITEM GENÉRICO
class Item:
    lista = []

# CONSTRUTOR
    def __init__(self, descricao):
        Item.lista.append(self)

        self._id = (self.lista.index(self) + 1)
        self.descricao = descricao        
        
# DEFINIR REPRESENTAÇÃO EM STRING
    def __str__(self):
        return f'{self._id} | {self.descricao}'

#PROPRIEDADES
    @property
    def quantidade_registros(self):
        quantidade = len(self.lista)
        return quantidade

#MÉTODOS
    @classmethod
    def listar_itens(cls):
        print(f'{"Quantidade Registros".ljust(30)}: {str(cls.quantidade_registros).ljust(50)} ')
        print(f'{"ID".ljust(5)} | {"Descrição".ljust(30)}')

        for registro in cls.lista:
            print(f'{str(registro._id).ljust(5)} | {registro.descricao.ljust(30)}')


