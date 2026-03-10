import os

print("Configurando email...")
comando_email = "git config user.email \"20241pvai0030031@estudantes.ifpr.edu.br\""
os.system(comando_email)

print("Adicionando modificações...")
comando1 = "git add *"
os.system(comando1)

mensagem = input("Digite seu commit: ")
while( len(mensagem) < 5):
    print("⚠️ Mensagem muito pequena, detalhe mais...")
    mensagem = input("Digite seu commit: ")

print("Registrando alterações...")
comando2 = f"git commit -m \"{mensagem}\""
os.system(comando2)
print("Enviando projeto ao GitHub")
comando3 = "git push"
os.system(comando3)