class Livro:
    
    def __init__ (self, titulo):
        self.titulo = titulo
        self.disponivel = True

    def emprestar(self):
      
        if(self.disponivel == True):
            self.disponivel = False
            print(f"livro {self.titulo} emprestado com sucesso!")
        else:
            print("Este livro já está emprestado, tente novamente!")

    def devolver(self):
       
        if(self.disponivel == False):
            self.disponivel = True
            print(f"O Livro {self.titulo} foi devolvido com sucesso")

livro1 = Livro("Heated Rivalry")
livro2 = Livro("Heartstopper")
livro1.emprestar()
livro1.emprestar()
livro1.devolver()
livro1.emprestar()