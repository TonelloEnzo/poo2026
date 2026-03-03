import random


num = 0
while(num < 10 or num > 15):
    print("Número inválido, tente novamente!")
    num = int(input("Digite um valor de 10 a 15: "))
   
    valor = random.randint(1, 10)


while(valor != num):
    num = int(input("Digite um valor de 10 a 15: "))

    if(num == valor):
        print("Você acertou, o número era ", valor)
    else:
        print("Você errou, o número era ", valor, ", tente novamente")

   




