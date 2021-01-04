
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import words
import time as t

def train(ficheiro):                                   # Função train - Recebe um ficheiro e cria um dicionário (vocabulary) das palavras usadas
    file = pd.read_csv(f"{ficheiro}.csv")                   # Leitura do ficheiro Treino.csv
    nltk.download("words")                                  # Download de uma lista de todas as palavras existentes no dicionário inglês
    set_words = set(words.words())                          # Criação de um set (lista não ordenada de valores únicos) para guardar o dicionário inglês

    for i in range(file.shape[0]):                          # Ciclo que corre todas as mensagens do ficheiro
        email = file.iloc[i, 0].split()                     # Mensagem separada por palavras

        for word in email:                                  # Ciclo que corre todas as palavras de uma mensagem
            if word.lower() not in vocabulary and word.lower() in set_words: # Verificação da existência da palavra no dicionário vocabulary e no set set_words
                vocabulary[word] = len(vocabulary)          # Atribuição de uma posição à palavra analisada no dicionário vocabulary
    generate(str(ficheiro))

def generate(ficheiro):                                # Função generate - Gera as matrizes data e verify
    file = pd.read_csv(f"{ficheiro}.csv")                   # Leitura do ficheiro Treino.csv

    global data                                             # Variável data definida como global
    data = np.zeros((file.shape[0], len(vocabulary)))       # Criação de uma matriz com número de linhas igual ao número de linhas do ficheiro e com número de colunas igual ao número de palavras (sem repetição) existentes no vocabulário
    global verify                                           # Variável verify definida como global
    verify = np.zeros(file.shape[0])                        # Criação de uma matriz com número de linhas igual ao número de linhas do ficheiro e com uma coluna

    for i in range(file.shape[0]):                          # Ciclo que corre todas as linhas do ficheiro
        email = file.iloc[i, 0].split()                     # Mensagem separada por palavras

        for word in email:                                  # Ciclo que corre todas as palavras de uma mensagem
            if word.lower() in vocabulary:                  # Verificação da existência da palavra no dicionário vocabulary
                data[i, vocabulary[word]] += 1              # Adição de valores à matriz data (+1 no índice da palavra que foi repetida)
                if file.iloc[i, 1] == 1:
                    verify[i] = 1                           # Adição de valores à matriz verify (adiciona 1 para spam)
                elif file.iloc[i, 1] == 0:
                    verify[i] = -1                          # Adição de valores à matriz verify (adiciona -1 para ham)

class Perceptron():
    def __init__(self, l_rate, n_iter):
        self.l_rate = l_rate
        self.n_iter = n_iter

    def classify(self, data, verify):
        self.errors_list = []
        probs = np.zeros(data.shape[0])

        for i in range(self.n_iter):
            errors = 0
            mail_count = 0
            for mail, target in zip(data, verify):
                prediction = self.predict(mail)
                update = self.l_rate * (target - prediction)
                if update != 0:
                    weight[1:] += update * mail
                    weight[0] += update
                errors += int(update != 0.0)
                probs[mail_count] = prediction
                mail_count += 1
            self.errors_list.append(errors)
        return probs

    def net_input(self, mail):
        return np.dot(mail, weight[1:]) + weight[0]

    def predict(self, mail):
        return np.where(self.net_input(mail) >= 0.0, 1, -1)

if __name__ == "__main__":
    vocabulary = {}
    start_time = t.time()
    train("Treino")
    weight = np.zeros(1 + data.shape[1])
    P = Perceptron(0.01, 20)
    P.classify(data, verify)
    train_time = t.time() - start_time

    generate("Treino")
    P = Perceptron(0, 1)
    classification = P.classify(data, verify)
    test_time = t.time() - start_time - train_time

    print("\nFicheiro\nNúmero de linhas analisadas: {}".format(data.shape[0]))
    print("Número de palavras existentes (sem repetição): {}".format(data.shape[1]))
    print("Número de mensagens classificadas como spam: {}".format(sum(verify == 1)))
    print("Número de mensagens classificadas como ham: {}".format(sum(verify == -1)))

    print("\nAlgoritmo Perceptrão\nNúmero de mensagens classificadas como spam: {}".format(sum(classification == 1)))
    print("Número de mensagens classificadas como ham: {}".format(sum(classification == -1)))
    print("\nPrecisão do algoritmo: {:0.3f} %".format(sum(classification == verify) / data.shape[0] * 100))
    print("\nTempo de treino: {0:.0f} segundo(s)".format(train_time))
    print("Tempo de teste: {0:.0f} segundo(s)".format(test_time))

    '''for value in verify:
        if value == 0.0:
            print(value)
    print(np.where(verify == 0))'''
