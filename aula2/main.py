import matplotlib.pyplot as plt


class Ponto:
    def __init__(self, x:float, y:float):
        # TODO 1: Definir x e y como propriedades
        pass

    def __repr__(self): # isso é método especial
        # TODO 2: Retorna uma string usada no Print, por exemplo, ex: "Ponto(x, y)"
        pass


class Secao:
    """Representa uma secao estrutural definida por um poligono fechado."""
    
    def __init__(self, nome: str):
        # TODO 3: Definir o nome como propriedade da seção,
        # e criar uma lista vazia chamada self.vertices
        pass

    def adicionar_vertice(self, x: float, y: float):
        """Cria um objeto Ponto e o adiciona a lista de vertices."""
        # TODO 4: Instanciar um Ponto usando x e y, e fazer o append na lista
        pass
        

    def remover_ultimo_vertice(self):
        """Remove o ultimo vertice adicionado."""
        # TODO 5: Verificar se a lista de vertices nao esta vazia.
        # Se nao estiver, usar o metodo .pop() para remover e printar o ponto removido.
        # Caso contrario, avisar que nao ha pontos.
        pass

    def _obter_poligono_fechado(self):
        """Metodo auxiliar para ligar o ultimo ponto de volta ao primeiro."""
        # TODO 6: Verificar se a lista tem pelo menos 3 pontos (lancar ValueError se nao tiver).
        # Retornar uma nova lista contendo todos os vertices + o primeiro vertice no final.
        pass

    def calcular_area(self) -> float:
        """Calcula a area pelo teorema de Shoelace."""
        # TODO 7: Chamar self._obter_poligono_fechado() e implementar a formula da area
        return 0.0

    def calcular_inercia(self) -> dict:
        """Calcula os momentos de inercia (Ix, Iy) em relacao a origem."""
        # TODO 8: Chamar self._obter_poligono_fechado() e implementar a formula de inercia
        # Retornar um dicionario no formato {"Ix": valor, "Iy": valor}
        return {
            "Ix": 0.0,
            "Iy": 0.0
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
            
            area = self.calcular_area()
            inercia = self.calcular_inercia()
            texto_resultados = (
                f"Area = {area:.2f} cm2\n"
                f"Ix = {inercia['Ix']:.2f} cm4\n"
                f"Iy = {inercia['Iy']:.2f} cm4"
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