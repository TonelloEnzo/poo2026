"""
questão 1
valores = [0]* 11

Armazenar e exibir valores véy
for cont in range(0, len(valores)):
    valores[cont] = cont + 1

for cont in range(0, len(valores)):
    print("valor: ", valores[cont])"""

""" 
questão 2

cont = 0
while(cont < 20):
    print(cont)
    cont = cont + 1
"""
"""
questão 3
def soma_valores(a, b):
    x = a + b
    return x

a = int(input("Fala um numero ae "))
b = int(input("Fala outro numero ae "))

soma = soma_valores(a,b)
print(soma)
"""
"""
questão 4
cidads = [0] * 5
cidads[0] = "Paranavaí"
cidads[1] = "New Hope"
cidads[2] = "Foz do Iguaçu"
cidads[3] = "Maringay"
cidads[4] = "Up paraná"


for i in range(0, 5):
    print(cidads[i])
"""
"""
def verifica_par (a):
    if(a % 2 == 0):
        par = True
    else:
        par = False
    return par

num = int(input("Diga um número"))
parouimpar = verifica_par(num)

print(parouimpar)
"""

"""num = int(input("Digite um número inteiro"))
while(num != 0):
    num = int(input("Digite um número inteiro"))
    if(num == 0):
        break
print("Você escolheu sair")"""

def calcDesconto(preco, porcentagem):
    # Remova o for i in range...
    novo_preco = preco - (preco * (porcentagem / 100))
    return novo_preco

prod = []
cont = 1
while(cont != 4):
    print(f"Menu de opções")
    print("1 - Cadastrar Produto")
    print("2 - Listar Produtos")
    print("3 - Aplicar Desconto")
    print("4 - Sair")
    cont = int(input("Digite uma opcao "))
    if(cont == 1):
        lista = int(input("Qual lista você quer usar? "))
        
        produto = str(input("Qual produto quer adicionar? "))
        preco = float(input("Qual o valor? "))
        quant = int(input("Qual a quantidade? "))
        prod.insert(lista, (produto, preco, quant,("x")))
    elif(cont == 2):

        escolha = int(input("Qual lista você quer ver? ")) 
        
        print(f"\nExibindo a lista de produtos:")
        if len(prod) == 0:
            print("A lista está vazia! Cadastre algo na opção 1.")
        else:
            for item in prod:
               
                print(f"Produto: {item[0]} | Preço: R${item[1]:.2f} | Qtd: {item[2]}")
    elif(cont == 3):
        print("\n--- Aplicar Desconto ---")
        desconto = float(input("Digite a porcentagem de desconto: "))
        
        if len(prod) == 0:
            print("A lista está vazia!")
        else:
            print("Produtos com novo preço:")
            for item in prod:
                # item[0] é o nome, item[1] é o preço original
                nome = item[0]
                preco_antigo = item[1]
                
                # Chama sua função para cada item da lista
                novo_preco = calcDesconto(preco_antigo, desconto)
                
                print(f"{nome}: de R${preco_antigo:.2f} por R${novo_preco:.2f}")

    elif(cont == 4):
        print("Você escolheu sair.")
        break
    


        