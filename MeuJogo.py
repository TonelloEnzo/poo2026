import arcade

Altura = 600
Largura = 800
Titulo = "Meu Jogo"
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

        #parar o personagem antes dele sair da tela
        if(self.right > Largura):
            self.change_x = 0
            self.right = Largura
        elif(self.left < 0):
            self.change_x = 0
            self.left = 0
        
        if(self.top > Altura):
            self.change_y = 0
            self.top = Altura
        elif(self.bottom < 0):
            self.change_y = 0
            self.bottom = 0
       

class Moeda(arcade.Sprite):
    def __init__(self):
        super().__init__("banana.png", scale=0.10)

    #atualizar personagem
    def update(self, delta_time):
       #Adicionar movimentação no eixo x e y
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.right > 800 or self.left <0:
            self.change_x *= -1
           

        elif self.top > 600 or self.bottom < 0:
            self.change_y *= -1
    
       

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

        self.moeda2 = Moeda()
        self.moeda2.left = 0
        self.moeda2.bottom = 300

        self.moeda3 = Moeda()
        self.moeda3.left = 700
        self.moeda3.bottom = 150

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

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT: 
            self.jogador.change_x += self.movimento
        if key == arcade.key.LEFT:
            self.jogador.change_x -= self.movimento
        if key == arcade.key.UP:
            self.jogador.change_y += self.movimento
        if key == arcade.key.DOWN:
            self.jogador.change_y -= self.movimento
        if key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT or key == arcade.key.LEFT: 
            self.jogador.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.jogador.change_y = 0     
 
def main():
    jogo = JanelaJogo()
    arcade.run()


if __name__== "__main__":
    main()
