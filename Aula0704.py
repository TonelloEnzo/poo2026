class Aluno:

    def __init__(self, nome, idade, curso, notas):
        self.nome = nome
        self.idade = idade
        self.curso = curso
        self.notas = notas

    def apresentar(self, nome, idade, curso):
        print(f"Olá, meu nome é {nome}, tenho {idade} anos e faço o curso de {curso}.")


    def calcularMedia(self):
        soma = 0.0
        for i in range(0, len(self.notas)):
            soma += self.notas[i]
            
        media = soma / len(self.notas)
        return media
    
        




    
nome = input("Nome: ")
idade = int(input("Idade: "))
curso = input("Curso: ")