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

        # Variáveis que guardam os caminhos e o filtro
        self.diretorio_origem = tk.StringVar()
        self.diretorio_destino = tk.StringVar()
        self.extensao_filtro = tk.StringVar(value=".dwg")
        
        # Lista onde serão armazenados os arquivos encontrados (Path objects)
        self.arquivos_encontrados = []

        # Constrói a interface gráfica
        self._criar_componentes()

    def _criar_componentes(self):
        """Cria todos os widgets da janela usando grid e pack."""
        
        # ---- Painel de configurações (topo) ----
        frame_config = ttk.LabelFrame(self.root, text=" Configurações ", padding=10)
        frame_config.pack(fill="x", padx=10, pady=10)

        # Linha 0: Diretório Origem + botão Procurar
        ttk.Label(frame_config, text="Origem:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(frame_config, textvariable=self.diretorio_origem, width=50).grid(row=0, column=1, padx=5, pady=5)
        # TODO: Associe o botão abaixo ao método _selecionar_origem
        ttk.Button(frame_config, text="Procurar...", command=self._selecionar_origem).grid(row=0, column=2, padx=5, pady=5)

        # Linha 1: Diretório Destino + botão Procurar
        ttk.Label(frame_config, text="Destino:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(frame_config, textvariable=self.diretorio_destino, width=50).grid(row=1, column=1, padx=5, pady=5)
        # TODO: Associe o botão abaixo ao método _selecionar_destino
        ttk.Button(frame_config, text="Destino...", command=self._selecionar_destino).grid(row=1, column=2, padx=5, pady=5)

        # Linha 2: Extensão do filtro
        ttk.Label(frame_config, text="Extensão:").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Entry(frame_config, textvariable=self.extensao_filtro, width=15).grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Botão para listar arquivos (chama _listar_arquivos)
        ttk.Button(frame_config, text="Listar Arquivos", command=self._listar_arquivos).grid(row=3, column=2, padx=5, pady=5)

        # ---- Painel central: mostra os arquivos encontrados ----
        frame_lista = ttk.LabelFrame(self.root, text=" Arquivos Encontrados ", padding=10)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=5)

        # Frame que vai conter os labels (será limpo a cada nova listagem)
        self.frame_arquivos = ttk.Frame(frame_lista)
        self.frame_arquivos.pack(fill="both", expand=True)

        # ---- Painel inferior: botão de ação ----
        frame_acoes = ttk.Frame(self.root, padding=10)
        frame_acoes.pack(fill="x", padx=10, pady=10)

        # Botão Mover 
        self.botao_mover = ttk.Button(
            frame_acoes,
            text="Mover Arquivos",
            command=self._executar_movimentacao,
            state="disabled"
        )
        self.botao_mover.pack(side="right", padx=5)

    # ================== MÉTODOS A SEREM IMPLEMENTADOS PELOS ALUNOS ==================

    def _selecionar_origem(self):
        """
        Abre uma caixa de diálogo para escolher a pasta de origem.
        Dica: use filedialog.askdirectory()
        Se um caminho for escolhido, atualize self.diretorio_origem com .set(caminho)
        """
        # TODO: Implemente a seleção da pasta de origem
        pass

    def _selecionar_destino(self):
        """
        Abre uma caixa de diálogo para escolher a pasta de destino.
        Análogo ao _selecionar_origem, mas atualiza self.diretorio_destino.
        """
        # TODO: Implemente a seleção da pasta de destino
        pass

    def _listar_arquivos(self):
        """
        1. Limpa a exibição anterior (apaga todos os widgets dentro de self.frame_arquivos).
        2. Lê o caminho de origem e a extensão do filtro.
        3. Valida:
           - Extensão deve começar com '.' (senão, exibe erro e desabilita botão mover)
           - Caminho de origem deve existir (senão, erro e desabilita botão mover)
        4. Usa Path(self.diretorio_origem.get()).rglob('*') para percorrer TODAS as subpastas.
        5. Para cada arquivo, verifica se é um arquivo normal (.is_file()) e se a extensão
           (arquivo.suffix) é igual à extensão do filtro (case insensitive).
        6. Adiciona os arquivos que passam o filtro à lista self.arquivos_encontrados.
        7. Exibe os arquivos encontrados dentro de self.frame_arquivos:
           - Crie um label para CADA arquivo, mas mostre no máximo 30.
           - Se houver mais de 30, mostre uma mensagem "... e mais X arquivos".
           - Dica: use um loop for com enumerate e self.arquivos_encontrados[:30].
           - Cada label deve ter texto como f"📄 {arquivo.name}" e anchor="w".
        8. Se não houver nenhum arquivo, mostre um label com "Nenhum arquivo encontrado".
        9. Habilite ou desabilite o botão mover conforme existência de arquivos.
        """
        # Limpa o frame que contém os labels
        for widget in self.frame_arquivos.winfo_children():
            widget.destroy()
        self.arquivos_encontrados.clear()

        # TODO: Obter os valores dos campos
        caminho_origem = ...   # self.diretorio_origem.get()
        extensao = ...         # self.extensao_filtro.get()

        # Validação 1: extensão
        if not extensao.startswith("."):
            messagebox.showerror("Erro", "A extensão deve começar com '.'")
            self.botao_mover.config(state="disabled")
            return

        # Validação 2: caminho de origem
        if not caminho_origem or not Path(caminho_origem).exists():
            messagebox.showerror("Erro", "Caminho de origem inválido")
            self.botao_mover.config(state="disabled")
            return

        # TODO: Percorrer o diretório e subpastas com rglob
        origem_path = Path(caminho_origem)
        # Exemplo: for arquivo in origem_path.rglob('*'):
        # ...

        # TODO: Exibir os primeiros 30 arquivos como labels
        max_labels = 30
        num_arquivos = len(self.arquivos_encontrados)
        # Exemplo: for i, arq in enumerate(self.arquivos_encontrados[:max_labels]):
        #     lbl = ttk.Label(self.frame_arquivos, text=f"📄 {arq.name}", anchor="w")
        #     lbl.pack(fill="x", pady=1)

        if num_arquivos > max_labels:
            resto = num_arquivos - max_labels
            lbl_resto = ttk.Label(self.frame_arquivos, text=f"... e mais {resto} arquivo(s)", foreground="gray")
            lbl_resto.pack(fill="x", pady=2)

        # Habilita/desabilita o botão mover
        if self.arquivos_encontrados:
            self.botao_mover.config(state="normal")
        else:
            self.botao_mover.config(state="disabled")
            # Se desejar, mostre um label informativo
            lbl_vazio = ttk.Label(self.frame_arquivos, text="Nenhum arquivo com essa extensão foi encontrado.")
            lbl_vazio.pack()

    def _executar_movimentacao(self):
        """
        Move todos os arquivos listados em self.arquivos_encontrados para o diretório de destino.
        Passos:
        1. Obter o caminho de destino (self.diretorio_destino.get()).
        2. Validar se o destino foi informado (senão, erro e return).
        3. Criar o diretório de destino se ele não existir (destino_path.mkdir(parents=True, exist_ok=True)).
        4. Para cada arquivo em self.arquivos_encontrados, usar shutil.move(origem, destino).
           O destino deve ser: destino_path / arquivo.name
        5. Contar quantos foram movidos com sucesso e exibir uma mensagem final.
        6. Após mover, chame self._listar_arquivos() para atualizar a lista.
        """
        caminho_destino = self.diretorio_destino.get()
        if not caminho_destino:
            messagebox.showerror("Erro", "Escolha um diretório de destino")
            return

        destino_path = Path(caminho_destino)
        # TODO: Criar a pasta de destino se não existir

        sucessos = 0
        for arquivo in self.arquivos_encontrados:
            try:
                # TODO: Mover o arquivo com shutil.move
                # Dica: shutil.move(str(arquivo), str(destino_path / arquivo.name))
                sucessos += 1
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao mover {arquivo.name}\n{e}")

        messagebox.showinfo("Concluído", f"{sucessos} arquivo(s) movido(s) com sucesso.")
        self._listar_arquivos()

# ================== PONTO DE ENTRADA ==================
if __name__ == "__main__":
    root = tk.Tk()
    app = OrganizadorArquivosApp(root)
    root.mainloop()