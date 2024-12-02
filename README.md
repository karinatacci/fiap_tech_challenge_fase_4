### **Tech Challenge: Análise de Atividades e Emoções em Vídeo**

---

#### **Descrição do Projeto**
Este projeto implementa uma aplicação para análise de vídeos, com foco em reconhecimento facial, análise de expressões emocionais e detecção de atividades. A aplicação processa um vídeo, identifica atividades realizadas por pessoas, analisa suas emoções predominantes e gera um resumo automático. Além disso, detecta movimentos anômalos, que não seguem os padrões das atividades detectadas.

---

#### **Funcionalidades Implementadas**
1. **Reconhecimento Facial:**
   - Detecta rostos presentes no vídeo e os marca.
   - Analisa expressões emocionais usando a biblioteca `DeepFace`.

2. **Análise de Expressões Emocionais:**
   - Identifica as emoções predominantes em cada rosto detectado.
   - Considera apenas emoções com alta confiança (>80%).

3. **Detecção de Atividades:**
   - Atividades detectadas:
     - **Pessoa lendo**: Mãos próximas ao rosto.
     - **Pessoa acenando para a câmera**: Uma mão levantada acima do ombro.
     - **Pessoa dançando**: Ambas as mãos acima dos ombros, em movimento simétrico.
     - **Pessoa mexendo no celular**: Mãos posicionadas abaixo do rosto.
   - Garante que cada atividade seja registrada apenas uma vez.

4. **Detecção de Movimentos Anômalos:**
   - Registra anomalias quando nenhuma atividade conhecida é detectada ou movimentos inesperados ocorrem.

5. **Geração de Resumo Automático:**
   - Cria um resumo com:
     - Total de frames analisados.
     - Número de anomalias detectadas.
     - Frequência de cada atividade.
     - Emoções predominantes.

---

#### **Como Executar o Projeto**
1. **Pré-requisitos:**
   - Python 3.8 ou superior.

2. **Instalação:**
   - Clone o repositório:
     ```bash
     git clone https://github.com/seu-usuario/tech-challenge.git
     ```
   - Navegue para o diretório do projeto:
     ```bash
     cd tech-challenge
     ```
   - Instale as dependências

3. **Executando o Projeto:**
   - Coloque o vídeo a ser processado na pasta raiz do projeto, com o nome `video_tech_challenge.mp4`.
   - Execute o script principal:
     ```bash
     python main.py
     ```
   - Após a execução, o vídeo processado será salvo como `video_tech_challenge_final_final.mp4` e o resumo será salvo como `video_summary_final_final.txt`.

4. **Saída Esperada:**
   - Um vídeo com marcações visuais das atividades e emoções detectadas.
   - Um resumo com informações detalhadas do vídeo.

---

#### **Estrutura do Projeto**
```plaintext
├── main.py                 # Script principal
├── requirements.txt        # Dependências do projeto
├── video_tech_challenge.mp4 # Vídeo de entrada
├── video_tech_challenge_final_final.mp4 # Vídeo processado
├── video_summary_final_final.txt        # Resumo gerado
└── README.md               # Documentação do projeto
```

---

#### **Requisitos Técnicos do Desafio**
Este projeto atende às especificações do Tech Challenge:

1. **Reconhecimento facial e análise de emoções:**
   - Identifica e marca rostos no vídeo.
   - Analisa emoções com precisão usando `DeepFace`.

2. **Detecção de atividades:**
   - Categoriza atividades realizadas no vídeo.
   - Detecta e registra apenas uma ocorrência de cada atividade.

3. **Detecção de anomalias:**
   - Identifica movimentos fora do padrão esperado.

4. **Resumo gerado automaticamente:**
   - Inclui:
     - Total de frames analisados.
     - Número de anomalias detectadas.
     - Frequência de cada atividade.
     - Emoções predominantes.

---
