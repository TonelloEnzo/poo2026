# importar bibliotecas
from peewee import *
import datetime

# Definir ondeestá o banco de dados (arquivo local)
conexao = SqliteDatabase("meu_banco.db")

# Criar minha classe de Contato
class Contato(Model):
    # Definir os atributos dela
    nome = CharField()
    telefone = CharField()

    # Sobrescrever o método que imprime o objeto inteiro
    def __str__(self):
        return f"{self.nome}: {self.telefone}"

    # Criar uma classe de Metadados para definir em qual banco será criado uma tabela para esta classe
    # Será criado uma tabela para esta classe
    class Meta:
        database = conexao

# Depois de criar todas as classes, vamos conectar ao banco de dados
conexao.connect()
# Pedir para a conexão criar as tabelas das classes, caso não existam
conexao.create_tables( [Contato] )