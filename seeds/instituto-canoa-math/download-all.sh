#!/bin/bash
# Download all Instituto Canoa math activities (public domain)
# Source: https://institutocanoa.org/atividades-de-matematica/
# URLs verified from the actual website on 2026-03-08
BASE="https://institutocanoa.org/novosite/wp-content/uploads"
DIR="$(dirname "$0")"

echo "Downloading Instituto Canoa math activities..."

# === 6º ANO ===
# Sólidos Geométricos
curl -sL -o "$DIR/6ano-solidos-1-agrupando-formas.pdf" "$BASE/2023/12/6o-ano-Solidos-geometricos-1.-Agrupando-formas-tridimensionais.pdf"
curl -sL -o "$DIR/6ano-solidos-2-sombras-geometricas.pdf" "$BASE/2024/04/6o-ano-Solidos-geometricos-2.-Sombras-geometricas.pdf"
curl -sL -o "$DIR/6ano-solidos-3-investigando-planificacoes.pdf" "$BASE/2023/12/6o-ano-Solidos-geometricos-3.-Investigando-planificacoes.pdf"

# Probabilidade
curl -sL -o "$DIR/6ano-prob-1-mais-chance.pdf" "$BASE/2023/12/6o-ano-Probabilidade-1.-O-que-tem-mais-chance-de-acontecer_.pdf-.pdf"
curl -sL -o "$DIR/6ano-prob-2-jogo-justo.pdf" "$BASE/2023/12/6o-ano-Probabilidade-2.-Jogo-justo-ou-injusto_.pdf"
curl -sL -o "$DIR/6ano-prob-3-saco-probabilistico.pdf" "$BASE/2023/12/6o-ano-Probabilidade-3.-Saco-probabilistico.pdf"

# Interpretando Gráficos
curl -sL -o "$DIR/6ano-graficos-1-buscando-praias.pdf" "$BASE/2023/12/6o-ano-Interpretando-graficos-1.-Buscando-praias.pdf"
curl -sL -o "$DIR/6ano-graficos-2-conectividade.pdf" "$BASE/2023/12/6o-ano-Interpretando-graficos-2.-Conectividade.pdf"
curl -sL -o "$DIR/6ano-graficos-3-retrato-da-turma.pdf" "$BASE/2023/12/6o-ano-Interpretando-graficos-3.-Retrato-da-turma.pdf"

# Ângulos
curl -sL -o "$DIR/6ano-angulos-1-reconhecendo.pdf" "$BASE/2023/12/6o-ano-Angulos-1.-Reconhecendo-angulos.pdf"
curl -sL -o "$DIR/6ano-angulos-2-relogio.pdf" "$BASE/2023/12/6o-ano-Angulos-2.-Relogio.pdf"
curl -sL -o "$DIR/6ano-angulos-3-cinema.pdf" "$BASE/2023/12/6o-ano-Angulos-3.-Angulos-no-cinema.pdf"

# Frações
curl -sL -o "$DIR/6ano-fracoes-1-meio.pdf" "$BASE/2023/12/6o-ano-Fracoes-1.-E-meio-ou-nao-e_.pdf"
curl -sL -o "$DIR/6ano-fracoes-2-tangram.pdf" "$BASE/2023/12/6o-ano-Fracoes-2.-Tangram.pdf"
curl -sL -o "$DIR/6ano-fracoes-3-comparando.pdf" "$BASE/2023/12/6o-ano-Fracoes-3.-Comparando-fracoes.pdf"

# Múltiplos e Divisores
curl -sL -o "$DIR/6ano-multiplos-1-pulseiras.pdf" "$BASE/2023/12/6o-ano-Multiplos-e-divisores-1.-Pulseiras-coloridas.pdf"
curl -sL -o "$DIR/6ano-multiplos-2-decifrando.pdf" "$BASE/2023/12/6o-ano-Multiplos-e-divisores-2.-Decifrando-o-seis.pdf"
curl -sL -o "$DIR/6ano-multiplos-3-pensando.pdf" "$BASE/2023/12/6o-ano-Multiplos-e-divisores-3.-Pensando-como-um-matematico.pdf"

# Operações com Frações
curl -sL -o "$DIR/6ano-op-fracoes-1-somando.pdf" "$BASE/2023/12/6o-ano-Operacoes-com-fracoes-1.-Somando-fracoes.pdf"
curl -sL -o "$DIR/6ano-op-fracoes-2-lanche.pdf" "$BASE/2023/12/6o-ano-Operacoes-com-fracoes-2.-Lanche-com-amigos.pdf"
curl -sL -o "$DIR/6ano-op-fracoes-3-quadrados.pdf" "$BASE/2023/12/6o-ano-Operacoes-com-fracoes-3.-Quadrados-pintados.pdf"

# Polígonos
curl -sL -o "$DIR/6ano-poligonos-1-formas-diversas.pdf" "$BASE/2023/12/6o-ano-Poligonos-1.-Formas-diversas.pdf"
curl -sL -o "$DIR/6ano-poligonos-2-quadrilatero.pdf" "$BASE/2023/12/6o-ano-Poligonos-2.-Que-quadrilatero-eu-sou_.pdf"
curl -sL -o "$DIR/6ano-poligonos-3-agrupando-triangulos.pdf" "$BASE/2023/12/6o-ano-Poligonos-3.-Agrupando-triangulos.pdf"
curl -sL -o "$DIR/6ano-poligonos-4-que-propriedade.pdf" "$BASE/2023/12/6o-ano-Poligonos-4.-Que-propriedade-e-essa_.pdf"

# === 7º ANO ===
# Área de Figuras Planas
curl -sL -o "$DIR/7ano-area-1-triangulo-retangulo.pdf" "$BASE/2023/10/7o-ano-Area-de-figuras-planas-1.-Area-do-triangulo-retangulo.pdf"
curl -sL -o "$DIR/7ano-area-2-triangulo-qualquer.pdf" "$BASE/2023/10/7o-ano-Area-de-figuras-planas-2.-Area-de-um-triangulo-qualquer.pdf"
curl -sL -o "$DIR/7ano-area-3-trapezio.pdf" "$BASE/2023/10/7o-ano-Area-de-figuras-planas-3.-Area-do-trapezio.pdf"

# Compondo e Decompondo Áreas
curl -sL -o "$DIR/7ano-comp-area-1-area-interessante.pdf" "$BASE/2023/10/7o-ano-Compondo-e-decompondo-areas-de-figuras-planas-Area-interessante.pdf"
curl -sL -o "$DIR/7ano-comp-area-2-grama-jardim.pdf" "$BASE/2023/10/7o-ano-Compondo-e-decompondo-areas-de-figuras-planas-Grama-no-jardim.pdf"
curl -sL -o "$DIR/7ano-comp-area-3-que-figura.pdf" "$BASE/2023/10/7o-ano-Compondo-e-decompondo-areas-de-figuras-planas-Que-figura-e-essa_.pdf"

# Equações do 1º Grau
curl -sL -o "$DIR/7ano-equacoes-1-tiras.pdf" "$BASE/2023/10/7o-ano-Equacoes-do-1o-grau-1.-Equacoes-em-tiras.pdf"
curl -sL -o "$DIR/7ano-equacoes-2-mobile.pdf" "$BASE/2023/10/7o-ano-Equacoes-do-1o-grau-2.-Mobile-de-equacoes.pdf"
curl -sL -o "$DIR/7ano-equacoes-3-festa-junina.pdf" "$BASE/2023/10/7o-ano-Equacoes-do-1o-grau-3.-Equacoes-na-festa-junina.pdf"

# Números Inteiros
curl -sL -o "$DIR/7ano-inteiros-1-bandeiras.pdf" "$BASE/2023/10/7o-ano-Numeros-inteiros-1.-Jogo-das-bandeiras.pdf"
curl -sL -o "$DIR/7ano-inteiros-2-somando.pdf" "$BASE/2023/10/7o-ano-Numeros-inteiros-2.-Somando-numeros-positivos-e-negativos.pdf"
curl -sL -o "$DIR/7ano-inteiros-3-temperaturas.pdf" "$BASE/2023/10/7o-ano-Numeros-inteiros-3.-Temperaturas-positivas-e-negativas.pdf"

# Porcentagem
curl -sL -o "$DIR/7ano-porcentagem-1-regua.pdf" "$BASE/2023/10/7o-ano-Porcentagem-1.-Regua-de-porcentagens.pdf"
curl -sL -o "$DIR/7ano-porcentagem-2-folheto.pdf" "$BASE/2023/10/7o-ano-Porcentagem-2.-Folheto-de-porcentagens.pdf"
curl -sL -o "$DIR/7ano-porcentagem-3-black-friday.pdf" "$BASE/2023/10/7o-ano-Porcentagem-3.-Black-Friday.pdf"

# Propriedades dos Polígonos
curl -sL -o "$DIR/7ano-prop-poligonos-1-construindo.pdf" "$BASE/2023/10/7o-ano-Propriedades-dos-poligonos-1.-Construindo-triangulos.pdf"
curl -sL -o "$DIR/7ano-prop-poligonos-2-somando-angulos.pdf" "$BASE/2023/10/7o-ano-Propriedades-dos-poligonos-2.-Somando-angulos.pdf"
curl -sL -o "$DIR/7ano-prop-poligonos-3-diagonais.pdf" "$BASE/2023/10/7o-ano-Propriedades-dos-poligonos-3.-Poligonos-e-suas-diagonais.pdf"

# Simetrias
curl -sL -o "$DIR/7ano-simetrias-1-figuras-embaralhadas.pdf" "$BASE/2023/10/7o-ano-Simetrias-1.-Figuras-embaralhadas.pdf"
curl -sL -o "$DIR/7ano-simetrias-2-reflexoes-geoplano.pdf" "$BASE/2023/10/7o-ano-Simetrias-2.-Reflexoes-com-o-geoplano.pdf"
curl -sL -o "$DIR/7ano-simetrias-3-poliminos.pdf" "$BASE/2023/10/7o-ano-Simetrias-3.-Simetria-dos-poliminos.pdf"

# Volume de Blocos Retangulares
curl -sL -o "$DIR/7ano-volume-1-construindo-blocos.pdf" "$BASE/2023/10/7o-ano-Volume-de-blocos-retangulares-1.-Construindo-blocos.pdf"
curl -sL -o "$DIR/7ano-volume-2-investigando.pdf" "$BASE/2023/10/7o-ano-Volume-de-blocos-retangulares-2.-Investigando-o-volume-de-caixas.pdf"
curl -sL -o "$DIR/7ano-volume-3-qual-volume.pdf" "$BASE/2023/10/7o-ano-Volume-de-blocos-retangulares-3.-Qual-e-o-volume-do-objeto_.pdf"

# === 8º ANO ===
# Unidades de Volume e Capacidade
curl -sL -o "$DIR/8ano-volume-cap-1-frasco.pdf" "$BASE/2023/10/8o-ano-Unidades-de-volume-e-capacidade-1.-Frasco-de-medir-volumes.pdf"
curl -sL -o "$DIR/8ano-volume-cap-2-aquario.pdf" "$BASE/2023/10/8o-ano-Unidades-de-volume-e-capacidade-2.-Construindo-um-aquario.pdf"
curl -sL -o "$DIR/8ano-volume-cap-3-copo-medidor.pdf" "$BASE/2023/10/8o-ano-Unidades-de-volume-e-capacidade-3.-Copo-medidor.pdf"

# Sistema de Equações
curl -sL -o "$DIR/8ano-sist-eq-1-passeios-cachorro.pdf" "$BASE/2023/10/8o-ano-Sistema-de-equacoes-1.-Passeios-com-cachorro.pdf"
curl -sL -o "$DIR/8ano-sist-eq-2-lampadas.pdf" "$BASE/2023/10/8o-ano-Sistema-de-equacoes-2.-Comparando-o-custo-de-lampadas.pdf"
curl -sL -o "$DIR/8ano-sist-eq-3-pipoca.pdf" "$BASE/2023/10/8o-ano-Sistema-de-equacoes-3.-Carrinho-de-pipoca.pdf"

# Relações Lineares
curl -sL -o "$DIR/8ano-lineares-1-corrida.pdf" "$BASE/2023/10/8o-ano-Relacoes-lineares-1.-Disputando-uma-corrida.pdf"
curl -sL -o "$DIR/8ano-lineares-2-combinando.pdf" "$BASE/2023/10/8o-ano-Relacoes-lineares-2.-Combinando-representacoes.pdf"
curl -sL -o "$DIR/8ano-lineares-3-torre-copos.pdf" "$BASE/2023/10/8o-ano-Relacoes-lineares-3.-Torre-de-copos.pdf"

# Probabilidade
curl -sL -o "$DIR/8ano-prob-1-cara-coroa.pdf" "$BASE/2023/10/8o-ano-Probabilidade-1.-Cara-ou-coroa.pdf"
curl -sL -o "$DIR/8ano-prob-2-par-impar.pdf" "$BASE/2023/10/8o-ano-Probabilidade-2.-Para-ou-impar.pdf"
curl -sL -o "$DIR/8ano-prob-3-acai.pdf" "$BASE/2023/10/8o-ano-Probabilidade-3.-Preparando-um-acai.pdf"

# Potenciação
curl -sL -o "$DIR/8ano-potencias-1-produto.pdf" "$BASE/2023/10/8o-ano-Potenciacao-1.-Produto-de-potencias.pdf"
curl -sL -o "$DIR/8ano-potencias-2-divisao.pdf" "$BASE/2023/10/8o-ano-Potenciacao-2.-Divisao-de-potencias.pdf"
curl -sL -o "$DIR/8ano-potencias-3-corpos-celestes.pdf" "$BASE/2023/10/8o-ano-Potenciacao-3.-Comparando-corpos-celestes.pdf"

# Medidas de Tendência Central
curl -sL -o "$DIR/8ano-tendencia-1-onibus.pdf" "$BASE/2023/10/8o-ano-Medidas-de-tendencia-central-1.-Linhas-de-onibus.pdf"
curl -sL -o "$DIR/8ano-tendencia-2-pesquisando.pdf" "$BASE/2023/10/8o-ano-Medidas-de-tendencia-central-2.-Pesquisando-a-turma.pdf"
curl -sL -o "$DIR/8ano-tendencia-3-natacao.pdf" "$BASE/2023/10/8o-ano-Medidas-de-tendencia-central-3.-Treino-de-natacao.pdf"

# Construções Geométricas
curl -sL -o "$DIR/8ano-construcoes-1-geometricas.pdf" "$BASE/2023/10/8o-ano-Construcoes-geometricas-1.-Construcoes-geometricas.pdf"
curl -sL -o "$DIR/8ano-construcoes-2-trapezio.pdf" "$BASE/2023/10/8o-ano-Construcoes-geometricas-2.-Construindo-um-trapezio.pdf"
curl -sL -o "$DIR/8ano-construcoes-3-parque.pdf" "$BASE/2023/10/8o-ano-Construcoes-geometricas-3.-Parque-de-diversoes.pdf"

# Área do Círculo
curl -sL -o "$DIR/8ano-circulo-1-dividindo.pdf" "$BASE/2023/10/8o-ano-Area-do-circulo-1.-Dividindo-um-circulo-em-partes.pdf"
curl -sL -o "$DIR/8ano-circulo-2-barbante.pdf" "$BASE/2023/10/8o-ano-Area-do-circulo-2.-Preenchendo-um-circulo-com-barbante.pdf"
curl -sL -o "$DIR/8ano-circulo-3-pastagem.pdf" "$BASE/2023/10/8o-ano-Area-do-circulo-3.-Area-de-pastagem.pdf"

# === 9º ANO ===
# Análise de Gráficos
curl -sL -o "$DIR/9ano-graficos-1-cetico.pdf" "$BASE/2023/08/9o-ano-Analise-de-graficos-1.-O-cetico-e-o-grafico.pdf"
curl -sL -o "$DIR/9ano-graficos-2-desmatamento.pdf" "$BASE/2023/08/9o-ano-Analise-de-graficos-2.-O-desmatamento-em-graficos.pdf"
curl -sL -o "$DIR/9ano-graficos-3-pantanal.pdf" "$BASE/2023/08/9o-ano-Analise-de-graficos-3.-Pantanal_-conhecer-e-preservar.pdf"

# Teorema de Pitágoras
curl -sL -o "$DIR/9ano-pitagoras-1-quadrados.pdf" "$BASE/2023/08/9o-ano-Teorema-de-Pitagoras-1.-Investigando-quadrados-no-triangulo.pdf"
curl -sL -o "$DIR/9ano-pitagoras-2-demonstrando.pdf" "$BASE/2023/08/9o-ano-Teorema-de-Pitagoras-2.-Demonstrando-o-Teorema-de-Pitagoras.pdf"
curl -sL -o "$DIR/9ano-pitagoras-3-barraca.pdf" "$BASE/2023/08/9o-ano-Teorema-de-Pitagoras-3.-Altura-da-barraca.pdf"

# Semelhança de Triângulos
curl -sL -o "$DIR/9ano-semelhanca-1-esquisito.pdf" "$BASE/2023/08/9o-ano-Semelhanca-de-triangulos-1.-Esquisito-por-que_.pdf"
curl -sL -o "$DIR/9ano-semelhanca-2-semelhantes.pdf" "$BASE/2025/04/9o-ano-Semelhanca-de-triangulos-2.-Triangulos-semelhantes.pdf"
curl -sL -o "$DIR/9ano-semelhanca-3-pontos-medios.pdf" "$BASE/2023/08/9o-ano-Semelhanca-de-triangulos-3.-Triangulo-e-pontos-medios.pdf"

# Volume de Prismas e Cilindros
curl -sL -o "$DIR/9ano-volume-1-caixas-fosforo.pdf" "$BASE/2023/08/9o-ano-Volume-de-prismas-e-cilindros-1.-Caixas-de-fosforo.pdf"
curl -sL -o "$DIR/9ano-volume-2-prismas.pdf" "$BASE/2023/08/9o-ano-Volume-de-prismas-e-cilindros-2.-Volume-de-prismas.pdf"
curl -sL -o "$DIR/9ano-volume-3-cilindros.pdf" "$BASE/2023/08/9o-ano-Volume-de-prismas-e-cilindros-3.-Investigando-cilindros.pdf"

# Números Irracionais
curl -sL -o "$DIR/9ano-irracionais-1-area-lado.pdf" "$BASE/2023/08/9o-ano-Numeros-irracionais-1.-Explorando-a-relacao-entre-a-medida-da-area-e-do-lado-de-quadrados.pdf"
curl -sL -o "$DIR/9ano-irracionais-2-medida-segmento.pdf" "$BASE/2023/08/9o-ano-Numeros-irracionais-2.-Qual-e-a-medida-desse-segmento_.pdf"

# Razão e Proporção
curl -sL -o "$DIR/9ano-razao-1-basquete.pdf" "$BASE/2023/08/9o-ano-Razao-e-proporcao-1.-Basquete.pdf"
curl -sL -o "$DIR/9ano-razao-2-piloto.pdf" "$BASE/2023/08/9o-ano-Razao-e-proporcao-2.-Quem-e-o-melhor-piloto-de-todos-os-tempos_.pdf"
curl -sL -o "$DIR/9ano-razao-3-messi-pele.pdf" "$BASE/2023/08/9o-ano-Razao-e-proporcao-3.-Messi-e-Pele.pdf"
curl -sL -o "$DIR/9ano-razao-4-formula1.pdf" "$BASE/2023/08/9o-ano-Razao-e-proporcao-4.-Circuitos-de-Formula-1.pdf"

# Funções
curl -sL -o "$DIR/9ano-funcoes-1-comandos.pdf" "$BASE/2023/08/9o-ano-Funcoes-1.-Descobrindo-comandos.pdf"
curl -sL -o "$DIR/9ano-funcoes-2-album-copa.pdf" "$BASE/2023/08/9o-ano-Funcoes-2.-Album-da-Copa.pdf"
curl -sL -o "$DIR/9ano-funcoes-3-viralizando.pdf" "$BASE/2023/08/9o-ano-Funcoes-3.-Viralizando-mensagens.pdf"

# Expressões Algébricas
curl -sL -o "$DIR/9ano-algebra-1-areas.pdf" "$BASE/2023/08/9o-ano-Expressoes-algebricas-1.-Areas-algebricas.pdf"
curl -sL -o "$DIR/9ano-algebra-2-somas-quadrado.pdf" "$BASE/2023/08/9o-ano-Expressoes-algebricas-2.-Visualizando-somas-ao-quadrado.pdf"
curl -sL -o "$DIR/9ano-algebra-3-investigando-produtos.pdf" "$BASE/2023/08/9o-ano-Expressoes-algebricas-3.-Investigando-produtos.pdf"

echo "Download complete! Verifying..."

# Verify all downloads are real PDFs
cd "$DIR"
real=0; fake=0; fakefiles=""
for f in *.pdf; do
  header=$(head -c 5 "$f" 2>/dev/null)
  if [ "$header" = "%PDF-" ]; then
    real=$((real+1))
  else
    fake=$((fake+1))
    fakefiles="$fakefiles $f"
  fi
done
echo "Real PDFs: $real | Failed: $fake"
if [ $fake -gt 0 ]; then
  echo "Failed files: $fakefiles"
fi
