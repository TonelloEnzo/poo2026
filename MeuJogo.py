import arcade
import random
from peewee import *

db = SqliteDatabase("ranking.db")
# ============================================================
# CONFIGURAÇÕES GLOBAIS DO JOGO
# ============================================================

ALTURA = 600          # Altura da janela em pixels
LARGURA = 800         # Largura da janela em pixels
TITULO = "Banana Jungle"   # Título da janela
GRAVIDADE = 0.5       # Força da gravidade aplicada aos elementos físicos
FORCA_PULO = 14       # Impulso vertical para o pulo do jogador


# ============================================================
# PLAYER (CLASSE DO JOGADOR)
# ============================================================

class Player(arcade.Sprite):

    def __init__(self):
        sheet_direita = arcade.load_spritesheet("player_direita.png")
        quadros_direita = sheet_direita.get_texture_grid(
        size=(192, 210),
        coluns= 8,
        count=8    
        )

        quadros_esquerda = []
        for frame in quadros_direita:
            quadros_esquerda.append(frame.flip_left_right())
    def __init__(self):
        # Inicializa a classe base Sprite carregando a imagem virada para a direita
        super().__init__(("dir macaco.png"), scale=0.20)

        # Carrega as duas texturas para trocar conforme a direção do movimento
        self.textura_direita = arcade.load_texture(("dir macaco.png"))
        self.textura_esquerda = arcade.load_texture(("esq macaco.png"))

    def update(self, delta_time):
        # Atualiza a posição X com base na velocidade horizontal
        self.center_x += self.change_x

        # Altera a imagem (sprite) dependendo para onde o jogador está andando
        if self.change_x > 0:
            self.texture = self.textura_direita
        elif self.change_x < 0:
            self.texture = self.textura_esquerda

        # Limita o movimento do jogador para que ele não saia das bordas da tela
        if self.right > LARGURA:
            self.change_x = 0
            self.right = LARGURA
        elif self.left < 0:
            self.change_x = 0
            self.left = 0


# ============================================================
# BLOCO / PLATAFORMA
# ============================================================

class Bloco(arcade.Sprite):
    def __init__(self, x: float, y: float):
        # Cria um bloco/plataforma com imagem e escala personalizadas
        super().__init__(("bloco.png"), scale=0.5)
        self.center_x = x
        self.center_y = y


# ============================================================
# MOEDA ESTÁTICA (BANANA COMUM)
# ============================================================

class Moeda(arcade.Sprite):
    valor_moeda = 1  # Atributo estático: vale 1 ponto

    def __init__(self):
        super().__init__(("banana.png"), scale=0.10)


# ============================================================
# MOEDA ESPECIAL (BANANA QUE SE MOVE E REBATE)
# ============================================================

class MoedaEspecial(arcade.Sprite):
    valor_moeda = 5  # Atributo estático: vale 5 pontos

    def __init__(self):
        super().__init__(("banana.png"), scale=0.14)

    def update(self, delta_time):
        # Move a moeda especial nos eixos X e Y
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Rebate na borda esquerda/direita invertendo a velocidade horizontal
        if self.left < 0 or self.right > LARGURA:
            self.change_x *= -1

        # Rebate na borda inferior/superior invertendo a velocidade vertical
        if self.bottom < 0 or self.top > ALTURA:
            self.change_y *= -1


# ============================================================
# INIMIGO COMUM (PERSEGUE O JOGADOR NO CHÃO COM FÍSICA)
# ============================================================

class Inimigo(arcade.Sprite):
    def __init__(self, blocos, jogador):
        super().__init__(("inimigo.png"), scale=0.15)
        self.jogador = jogador  # Guarda referência do jogador para perseguição
        self.velocidade = 1.8
        
        # Engine de física para respeitar gravidade e colisão com o chão
        self.engine_fisica = arcade.PhysicsEnginePlatformer(
            player_sprite=self,
            walls=blocos,
            gravity_constant=GRAVIDADE
        )

    def update(self, delta_time):
        # Persegue o jogador no eixo horizontal
        if self.center_x < self.jogador.center_x:
            self.change_x = self.velocidade
        elif self.center_x > self.jogador.center_x:
            self.change_x = -self.velocidade
        else:
            self.change_x = 0

        self.engine_fisica.update()  # Processa a física de queda/plataforma do inimigo


# ============================================================
# INIMIGO ESPECIAL (VOA E REBATE NAS BORDAS DA TELA)
# ============================================================

class InimigoEspecial(arcade.Sprite):
    def __init__(self):
        super().__init__(("inimigo.png"), scale=0.18)
        # Sorteia velocidades iniciais para os eixos X e Y
        self.change_x = random.choice([-3.0, 3.0])
        self.change_y = random.choice([-3.0, 3.0])

    def update(self, delta_time):
        # Atualiza a posição livremente pela tela
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Rebate nas bordas laterais
        if self.left < 0 or self.right > LARGURA:
            self.change_x *= -1

        # Rebate nas bordas superior e inferior
        if self.bottom < 0 or self.top > ALTURA:
            self.change_y *= -1


# ============================================================
# TELA INICIAL (MENU PRINCIPAL)
# ============================================================

class TelaInicial(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color((100, 10, 70))  # Define fundo tom roxo/vinho

        # Prepara todos os textos estáticos do menu
        self.txt_titulo = arcade.Text("BANANA JUNGLE", LARGURA / 2, 430, arcade.color.WHITE, 34, anchor_x="center")
        self.txt_jogar = arcade.Text("[J] Jogar", LARGURA / 2, 320, arcade.color.WHITE, 20, anchor_x="center")
        self.txt_tutorial = arcade.Text("[T] Tutorial", LARGURA / 2, 280, arcade.color.WHITE, 20, anchor_x="center")
        self.txt_sobre = arcade.Text("[S] Sobre o Jogo", LARGURA / 2, 240, arcade.color.WHITE, 20, anchor_x="center")
        self.txt_sair = arcade.Text("[ESC] Sair", LARGURA / 2, 200, arcade.color.WHITE, 20, anchor_x="center")

    def on_draw(self):
        self.clear()  # Limpa a tela antes de redesenhar
        # Desenha os textos do menu
        self.txt_titulo.draw()
        self.txt_jogar.draw()
        self.txt_tutorial.draw()
        self.txt_sobre.draw()
        self.txt_sair.draw()

    def on_key_press(self, key, modifiers):
        # Trata a navegação entre as telas do menu por teclado
        if key == arcade.key.J:
            self.window.show_view(TelaJogo())
        elif key == arcade.key.T:
            self.window.show_view(TelaTutorial())
        elif key == arcade.key.S:
            self.window.show_view(TelaSobre())
        elif key == arcade.key.ESCAPE:
            arcade.close_window()


# ============================================================
# TELA DE TUTORIAL
# ============================================================

class TelaTutorial(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color((100, 10, 70))

        # Configura as linhas de instrução de como jogar
        self.txt_titulo = arcade.Text("COMO JOGAR", LARGURA / 2, 480, arcade.color.WHITE, 30, anchor_x="center")
        self.txt_l1 = arcade.Text("Use A, D ou ⬅ ⮕ para mover os lados", LARGURA / 2, 420, arcade.color.WHITE, 17, anchor_x="center")
        self.txt_l2 = arcade.Text("Pressione W, ESPAÇO ou ⬆ para PULAR", LARGURA / 2, 380, arcade.color.WHITE, 17, anchor_x="center")
        self.txt_l3 = arcade.Text("Banana comum: +1 ponto", LARGURA / 2, 340, arcade.color.WHITE, 17, anchor_x="center")
        self.txt_l4 = arcade.Text("Banana especial: +5 pontos", LARGURA / 2, 305, arcade.color.WHITE, 17, anchor_x="center")
        self.txt_l5 = arcade.Text("Inimigos: -1 ponto ao colidir", LARGURA / 2, 270, arcade.color.WHITE, 17, anchor_x="center")
        self.txt_voltar = arcade.Text("[T] ou [ESC] para voltar ao menu", LARGURA / 2, 120, arcade.color.WHITE, 18, anchor_x="center")

    def on_draw(self):
        self.clear()
        self.txt_titulo.draw()
        self.txt_l1.draw()
        self.txt_l2.draw()
        self.txt_l3.draw()
        self.txt_l4.draw()
        self.txt_l5.draw()
        self.txt_voltar.draw()

    def on_key_press(self, key, modifiers):
        # Retorna ao menu inicial se pressionar T ou ESC
        if key == arcade.key.T or key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())


# ============================================================
# TELA SOBRE O JOGO
# ============================================================

class TelaSobre(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color((100, 10, 70))

        # Exibe a foto/avatar do desenvolvedor centralizada
        self.sprite_desenvolvedor = arcade.SpriteList()
        self.avatar = arcade.Sprite(("inimigo.png"), scale=0.18)
        self.avatar.center_x = LARGURA / 2
        self.avatar.center_y = 350
        self.sprite_desenvolvedor.append(self.avatar)

        # Informações sobre a autoria do projeto
        self.txt_titulo = arcade.Text("SOBRE O JOGO", LARGURA / 2, 500, arcade.color.WHITE, 32, anchor_x="center")
        self.txt_l1 = arcade.Text("Integrantes: [Enzo]", LARGURA / 2, 230, arcade.color.WHITE, 17, anchor_x="center")
        self.txt_l2 = arcade.Text("Jogo desenvolvido em Python com a biblioteca Arcade.", LARGURA / 2, 190, arcade.color.WHITE, 17, anchor_x="center")
        self.txt_l3 = arcade.Text("Atividade de Programação Orientada a Objetos (POO).", LARGURA / 2, 155, arcade.color.WHITE, 17, anchor_x="center")
        self.txt_voltar = arcade.Text("ESC ou M: voltar ao menu.", LARGURA / 2, 80, arcade.color.WHITE, 17, anchor_x="center")

    def on_draw(self):
        self.clear()
        self.txt_titulo.draw()
        self.sprite_desenvolvedor.draw()
        self.txt_l1.draw()
        self.txt_l2.draw()
        self.txt_l3.draw()
        self.txt_voltar.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE or key == arcade.key.M:
            self.window.show_view(TelaInicial())


# ============================================================
# TELA DO JOGO (GAMEPLAY PRINCIPAL)
# ============================================================

class TelaJogo(arcade.View):
    def __init__(self):
        super().__init__()

        # Carrega imagem de fundo
        self.fundo = arcade.load_texture(("floresta.png"))

        # Atributos de estado da partida
        self.movimento = 4
        self.pontuacao = 0
        self.tempo = 0.0
        self.dano = False          # Controla a visibilidade do aviso de dano
        self.alerta_timer = 0     # Temporizador para o texto de dano sumir

        # Quantidades de elementos do jogo
        self.qtd_moedas = 25
        self.qtd_moedas_especiais = 5
        self.qtd_inimigos = 3

        # Calcula a pontuação perfeita possível sem tomar nenhum dano
        self.pontuacao_maxima = (
            self.qtd_moedas * Moeda.valor_moeda
            + self.qtd_moedas_especiais * MoedaEspecial.valor_moeda
        )

        # Inicializa as listas organizadoras de Sprites para renderização e colisões
        self.sprite_blocos = arcade.SpriteList()
        self.sprite_jogador = arcade.SpriteList()
        self.sprite_moedas = arcade.SpriteList()
        self.sprite_moedas_especiais = arcade.SpriteList()
        self.sprite_inimigos = arcade.SpriteList()
        self.sprite_inimigo_especial = arcade.SpriteList()

        # --- CRIAÇÃO DO CHÃO CONTINUO ---
        tamanho_bloco = 64
        for x in range(32, LARGURA + 32, tamanho_bloco):
            chao = Bloco(x=x, y=30)
            self.sprite_blocos.append(chao)

        # --- CRIAÇÃO DE PLATAFORMAS FLUTUANTES ---
        plataformas_pos = [
            (300, 220),  # Esquerda
            (550, 220)   # Direita
        ]
        for x, y in plataformas_pos:
            plataforma = Bloco(x, y)
            self.sprite_blocos.append(plataforma)

        # --- CRIAÇÃO E POSICIONAMENTO DO JOGADOR ---
        self.jogador = Player()
        self.jogador.center_x = 64
        self.jogador.center_y = 100
        self.sprite_jogador.append(self.jogador)

        # Engine de física principal do jogador para colisão com chão/plataformas e gravidade
        self.engine_fisica = arcade.PhysicsEnginePlatformer(
            player_sprite=self.jogador,
            walls=self.sprite_blocos,
            gravity_constant=GRAVIDADE
        )

        # --- GERAÇÃO DAS MOEDAS NORMAIS ---
        for i in range(self.qtd_moedas):
            moeda = Moeda()
            moeda.center_x = random.randint(30, LARGURA - 30)
            moeda.center_y = random.randint(100, ALTURA - 30)
            self.sprite_moedas.append(moeda)

        # --- GERAÇÃO DAS MOEDAS ESPECIAIS (COM MOVIMENTO) ---
        for i in range(self.qtd_moedas_especiais):
            moeda_especial = MoedaEspecial()
            moeda_especial.center_x = random.randint(50, LARGURA - 50)
            moeda_especial.center_y = random.randint(100, ALTURA - 50)
            moeda_especial.change_x = random.choice([-self.movimento, self.movimento])
            moeda_especial.change_y = random.choice([-self.movimento, self.movimento])
            self.sprite_moedas_especiais.append(moeda_especial)

        # --- GERAÇÃO DOS INIMIGOS TERRESTRES (PERSEGUIDORES) ---
        for i in range(self.qtd_inimigos):
            inimigo = Inimigo(self.sprite_blocos, self.jogador)
            self.respawn_longe_do_jogador(inimigo, 180)  # Evita nascer em cima do player
            inimigo.center_y = 100
            self.sprite_inimigos.append(inimigo)

        # --- GERAÇÃO DO INIMIGO VOADOR (REBATE NAS BORDAS) ---
        self.inimigo_especial = InimigoEspecial()
        self.respawn_longe_do_jogador(self.inimigo_especial, 300)
        self.sprite_inimigo_especial.append(self.inimigo_especial)

        # Textos da Interface (HUD)
        self.txt_pontos = arcade.Text(f"Pontos: {self.pontuacao}", 10, 570, arcade.color.WHITE, 16)
        self.txt_tempo = arcade.Text(f"Tempo: {self.tempo:.1f}s", 10, 545, arcade.color.WHITE, 16)
        self.txt_maximo = arcade.Text(f"Máximo: {self.pontuacao_maxima}", 10, 520, arcade.color.WHITE, 16)
        self.txt_dano = arcade.Text("DANO RECEBIDO! -1 PONTO", LARGURA / 2, ALTURA / 2, arcade.color.RED, 28, anchor_x="center")

    def respawn_longe_do_jogador(self, inimigo, distancia_minima):
        """Gera posições aleatórias para os inimigos até encontrar uma distante do jogador."""
        while True:
            inimigo.center_x = random.randint(40, LARGURA - 40)
            inimigo.center_y = random.randint(100, ALTURA - 40)
            distancia = arcade.get_distance_between_sprites(inimigo, self.jogador)
            if distancia >= distancia_minima:
                break

    def on_draw(self):
        self.clear()

        # Desenha a textura de fundo esticada para toda a janela
        arcade.draw_texture_rect(
            texture=self.fundo,
            rect=arcade.XYWH(LARGURA / 2, ALTURA / 2, LARGURA, ALTURA)
        )

        # Desenha todas as listas de sprites na ordem de visualização (Camadas)
        self.sprite_blocos.draw()
        self.sprite_jogador.draw()
        self.sprite_moedas.draw()
        self.sprite_moedas_especiais.draw()
        self.sprite_inimigos.draw()
        self.sprite_inimigo_especial.draw()

        # Desenha os textos do HUD
        self.txt_pontos.draw()
        self.txt_tempo.draw()
        self.txt_maximo.draw()

        # Exibe mensagem temporária de dano apenas se self.dano for True
        if self.dano:
            self.txt_dano.draw()

    def on_update(self, delta_time):
        self.tempo += delta_time
        self.engine_fisica.update()  # Atualiza posições físicas e gravidade do jogador

        # Atualiza os textos do HUD com os valores atuais
        self.txt_pontos.text = f"Pontos: {self.pontuacao}"
        self.txt_tempo.text = f"Tempo: {self.tempo:.1f}s"

        # Executa o método update de cada grupo de objetos
        self.sprite_jogador.update(delta_time)
        self.sprite_moedas.update(delta_time)
        self.sprite_moedas_especiais.update(delta_time)

        for inimigo in self.sprite_inimigos:
            inimigo.update(delta_time)

        self.sprite_inimigo_especial.update(delta_time)

        # --- LÓGICA DE COLISÕES COM MOEDAS NORMAIS ---
        moedas_colididas = arcade.check_for_collision_with_list(self.jogador, self.sprite_moedas)
        for moeda in moedas_colididas:
            self.pontuacao += moeda.valor_moeda
            moeda.remove_from_sprite_lists()  # Deleta a moeda coletada

        # --- LÓGICA DE COLISÕES COM MOEDAS ESPECIAIS ---
        moedas_especiais_colididas = arcade.check_for_collision_with_list(self.jogador, self.sprite_moedas_especiais)
        for moeda in moedas_especiais_colididas:
            self.pontuacao += moeda.valor_moeda
            moeda.remove_from_sprite_lists()

        # --- LÓGICA DE COLISÕES COM INIMIGOS TERRESTRES ---
        inimigos_colididos = arcade.check_for_collision_with_list(self.jogador, self.sprite_inimigos)
        for inimigo in inimigos_colididos:
            self.pontuacao -= 1
            self.alerta_dano()
            self.respawn_longe_do_jogador(inimigo, 150)  # Teleporta o inimigo após colisão
            inimigo.center_y = 100

        # --- LÓGICA DE COLISÃO COM INIMIGO ESPECIAL ---
        if arcade.check_for_collision(self.jogador, self.inimigo_especial):
            self.pontuacao -= 1
            self.alerta_dano()
            self.respawn_longe_do_jogador(self.inimigo_especial, 300)

        # Controla o tempo de exibição do alerta vermelho na tela
        if self.dano:
            self.alerta_timer -= delta_time
            if self.alerta_timer <= 0:
                self.dano = False

        # CONDIÇÃO DE VITÓRIA / TÉRMINO: Se não houver mais moedas no mapa
        if len(self.sprite_moedas) == 0 and len(self.sprite_moedas_especiais) == 0:
            self.window.show_view(TelaFinal(self.pontuacao, self.tempo, self.pontuacao_maxima))

    def alerta_dano(self):
        """Ativa o aviso visual de dano por 0,5 segundo."""
        self.dano = True
        self.alerta_timer = 0.5

    def on_key_press(self, key, modifiers):
        # Trata as teclas pressionadas para movimentação e pause/saída
        if key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())
            return

        # Movimento Lateral
        if key in (arcade.key.A, arcade.key.LEFT):
            self.jogador.change_x = -self.movimento
        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.jogador.change_x = self.movimento

        # Pulo (Verifica se está pisando em algum bloco/chão antes de pular)
        if key in (arcade.key.W, arcade.key.SPACE, arcade.key.UP):
            if self.engine_fisica.can_jump():
                self.jogador.change_y = FORCA_PULO

    def on_key_release(self, key, modifiers):
        # Zera a velocidade horizontal quando solta a tecla de andar
        if key in (arcade.key.A, arcade.key.D, arcade.key.LEFT, arcade.key.RIGHT):
            self.jogador.change_x = 0


# ============================================================
# TELA FINAL (RESULTADOS)
# ============================================================

class TelaFinal(arcade.View):
    def __init__(self, pontos, tempo, pontuacao_maxima):
        super().__init__()
        self.pontos = pontos
        self.tempo = tempo
        self.pontuacao_maxima = pontuacao_maxima
        arcade.set_background_color((100, 10, 70))

        # Montagem das mensagens de resumo
        self.txt_titulo = arcade.Text("JOGO FINALIZADO!", LARGURA / 2, 430, arcade.color.WHITE, 34, anchor_x="center")
        self.txt_pontos = arcade.Text(f"Pontuação: {self.pontos}", LARGURA / 2, 350, arcade.color.WHITE, 22, anchor_x="center")
        self.txt_tempo = arcade.Text(f"Tempo total: {self.tempo:.1f}s", LARGURA / 2, 315, arcade.color.WHITE, 20, anchor_x="center")

        # Verifica se o jogador obteve a pontuação perfeita
        if self.pontos >= self.pontuacao_maxima:
            self.txt_status = arcade.Text("PARABÉNS! PONTUAÇÃO MÁXIMA!", LARGURA / 2, 255, arcade.color.YELLOW, 24, anchor_x="center")
            self.txt_sub = arcade.Text("Você escapou de todos os inimigos perfeitamente!", LARGURA / 2, 220, arcade.color.WHITE, 17, anchor_x="center")
        else:
            self.txt_status = arcade.Text("PARABÉNS! O JOGO FOI CONCLUÍDO!", LARGURA / 2, 255, arcade.color.WHITE, 22, anchor_x="center")
            self.txt_sub = None

        self.txt_menu = arcade.Text("[M] Voltar ao Menu Principal", LARGURA / 2, 150, arcade.color.WHITE, 18, anchor_x="center")
        self.txt_sair = arcade.Text("[ESC] Sair do Jogo", LARGURA / 2, 110, arcade.color.WHITE, 18, anchor_x="center")

    def on_draw(self):
        self.clear()
        self.txt_titulo.draw()
        self.txt_pontos.draw()
        self.txt_tempo.draw()
        self.txt_status.draw()
        if self.txt_sub:
            self.txt_sub.draw()
        self.txt_menu.draw()
        self.txt_sair.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.M:
            self.window.show_view(TelaInicial())
        elif key == arcade.key.ESCAPE:
            arcade.close_window()


# ============================================================
# PONTO DE ENTRADA DO PROGRAMA
# ============================================================

def main():
    # Inicializa a janela principal do Arcade
    janela = arcade.Window(LARGURA, ALTURA, TITULO)
    # Define a view inicial exibida ao abrir o jogo
    janela.show_view(TelaInicial())
    # Inicia o loop principal do Arcade
    arcade.run()


if __name__ == "__main__":
    main()