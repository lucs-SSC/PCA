# -*- coding: utf-8 -*-
"""Exercício de Implementação: PCA

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iLaxKwLuW28op1AlTlXJ53gaUdGYhexW

Lucas da Silva Souza Corrêa - 202010408 <br>
Gabriel Almeida Pimentel - 202010403
"""

# Como primeiro passo, vamos importar a biblioteca pandas:
import pandas as pd

# O scikit-learn possui alguns conjuntos de dados prontos para uilitzarmos em aulas práticas. Nesse caso,
# vamos usar o scikit-learn para importar um dataset de caracteres manuscritos, somente como exemplo:
from sklearn.datasets import load_wine

# Vamos carregar nosso dataset de dígitos, e explorá-lo um pouco:
dataset = load_wine()

# Criando nosso dataframe:
df = pd.DataFrame( dataset.data, columns=dataset.feature_names)

# Imprimindo os primeiros valores, só para confirmar o resultado:
df.head(4)

# Vamos ver uma descrição do dataset (estatísticas):
df.describe() # Vamos ver que os valores dos pixels vão de 0 a 16!

# Criando nossos X's e nossos y's correspondentes:
X = df
y = dataset.target

# Para utilizarmos qualquer PCA, o primeiro passo consiste em escalonar nossos dados para média 0 e Var 1:
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
# Escalonando nosso dataset para que os valores tenham média 0 e variância 1.0:
X_scaled = scaler.fit_transform(X)

# Podemos ver que a relação entre os valores dos pixels se manteve, mas escalonados [-1.0, 1.0]:
print(X_scaled)

# Lembrem-se das nossas aulas anteriores. Precisamos dividir nosso dataset entre conjuntos de treino e teste:
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split( X_scaled, y, test_size=0.10, random_state=30)

# Somente como exemplo, vamos usar um algoritmo de Regressão logística (podemos usar outros depois):
#from sklearn.linear_model import LogisticRegression
# Importando a classe Ridge do sklearn.linear_model:
from sklearn.linear_model import Ridge

# Criando o modelo:
model = Ridge()

# Passando o conjunto de treino:
model.fit(X_train, y_train)

# Fazendo previsões no conjunto de testes:
y_pred = model.predict(X_test)

# Avaliando o modelo (por exemplo, usando a métrica R²):
from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_pred)
print("Coeficiente de determinação (R²):", r2)

# Agora podemos usar PCA nas amostras e ver como ele vai funcionar:
from sklearn.decomposition import PCA

# Podemos "forçar" o número de variáveis, ou estabelecer a porcentagem de variância que queremos capturar:

# Forçando o número de componentes seria:
# pca = PCA(n_components=3)

# Fixando somente a variância:
pca = PCA(0.98) # << Capturando 95% da variância.
# Calculando o PCA:
X_pca = pca.fit_transform(X_scaled)

# Imprimindo o novo shape, ou seja, o número de novos x's (o original é 64):
print(X_pca.shape)

# Vamos imprimir a captura de variância de cada dimensão do PCA. Claro, as primeiras dimensões deveriam ser
# as mais importantes, portanto capturando mais variância:
print(pca.explained_variance_ratio_)

# Agora podemos treinar nosso algoritmo novamente, utilizando os mesmos y's como saída, mas substituindo as
# entradas originais pelas entradas fornecidas pelo PCA:

# Dividindo o dataset novamente em treino e teste:
X_train_pca, X_test_pca, y_train, y_test = train_test_split( X_pca, y, test_size=0.30, random_state=30)

# Treinando novamente os dados:

# Criando o modelo:
model_pca = Ridge()
# Passando o conjunto de treino:
model_pca.fit( X_train_pca, y_train)
# E o conjutno de testes:
model_pca.score(X_test_pca, y_test)