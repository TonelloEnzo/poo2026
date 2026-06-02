import arcade

#personagem
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("dir macaco.png", scale=0.20)
        self.textura_direita = arcade.load_texture("dir macaco.png")
        self.textura_esquerda = arcade.load_texture("esq macaco.png")

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.change_x > 0:
            self.texture = self.textura_direita
        elif self.change_x < 0:
            self.texture = self.textura_esquerda

       

class Moeda(arcade.Sprite):
    def __init__(self):
        super().__init__("moeda.png", scale=0.10)

    #atualizar personagem
    def update(self, delta_time):
       #Adicionar movimentação no eixo x e y
       self.center_x += self.change_x
       self.center_y += self.change_y
       

class JanelaJogo(arcade.Window):
    def __init__(self):
         super().__init__(800, 600, "Meu Jogo")
         #cor RGB (vermelho, verde, azul)
         arcade.set_background_color((100, 10, 70))
         #definir velocidade   
         self.movimento = 3
        #criar personagem
         self.jogador = Player()
         self.moeda = Moeda()
         #posicionar ele na tela
         self.jogador.center_x = 400
         self.jogador.center_y = 300
         self.moeda.center_x = 500
         self.moeda.center_y = 300
         self.moeda.change_x = self.movimento
         self.moeda.change_y = self.movimento

         self.sprite_jogador = arcade.SpriteList()
         self.sprite_jogador.append(self.jogador)

         self.sprite_moeda = arcade.SpriteList()
         self.sprite_moeda.append(self.moeda)

    def on_update(self, delta_time):
        self.sprite_jogador.update(delta_time)
        self.sprite_moeda.update(delta_time)
         
    #metodo para desenhar na tela
    def on_draw(self):
        self.clear()
        #desenhar meu personagem
        self.sprite_jogador.draw()
        self.sprite_moeda.draw()
 
def main():
    jogo = JanelaJogo()
    arcade.run()


if __name__== "__main__":
    main()
