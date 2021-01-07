import pandas as pd
import math

bagOfWords = []


def training(filename, c):
    # importa o data set como um data-frame, usa o latin-1 com decoding para ler o ficheiro e seleciona as colunas v1 e v2 como as unicas a ser usadas (o ficheiro tem mais 3 colunas mas vazias)
    file = pd.read_csv(filename, encoding="latin-1", usecols=["v1", "v2"])
    file.columns = ["Status", "Mensagem"]

    nMails = 0
    nSpam = 0
    nHam = 0
    messages = []

    for i in range(file.shape[0]):  # por cada linha do ficheiro
        if file.iloc[i, 0] == "spam":  # compute m || ve se a primeira celula da linha é spam
            nSpam += 1  # spam mails + 1
        else:
            nHam += 1  # ham mails + 1
        D = {}  # Dictionary D
        # limpa as mensagens individuais por palavras
        message = file['Mensagem'][i].split()
        for word in message:  # compute dictionary D
            if word not in bagOfWords:  # se a palavra nao está no bag of words
                bagOfWords.append(word)  # agora vai estar
            if word not in D:  # se a palavra nao e repetida
                D[word] = 1  # agora é 1
            else:
                D[word] += 1  # se a palavra for repetida é palavras existentes +1
        # agora temos mais uma mensagem/mail numa matriz [mails][words por mail]
        messages.append([file.iloc[i], D])
        nMails += 1  # numero de mensagens lidas incrementa

    b = initializeB(c, nHam, nSpam)  # initialize b
    global p
    # matriz 3*n em que n é cada palavra do bag
    p = [[1] * 2 for _ in range(len(bagOfWords))]
    spamWords = len(bagOfWords)
    hamWords = len(bagOfWords)

    for message in messages:  # for i = 1 to m do | por cada mail preenchido anteriormente
        if message[0][0] == "spam":  # if y = spam then | se for considerado spam
            # for j = 1 to n do | cada palavra desse mail
            for word in message[0][1].split():
                p[bagOfWords.index(word)][0] += message[1].get(
                    word)  # p_0.j <- p_1.j + x_j^i | ele fica com as palavras do mail no index 0 da matriz p[word][0] ou seja a frequencia da palavra ser spam
                # w_spam <- w_spam + x_j^i | o numero de spam words aumenta
                spamWords += message[1].get(word)
        if message[0][0] == "ham":  # else (nah nah nao vá o diabo tecê-las)
            # for j = 1 to n do | cada palavra desse mail
            for word in message[0][1].split():
                p[bagOfWords.index(word)][1] += message[1].get(
                    word)  # p_1.j <- p_1.j + x_j^i | ele fica com as palavras do mail no index 0 da matriz p[word][1] ou seja ham
                # w_ham <- w_ham + x_j^i | ham words aumenta
                hamWords += message[1].get(word)

    # normalize counts to yield word probabilities
    for j in p:  # for j = 1 to n do | por cada elemento do p, ou seja mail
        j[0] = j[
            0] / spamWords  # p_0.j <- p_0.j/w_spam | transformar frequencias absolutas em frequencias relativas em spam words
        j[1] = j[1] / hamWords  # p_1.j <- p_1.j/w_spam | e em ham words

    return nMails, nSpam, nHam, b


def initializeB(c, nHam, nSpam):
    # YEEHAW MATH
    return math.log(c, 10) + math.log(nHam, 10) - math.log(nSpam, 10)


def classify(x, b):
    file = pd.read_csv(x, encoding="latin-1", usecols=["v1", "v2"])
    file.columns = ["Status", "Mensagem"]
    nMails = 0
    nSpam = 0
    nHam = 0
    messages = []
    acertou = 0
    nSpamReais = 0
    nHamReais = 0

    for i in range(file.shape[0]):
        message = file['Mensagem'][i].split()
        classifyD = {}
        t = -b
        if file.iloc[i, 0] == "spam":
            nSpamReais += 1
        else:
            nHamReais += 1

        for word in message:
            if not classifyD.get(word):
                classifyD.update({word: 1})
            else:
                classifyD[word] += 1
        nMails += 1  # numero de mensagens lidas incrementa
        for j in range(len(p)):  # for j = 1 to n do
            if bagOfWords[j] in classifyD.keys():
                # t <- t + x^j(log_p0.j - log_p1.j)
                t += classifyD.get(bagOfWords[j]) * \
                    (math.log(p[j][0], 10) - math.log(p[j][1], 10))
        messages.append([file.iloc[i], t])
    for message in range(len(messages)):
        if messages[message][1] > 0:  # if t > 0 then
            if messages[message][0].iloc[0] == 'spam':
                acertou += 1
            nSpam += 1
        else:
            if messages[message][0].iloc[0] == 'ham':
                acertou += 1
            nHam += 1

    return acertou, nSpamReais, nHamReais, nSpam, nHam, nMails


if __name__ == '__main__':
    nMailsTreino, nSpamTreino, nHamTreino, b = training("spamTraining.csv", 1)
    acertou, nSpamReais, nHamReais, nSpam, nHam, nMails = classify(
        "spamTest.csv", b)
    print("--Naive Bayes--")
    print("\n--Processo de Treino--")
    print("Número de mails lidos: {}".format(nMailsTreino))
    print("Número de mails que são spam: {}".format(nSpamTreino))
    print("Número de mails que são ham: {}".format(nHamTreino))
    print("\n--Processo de Validação--")
    print("Número de mails lidos: {}".format(nMails))
    print("Número de mails reais que são spam: {}".format(nSpamReais))
    print("Número de mails reais que são ham: {}".format(nHamReais))
    print("Número de mails classificados como spam pelo algoritmo: {}".format(nSpam))
    print("Número de mails classificados como ham pelo algoritmo: {}".format(nHam))
    print("Pontaria do algoritmo: {:0.3f}%".format((acertou/nMails) * 100))
