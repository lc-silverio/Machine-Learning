import pandas
import random

def sliceydicey():
    mails = pandas.read_csv('Naive Bayes/spam.csv', encoding='latin-1')
    mails = mails.sample(frac=1, random_state=random.randint(1, 100))
    trainingMails = mails[:int(len(mails) * 0.70)].reset_index(drop=True)
    buffer = mails[int(len(mails) * 0.70):].reset_index(drop=True)
    buffer = buffer.sample(frac=1, random_state=random.randint(1, 100))
    testingMails = buffer[:int(len(buffer) * 0.50)].reset_index(drop=True)
    verificationMails = buffer[int(len(buffer) * 0.50):].reset_index(drop=True)
    trainingMails.to_csv(r'spamTraining.csv', index=False, header=True)
    testingMails.to_csv(r'spamTest.csv', index=False, header=True)
    verificationMails.to_csv(r'spamVerify.csv', index=False, header=True)

if __name__ == '__main__':
    sliceydicey()
