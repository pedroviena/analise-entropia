import requests
import nltk
import math
import numpy as np
import seaborn as sns
from collections import Counter
import os
from datetime import datetime
import matplotlib


if os.environ.get('CI'):
    matplotlib.use('Agg')

import matplotlib.pyplot as plt

BOOKS_TO_ANALYZE = [
    {
        "name": "Moby Dick",
        "url": "https://www.gutenberg.org/files/2701/2701-0.txt",
        "filename": "moby_dick.txt"
    },
    {
        "name": "Frankenstein",
        "url": "https://www.gutenberg.org/files/84/84-0.txt",
        "filename": "frankenstein.txt"
    },
    {
        "name": "The Adventures of Sherlock Holmes",
        "url": "https://www.gutenberg.org/files/1661/1661-0.txt",
        "filename": "sherlock_holmes.txt"
    }
]

# --- FUNÇÕES PRINCIPAIS ---

def download_file(url, filename):
    """Baixa um arquivo se ele ainda não existir no diretório."""
    if not os.path.exists(filename):
        print(f"Baixando '{filename}'...")
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("Download concluído.")
        except requests.RequestException as e:
            print(f"Erro ao baixar o arquivo: {e}")
            return False
    else:
        print(f"Arquivo '{filename}' já existe.")
    return True

def setup_nltk():
    """Verifica e baixa os pacotes NLTK necessários, se preciso."""
    required_resources = ['punkt']
    for resource in required_resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            print(f"Baixando dados do NLTK: '{resource}'...")
            nltk.download(resource, quiet=True)
            print(f"Download de '{resource}' concluído.")

def calculate_shannon_entropy(text):
    """
    Calcula a Entropia de Shannon para um dado texto.
    A entropia é medida em bits por caractere.
    """
    if not text:
        return 0.0
    
    freq_counter = Counter(text)
    text_len = len(text)
    entropy = 0.0
    
    for count in freq_counter.values():
        probability = count / text_len
        entropy -= probability * math.log2(probability)
        
    return entropy

def process_book_text(filename):
    """Lê um livro e o divide em uma lista de frases limpas."""
    print(f"Processando texto de '{filename}'...")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
        sentences = nltk.sent_tokenize(text)
        # Filtra frases para ter um tamanho mínimo, removendo ruídos
        clean_sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        print(f"Texto processado. Encontradas {len(clean_sentences)} frases relevantes.")
        return clean_sentences
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado.")
        return []

def create_entropy_plot(analysis_results):
    """Cria e salva um gráfico de barras comparando as entropias de várias fontes."""
    print("Gerando o gráfico comparativo...")
    
    # Entropia máxima para caracteres ASCII imprimíveis (95 caracteres)
    max_char_entropy = math.log2(95)
    # Densidade de entropia para dados criptográficos (1 byte = 8 bits)
    max_crypto_entropy_per_char = 8

    # Labels e valores para o gráfico
    labels = [f'"{name}"' for name in analysis_results.keys()]
    values = list(analysis_results.values())
    
    # Adicionando cenários teóricos
    labels.extend([
        'Máxima Teórica\n(95 caracteres aleatórios)',
        'Chave Cripto AES-256\n(Densidade)',
        'Chave Pós-Quântica (Kyber)\n(Densidade)'
    ])
    values.extend([
        max_char_entropy,
        max_crypto_entropy_per_char,
        max_crypto_entropy_per_char  # A densidade é a mesma, mas a chave é maior
    ])

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(15, 10))
    
    palette = sns.color_palette("viridis", n_colors=len(analysis_results)) + ["#FF5733", "#C70039", "#900C3F"]
    barplot = sns.barplot(x=labels, y=values, palette=palette)
    
    plt.title('Análise de Entropia: Textos vs. Aleatoriedade Teórica e Criptográfica', fontsize=18, weight='bold')
    plt.ylabel('Entropia (bits por caractere)', fontsize=14)
    plt.xticks(rotation=15, ha="right")
    plt.ylim(0, max(values) * 1.1)
    
    # Adiciona os valores no topo das barras
    for i, v in enumerate(values):
        barplot.text(i, v + 0.08, f"{v:.2f}", color='black', ha="center", weight='bold')
        
    plt.figtext(0.5, -0.15, 
                ('Nota: Este gráfico compara a *densidade* de entropia (bits/caractere).\n'
                 'Uma chave criptográfica real (ex: AES-256) tem uma entropia TOTAL de 256 bits.\n'
                 'Chaves pós-quânticas (ex: Kyber-1024) possuem entropia total ainda maior (8192 bits), '
                 'representando uma complexidade ordens de magnitude maior que a de qualquer texto.'), 
                ha='center', fontsize=10, style='italic', bbox={"facecolor":"white", "alpha":0.6, "pad":5})

    output_filename = 'grafico_entropia_comparativo.png'
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Gráfico salvo com sucesso como '{output_filename}'!")
    
    # Exibe o gráfico apenas se NÃO estiver em um ambiente de CI
    if not os.environ.get('CI'):
        plt.show()

def generate_report(results):
    """Gera um arquivo de relatório simples para ser usado em CI/CD."""
    report_filename = "entropy_report.txt"
    print(f"Gerando relatório em '{report_filename}'...")
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("Relatório de Análise de Entropia\n")
        f.write("="*35 + "\n")
        f.write(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for name, entropy in results.items():
            f.write(f"- Entropia média para '{name}': {entropy:.4f} bits/caractere\n")
        f.write("\nRelatório gerado com sucesso.")
    print("Relatório finalizado.")

def main():
    """Função principal que orquestra o download, processamento e análise."""
    setup_nltk()
    
    analysis_results = {}
    
    for book in BOOKS_TO_ANALYZE:
        print(f"\n--- Iniciando Análise para: {book['name']} ---")
        if download_file(book['url'], book['filename']):
            sentences = process_book_text(book['filename'])
            
            if sentences:
                # Usando list comprehension para calcular entropia de cada frase
                entropies = [calculate_shannon_entropy(s) for s in sentences]
                average_entropy = np.mean(entropies)
                analysis_results[book['name']] = average_entropy
                
                print(f"Resultado para '{book['name']}': Entropia Média = {average_entropy:.4f} bits/caractere")

    if analysis_results:
        print("\n--- Análise de todos os livros concluída ---")
        create_entropy_plot(analysis_results)
        generate_report(analysis_results)
    else:
        print("Nenhuma análise pôde ser concluída.")

if __name__ == "__main__":
    main()

