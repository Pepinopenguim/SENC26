import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import shutil

class OrganizadorArquivosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Organizador de Arquivos")
        self.root.geometry("650x500")
        self.root.minsize(600, 400)

        # Variáveis de controle
        self.diretorio_origem = tk.StringVar()
        self.diretorio_destino = tk.StringVar()
        self.extensao_filtro = tk.StringVar(value=".dwg")
        self.arquivos_encontrados = []

        self._criar_componentes()

    def _criar_componentes(self):
        """Cria todos os widgets da janela usando grid e pack."""
        
        # Painel de configurações (topo)
        frame_config = ttk.LabelFrame(self.root, text=" Configurações ", padding=10)
        frame_config.pack(fill="x", padx=10, pady=10)

        # Linha 0: Origem
        ttk.Label(frame_config, text="Origem:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(frame_config, textvariable=self.diretorio_origem, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_config, text="Procurar...", command=self._selecionar_origem).grid(row=0, column=2, padx=5, pady=5)

        # Linha 1: Destino
        ttk.Label(frame_config, text="Destino:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(frame_config, textvariable=self.diretorio_destino, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame_config, text="Destino...", command=self._selecionar_destino).grid(row=1, column=2, padx=5, pady=5)

        # Linha 2: Extensão
        ttk.Label(frame_config, text="Extensão:").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Entry(frame_config, textvariable=self.extensao_filtro, width=15).grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Botão listar
        ttk.Button(frame_config, text="Listar Arquivos", command=self._listar_arquivos).grid(row=3, column=2, padx=5, pady=5)

        # Painel central: exibição dos arquivos (labels)
        frame_lista = ttk.LabelFrame(self.root, text=" Arquivos Encontrados ", padding=10)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=5)

        self.frame_arquivos = ttk.Frame(frame_lista)
        self.frame_arquivos.pack(fill="both", expand=True)

        # Painel inferior: botão mover
        frame_acoes = ttk.Frame(self.root, padding=10)
        frame_acoes.pack(fill="x", padx=10, pady=10)

        self.botao_mover = ttk.Button(
            frame_acoes,
            text="Mover Arquivos",
            command=self._executar_movimentacao,
            state="disabled"
        )
        self.botao_mover.pack(side="right", padx=5)

    # ---------- Métodos de seleção de pastas ----------
    def _selecionar_origem(self):
        caminho = filedialog.askdirectory(title="Selecione o diretório de origem")
        if caminho:
            self.diretorio_origem.set(caminho)

    def _selecionar_destino(self):
        caminho = filedialog.askdirectory(title="Selecione o diretório de destino")
        if caminho:
            self.diretorio_destino.set(caminho)

    # ---------- Lógica principal ----------
    def _listar_arquivos(self):
        # Limpa exibição anterior
        for widget in self.frame_arquivos.winfo_children():
            widget.destroy()
        self.arquivos_encontrados.clear()

        caminho_origem = self.diretorio_origem.get()
        extensao = self.extensao_filtro.get()

        # Validações
        if not extensao.startswith("."):
            messagebox.showerror("Erro", "A extensão deve começar com '.'")
            self.botao_mover.config(state="disabled")
            return

        if not caminho_origem or not Path(caminho_origem).exists():
            messagebox.showerror("Erro", "Caminho de origem inválido")
            self.botao_mover.config(state="disabled")
            return

        # Percorre todas as subpastas com rglob
        origem_path = Path(caminho_origem)
        for arquivo in origem_path.rglob('*'):
            if arquivo.is_file() and arquivo.suffix.lower() == extensao.lower():
                self.arquivos_encontrados.append(arquivo)

        # Exibe no máximo 30 arquivos como labels
        max_labels = 30
        num_arquivos = len(self.arquivos_encontrados)
        for i, arq in enumerate(self.arquivos_encontrados[:max_labels]):
            lbl = ttk.Label(self.frame_arquivos, text=f"📄 {arq.name}", anchor="w")
            lbl.pack(fill="x", pady=1)

        if num_arquivos > max_labels:
            resto = num_arquivos - max_labels
            lbl_resto = ttk.Label(self.frame_arquivos, text=f"... e mais {resto} arquivo(s)", foreground="gray")
            lbl_resto.pack(fill="x", pady=2)

        # Habilita/desabilita botão mover
        if self.arquivos_encontrados:
            self.botao_mover.config(state="normal")
        else:
            self.botao_mover.config(state="disabled")
            lbl_vazio = ttk.Label(self.frame_arquivos, text="Nenhum arquivo com essa extensão foi encontrado.")
            lbl_vazio.pack()

    def _executar_movimentacao(self):
        caminho_destino = self.diretorio_destino.get()
        if not caminho_destino:
            messagebox.showerror("Erro", "Escolha um diretório de destino")
            return

        destino_path = Path(caminho_destino)
        destino_path.mkdir(parents=True, exist_ok=True)  # cria se não existir

        sucessos = 0
        for arquivo in self.arquivos_encontrados:
            try:
                shutil.move(str(arquivo), str(destino_path / arquivo.name))
                sucessos += 1
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao mover {arquivo.name}\n{e}")

        messagebox.showinfo("Concluído", f"{sucessos} arquivo(s) movido(s) com sucesso.")
        self._listar_arquivos()  # atualiza a lista após mover

# ---------- Ponto de entrada ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = OrganizadorArquivosApp(root)
    root.mainloop()