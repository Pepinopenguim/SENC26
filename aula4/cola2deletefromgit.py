
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import shutil
from send2trash import send2trash

class AutomatizadorArquivosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Organizador de Diretórios - Automação de Escritório")
        self.root.geometry("650x500")
        self.root.minsize(600, 400)
        
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

        # Seleção de Origem
        ttk.Label(frame_config, text="Diretório Origem:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(frame_config, textvariable=self.diretorio_origem, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_config, text="Procurar...", command=self._selecionar_origem).grid(row=0, column=2, padx=5, pady=5)

        # Seleção de Destino
        ttk.Label(frame_config, text="Diretório Destino:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(frame_config, textvariable=self.diretorio_destino, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame_config, text="Procurar...", command=self._selecionar_destino).grid(row=1, column=2, padx=5, pady=5)

        # Filtro de Extensão
        ttk.Label(frame_config, text="Extensão do Arquivo:").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Entry(frame_config, textvariable=self.extensao_filtro, width=15).grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Botão para listar
        ttk.Button(frame_config, text="Listar Arquivos", command=self._listar_arquivos).grid(row=2, column=1, sticky="e", padx=5, pady=5)

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

        self.btn_mover = ttk.Button(frame_acoes, text="Mover Arquivos", command=self._executar_movimentacao, state="disabled")
        self.btn_mover.pack(side="right", padx=5)

        self.btn_lixeira = ttk.Button(frame_acoes, text="Enviar para Lixeira", command=self._executar_exclusao, state="disabled")
        self.btn_lixeira.pack(side="right", padx=5)

    # Métodos de Seleção de Diretório
    def _selecionar_origem(self):
        caminho = filedialog.askdirectory(title="Selecione o Diretório de Origem")
        if caminho:
            self.diretorio_origem.set(caminho)

    def _selecionar_destino(self):
        caminho = filedialog.askdirectory(title="Selecione o Diretório de Destino")
        if caminho:
            self.diretorio_destino.set(caminho)

    # Métodos de Lógica Operacional
    def _listar_arquivos(self):
        """Mapeia o diretório e popula a Listbox com os caminhos encontrados."""
        self.listbox_arquivos.delete(0, tk.END)
        self.arquivos_encontrados.clear()

        caminho_origem = self.diretorio_origem.get()
        extensao = self.extensao_filtro.get().strip()

        if not caminho_origem or not Path(caminho_origem).exists():
            messagebox.showerror("Erro de Validação", "Diretório de origem inválido ou não informado.")
            return

        if not extensao.startswith("."):
            messagebox.showwarning("Aviso de Filtro", "A extensão informada deve começar com ponto (ex: .pdf).")
            return

        # Varredura do diretório utilizando pathlib
        origem_path = Path(caminho_origem)
        for arquivo in origem_path.iterdir():
            if arquivo.is_file() and arquivo.suffix.lower() == extensao.lower():
                self.arquivos_encontrados.append(arquivo)
                self.listbox_arquivos.insert(tk.END, str(arquivo.resolve()))

        if self.arquivos_encontrados:
            self.btn_mover.config(state="normal")
            self.btn_lixeira.config(state="normal")
        else:
            self.btn_mover.config(state="disabled")
            self.btn_lixeira.config(state="disabled")
            messagebox.showinfo("Busca Concluída", "Nenhum arquivo correspondente ao filtro foi encontrado.")

    def _executar_movimentacao(self):
        """Transfere os arquivos listados para o ponto de destino."""
        caminho_destino = self.diretorio_destino.get()

        if not caminho_destino:
            messagebox.showerror("Erro de Destino", "Informe um diretório de destino válido.")
            return

        destino_path = Path(caminho_destino)
        destino_path.mkdir(parents=True, exist_ok=True)

        sucessos = 0
        for arquivo in self.arquivos_encontrados:
            try:
                shutil.move(str(arquivo), str(destino_path / arquivo.name))
                sucessos += 1
            except Exception as e:
                messagebox.showerror("Erro na Operação", f"Falha ao mover o arquivo {arquivo.name}.\nMotivo: {e}")

        messagebox.showinfo("Processo Concluído", f"{sucessos} de {len(self.arquivos_encontrados)} arquivos movidos.")
        self._listar_arquivos()

    def _executar_exclusao(self):
        """Envia os arquivos detectados para a lixeira do Sistema Operacional de forma segura."""
        confirmacao = messagebox.askyesno(
            "Confirmação de Exclusão", 
            f"Deseja realmente enviar os {len(self.arquivos_encontrados)} arquivos listados para a lixeira?"
        )
        
        if not confirmacao:
            return

        sucessos = 0
        for arquivo in self.arquivos_encontrados:
            try:
                send2trash(str(arquivo.resolve()))
                sucessos += 1
            except Exception as e:
                messagebox.showerror("Erro de Sistema", f"Não foi possível descartar {arquivo.name}.\nMotivo: {e}")

        messagebox.showinfo("Processo Concluído", f"{sucessos} arquivos enviados para a lixeira.")
        self._listar_arquivos()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomatizadorArquivosApp(root)
    root.mainloop()