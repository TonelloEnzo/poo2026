import arcade
import random
import datetime
from peewee import (
    Model,
    CharField,
    IntegerField,
    FloatField,
    DateTimeField,
    SqliteDatabase,
)

# ============================================================
# CONFIGURAÇÕES GERAIS
# ============================================================
LARGURA = 800
ALTURA = 600
TITULO = "Banana Jungle"
GRAVIDADE = 0.5
FORCA_PULO = 14
VELOCIDADE_JOGADOR = 4
COR_MENU = (100, 10, 70)

# Folha enviada: 2048 x 682 pixels, com 4 quadros horizontais.
# Cada quadro mede 512 x 682 pixels. Os 3 primeiros são caminhada
# e o 4º é a pose de pulo.
TAMANHO_QUADRO = (512, 682)
COLUNAS_SPRITESHEET = 4
QUANTIDADE_QUADROS = 4
QUADROS_CAMINHADA = 3
TEMPO_QUADRO = 0.12

# ============================================================
# BANCO DE DADOS — PEEWEE ORM
# ============================================================
db = SqliteDatabase("ranking.db")


class BaseModel(Model):
    class Meta:
        database = db


class Pontuacao(BaseModel):
    nome_jogador = CharField()
    pontos = IntegerField()
    tempo_partida = FloatField()
    data_hora = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return (
            f"{self.nome_jogador} - {self.pontos} pts "
            f"({self.tempo_partida:.1f}s)"
        )


def preparar_banco():
    """Abre o banco e cria a tabela caso ela ainda não exista."""
    if db.is_closed():
        db.connect(reuse_if_open=True)
    db.create_tables([Pontuacao])


# ============================================================
# PLAYER — PERSONAGEM CONTROLADO PELO JOGADOR
# ============================================================
class Player(arcade.Sprite):
    def __init__(self):
        # O requisito da atividade pede load_spritesheet e get_texture_grid.
        # A folha é fatiada em quadros para a animação de caminhada.
        self.spritesheet_ok = False
        self.quadros_direita = []

        try:
            folha = arcade.load_spritesheet("player_direita.png")
            self.quadros_direita = folha.get_texture_grid(
                size=TAMANHO_QUADRO,
                columns=COLUNAS_SPRITESHEET,
                count=QUANTIDADE_QUADROS,
            )
            if not self.quadros_direita:
                raise ValueError("A folha de sprites não retornou quadros.")
            self.spritesheet_ok = True
            textura_inicial = self.quadros_direita[0]
        except (FileNotFoundError, OSError, ValueError, TypeError, AttributeError):
            # Compatibilidade com os sprites antigos do projeto.
            # Para cumprir integralmente a atividade, mantenha a spritesheet
            # player_direita.png na pasta do jogo e confira suas dimensões.
            textura_inicial = arcade.load_texture("dir macaco.png")

        super().__init__(textura_inicial, scale=0.16)

        self.virado_para = "direita"
        self.textura_parado_direita = self.quadros_direita[0] if self.spritesheet_ok else arcade.load_texture("dir macaco.png")
        if self.spritesheet_ok:
            self.texturas_andando_direita = self.quadros_direita
            self.texturas_andando_esquerda = [
                textura.flip_left_right() for textura in self.quadros_direita
            ]
            # O 4º quadro é a pose de pulo; não entra no ciclo de caminhada.
            self.textura_pulo_direita = self.quadros_direita[3]
            self.texturas_andando_direita = self.quadros_direita[:QUADROS_CAMINHADA]
            self.textura_parado_esquerda = self.textura_parado_direita.flip_left_right()
            self.textura_pulo_esquerda = self.textura_pulo_direita.flip_left_right()
        else:
            self.textura_parado_esquerda = arcade.load_texture("esq macaco.png")
            self.texturas_andando_direita = [self.textura_parado_direita]
            self.texturas_andando_esquerda = [self.textura_parado_esquerda]
            self.textura_pulo_direita = self.textura_parado_direita
            self.textura_pulo_esquerda = self.textura_parado_esquerda

        self.indice_quadro = 0
        self.tempo_animacao = 0.0
        self.estado_atual = "parado"

    def update(self, delta_time: float = 1 / 60):
        # Prioridade de estados exigida na atividade:
        # 1. Pulo/queda; 2. Parado; 3. Andando.
        if self.change_x > 0:
            self.virado_para = "direita"
        elif self.change_x < 0:
            self.virado_para = "esquerda"

        if self.change_y != 0:
            self.estado_atual = "pulo"
            self.texture = (
                self.textura_pulo_direita
                if self.virado_para == "direita"
                else self.textura_pulo_esquerda
            )
            self.tempo_animacao = 0.0
        elif self.change_x == 0:
            self.estado_atual = "parado"
            self.texture = (
                self.textura_parado_direita
                if self.virado_para == "direita"
                else self.textura_parado_esquerda
            )
            self.tempo_animacao = 0.0
        else:
            self.estado_atual = "andando"
            self.tempo_animacao += delta_time
            if self.tempo_animacao >= TEMPO_QUADRO:
                self.tempo_animacao -= TEMPO_QUADRO
                self.indice_quadro = (
                    self.indice_quadro + 1
                ) % len(self.texturas_andando_direita)

            quadros = (
                self.texturas_andando_direita
                if self.virado_para == "direita"
                else self.texturas_andando_esquerda
            )
            self.texture = quadros[self.indice_quadro]

        # Limita o personagem à largura da janela.
        if self.right > LARGURA:
            self.right = LARGURA
            self.change_x = 0
        elif self.left < 0:
            self.left = 0
            self.change_x = 0




# ============================================================
# BLOCO / PLATAFORMA
# ============================================================
class Bloco(arcade.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__("bloco.png", scale=0.5)
        self.center_x = x
        self.center_y = y


# ============================================================
# MOEDA COMUM
# ============================================================
class Moeda(arcade.Sprite):
    valor_moeda = 1

    def __init__(self):
        super().__init__("banana.png", scale=0.10)


# ============================================================
# MOEDA ESPECIAL
# ============================================================
class MoedaEspecial(arcade.Sprite):
    valor_moeda = 5

    def __init__(self):
        super().__init__("banana.png", scale=0.14)

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
            self.change_x = abs(self.change_x)
        elif self.right > LARGURA:
            self.right = LARGURA
            self.change_x = -abs(self.change_x)

        if self.center_y < 70:
            self.center_y = 70
            self.change_y = abs(self.change_y)
        elif self.center_y > 245:
            self.center_y = 245
            self.change_y = -abs(self.change_y)


# ============================================================
# INIMIGO TERRESTRE
# ============================================================
class Inimigo(arcade.Sprite):
    """Inimigo terrestre que patrulha de um lado para o outro sem perseguir o jogador."""
    def __init__(self, blocos: arcade.SpriteList, jogador: Player = None):
        super().__init__("inimigo.png", scale=0.15)
        # Mantém o parâmetro jogador por compatibilidade, mas não o usa para perseguir.
        self.velocidade = random.choice([1.5, 1.8, 2.1])
        self.direcao = random.choice([-1, 1])
        self.change_x = self.velocidade * self.direcao
        self.engine_fisica = arcade.PhysicsEnginePlatformer(
            player_sprite=self,
            walls=blocos,
            gravity_constant=GRAVIDADE,
        )

    def update(self, delta_time: float = 1 / 60):
        # Patrulha o chão e inverte a direção ao tocar nas bordas da tela.
        self.change_x = self.velocidade * self.direcao
        self.engine_fisica.update()

        if self.left <= 0:
            self.left = 0
            self.direcao = 1
        elif self.right >= LARGURA:
            self.right = LARGURA
            self.direcao = -1


# ============================================================
# INIMIGO ESPECIAL VOADOR
# ============================================================
class InimigoEspecial(arcade.Sprite):
    def __init__(self):
        super().__init__("inimigo.png", scale=0.15)
        self.change_x = random.choice([-3.0, 3.0])
        self.change_y = random.choice([-3.0, 3.0])

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
            self.change_x = abs(self.change_x)
        elif self.right > LARGURA:
            self.right = LARGURA
            self.change_x = -abs(self.change_x)

        if self.bottom < 0:
            self.bottom = 0
            self.change_y = abs(self.change_y)
        elif self.top > ALTURA:
            self.top = ALTURA
            self.change_y = -abs(self.change_y)

class Explosao(arcade.Sprite):
    def __init__(self, x, y):
        folha = arcade.load_spritesheet("explosao.png")
        self.quadros = folha.get_texture_grid(
            size=(334, 334),
            columns=4,
            count=4
        )

        super().__init__(self.quadros[0], scale=0.55)

        self.center_x = x
        self.center_y = y
        self.indice_quadro = 0
        self.tempo = 0

    def update(self, delta_time=1 / 60):
        self.tempo += delta_time

        if self.tempo >= 0.07:
            self.tempo = 0
            self.indice_quadro += 1

            if self.indice_quadro >= len(self.quadros):
                self.remove_from_sprite_lists()
                return

            self.texture = self.quadros[self.indice_quadro]

# ============================================================
# TELA INICIAL
# ============================================================
class TelaInicial(arcade.View):
    def __init__(self):
        super().__init__()
        self.txt_titulo = arcade.Text("BANANA JUNGLE", LARGURA / 2, 440, arcade.color.WHITE, 34, anchor_x="center")
        self.txt_jogar = arcade.Text("[J] Jogar", LARGURA / 2, 340, arcade.color.WHITE, 20, anchor_x="center")
        self.txt_tutorial = arcade.Text("[T] Tutorial", LARGURA / 2, 300, arcade.color.WHITE, 20, anchor_x="center")
        self.txt_sobre = arcade.Text("[S] Sobre o jogo", LARGURA / 2, 260, arcade.color.WHITE, 20, anchor_x="center")
        self.txt_ranking = arcade.Text("[R] Ranking Top 10", LARGURA / 2, 220, arcade.color.WHITE, 20, anchor_x="center")
        self.txt_sair = arcade.Text("[ESC] Sair", LARGURA / 2, 180, arcade.color.WHITE, 20, anchor_x="center")

    def on_show_view(self):
        arcade.set_background_color(COR_MENU)

    def on_draw(self):
        self.clear()
        for texto in (self.txt_titulo, self.txt_jogar, self.txt_tutorial, self.txt_sobre, self.txt_ranking, self.txt_sair):
            texto.draw()

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.J, arcade.key.ENTER):
            self.window.show_view(TelaJogo())
        elif key == arcade.key.T:
            self.window.show_view(TelaTutorial())
        elif key == arcade.key.S:
            self.window.show_view(TelaSobre())
        elif key == arcade.key.R:
            self.window.show_view(TelaRanking())
        elif key == arcade.key.ESCAPE:
            arcade.close_window()


# ============================================================
# TELA DE TUTORIAL
# ============================================================
class TelaTutorial(arcade.View):
    def __init__(self):
        super().__init__()
        self.textos = [
            arcade.Text("COMO JOGAR", LARGURA / 2, 480, arcade.color.WHITE, 30, anchor_x="center"),
            arcade.Text("Use A, D ou as setas para andar", LARGURA / 2, 420, arcade.color.WHITE, 17, anchor_x="center"),
            arcade.Text("Pressione W, ESPAÇO ou ↑ para pular", LARGURA / 2, 380, arcade.color.WHITE, 17, anchor_x="center"),
            arcade.Text("Banana comum: +1 ponto", LARGURA / 2, 340, arcade.color.WHITE, 17, anchor_x="center"),
            arcade.Text("Banana especial: +5 pontos", LARGURA / 2, 305, arcade.color.WHITE, 17, anchor_x="center"),
            arcade.Text("Colidir com inimigos: -1 ponto", LARGURA / 2, 270, arcade.color.WHITE, 17, anchor_x="center"),
            arcade.Text("[ESC] Voltar ao menu", LARGURA / 2, 120, arcade.color.WHITE, 18, anchor_x="center"),
        ]

    def on_show_view(self):
        arcade.set_background_color(COR_MENU)

    def on_draw(self):
        self.clear()
        for texto in self.textos:
            texto.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())


# ============================================================
# TELA SOBRE
# ============================================================
class TelaSobre(arcade.View):
    def __init__(self):
        super().__init__()
        self.avatar = arcade.Sprite("inimigo.png", scale=0.18)
        self.avatar.center_x = LARGURA / 2
        self.avatar.center_y = 350
        self.sprite_desenvolvedor = arcade.SpriteList()
        self.sprite_desenvolvedor.append(self.avatar)
        self.textos = [
            arcade.Text("SOBRE O JOGO", LARGURA / 2, 500, arcade.color.WHITE, 32, anchor_x="center"),
            arcade.Text("Integrante: Enzo", LARGURA / 2, 230, arcade.color.WHITE, 17, anchor_x="center"),
            arcade.Text("Jogo desenvolvido em Python com Arcade.", LARGURA / 2, 190, arcade.color.WHITE, 17, anchor_x="center"),
            arcade.Text("Atividade de Programação Orientada a Objetos.", LARGURA / 2, 155, arcade.color.WHITE, 17, anchor_x="center"),
            arcade.Text("[ESC] Voltar ao menu", LARGURA / 2, 80, arcade.color.WHITE, 17, anchor_x="center"),
        ]

    def on_show_view(self):
        arcade.set_background_color(COR_MENU)

    def on_draw(self):
        self.clear()
        self.sprite_desenvolvedor.draw()
        for texto in self.textos:
            texto.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())


# ============================================================
# TELA DO JOGO
# ============================================================
class TelaJogo(arcade.View):
    def __init__(self):
        super().__init__()
        self.sprite_explosoes = arcade.SpriteList()
        self.fundo = arcade.load_texture("floresta.png")
        self.pontuacao = 0
        self.tempo = 0.0
        self.dano = False
        self.alerta_timer = 0.0
        self.movimento = VELOCIDADE_JOGADOR

        self.qtd_moedas = 25
        self.qtd_moedas_especiais = 5
        self.qtd_inimigos = 3
        self.pontuacao_maxima = (
            self.qtd_moedas * Moeda.valor_moeda
            + self.qtd_moedas_especiais * MoedaEspecial.valor_moeda
        )

        self.sprite_blocos = arcade.SpriteList()
        self.sprite_jogador = arcade.SpriteList()
        self.sprite_moedas = arcade.SpriteList()
        self.sprite_moedas_especiais = arcade.SpriteList()
        self.sprite_inimigos = arcade.SpriteList()
        self.sprite_inimigo_especial = arcade.SpriteList()

        # Chão e plataformas suspensas.
        for x in range(32, LARGURA + 32, 64):
            self.sprite_blocos.append(Bloco(x, 30))
        for x, y in [(270, 190), (700, 190), (500, 350)]:
            self.sprite_blocos.append(Bloco(x, y))

        self.jogador = Player()
        self.jogador.center_x = 64
        self.jogador.center_y = 100
        self.sprite_jogador.append(self.jogador)

        self.engine_fisica = arcade.PhysicsEnginePlatformer(
            player_sprite=self.jogador,
            walls=self.sprite_blocos,
            gravity_constant=GRAVIDADE,
        )

        # Bananas distribuídas pelo chão e também logo acima das plataformas.
        # As plataformas ficam em uma altura moderada para serem alcançáveis.
        posicoes_bananas = []

        def registrar_posicao(x, y):
            posicoes_bananas.append((x, y))
            return x, y

        def escolher_posicao_banana():
            # Alterna entre regiões baixas, saltos médios e áreas acima das plataformas.
            faixas = [(65, 105), (90, 140), (125, 170), (205, 235)]
            for _tentativa in range(60):
                x = random.randint(45, LARGURA - 45)
                y = random.randint(*random.choice(faixas))
                # Evita aglomeração, mas permite que o mapa fique bem preenchido.
                if all(abs(x - px) > 55 or abs(y - py) > 28 for px, py in posicoes_bananas):
                    return registrar_posicao(x, y)
            return registrar_posicao(random.randint(45, LARGURA - 45), random.randint(70, 225))

        # Parte das bananas fica propositalmente acima das duas plataformas.
        posicoes_plataformas = [
            (random.randint(220, 320), random.randint(215, 230)),
            (random.randint(490, 590), random.randint(215, 230)),
        ]
        for x, y in posicoes_plataformas:
            registrar_posicao(x, y)

        # Cria bananas comuns; as primeiras duas ficam sobre as plataformas.
        for indice in range(self.qtd_moedas):
            moeda = Moeda()
            if indice < len(posicoes_plataformas):
                moeda.center_x, moeda.center_y = posicoes_plataformas[indice]
            else:
                moeda.center_x, moeda.center_y = escolher_posicao_banana()
            self.sprite_moedas.append(moeda)

        # Bananas especiais se movem tanto na horizontal quanto na vertical.
        # A velocidade diagonal muda de sinal ao tocar os limites do espaço jogável.
        for _ in range(self.qtd_moedas_especiais):
            moeda = MoedaEspecial()
            moeda.center_x, moeda.center_y = escolher_posicao_banana()
            moeda.change_x = random.choice([-1.2, -0.8, 0.8, 1.2])
            moeda.change_y = random.choice([-0.7, -0.5, 0.5, 0.9])
            self.sprite_moedas_especiais.append(moeda)

        for _ in range(self.qtd_inimigos):
            inimigo = Inimigo(self.sprite_blocos, self.jogador)
            self.respawn_longe_do_jogador(inimigo, 180)
            inimigo.center_y = 100
            self.sprite_inimigos.append(inimigo)

        self.inimigo_especial = InimigoEspecial()
        self.respawn_longe_do_jogador(self.inimigo_especial, 300)
        self.sprite_inimigo_especial.append(self.inimigo_especial)

        self.txt_pontos = arcade.Text("", 10, 570, arcade.color.WHITE, 16)
        self.txt_tempo = arcade.Text("", 10, 545, arcade.color.WHITE, 16)
        self.txt_maximo = arcade.Text(f"Máximo: {self.pontuacao_maxima}", 10, 520, arcade.color.WHITE, 16)
        self.txt_dano = arcade.Text("DANO RECEBIDO! -1 PONTO", LARGURA / 2, ALTURA / 2, arcade.color.RED, 25, anchor_x="center")

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def respawn_longe_do_jogador(self, inimigo, distancia_minima):
        for _ in range(100):
            inimigo.center_x = random.randint(40, LARGURA - 40)
            
            if arcade.get_distance_between_sprites(inimigo, self.jogador) >= distancia_minima:
                return
        # Fallback para evitar um loop infinito em mapas pequenos.
        inimigo.center_x = LARGURA - 60
        inimigo.center_y = ALTURA - 60

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            texture=self.fundo,
            rect=arcade.XYWH(LARGURA / 2, ALTURA / 2, LARGURA, ALTURA),
        )
        self.sprite_explosoes.draw()
        self.sprite_blocos.draw()
        self.sprite_moedas.draw()
        self.sprite_moedas_especiais.draw()
        self.sprite_jogador.draw()
        self.sprite_inimigos.draw()
        self.sprite_inimigo_especial.draw()
        self.txt_pontos.draw()
        self.txt_tempo.draw()
        self.txt_maximo.draw()
        if self.dano:
            self.txt_dano.draw()

    def on_update(self, delta_time: float):
        self.tempo += delta_time
        self.sprite_explosoes.update(delta_time)

        # A engine atualiza física e gravidade do jogador.
        self.engine_fisica.update()

        # O Player.update trata apenas estados visuais; os outros atores
        # mantêm seus próprios comportamentos. Isso usa polimorfismo.
        self.sprite_jogador.update(delta_time)
        self.sprite_moedas.update(delta_time)
        self.sprite_moedas_especiais.update(delta_time)
        self.sprite_inimigos.update(delta_time)
        self.sprite_inimigo_especial.update(delta_time)

        self.txt_pontos.text = f"Pontos: {self.pontuacao}"
        self.txt_tempo.text = f"Tempo: {self.tempo:.1f}s"

        for moeda in arcade.check_for_collision_with_list(self.jogador, self.sprite_moedas):
            self.pontuacao += moeda.valor_moeda
            moeda.remove_from_sprite_lists()

        for moeda in arcade.check_for_collision_with_list(self.jogador, self.sprite_moedas_especiais):
            self.pontuacao += moeda.valor_moeda
            moeda.remove_from_sprite_lists()

        for inimigo in arcade.check_for_collision_with_list(
            self.jogador, self.sprite_inimigos
        ):
            explosao = Explosao(
                self.jogador.center_x,
                self.jogador.center_y
            )
            self.sprite_explosoes.append(explosao)

            self.pontuacao -= 1
            self.alerta_dano()
            self.respawn_longe_do_jogador(inimigo, 150)
            inimigo.center_y = 100
            inimigo.change_y = 0

        if arcade.check_for_collision(self.jogador, self.inimigo_especial):
            explosao = Explosao(
                self.jogador.center_x,
                self.jogador.center_y
            )
            self.sprite_explosoes.append(explosao)

            self.pontuacao -= 1
            self.alerta_dano()
            self.respawn_longe_do_jogador(self.inimigo_especial, 300)

        if self.dano:
            self.alerta_timer -= delta_time
            if self.alerta_timer <= 0:
                self.dano = False

        if len(self.sprite_moedas) == 0 and len(self.sprite_moedas_especiais) == 0:
            self.window.show_view(
                TelaFinal(self.pontuacao, self.tempo, self.pontuacao_maxima)
            )

    def alerta_dano(self):
        self.dano = True
        self.alerta_timer = 0.5

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())
            return
        if key in (arcade.key.A, arcade.key.LEFT):
            self.jogador.change_x = -self.movimento
        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.jogador.change_x = self.movimento
        elif key in (arcade.key.W, arcade.key.SPACE, arcade.key.UP):
            # can_jump() bloqueia o pulo duplo no ar.
            if self.engine_fisica.can_jump():
                self.jogador.change_y = FORCA_PULO

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.D, arcade.key.LEFT, arcade.key.RIGHT):
            self.jogador.change_x = 0


# ============================================================
# TELA FINAL — CAPTURA DO NOME E SALVAMENTO
# ============================================================
class TelaFinal(arcade.View):
    def __init__(self, pontos: int, tempo: float, pontuacao_maxima: int):
        super().__init__()
        self.pontos = pontos
        self.tempo = tempo
        self.pontuacao_maxima = pontuacao_maxima
        self.nome_digitado = ""
        self.salvo = False
        self.mensagem = "Digite seu nome e pressione ENTER para salvar."
        self.cor_mensagem = arcade.color.WHITE

        self.txt_titulo = arcade.Text("JOGO FINALIZADO!", LARGURA / 2, 455, arcade.color.WHITE, 32, anchor_x="center")
        self.txt_pontos = arcade.Text(f"Pontuação: {pontos}", LARGURA / 2, 395, arcade.color.WHITE, 22, anchor_x="center")
        self.txt_tempo = arcade.Text(f"Tempo total: {tempo:.1f}s", LARGURA / 2, 360, arcade.color.WHITE, 20, anchor_x="center")
        self.txt_instrucao = arcade.Text(self.mensagem, LARGURA / 2, 290, arcade.color.WHITE, 16, anchor_x="center")
        self.txt_nome = arcade.Text("", LARGURA / 2, 245, arcade.color.YELLOW, 22, anchor_x="center")
        self.txt_ranking = arcade.Text("[R] Ver ranking Top 10", LARGURA / 2, 150, arcade.color.WHITE, 18, anchor_x="center")
        self.txt_menu = arcade.Text("[M] Voltar ao menu", LARGURA / 2, 115, arcade.color.WHITE, 18, anchor_x="center")
        self.txt_sair = arcade.Text("[ESC] Sair", LARGURA / 2, 80, arcade.color.WHITE, 18, anchor_x="center")

    def on_show_view(self):
        arcade.set_background_color(COR_MENU)

    def on_draw(self):
        self.clear()
        self.txt_titulo.draw()
        self.txt_pontos.draw()
        self.txt_tempo.draw()
        self.txt_instrucao.draw()
        self.txt_nome.draw()
        self.txt_ranking.draw()
        self.txt_menu.draw()
        self.txt_sair.draw()

    def on_text(self, text):
        if self.salvo:
            return
        # Aceita letras, números e espaços, limitando o nome a 24 caracteres.
        texto_limpo = "".join(caractere for caractere in text if caractere.isprintable())
        self.nome_digitado = (self.nome_digitado + texto_limpo)[:24]
        self.txt_nome.text = self.nome_digitado

    def on_key_press(self, key, modifiers):
        if key == arcade.key.BACKSPACE and not self.salvo:
            self.nome_digitado = self.nome_digitado[:-1]
            self.txt_nome.text = self.nome_digitado
        elif key in (arcade.key.ENTER, arcade.key.RETURN) and not self.salvo:
            self.salvar_pontuacao()
        elif key == arcade.key.R:
            if self.salvo:
                self.window.show_view(TelaRanking())
            else:
                self.mensagem = "Salve a pontuação antes de abrir o ranking."
                self.txt_instrucao.text = self.mensagem
        elif key == arcade.key.M:
            self.window.show_view(TelaInicial())
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

    def salvar_pontuacao(self):
        nome = self.nome_digitado.strip()
        if not nome:
            self.mensagem = "Digite um nome antes de pressionar ENTER."
            self.txt_instrucao.text = self.mensagem
            return

        try:
            preparar_banco()
            Pontuacao.create(
                nome_jogador=nome,
                pontos=self.pontos,
                tempo_partida=self.tempo,
            )
            self.salvo = True
            self.mensagem = "Pontuação salva! Pressione R para ver o ranking."
            self.txt_instrucao.text = self.mensagem
        except Exception as erro:
            self.mensagem = f"Erro ao salvar no banco: {erro}"
            self.txt_instrucao.text = self.mensagem


# ============================================================
# TELA RANKING — TOP 10
# ============================================================
class TelaRanking(arcade.View):
    def __init__(self):
        super().__init__()
        preparar_banco()

        # IMPORTANTE: a consulta ocorre uma única vez no __init__,
        # nunca dentro de on_draw(), conforme o documento do professor.
        self.melhores = list(
            Pontuacao.select()
            .order_by(Pontuacao.pontos.desc(), Pontuacao.tempo_partida.asc())
            .limit(10)
        )

        self.txt_titulo = arcade.Text("RANKING — TOP 10", LARGURA / 2, 520, arcade.color.WHITE, 30, anchor_x="center")
        self.txt_ajuda = arcade.Text("[M] Menu principal   [ESC] Sair", LARGURA / 2, 55, arcade.color.WHITE, 16, anchor_x="center")
        self.txt_vazio = arcade.Text("Ainda não há pontuações registradas.", LARGURA / 2, 300, arcade.color.WHITE, 18, anchor_x="center")
        self.linhas = []
        for indice, registro in enumerate(self.melhores):
            y = 455 - indice * 38
            linha = arcade.Text(
                f"{indice + 1}. {registro.nome_jogador} — {registro.pontos} pts — {registro.tempo_partida:.1f}s",
                100, y, arcade.color.WHITE, 18,
            )
            self.linhas.append(linha)

    def on_show_view(self):
        arcade.set_background_color(COR_MENU)

    def on_draw(self):
        self.clear()
        self.txt_titulo.draw()
        if not self.melhores:
            self.txt_vazio.draw()
        else:
            for linha in self.linhas:
                linha.draw()
        self.txt_ajuda.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.M:
            self.window.show_view(TelaInicial())
        elif key == arcade.key.ESCAPE:
            arcade.close_window()


# ============================================================
# INICIALIZAÇÃO
# ============================================================
def main():
    preparar_banco()
    janela = arcade.Window(LARGURA, ALTURA, TITULO)
    janela.show_view(TelaInicial())
    arcade.run()


if __name__ == "__main__":
    main()
