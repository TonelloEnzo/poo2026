class Campus:

    def __init__(self):
        self.endereco = ""
        self.nome = ""

    def __str__(self):
        return f"Campus: {self.nome}"
class Estudante: 

    def __init__(self):
        self.nome = ""
        self.cpf = ""
        self.data_nasc = ""

    def __str__(self):
        return f"Campus: {self.nome}"
    
    def apresentar(self):
        print(f"O(a) estudante se chama {self.nome}, nasceu em {self.data_nasc}")
        if(self.cpf == ""):
            print("O(a) estudante não cadastrou cpf")
        else:
            print("CPF:", self.cpf[0:3], "...")


maria = Estudante()
maria.nome = "Maria Vitória"
maria.cpf = "123.456.789-10"
maria.data_nasc = "20/01/2009"
print(f"O {maria.nome} nasceu em {maria.data_nasc}")

enzo = Estudante()
enzo.nome = "Enzo de Souza"
enzo.cpf = "136.941.889-24"
enzo.data_nasc = "10/06/2008"
print(f"O {enzo.nome} nasceu em {enzo.data_nasc}")


