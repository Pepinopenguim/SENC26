import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import shutil
from send2trash import send2trash

class AutomatizadorArquivosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Organizador de Arquivos")
        self.root.geometry("650x500") # podemos definir o tamanho da janela
        self.root.minsize(600, 400) # aqui, impedimos que a janela seja minimizada demais
        
        # Variáveis de controle de estado do aplicativo 
        self.diretorio_origem = tk.StringVar()
        self.diretorio_destino = tk.StringVar()
        self.extensao_filtro = tk.StringVar(value=".dwg")
        self.arquivos_encontrados = []

        # Inicialização dos componentes de interface
        self._criar_componentes()

    def _criar_componentes(self):
        """Configura a disposição dos elementos na janela utilizando o gerenciador de grid."""
        
        # Painel Superior: Configurações de Caminhos e Filtros
        frame_config = ttk.LabelFrame(self.root, text=" Configurações de Parâmetros ", padding=10)
        frame_config.pack(fill="x", padx=10, pady=10)

        # Seleção de Origem
        ttk.Label(frame_config, text="Diretório Origem:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(frame_config, textvariable=self.diretorio_origem, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_config, text="Procurar...", command=self._selecionar_origem).grid(row=0, column=2, padx=5, pady=5)

        # Seleção de Destino
        ttk.Label(frame_config, text="Diretório de Destino:").grid(row=1, column=0, sticky="w", pady=5)    
        ttk.Entry(frame_config, textvariable=self.diretorio_destino, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame_config, text="Destino...", command=self._selecionar_destino).grid(row=1, column=2, padx=5, pady=5)

        # Filtro de Extensão (Mantido na linha 2)
        ttk.Label(frame_config, text="Extensão do Arquivo:").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Entry(frame_config, textvariable=self.extensao_filtro, width=15).grid(row=2, column=1, sticky="w", padx=5, pady=5)
    

        ttk.Button(frame_config, text="Listar Arquivos", command=self._listar_arquivos).grid(row=3, column=2, padx=5, pady=5)

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

        self.botao_mover = ttk.Button(frame_acoes, text="Mover Arquivos", command=self._executar_movimentacao, state="disabled")
        self.botao_mover.pack(side="right", padx=5)

        self.botao_lixeira = ttk.Button(frame_acoes, text="Enviar Para Lixeira", command=self._executar_exclusao, state="disabled")
        self.botao_lixeira.pack(side="right", padx=5)


    # Métodos de Seleção de Diretório
    def _selecionar_origem(self):
        """Abre caixa de diálogo para seleção do diretório de origem."""
        # TODO: implementar lógica de abrir a pasta e obter o caminho necessário
        # Use a função filedialog.askdirectory() para abrir a pasta de arquivos
        # se o caminho for válido, (não nulo por exemplo)
        # defina a variável self.diretorio_origem como esse valor
        
        caminho = filedialog.askdirectory(title="Selecione o diretório de origem")
        if caminho:
            self.diretorio_origem.set(caminho)

    def _selecionar_destino(self):
        """Abre caixa de diálogo para seleção do diretório de destino."""
        # TODO: Implementar lógica análoga ao método _selecionar_origem, atualizando 'self.diretorio_destino'
        caminho = filedialog.askdirectory(title="Selecione o diretório de destino")
        if caminho:
            self.diretorio_destino.set(caminho)

    # Métodos de Lógica Operacional (Backend da GUI)
    def _listar_arquivos(self):
        """Mapeia o diretório de origem e popula a Listbox com os caminhos encontrados baseado no filtro."""
        
        # 1. limpar os arquivos anteriores
        self.listbox_arquivos.delete(0, tk.END)
        self.arquivos_encontrados.clear()
        
        # 2. Checar se a extensão é válida

        caminho_origem = self.diretorio_origem.get()
        extensao = self.extensao_filtro.get()

        if not extensao.startswith("."):
            messagebox.showerror("Erro de Validação", "A extensão deve iniciar com '.'")
            self.botao_lixeira.config(state="disabled")
            self.botao_mover.config(state="disabled")
            return

        if not caminho_origem or not Path(caminho_origem).exists():
            messagebox.showerror("Erro de caminho!", "Insira um caminho de origem válido")
            self.botao_lixeira.config(state="disabled")
            self.botao_mover.config(state="disabled")
            return

        # 3. usar a função path.iterdir para iterar sobre todos os arquivos
        # Path do pathlib

        origem_path = Path(caminho_origem)
        for arquivo in origem_path.iterdir():
            if arquivo.is_file() and arquivo.suffix.lower() == extensao.lower():
                self.arquivos_encontrados.append(arquivo)
                self.listbox_arquivos.insert(tk.END, str(arquivo.resolve()))

        if self.arquivos_encontrados:
            self.botao_lixeira.config(state="normal")
            self.botao_mover.config(state="normal")
        else:
            self.botao_lixeira.config(state="disabled")
            self.botao_mover.config(state="disabled")
            #messagebox.showinfo("Aviso", "Não foram encontrados arquivos")

    def _executar_movimentacao(self):
        """Transfere os arquivos listados para o ponto de destino usando a biblioteca shutil."""
        
        caminho_destino = self.diretorio_destino.get()

        if not caminho_destino:
            messagebox.showerror("Erro de Destino", "Insira um caminho de destino válido")
            return
        
        destino_path = Path(caminho_destino)
        destino_path.mkdir(parents=True, exist_ok=True)

        sucessos = 0
        for arquivo in self.arquivos_encontrados:
            try:
                shutil.move(str(arquivo), str(destino_path / arquivo.name))
                sucessos += 1
            except:
                messagebox.showerror("Erro na operação", f"Falha ao mover o arquivo {arquivo}")

        messagebox.showinfo("Processo concluído", f"{sucessos} arquivos movidos de forma bem sucedida")
        self._listar_arquivos() # reiniciar a lista de arquivos

    def _executar_exclusao(self):
        """Envia os arquivos detectados para a lixeira do Sistema Operacional usando send2trash."""
        
        confirmacao = messagebox.askyesno(
            "Confirmação de Exclusão", f"Deseja realmente enviar {len(self.arquivos_encontrados)} arquivos para a lixeira?"
        )

        if not confirmacao:
            return
        
        successos = 0
        for arquivo in self.arquivos_encontrados:
            try:
                send2trash(str(arquivo.resolve()))
                successos += 1
            except Exception as e:
                messagebox.showerror("Erro no Sistema", e)

        messagebox.showinfo("Processo Concluído", f"{successos} arquivos enviados para a lixeira.")
        self._listar_arquivos()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomatizadorArquivosApp(root)
    root.mainloop()