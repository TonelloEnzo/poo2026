import arcade
import random

# ============================================================
# CONFIGURAÇÕES
# ============================================================

ALTURA = 600
LARGURA = 800
TITULO = "Meu Jogo"


# ============================================================
# PLAYER
# ============================================================
class Bloco(arcade.Sprite):
    def __init__(self, x: float, y: float):
        super().__init__("bloco.png", scale=0.5)
        self.center_x = x
        self.center_y = y
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("dir macaco.png", scale=0.20)

        self.textura_direita = arcade.load_texture("dir macaco.png")
        self.textura_esquerda = arcade.load_texture("esq macaco.png")

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # A textura muda de acordo com o sentido horizontal.
        if self.change_x > 0:
            self.texture = self.textura_direita
        elif self.change_x < 0:
            self.texture = self.textura_esquerda

        # Travar o jogador dentro da janela.
        if self.right > LARGURA:
            self.change_x = 0
            self.right = LARGURA
        elif self.left < 0:
            self.change_x = 0
            self.left = 0

        if self.top > ALTURA:
            self.change_y = 0
            self.top = ALTURA
        elif self.bottom < 0:
            self.change_y = 0
            self.bottom = 0


# ============================================================
# MOEDA ESTÁTICA
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
        # Mantém a imagem já existente do projeto.
        super().__init__("banana.png", scale=0.14)

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Rebote nas bordas.
        if self.left < 0 or self.right > LARGURA:
            self.change_x *= -1

        if self.bottom < 0 or self.top > ALTURA:
            self.change_y *= -1


# ============================================================
# INIMIGO COMUM
# ============================================================

class Inimigo(arcade.Sprite):
    def __init__(self):
        super().__init__("inimigo.png", scale=0.15)

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # O inimigo também utiliza rebote.
        if self.left < 0 or self.right > LARGURA:
            self.change_x *= -1

        if self.bottom < 0 or self.top > ALTURA:
            self.change_y *= -1


# ============================================================
# INIMIGO ESPECIAL - SEGUE O PLAYER
# ============================================================

class InimigoEspecial(arcade.Sprite):
    def __init__(self, jogador):
        super().__init__("inimigo.png", scale=0.18)

        self.jogador = jogador
        self.movimento = 1.5

    def update(self, delta_time):
        # Persegue continuamente o jogador.
        if self.center_x < self.jogador.center_x:
            self.center_x += self.movimento
        elif self.center_x > self.jogador.center_x:
            self.center_x -= self.movimento

        if self.center_y < self.jogador.center_y:
            self.center_y += self.movimento
        elif self.center_y > self.jogador.center_y:
            self.center_y -= self.movimento


# ============================================================
# TELA INICIAL / MENU
# ============================================================

class TelaInicial(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color((100, 10, 70))

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "COLETOR DE BANANAS",
            LARGURA / 2,
            430,
            arcade.color.WHITE,
            34,
            anchor_x="center"
        )

        arcade.draw_text(
            "[J] Jogar",
            LARGURA / 2,
            320,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "[I] Instruções",
            LARGURA / 2,
            280,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "[S] Sobre o Jogo",
            LARGURA / 2,
            240,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "[ESC] Sair",
            LARGURA / 2,
            200,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.J:
            self.window.show_view(TelaJogo())

        elif key == arcade.key.I:
            self.window.show_view(TelaInstrucoes())

        elif key == arcade.key.S:
            self.window.show_view(TelaSobre())

        elif key == arcade.key.ESCAPE:
            arcade.close_window()


# ============================================================
# TELA DE INSTRUÇÕES
# ============================================================

class TelaInstrucoes(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color((100, 10, 70))

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "INSTRUÇÕES",
            LARGURA / 2,
            500,
            arcade.color.WHITE,
            32,
            anchor_x="center"
        )

        arcade.draw_text(
            "Objetivo: colete todas as bananas para finalizar o jogo.",
            LARGURA / 2,
            440,
            arcade.color.WHITE,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "Use W, A, S, D ou as SETAS para movimentar o macaco.",
            LARGURA / 2,
            400,
            arcade.color.WHITE,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "Banana comum: +1 ponto.",
            LARGURA / 2,
            360,
            arcade.color.WHITE,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "Banana especial: +5 pontos e se movimenta pela tela.",
            LARGURA / 2,
            325,
            arcade.color.WHITE,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "Inimigos: -1 ponto por colisão e continuam no jogo.",
            LARGURA / 2,
            290,
            arcade.color.WHITE,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "Inimigo especial: persegue o jogador e se teletransporta após a colisão.",
            LARGURA / 2,
            255,
            arcade.color.WHITE,
            15,
            anchor_x="center"
        )

        arcade.draw_text(
            "ESC ou M: voltar ao menu principal.",
            LARGURA / 2,
            150,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE or key == arcade.key.M:
            self.window.show_view(TelaInicial())


# ============================================================
# TELA SOBRE O JOGO
# ============================================================

class TelaSobre(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color((100, 10, 70))

        # Sprite do desenvolvedor.
        # Se você tiver uma foto/avatar, pode substituir "inimigo.png"
        # pelo nome do arquivo da sua foto.
        self.sprite_desenvolvedor = arcade.SpriteList()

        self.avatar = arcade.Sprite("inimigo.png", scale=0.18)
        self.avatar.center_x = LARGURA / 2
        self.avatar.center_y = 350
        self.sprite_desenvolvedor.append(self.avatar)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "SOBRE O JOGO",
            LARGURA / 2,
            500,
            arcade.color.WHITE,
            32,
            anchor_x="center"
        )

        self.sprite_desenvolvedor.draw()

        # Substitua pelo(s) nome(s) real(is) do grupo.
        arcade.draw_text(
            "Integrantes: [Enzo]",
            LARGURA / 2,
            230,
            arcade.color.WHITE,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "Jogo desenvolvido em Python com a biblioteca Arcade.",
            LARGURA / 2,
            190,
            arcade.color.WHITE,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "Atividade de Programação Orientada a Objetos (POO).",
            LARGURA / 2,
            155,
            arcade.color.WHITE,
            17,
            anchor_x="center"
        )

        arcade.draw_text(
            "ESC ou M: voltar ao menu.",
            LARGURA / 2,
            80,
            arcade.color.WHITE,
            17,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE or key == arcade.key.M:
            self.window.show_view(TelaInicial())


# ============================================================
# TELA DO JOGO
# ============================================================

class TelaJogo(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color((100, 10, 70))

        
        
        self.fundo = arcade.load_texture("floresta.png")

        self.movimento = 3
        self.pontuacao = 0
        self.tempo = 0.0
        self.dano = False
        self.alerta_timer = 0

        # Quantidades exigidas.
        self.qtd_moedas = 25
        self.qtd_moedas_especiais = 5
        self.qtd_inimigos = 3

        # Pontuação máxima possível.
        self.pontuacao_maxima = (
            self.qtd_moedas * Moeda.valor_moeda
            + self.qtd_moedas_especiais * MoedaEspecial.valor_moeda
        )

        # SpriteLists.
        self.sprite_blocos = arcade.SpriteList()
        self.sprite_jogador = arcade.SpriteList()
        self.sprite_moedas = arcade.SpriteList()
        self.sprite_moedas_especiais = arcade.SpriteList()
        self.sprite_inimigos = arcade.SpriteList()
        self.sprite_inimigo_especial = arcade.SpriteList()

        # Jogador.
        self.jogador = Player()
        self.jogador.center_x = LARGURA / 2
        self.jogador.center_y = ALTURA / 2
        self.sprite_jogador.append(self.jogador)

        self.engine_fisica = arcade.PhysicsEnginePlatformer(
            player_sprite=self.jogador,
            walls=self.sprite_blocos,
            gravity_constant=0.5)

        # 25 moedas estáticas.
        for i in range(self.qtd_moedas):
            moeda = Moeda()
            moeda.center_x = random.randint(30, LARGURA - 30)
            moeda.center_y = random.randint(30, ALTURA - 30)
            self.sprite_moedas.append(moeda)

        # 5 moedas especiais dinâmicas.
        for i in range(self.qtd_moedas_especiais):
            moeda_especial = MoedaEspecial()
            moeda_especial.center_x = random.randint(50, LARGURA - 50)
            moeda_especial.center_y = random.randint(50, ALTURA - 50)

            moeda_especial.change_x = random.choice([-self.movimento, self.movimento])
            moeda_especial.change_y = random.choice([-self.movimento, self.movimento])

            self.sprite_moedas_especiais.append(moeda_especial)

        # 3 inimigos comuns persistentes.
        for i in range(self.qtd_inimigos):
            inimigo = Inimigo()
            self.respawn_longe_do_jogador(inimigo, 180)

            velocidade = random.randint(1, 3)
            inimigo.change_x = random.choice([-velocidade, velocidade])
            inimigo.change_y = random.choice([-velocidade, velocidade])

            self.sprite_inimigos.append(inimigo)

        # 1 inimigo especial perseguidor.
        self.inimigo_especial = InimigoEspecial(self.jogador)
        self.respawn_longe_do_jogador(self.inimigo_especial, 300)
        self.sprite_inimigo_especial.append(self.inimigo_especial)

    # Sorteia uma posição evitando que o inimigo nasça perto do jogador.
    def respawn_longe_do_jogador(self, inimigo, distancia_minima):
        while True:
            inimigo.center_x = random.randint(40, LARGURA - 40)
            inimigo.center_y = random.randint(40, ALTURA - 40)

            distancia = arcade.get_distance_between_sprites(
                inimigo,
                self.jogador
            )

            if distancia >= distancia_minima:
                break

    def on_draw(self):
        self.clear()
        #floresta
        arcade.draw_texture_rect(
    texture=self.fundo,
    rect=arcade.XYWH(
        LARGURA / 2,
        ALTURA / 2,
        LARGURA,
        ALTURA
    )
)
        # Sprites.
        self.sprite_blocos.draw()
        self.sprite_jogador.draw()
        self.sprite_moedas.draw()
        self.sprite_moedas_especiais.draw()
        self.sprite_inimigos.draw()
        self.sprite_inimigo_especial.draw()

        # HUD.
        arcade.draw_text(
            f"Pontos: {self.pontuacao}",
            10,
            570,
            arcade.color.WHITE,
            16
        )

        arcade.draw_text(
            f"Tempo: {self.tempo:.1f}s",
            10,
            545,
            arcade.color.WHITE,
            16
        )

        arcade.draw_text(
            f"Máximo: {self.pontuacao_maxima}",
            10,
            520,
            arcade.color.WHITE,
            16
        )

        # Alerta visual imediato de dano.
        if self.dano:
            arcade.draw_text(
                "DANO RECEBIDO! -1 PONTO",
                LARGURA / 2,
                ALTURA / 2,
                arcade.color.RED,
                28,
                anchor_x="center"
            )

    def on_update(self, delta_time):
        # Cronômetro em tempo real.
        self.tempo += delta_time

        # Atualização dos objetos.
        self.sprite_jogador.update(delta_time)
        self.sprite_moedas.update(delta_time)
        self.sprite_moedas_especiais.update(delta_time)
        self.sprite_inimigos.update(delta_time)
        self.sprite_inimigo_especial.update(delta_time)

        # --------------------------------------------------------
        # COLISÕES COM MOEDAS COMUNS
        # --------------------------------------------------------

        moedas_colididas = arcade.check_for_collision_with_list(
            self.jogador,
            self.sprite_moedas
        )

        for moeda in moedas_colididas:
            self.pontuacao += moeda.valor_moeda
            moeda.remove_from_sprite_lists()

        # --------------------------------------------------------
        # COLISÕES COM MOEDAS ESPECIAIS
        # --------------------------------------------------------

        moedas_especiais_colididas = arcade.check_for_collision_with_list(
            self.jogador,
            self.sprite_moedas_especiais
        )

        for moeda in moedas_especiais_colididas:
            self.pontuacao += moeda.valor_moeda
            moeda.remove_from_sprite_lists()

        # --------------------------------------------------------
        # COLISÕES COM INIMIGOS COMUNS
        # --------------------------------------------------------

        inimigos_colididos = arcade.check_for_collision_with_list(
            self.jogador,
            self.sprite_inimigos
        )

        for inimigo in inimigos_colididos:
            self.pontuacao -= 1
            self.alerta_dano()

            # IMPORTANTE:
            # O inimigo NÃO é removido.
            # Ele continua persistente no jogo.

            # Afasta o inimigo para evitar múltiplas colisões
            # no mesmo ponto, sem removê-lo da SpriteList.
            self.respawn_longe_do_jogador(inimigo, 150)

        # --------------------------------------------------------
        # COLISÃO COM INIMIGO ESPECIAL
        # --------------------------------------------------------

        if arcade.check_for_collision(
            self.jogador,
            self.inimigo_especial
        ):
            self.pontuacao -= 1
            self.alerta_dano()

            # Teletransporte para uma nova posição aleatória.
            self.respawn_longe_do_jogador(
                self.inimigo_especial,
                300
            )

        # --------------------------------------------------------
        # ALERTA DE DANO
        # --------------------------------------------------------

        if self.dano:
            self.alerta_timer -= delta_time

            if self.alerta_timer <= 0:
                self.dano = False

        # --------------------------------------------------------
        # FINALIZAÇÃO
        # --------------------------------------------------------

        total_moedas_restantes = (
            len(self.sprite_moedas)
            + len(self.sprite_moedas_especiais)
        )

        if total_moedas_restantes == 0:
            self.window.show_view(
                TelaFinal(
                    self.pontuacao,
                    self.tempo,
                    self.pontuacao_maxima
                )
            )

    def alerta_dano(self):
        self.dano = True
        self.alerta_timer = 0.5

    def on_key_press(self, key, modifiers):
        # ESC interrompe imediatamente a partida e volta ao menu.
        if key == arcade.key.ESCAPE:
            self.window.show_view(TelaInicial())
            return

        # WASD.
        if key == arcade.key.A:
            self.jogador.change_x = -self.movimento
        elif key == arcade.key.D:
            self.jogador.change_x = self.movimento
        elif key == arcade.key.W:
            self.jogador.change_y = self.movimento
        elif key == arcade.key.S:
            self.jogador.change_y = -self.movimento

        # Setas.
        elif key == arcade.key.LEFT:
            self.jogador.change_x = -self.movimento
        elif key == arcade.key.RIGHT:
            self.jogador.change_x = self.movimento
        elif key == arcade.key.UP:
            self.jogador.change_y = self.movimento
        elif key == arcade.key.DOWN:
            self.jogador.change_y = -self.movimento

    def on_key_release(self, key, modifiers):
        if key in (
            arcade.key.A,
            arcade.key.D,
            arcade.key.LEFT,
            arcade.key.RIGHT
        ):
            self.jogador.change_x = 0

        elif key in (
            arcade.key.W,
            arcade.key.S,
            arcade.key.UP,
            arcade.key.DOWN
        ):
            self.jogador.change_y = 0


# ============================================================
# GAME OVER / TELA FINAL
# ============================================================

class TelaFinal(arcade.View):
    def __init__(self, pontos, tempo, pontuacao_maxima):
        super().__init__()

        self.pontos = pontos
        self.tempo = tempo
        self.pontuacao_maxima = pontuacao_maxima

        arcade.set_background_color((100, 10, 70))

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "JOGO FINALIZADO!",
            LARGURA / 2,
            430,
            arcade.color.WHITE,
            34,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Pontuação: {self.pontos}",
            LARGURA / 2,
            350,
            arcade.color.WHITE,
            22,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Tempo total: {self.tempo:.1f}s",
            LARGURA / 2,
            315,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

        # Ramificação exigida pelo enunciado.
        if self.pontos >= self.pontuacao_maxima:
            arcade.draw_text(
                "PARABÉNS! PONTUAÇÃO MÁXIMA!",
                LARGURA / 2,
                255,
                arcade.color.YELLOW,
                24,
                anchor_x="center"
            )

            arcade.draw_text(
                "Você escapou de todos os inimigos perfeitamente!",
                LARGURA / 2,
                220,
                arcade.color.WHITE,
                17,
                anchor_x="center"
            )
        else:
            arcade.draw_text(
                "PARABÉNS! O JOGO FOI CONCLUÍDO!",
                LARGURA / 2,
                255,
                arcade.color.WHITE,
                22,
                anchor_x="center"
            )

        arcade.draw_text(
            "[M] Voltar ao Menu Principal",
            LARGURA / 2,
            150,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

        arcade.draw_text(
            "[ESC] Sair do Jogo",
            LARGURA / 2,
            110,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.M:
            self.window.show_view(TelaInicial())

        elif key == arcade.key.ESCAPE:
            arcade.close_window()


# ============================================================
# JANELA PRINCIPAL
# ============================================================

def main():
    # arcade.Window é apenas a janela base.
    janela = arcade.Window(LARGURA, ALTURA, TITULO)

    # A primeira tela é uma arcade.View.
    janela.show_view(TelaInicial())

    arcade.run()


if __name__ == "__main__":
    main()
