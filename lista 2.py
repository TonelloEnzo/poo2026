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



