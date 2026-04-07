class Pedido:

    def __init__ (self, produto, quantidade, preco_unitario):
        self.produto = produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

    def descrever (self):
        valor = 0.0
        valor = self.quantidade * self.preco_unitario
        print(f"Pedido: {self.quantidade} x {self.produto} — Total: R${valor}")

produto = input("Nome do produto:")
quantidade = int(input("Qual a quantidade:"))
preco_unitario = float(input("Preço"))
p1 = Pedido(produto, quantidade, preco_unitario)


print(p1.descrever())