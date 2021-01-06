import csv
import math


def train(filename: str, c):

    num_mails = 0
    num_mails_spam = 0
    num_mails_ham = 0
    mails = []
    with open(filename, newline="") as file:
        csvfile = csv.reader(file)
        csvfile.__next__()                      # salta a primeira linha

        for row in csvfile: # por cada linha do ficheiro
            if row[0] == "ham": # ve se a primeira celula da linha (o csvfile le por celulas e csvs sao separados por virgulas é ham)
                num_mails_ham += 1 # ham mails + 1
            else:
                num_mails_spam += 1 # spam mails + 1
            current_dict = dict()
            for word in row[1].replace('\W', " ").lower().split(): # limpa as palavras individuais

                if word not in saco_palavras: # se a palavra nao está no bag of words
                    saco_palavras.append(word) # agora vai estar
                if word not in current_dict: # se a palavra nao e repetida
                    current_dict[word] = 1 # agora é 1
                else:
                    current_dict[word] += 1 # se a palavra for repetida é +1
            mails.append([row[0], current_dict]) # agora temos mais uma mensagem/mail numa matriz [mails][words por mail]
            num_mails += 1 # numero de mensagens lidas incrementa

    b = math.log(c, 10) + math.log(num_mails_ham, 10) - math.log(num_mails_spam, 10) # formula do b

    global p
    p = [[1] * 2 for i in range(len(saco_palavras))] # matriz 3*n em que n é cada palavra do bag
    spam_words = len(saco_palavras)
    ham_words = spam_words

    for mail in mails: # por cada mail preenchido anteriormente
        if mail[0] == "spam": # se for considerado spam
            for word in mail[1]: # cada palavra desse mail
                p[saco_palavras.index(word)][0] += mail[1].get(word)  #ele fica com as palavras do mail no index 0 da matriz p[mail][0] ou seja spam
                spam_words += mail[1].get(word) # o numero de spam words aumenta
        else:
            for word in mail[1]: # cada palavra desse mail
                p[saco_palavras.index(word)][1] += mail[1].get(word) #ele fica com as palavras do mail no index 0 da matriz p[mail][1] ou seja ham
                ham_words += mail[1].get(word) # ham words aumenta

    for j in p: # por cada elemento do p, ou seja mail
        j[0] /= spam_words # https://i.imgur.com/CbkxDB3.png esta parte do pseudocodigo
        j[1] /= ham_words # transforma frequencias absolutas em frequencias relativas

    return b


def classify(documento, b):
    t = -b # mais matematica
    classify_dict = dict()
    for word in documento.replace('\W', " ").lower().split(): # limpar as palavras
        if not classify_dict.get(word): # se a palavra nao estiver repetida
            classify_dict.update({word: 1})
        else: # se a palavra estiver repetida
            classify_dict[word] += 1

    for j in range(len(p)): # agora
        if saco_palavras[j] in classify_dict.keys(): # se as palavras do p anterior (bagofwords) estiverem no novo documento
            t += classify_dict.get(word) * (math.log(p[j][0], 10) - math.log(p[j][1], 10)) # o t irá aumentar segundo esta formula

    if t > 0: # de acordo com o resultado do t
        print("spam")
    else: # magia
        print("ham")


saco_palavras = []
global p
b = train("spam.csv", 1)

classify("Havent planning to buy later. I check already lido only got 530 show in e afternoon. U finish work already?", b)
