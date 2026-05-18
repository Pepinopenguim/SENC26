import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import shutil
from send2trash import send2trash

class AutomatizadorArquivosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("[NOME DO APP]")
        self.root.geometry("650x500") # podemos definir o tamanho da janela
        self.root.minsize(600, 400) # aqui, impedimos que a janela seja minimizada demais
        
        # Variáveis de controle de estado do aplicativo 
        self.diretorio_origem = tk.StringVar()
        self.diretorio_destino = tk.StringVar()
        self.extensao_filtro = tk.StringVar(value=".pdf")
        self.arquivos_encontrados = []

        # Inicialização dos componentes de interface
        self._criar_componentes()

    def _criar_componentes(self):
        """Configura a disposição dos elementos na janela utilizando o gerenciador de grid."""
        
        # Painel Superior: Configurações de Caminhos e Filtros
        frame_config = ttk.LabelFrame(self.root, text=" Configurações de Parâmetros ", padding=10)
        frame_config.pack(fill="x", padx=10, pady=10)

        # Seleção de Origem (Mantido como exemplo para os alunos)
        ttk.Label(frame_config, text="Diretório Origem:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(frame_config, textvariable=self.diretorio_origem, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_config, text="Procurar...", command=self._selecionar_origem).grid(row=0, column=2, padx=5, pady=5)

        # TODO: Seleção de Destino


        # Filtro de Extensão (Mantido na linha 2)
        ttk.Label(frame_config, text="Extensão do Arquivo:").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Entry(frame_config, textvariable=self.extensao_filtro, width=15).grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # TODO: Botão para Listar Arquivos
        # TODO: Posicionar um botão na linha 2 para disparar o método 'self._listar_arquivos'

        # Painel Central: Exibição da Scrollable Listbox
        frame_lista = ttk.LabelFrame(self.root, text=" Arquivos Identificados ", padding=10)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=5)

        self.scrollbar_y = ttk.Scrollbar(frame_lista, orient="vertical")
        self.scrollbar_x = ttk.Scrollbar(frame_lista, orient="horizontal")
        
        self.listbox_arquivos = tk.Listbox(
            frame_lista, 
            yscrollcommand=self.scrollbar_y.set, 
            xscrollcommand=self.scrollbar_x.set,
            selectmode=tk.MULTIPLE
        )
        
        self.scrollbar_y.config(command=self.listbox_arquivos.yview)
        self.scrollbar_x.config(command=self.listbox_arquivos.xview)

        # Posicionamento da listbox e suas barras de rolagem
        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.listbox_arquivos.pack(side="left", fill="both", expand=True)

        # Painel Inferior: Botões de Ação Executiva
        frame_acoes = ttk.Frame(self.root, padding=10)
        frame_acoes.pack(fill="x", padx=10, pady=10)

        # TODO: Botões de Ação Mover e Excluir
        # TODO: Instanciar 'self.btn_mover' e 'self.btn_lixeira' dentro de frame_acoes
        # Configurar estado inicial como "disabled" (state="disabled")
        # Associar respectivamente aos métodos '_executar_movimentacao' e '_executar_exclusao'

    # Métodos de Seleção de Diretório
    def _selecionar_origem(self):
        """Abre caixa de diálogo para seleção do diretório de origem."""
        # TODO: implementar lógica de abrir a pasta e obter o caminho necessário
        # Use a função filedialog.askdirectory() para abrir a pasta de arquivos
        # se o caminho for válido, (não nulo por exemplo)
        # defina a variável self.diretorio_origem como esse valor
        pass

    def _selecionar_destino(self):
        """Abre caixa de diálogo para seleção do diretório de destino."""
        # TODO: Implementar lógica análoga ao método _selecionar_origem, atualizando 'self.diretorio_destino'
        pass

    # Métodos de Lógica Operacional (Backend da GUI)
    def _listar_arquivos(self):
        """Mapeia o diretório de origem e popula a Listbox com os caminhos encontrados baseado no filtro."""
        # Passo 1: Limpar listbox (.delete) e a lista interna self.arquivos_encontrados (.clear)
        
        # Passo 2: Validar se o caminho de origem existe e se a extensão inicia com ponto (.)
        
        # Passo 3: Utilizar o Path(caminho_origem).iterdir() para iterar sobre os arquivos
        
        # Passo 4: Filtrar por sufixo, adicionar à lista interna e inserir na interface gráfica (.insert)
        
        # Passo 5: Habilitar ou desabilitar os botões de ação baseado na presença de arquivos encontrados
        pass

    def _executar_movimentacao(self):
        """Transfere os arquivos listados para o ponto de destino usando a biblioteca shutil."""
        # Passo 1: Validar se o diretório de destino foi informado
        
        # Passo 2: Garantir a criação do diretório de destino caso não exista (.mkdir)
        
        # Passo 3: Iterar pela lista self.arquivos_encontrados e aplicar shutil.move() protegido por try-except
        
        # Passo 4: Exibir feedback de sucesso (messagebox) e atualizar a listbox chamando self._listar_arquivos()
        pass

    def _executar_exclusao(self):
        """Envia os arquivos detectados para a lixeira do Sistema Operacional usando send2trash."""
        # Passo 1: Exibir caixa de diálogo de confirmação (messagebox.askyesno) para evitar acidentes
        
        # Passo 2: Se confirmado, iterar pela lista de arquivos e aplicar a função send2trash() em cada item
        
        # Passo 3: Tratar possíveis exceções de permissão ou arquivo bloqueado com bloco try-except
        
        # Passo 4: Atualizar a interface gráfica e emitir relatório de encerramento
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomatizadorArquivosApp(root)
    root.mainloop()