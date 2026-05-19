import random
from pathlib import Path

def gerar_ambiente_teste():
    """
    Cria uma estrutura de diretórios e arquivos falsos para testar
    a rotina de automação e filtragem do aplicativo.
    """
    # Define o diretório raiz de testes
    diretorio_raiz = Path("arquivos")
    diretorio_raiz.mkdir(exist_ok=True)
    
    # Subdiretórios para simular uma estrutura real de escritório
    subdiretorios = ["Documentos_Antigos", "Relatorios_Fiscais", "Downloads_Temporarios"]
    for sub in subdiretorios:
        (diretorio_raiz / sub).mkdir(parents=True, exist_ok=True)
        
    # Extensões e nomes de arquivos base para a simulação
    extensoes = [".pdf", ".docx", ".xlsx", ".txt", ".png"]
    nomes_arquivos = [
        "relatorio_financeiro",
        "contrato_prestacao_servicos",
        "cronograma_senc26",
        "projeto_estrutural_revisado",
        "manual_do_usuario",
        "nota_fiscal_0492",
        "lista_de_insumos",
        "ata_de_reuniao",
    ] 

    proj_files = [
        f"{n}-{i:02d}_{j:02d}_{k:04d}.dwg"
        for n, i, j, k
        in zip(
            [random.choice(list("ABCDEFGHIJKLMNOP")) for _ in range(30)],
            [random.randint(1,31) for _ in range(30)],
            [random.randint(1,12) for _ in range(30)],
            [random.randint(2020,2026) for _ in range(30)],
        )
    ]
    
    total_arquivos = 0
    
    for nome in nomes_arquivos[:4]:
        for ext in extensoes:
            caminho_arquivo = diretorio_raiz / f"{nome}{ext}"
            # Escreve um texto simples dentro do arquivo para que ele não fique corrompido
            caminho_arquivo.write_text(f"Conteúdo simulado para validação de script: {nome}{ext}\n", encoding="utf-8")
            total_arquivos += 1

    for fname in proj_files:
        caminho_arquivo = diretorio_raiz / fname
        caminho_arquivo.write_text(f"Conteúdo simulado para validação de script: {fname}\n", encoding="utf-8")
        total_arquivos += 1
            
    for sub in subdiretorios:
        for nome in nomes_arquivos[4:]:
            # Escolhe uma extensão aleatória para pulverizar os tipos de arquivos
            ext = random.choice(extensoes)
            caminho_arquivo = diretorio_raiz / sub / f"{nome}{ext}"
            caminho_arquivo.write_text(f"Arquivo temporário alocado em {sub}: {nome}{ext}\n", encoding="utf-8")
            total_arquivos += 1

    print(f"Sucesso: {total_arquivos} arquivos de teste gerados no diretório '{diretorio_raiz.resolve()}'.")

if __name__ == "__main__":
    gerar_ambiente_teste()