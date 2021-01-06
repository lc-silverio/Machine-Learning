board = [[0 for i in range(9)] for j in range(9)]  # o board contém 9 regiões
regioes = [[{1, 2, 3, 4, 5, 6, 7, 8, 9} for i in range(9)] for j in
           range(9)]  # as regiões contém 9 células que vão de 1 a 9
neighbours = {}  # vai ser inicializado depois, cada célula vai ter uma lista de neighbours (referir a: initializeNeighbours)


# é obvio o que isto faz...
def printBoard(board):
    for ri, linha in enumerate(board):
        if ri > 0 and ri % 3 == 0:
            print("\n", end="")
        for rc, num in enumerate(linha):
            if rc > 0 and (rc % 3) == 0:
                print('\t', end='')
            print(num, end=' ')
        print()
    print("\n")


# lê o input.txt e atribui o que l
# a formatação do ficheiro txt é importante
def readFile(txt_file):
    file_buf = open(txt_file, "r")  # opens file
    for i in range(9):
        line = [int(letter) for letter in file_buf.readline().split(' ')]  # splits line characters by delimiter
        for j in range(9):
            num = line[j]
            if num != 0:
                board[i][j] = line[j]
                regioes[i][j] = {line[j]}


# esta função inicializa listas para ser preenchidas com todos os neighbours de cada celula
def initializeNeighbours():
    for linha in range(9):
        for coluna in range(9):
            key = (linha, coluna)
            neighbours[key] = []


# esta funcao arranja o board novo, mas com as restrições já tratadas
def makeNewBoard(board):
    for i in range(9):
        for j in range(9):
            board[i][j] = list(regioes[i][j])[0]


# inicia a fila com as restrições
# basicamente a parte mais complexa da script...
def initializeQueue():
    queue = []
    # esta função verifica se há alguma restrição horizontal
    for linha in range(9):
        for coluna in range(8):
            for k in range(coluna + 1, 9):
                restricao1 = (linha, coluna, linha, k)
                restricao2 = (linha, k, linha, coluna)
                queue.append(restricao1)
                queue.append(restricao2)
                if (linha, k) not in neighbours[(linha, coluna)]:
                    neighbours[(linha, coluna)].append((linha, k))
                if (linha, coluna) not in neighbours[(linha, k)]:
                    neighbours[(linha, k)].append((linha, coluna))

    # e verifica se há alguma restrições a nível vertical
    for coluna in range(9):
        for linha in range(8):
            for k in range(linha + 1, 9):
                restricao1 = (linha, coluna, k, coluna)
                restricao2 = (k, coluna, linha, coluna)
                queue.append(restricao1)
                queue.append(restricao2)
                if (k, coluna) not in neighbours[(linha, coluna)]:
                    neighbours[(linha, coluna)].append((k, coluna))
                if (linha, coluna) not in neighbours[(k, coluna)]:
                    neighbours[(k, coluna)].append((linha, coluna))
    # e por ultimo verifica nas regiões
    for linha in range(3):
        for coluna in range(3):
            for linha2 in range(3):
                for coluna2 in range(3):
                    if linha != linha2 and coluna != coluna2:
                        restricao1 = (linha, coluna, linha2, coluna2)
                        restricao2 = (linha2, coluna2, linha, coluna)
                        # se passou pelas duas de cima e nao passou por esta, vai entrar na fila agora
                        # ou entao se nao houver restricao, entao ta feito
                        for i in range(3):
                            for j in range(3):
                                r1 = linha + 3 * i
                                c1 = coluna + 3 * j
                                r2 = linha2 + 3 * i
                                c2 = coluna2 + 3 * j
                                t = (r1, c1, r2, c2)
                                queue.append(t)
                                queue.append((r2, c2, r1, c1))
                                if (r2, c2) not in neighbours[(r1, c1)]:
                                    neighbours[(r1, c1)].append((r2, c2))
                                if (r1, c1) not in neighbours[(r2, c2)]:
                                    neighbours[(r2, c2)].append((r1, c1))
    queue = list(set(queue))
    return queue


# o incrivel ac3 em toda a sua gloria
def AC3(queue):
    while queue:
        t = queue.pop(0)
        i1, j1, i2, j2 = t
        isRevised = revise(t)
        if isRevised:
            for (ni1, nj1) in neighbours[(i1, j1)]:
                if (ni1, j1) == (i2, j2):
                    continue
                if (ni1, nj1, i1, j1) not in queue:
                    queue.append((ni1, nj1, i1, j1))


def revise(t):
    i1, j1, i2, j2 = t
    regiao1 = regioes[i1][j1]
    regiao2 = regioes[i2][j2]
    for num in regiao1:
        if len(regiao2 - {num}) == 0:
            regioes[i1][j1].remove(num)  # revises regiao
            return True
    return False


# esta funcao só está aqui para organizarmos o processo
# ela sinceramente podia nem existir e isto estar tudo no main
# whatever, assim é mais facil depois se quisermos expandir isto por hobby
def solve(board):
    # printBoard(board) # retorna o sudoku ainda por fazer, é so uma picuisse para testar se estava a ler bem
    initializeNeighbours()
    queue = initializeQueue()
    AC3(queue)
    makeNewBoard(board)
    printBoard(board)


# main
# retorna o sudoku já feito imprimido numa formatacao legivel por humanos
if __name__ == "__main__":
    readFile("input.txt")
    solve(board)
