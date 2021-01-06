import numpy as np
import pandas as pd
import nltk
from nltk.corpus import words

## Globais
try:
    nltk.data.find("words")
except LookupError:
    nltk.download("words")
dictionary = set(words.words())

def train(ficheiro):
    file = pd.read_csv(f"{ficheiro}.csv", encoding="latin-1")
    fileLines = file.shape[0]
    for i in range(fileLines):
        message = file.iloc[i, 1].split()  # mensagem separada
        for word in message:
            if word.lower() not in bagOfWords and word.lower() in dictionary:
                bagOfWords[word] = len(bagOfWords)  # atribui uma posicao a palavra
    generate(str(ficheiro))


def generate(ficheiro):
    file = pd.read_csv(f"{ficheiro}.csv", encoding="latin-1")  # le o ficheiro novamente porque é suposto usarmos dois ficheiros
    fileLines = file.shape[0]

    global data
    data = np.zeros((file.shape[0], len(bagOfWords)))  # matriz que vê as vezes que as palavras foram repetidas
    global verify
    verify = np.zeros(file.shape[0])  # matriz que vê as palavras que sao spam ou ham

    for i in range(fileLines):
        message = file.iloc[i, 1].split()
        for word in message:
            if word.lower() in bagOfWords:  # ve se a palavra está no bagofwords que o algoritmo conhece
                data[i, bagOfWords[word.lower()]] += 1  # o algoritmo reconheceu a palavra e coloca-a na matriz para vermos quantas vezes vai repetir-se
                if file.iloc[i, 0] == 'spam':
                    verify[i] = 1  # é spam portanto 1
                elif file.iloc[i, 0] == 'ham':
                    verify[i] = -1  # é ham portanto -1

class Perceptron():
    def __init__(self, l_rate, n_iter):
        self.l_rate = l_rate
        self.n_iter = n_iter

    def classify(self, data, verify):
        results = np.zeros(data.shape[0])
        for i in range(self.n_iter):
            c = 0
            for message, realValue in zip(data, verify):
                prediction = self.predict(message)
                theta = self.l_rate * (realValue - prediction)
                if theta != 0:
                    weight[1:] += theta * message
                    weight[0] += theta
                results[c] = prediction
                c += 1
        return results

    def net_input(self, mail):
        return np.dot(mail, weight[1:]) + weight[0]

    def predict(self, mail):
        return np.where(self.net_input(mail) >= 0.0, 1, -1)


if __name__ == "__main__":
    bagOfWords = {}
    train("Treino")
    weight = np.zeros(1 + data.shape[1])
    P = Perceptron(0.01, 20)
    P.classify(data, verify)
    generate("Treino")
    P = Perceptron(0, 1)
    classification = P.classify(data, verify)

    print("Número de linhas analisadas: {}".format(data.shape[0]))
    print("Número de palavras existentes (sem repetição): {}".format(data.shape[1]))
    print("Número de mensagens classificadas como spam: {}".format(sum(verify == 1)))
    print("Número de mensagens classificadas como ham: {}".format(sum(verify == -1)))

    print("O que o algoritmo percebeu:")
    print("Número de mensagens classificadas como spam: {}".format(sum(classification == 1)))
    print("Número de mensagens classificadas como ham: {}".format(sum(classification == -1)))
    print("A precisão do algoritmo é de: {:0.3f} %".format(sum(classification == verify) / data.shape[0] * 100))
