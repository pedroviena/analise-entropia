# Analisador de Entropia de Texto

Este projeto realiza uma análise da **Entropia de Shannon** em textos de linguagem natural, comparando-a com cenários de aleatoriedade teórica e densidade de informação em chaves criptográficas, incluindo uma simulação conceitual de chaves pós-quânticas.

---

## Funcionalidades

- **Análise de Múltiplos Livros:** Automatiza o download e processamento de múltiplos livros do Projeto Gutenberg.  
- **Cálculo de Entropia de Shannon:** Calcula a entropia média (em bits por caractere) para cada texto.  
- **Visualização Comparativa:** Gera um gráfico de barras detalhado comparando a entropia dos textos com:
  - Entropia máxima teórica para caracteres ASCII.  
  - Densidade de entropia de chaves criptográficas padrão (ex: AES-256).  
  - Densidade de entropia de chaves pós-quânticas (ex: Kyber), destacando a diferença na complexidade total.  
- **Testes Unitários:** Inclui um conjunto de testes para validar a precisão da função de cálculo de entropia.  
- **Geração de Relatório para CI/CD:** Cria um arquivo `entropy_report.txt` com os resultados, ideal para automação.  
- **Exemplo de CI/CD:** Fornece um arquivo de workflow (`.github/workflows/main.yml`) para GitHub Actions que automatiza os testes e a geração do relatório.  

---

## Análise Pós-Quântica

A comparação "pós-quântica" no gráfico é conceitual. Ela demonstra que, embora a densidade de entropia (bits por caractere/byte) seja a mesma de uma chave tradicional (idealmente 8 bits/byte), o **comprimento total dessas chaves é muito maior**.  

Por exemplo:  
- Uma chave **Kyber-1024** tem **8192 bits de entropia total**  
- Em comparação com os **256 bits** de uma chave AES-256  

Isso se traduz em uma resistência muito superior contra ataques de computadores quânticos, uma complexidade que a entropia de textos em linguagem natural, por sua previsibilidade, jamais alcançaria.

---

## Como Usar

### Pré-requisitos
- Python 3.8 ou superior  
- Pip (gerenciador de pacotes)

### Instalação
Clone o repositório:

```bash
git clone <url-do-seu-repositorio>
cd <nome-do-repositorio>

pip install -r requirements.txt
python analise_entropia.py
python -m unittest test_entropy.py

.
├── .github/
│   └── workflows/
│       └── main.yml      # Workflow de CI/CD para GitHub Actions
├── analise_entropia.py   # Script principal de análise
├── test_entropy.py       # Testes unitários para o cálculo de entropia
├── requirements.txt      # Lista de dependências Python
└── README.md             # Esta documentação
