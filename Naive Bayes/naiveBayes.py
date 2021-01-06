import pandas as pd
import math

bagOfWords = []

def training(filename, c):
     file = pd.read_csv(filename, encoding = "latin-1", usecols=["v1", "v2"])## importa o data set como um data-frame, usa o latin-1 com decoding para ler o ficheiro e seleciona as colunas v1 e v2 como as unicas a ser usadas (o ficheiro tem mais 3 colunas mas vazias)
     file.columns = ["Status", "Mensagem"]

     nMails = 0
     nSpam = 0
     nHam = 0
     messages = []

     for i in range(file.shape[0]): # por cada linha do ficheiro
          if file.iloc[i, 0] == "spam": # compute m || ve se a primeira celula da linha é spam
               nSpam += 1 # spam mails + 1
          else:
               nHam += 1 # ham mails + 1
          D = {} # Dictionary D
          message = file['Mensagem'][i].split() # limpa as mensagens individuais por palavras
          for word in message: # compute dictionary D
               if word not in bagOfWords: # se a palavra nao está no bag of words
                    bagOfWords.append(word)  # agora vai estar
               if word not in D: # se a palavra nao e repetida
                    D[word] = 1 # agora é 1
               else:
                    D[word] += 1 # se a palavra for repetida é palavras existentes +1
          messages.append([file.iloc[i], D]) # agora temos mais uma mensagem/mail numa matriz [mails][words por mail]
          nMails += 1 # numero de mensagens lidas incrementa

     b = initializeB(c, nHam, nSpam) # initialize b
     global p
     p = [[1] * 2 for _ in range(len(bagOfWords))] # matriz 3*n em que n é cada palavra do bag
     spamWords = len(bagOfWords)
     hamWords = len(bagOfWords)

     for message in messages: # for i = 1 to m do | por cada mail preenchido anteriormente
          if message[0][0] == "spam": # if y = spam then | se for considerado spam
               for word in message[0][1].split(): # for j = 1 to n do | cada palavra desse mail
                    p[bagOfWords.index(word)][0] += message[1].get(word) # p_0.j <- p_1.j + x_j^i | ele fica com as palavras do mail no index 0 da matriz p[word][0] ou seja a frequencia da palavra ser spam
                    spamWords += message[1].get(word) # w_spam <- w_spam + x_j^i | o numero de spam words aumenta
          if message[0][0] == "ham": # else (nah nah nao vá o diabo tecê-las)
               for word in message[0][1].split(): # for j = 1 to n do | cada palavra desse mail
                    p[bagOfWords.index(word)][1] += message[1].get(word) # p_1.j <- p_1.j + x_j^i | ele fica com as palavras do mail no index 0 da matriz p[word][1] ou seja ham
                    hamWords += message[1].get(word) # w_ham <- w_ham + x_j^i | ham words aumenta

     # normalize counts to yield word probabilities
     for j in p: # for j = 1 to n do | por cada elemento do p, ou seja mail
          j[0] = j[0] / spamWords # p_0.j <- p_0.j/w_spam | transformar frequencias absolutas em frequencias relativas em spam words
          j[1] = j[1] / hamWords # p_1.j <- p_1.j/w_spam | e em ham words

     return b

def initializeB(c, nHam, nSpam):
     return math.log(c, 10) + math.log(nHam, 10) - math.log(nSpam, 10) # YEEHAW MATH

def classify(x, b):
     t = -b # initialize score threshold
     classifyD = {}
     for word in x.replace('\W', " ").lower().split():
          if not classifyD.get(word):
               classifyD.update({word:1})
          else:
               classifyD[word] += 1

     for j in range(len(p)): # for j = 1 to n do
          if bagOfWords[j] in classifyD.keys():
               t += classifyD.get(bagOfWords[j]) * (math.log(p[j][0], 10) - math.log(p[j][1], 10)) # t <- t + x^j(log_p0.j - log_p1.j)

     if t > 0:
          print("this is sparta") # spam
     else:
          print("madness?") # ham

if __name__ == '__main__':
    b = training("../../pythonProject1/Treino.csv", 1)
    classify("i like big butts and i cannot lie you other brothers can't deny", b)

