"""
Esse gabarito possui conteúdo extra sobre cálculo de centróides
"""

import matplotlib.pyplot as plt


class Ponto:
    def __init__(self, x, y):
        self.x = x # isso é uma propriedade
        self.y = y

    def __repr__(self): # isso é método especial
        # TODO 2: Retorna uma string usada no Print, por exemplo, ex: "Ponto(x, y)"
        return f"Ponto({self.x},{self.y})"


class Secao:
    """Representa uma secao estrutural definida por um poligono fechado."""
    
    def __init__(self, nome: str):
        self.nome = nome
        self.vertices = []

    def adicionar_vertice(self, x: float, y: float):
        """Cria um objeto Ponto e o adiciona a lista de vertices."""

        ponto_atual = Ponto(x, y)
        self.vertices.append(ponto_atual)
        

    def remover_ultimo_vertice(self):
        """Remove o ultimo vertice adicionado."""
        
        # Checar se a lista de vértices não está vazia
        if self.vertices: # se a lista não está vazia
            self.vertices.pop()
        else:
            print("Não há pontos para serem removidos!")

    def _obter_poligono_fechado(self):
        """Metodo auxiliar para ligar o ultimo ponto de volta ao primeiro."""
        # Retornar uma nova lista contendo todos os vertices + o primeiro vertice no final.

        # checar se temos pelo menos 3 pontos
        if len(self.vertices) < 3:
            raise ValueError("Um polígono deve ter pelo menos 3 vértices!")
        
        # pegar o primeiro ponto da lista
        if self.vertices[0].x != self.vertices[-1].x or self.vertices[0].y != self.vertices[-1].y:
            ponto_inicial = self.vertices[0]

            self.vertices.append(ponto_inicial)

    def calcular_area(self) -> float:
        """Calcula a area pelo teorema de Shoelace."""
        
        self._obter_poligono_fechado() # isso garante que o meu poligono estará fechado!

        area = 0
        for i in range(1, len(self.vertices)):
            ponto_antes = self.vertices[i-1]
            ponto_depois = self.vertices[i]

            x_antes, y_antes = ponto_antes.x, ponto_antes.y
            x_depois, y_depois = ponto_depois.x, ponto_depois.y
            
            area += x_antes * y_depois - x_depois * y_antes

        return abs(area / 2)
    

    def calcular_centroide(self):
        xc = 0
        yc = 0
        area = self.calcular_area()

        for i in range(1, len(self.vertices)):
            ponto_antes = self.vertices[i-1]
            ponto_depois = self.vertices[i]

            x_antes, y_antes = ponto_antes.x, ponto_antes.y
            x_depois, y_depois = ponto_depois.x, ponto_depois.y

            mult = (x_antes * y_depois - x_depois * y_antes)
            
            xc += mult * (x_antes + x_depois)
            yc += mult * (y_antes + y_depois)

        xc /= 6 * area
        yc /= 6 * area

        return {
            "xc": xc,
            "yc": yc
        }
        

    def calcular_inercia(self) -> dict:
        """Calcula os momentos de inercia (Ix, Iy) em relacao a origem."""
        # Retornar um dicionario no formato {"Ix": valor, "Iy": valor}

        self._obter_poligono_fechado()
        
        momento_x = 0
        momento_y = 0

        for i in range(1, len(self.vertices)):
            ponto_antes = self.vertices[i-1]
            ponto_depois = self.vertices[i]

            x_antes, y_antes = ponto_antes.x, ponto_antes.y
            x_depois, y_depois = ponto_depois.x, ponto_depois.y

            mult = (x_antes * y_depois - x_depois * y_antes)
            
            momento_x += mult * (y_antes**2 + y_antes * y_depois + y_depois ** 2)
            momento_y += mult * (x_antes**2 + x_antes * x_depois + x_depois ** 2)

        momento_x = abs(momento_x / 12)
        momento_y = abs(momento_y / 12)

        area = self.calcular_area()
        centroides = self.calcular_centroide()

        momento_x_centroide = momento_x - area * centroides["yc"] ** 2
        momento_y_centroide = momento_y - area * centroides["xc"] ** 2

        
        
        return {
            "Ix": momento_x,
            "Iy": momento_y,
            "Ixc": momento_x_centroide,
            "Iyc": momento_y_centroide
        }

    def atualizar_grafico(self, finalizar: bool = False):
        """Limpa e redesenha o grafico. Se finalizar=True, fecha a forma e calcula."""
        plt.clf() 
        
        if not hasattr(self, 'vertices') or not self.vertices:
            plt.draw()
            return

        x_coords = [p.x for p in self.vertices]
        y_coords = [p.y for p in self.vertices]

        if finalizar and len(self.vertices) >= 3:
            x_coords.append(self.vertices[0].x)
            y_coords.append(self.vertices[0].y)
            plt.fill(x_coords, y_coords, color='steelblue', alpha=0.4)
            
            area = self.calcular_area() # IMPORTANTES
            centroide = self.calcular_centroide()
            inercia = self.calcular_inercia() # IMPORTANTES
            texto_resultados = (
                f"Area = {area:.2f} cm2\n"
                f"Centroide = ({centroide['xc']:.2f}, {centroide['yc']:.2f})\n"
                f"Ix = {inercia['Ix']:.2f} cm4\n"
                f"Iy = {inercia['Iy']:.2f} cm4\n"
                f"Ixc = {inercia['Ixc']:.2f} cm4\n"
                f"Iyc = {inercia['Iyc']:.2f} cm4"
            )
            plt.text(0.05, 0.95, texto_resultados, transform=plt.gca().transAxes,
                     fontsize=11, verticalalignment='top', 
                     bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

        plt.plot(x_coords, y_coords, color='navy', marker='o', linewidth=2) 
        
        nome_secao = getattr(self, 'nome', 'Desconhecido')
        plt.title(f"Secao Transversal: {nome_secao}", fontweight='bold')
        plt.xlabel("X (cm)")
        plt.ylabel("Y (cm)")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.axis('equal') 
        
        plt.draw()
        plt.pause(0.001)

# ====================================================================
# CODIGO PRONTO: Loop de Execucao no Terminal
# ====================================================================
if __name__ == "__main__":
    print("--- Calculadora de Secao Estrutural ---")
    print("Comandos:")
    print("  - Digite coordenadas como 'X,Y' (ex: '10,20')")
    print("  - Digite 'remover' para deletar o ultimo ponto")
    print("  - Digite 'calcular' para fechar a forma e ver resultados")
    print("  - Digite 'sair' para encerrar")
    print("-" * 39)

    # Ativa o modo interativo do matplotlib
    plt.ion() 
    plt.figure(figsize=(6, 6))
    
    secao = Secao("Formato Customizado")
    
    while True:
        cmd = input("\nComando ou X,Y: ").strip().lower()
        
        if cmd == 'sair':
            print("Encerrando...")
            break
            
        elif cmd == 'remover':
            secao.remover_ultimo_vertice()
            secao.atualizar_grafico()
            
        elif cmd == 'calcular':
            try:
                secao.atualizar_grafico(finalizar=True)
                print("Calculo concluido. Feche a janela do grafico para encerrar o script.")
                plt.ioff() 
                plt.show() 
                break
            except Exception as e:
                print(f"Erro: {e}")
                
        else:
            try:
                x_str, y_str = cmd.split(',')
                secao.adicionar_vertice(float(x_str), float(y_str))
                secao.atualizar_grafico()
            except ValueError:
                print("Formato invalido. Use 'X,Y' (ex: '10,20') ou um comando valido.")