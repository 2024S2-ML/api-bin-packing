# Projeto **Nowastee**

# 1.**Otimização do Layout e Processamento**

### **1.1 Encaixe de Figuras Variadas**

**Objetivo:**

Permitir que o sistema aceite e posicione peças com formatos geométricos diversos para melhor aproveitamento do espaço e redução do desperdício.

**Benefícios Esperados:**

- Maior eficiência no uso do tecido.
- Redução do desperdício de matéria-prima.
- Possibilidade de otimização de layouts mais complexos.

**Recursos Tecnológicos Necessários:**

- Algoritmo de bin-packing adaptado para múltiplos formatos.
- Biblioteca de manipulação geométrica.
- Banco de dados para armazenar os formatos de peças.

**Plano de Implementação:**

1. Levantar os formatos geométricos suportados.
2. Ajustar o algoritmo de bin-packing para diferentes formas.
3. Desenvolver testes unitários e de integração.
4. Atualizar a documentação técnica.

**Indicadores de Desempenho:**

- Percentual de redução do desperdício de tecido.
- Tempo médio de processamento para cada disposição de peças.
- Taxa de aceitação das sugestões de layout.

---

### **1.2 Aplicação de Técnicas de Reorganização**

**Objetivo:**

Implementar técnicas para reorganizar o layout da mesa de corte, reduzindo lacunas e desperdício.

**Benefícios Esperados:**

- Maior eficiência no aproveitamento da mesa de corte.
- Redução do tempo de ajuste manual pelo operador.

**Recursos Tecnológicos Necessários:**

- Algoritmos heurísticos e evolutivos.
- Interface para visualização das sugestões.
- Banco de dados para armazenar históricos de corte.

**Plano de Implementação:**

1. Pesquisar e selecionar algoritmos de otimização.
2. Desenvolver um módulo que proponha reorganizações.
3. Criar uma interface ou API para visualização das sugestões.
4. Validar os resultados em testes práticos.

**Indicadores de Desempenho:**

- Percentual de melhora na ocupação da mesa.
- Tempo médio de reorganização automática.
- Aceitação das sugestões pelos operadores.

---

### **1.3 Mecanismo de Sugestão de Combinações de Peças**

**Objetivo:**

Criar um sistema que sugira combinações de peças para preencher lacunas na mesa de corte.

**Benefícios Esperados:**

- Redução do desperdício.
- Maior eficiência na organização do corte.

**Recursos Tecnológicos Necessários:**

- Algoritmo de análise de cortes passados.
- Sistema de recomendação baseado em IA.
- Interface gráfica para exibição das sugestões.

**Plano de Implementação:**

1. Coletar e armazenar dados históricos de cortes.
2. Desenvolver um algoritmo de sugestão.
3. Criar uma interface para apresentação das sugestões.
4. Ajustar o sistema com base nos resultados práticos.

**Indicadores de Desempenho:**

- Percentual de redução de desperdício.
- Precisão das sugestões em comparação com layouts manuais.
- Tempo médio de processamento das recomendações.

---

## **2. Customização**

### **2.1 Visualização de Design**

**Objetivo:**

Conseguir visualizar e personalizar o design da camisa em um ambiente 3D, permitindo a aplicação de estampas e a simulação do caimento de diferentes tipos de tecido.

**Benefícios Esperados:**

- Maior controle sobre as peças durante o processo produtivo.
- Melhoria na experiência do cliente ao permitir visualização prévia da peça personalizada.
- Redução de erros na produção devido à pré-visualização detalhada.

**Recursos Tecnológicos Necessários:**

- Uso do Blender ou outra ferramenta de modelagem 3D para geração de modelos.
- Capacidade de upload de imagens via web para personalização das estampas.
- Definição se a aplicação das estampas será em tempo real ou processada antes da visualização.

**Plano de Implementação:**

1. Selecionar e configurar a ferramenta 3D mais adequada para a modelagem das camisetas.
2. Desenvolver uma interface web que permita o upload de estampas e a customização das peças.
3. Integrar um sistema de renderização que possibilite a visualização do caimento dos tecidos.
4. Implementar testes para garantir a compatibilidade entre diferentes navegadores e dispositivos.
5. Validar a experiência do usuário e otimizar a interação com o sistema.
6. Implantar a solução gradualmente, coletando feedbacks para melhorias contínuas.

**Indicadores de Desempenho:**

- Tempo médio de renderização da peça personalizada.
- Nível de satisfação dos usuários medido por feedbacks e pesquisas.
    - Redução de retrabalho na produção devido a erros na personalização.

---

# Extra

Projetos pensados mas não estão exatamente de acordo com a dor do cliente. São apenas etapas de melhorias do processo.

## **1. Validação e Controle de Qualidade**

### **1.1 Validação de Imagem de Enfesto**

**Objetivo:**

Garantir que o corte real esteja de acordo com o planejamento digital, utilizando visão computacional.

**Benefícios Esperados:**

- Redução de erros de corte.
- Aumento da precisão na produção.

**Recursos Tecnológicos Necessários:**

- Modelo YOLO pré-treinado.
- Algoritmos de processamento de imagem.
- Banco de dados para armazenar imagens de referência.

**Plano de Implementação:**

1. Integrar o modelo YOLO ao sistema.
2. Desenvolver um módulo para captura e processamento de imagens.
3. Comparar o layout real com o planejado.
4. Gerar relatórios e feedbacks automatizados.

**Indicadores de Desempenho:**

- Percentual de cortes corretamente validados.
- Redução de erros em comparação com processos manuais.
- Tempo médio de processamento das validações.

---

### **1.2 Validação da Camiseta Costurada com IA**

**Objetivo:**

Desenvolver um modelo de inteligência artificial para validar a conformidade da camiseta costurada.

**Benefícios Esperados:**

- Maior controle de qualidade na produção.
- Redução de peças defeituosas.

**Recursos Tecnológicos Necessários:**

- Modelo de IA para reconhecimento de padrões.
- Algoritmos de análise de conformidade.
- Sistema de captura de imagens.

**Plano de Implementação:**

1. Treinar ou integrar um modelo de IA para validação.
2. Criar um pipeline de captura e análise de imagens.
3. Comparar a peça produzida com o modelo padrão.
4. Ajustar a IA conforme novos dados.

**Indicadores de Desempenho:**

- Taxa de detecção de falhas.
- Percentual de conformidade das camisetas analisadas.
- Tempo médio de processamento das validações.