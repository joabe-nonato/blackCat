
#CONEXÃO
class Conexao:
    lista = []

    def __init__(self, ambiente, cliente, servidor, usuario, senha, base):
        self.ambiente = ambiente
        self.cliente = cliente
        self.servidor = servidor
        self.usuario = usuario
        self.senha = senha
        self.base = base
        self.conetar = f"Driver=SQL Server;Server={self.servidor};Database={self.base};UID={self.usuario};PWD={self.senha}"
        
        if len(ambiente) > 0 and len(cliente) > 0 and len(servidor) > 0 and len(usuario) > 0 and len(senha) > 0 and len(base) > 0:
            Conexao.lista.append(self)
            self._id = (Conexao.lista.index(self) + 1)

    def __str__(self):
        return f'{self._id} = {self.ambiente} - {self.cliente}'

#MÉTODOS
    @classmethod
    def listar_conexoes(cls):
        print(f'{"ambiente".ljust(5)}')

        for registro in cls.lista:
            print(f'{registro.ambiente} Base: {registro.base} ')



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


