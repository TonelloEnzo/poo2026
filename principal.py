from classes import Jogador, Equipe

lista_jogadores = []
lista_equipes = []

def cadastrar_jogador():
    nome = input("Digite o nome do jogador:")
    nickname = input("Digite o nickname do jogador")
    turma = input("Digite a turma do jogador:")

    novo_jogador = Jogador(nome, nickname, turma)
    lista_jogadores.append(novo_jogador)

    print(f"Novo jogador {novo_jogador.nome} cadastrado com sucesso!")

def cadastrar_equipe():
    nome_equipe = input("Informe o nome da equipe:")
    jogo = input("Digite o jogo:")

    nova_equipe = Equipe(jogo, nome_equipe)
    lista_equipes.append(nova_equipe)

    print(f"Nova equipe {nova_equipe.nome_equipe} cadastrado com sucesso!")

def adicionar_jogador_a_equipe ():

    equipe_add = input("Qual o nome da equipe?")
    nickname_add = input("Qual o nickname do jogador?")

    equipe_encontrada = False
    nickname_encontrado = False

    
    for i in lista_equipes:
        if i.nome_equipe == equipe_add:
            equipe_encontrada = True
            equipe_i = i
          

  
    for j in lista_jogadores:
        if j.nickname == nickname_add:
            nickname_encontrado = True
            nickname_j = j

    
    if equipe_encontrada == True and nickname_encontrado == True:
       
        equipe_i.membros.append(nickname_j)
        print(f"Sucesso! {nickname_add} adicionado ao time {equipe_add}")
    else:
        print("Erro: Verifique se o nome da equipe e o nick estão corretos.")


def listar_equipes():
    # Checa se a lista de equipes está vazia
    if len(lista_equipes) == 0:
        print("\nNenhuma equipe foi cadastrada ainda! Escolha a opção 2 primeiro.")
        return # O return faz a função parar por aqui e voltar pro menu
    
    # Se a lista não estiver vazia, ele imprime normalmente
    for i in lista_equipes:
        quantidade = len(i.membros)
        print(f"Equipe: {i.nome_equipe} | Jogo: {i.jogo} | Jogadores: {quantidade}")

def listar_jogadores():
   
  for i in lista_jogadores:
    print(f"Nome: {i.nome} Nickname: {i.nickname} Turma: {i.turma}")

def buscar_jogador():
    buscar = input("Digite o nickname que deseja buscar: ")

    
    for i in lista_jogadores:
       
        if i.nickname == buscar:
           

            print(f"Nome: {i.nome}")
            print(f"Nickname: {i.nickname}")
            print(f"Turma: {i.turma}")
            return
    print("Jogador não encontrado.")    
    
while True:
    print("\n========================================")
    print("CAMPEONATO INTERCLASSE DE E-SPORTS")
    print("========================================")
    print("1. Cadastrar jogador")
    print("2. Cadastrar equipe")
    print("3. Adicionar jogador a uma equipe")
    print("4. Listar todas as equipes")
    print("5. Listar jogadores de uma equipe")
    print("6. Buscar jogador por nickname")
    print("0. Sair")
    print("========================================")
    
    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        cadastrar_jogador()
    elif opcao == 2:
        cadastrar_equipe()
    elif opcao == 3:
        adicionar_jogador_a_equipe()
    elif opcao == 4:
        listar_equipes()
    elif opcao == 5:
        listar_jogadores()
    elif opcao == 6:
        buscar_jogador()
    elif opcao == 0:
        print("Saindo...")
        break # O break encerra o while True e fecha o programa
    else:
        print("Opção inválida. Tente novamente.")