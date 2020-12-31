board = [[0 for i in range(9)] for j in range(9)]
domains = [[{1, 2, 3, 4, 5, 6, 7, 8, 9} for i in range(9)] for j in range(9)]
neighbours = {}


def printBoard(board):
    for ri, row in enumerate(board):
        if ri > 0 and ri % 3 == 0:
            print("\n", end="")
        for rc, num in enumerate(row):
            if rc > 0 and (rc % 3) == 0:
                print('\t', end='')
            print(num, end=' ')
        print()
    print("\n")


def readFile(txt_file):
    file_buf = open(txt_file, "r")  # opens file
    for i in range(9):
        line = [int(letter) for letter in file_buf.readline().split(' ')]  # splits line characters by delimiter
        for j in range(9):
            num = line[j]
            if num != 0:
                board[i][j] = line[j]
                domains[i][j] = {line[j]}


# inserts all keys. values are lists
def initializeNeighbours():
    for row in range(9):
        for col in range(9):
            key = (row, col)
            neighbours[key] = []


def applyDomain(board):
    for i in range(9):
        for j in range(9):
            board[i][j] = list(domains[i][j])[0]


# put all constraints in a queue
def initializeQueue():
    queue = []
    # all horizontal
    for row in range(9):
        for col in range(8):
            for k in range(col + 1, 9):
                constraint1 = (row, col, row, k)
                constraint2 = (row, k, row, col)
                queue.append(constraint1)
                queue.append(constraint2)
                if (row, k) not in neighbours[(row, col)]:
                    neighbours[(row, col)].append((row, k))
                if (row, col) not in neighbours[(row, k)]:
                    neighbours[(row, k)].append((row, col))

    # all vertical
    for col in range(9):
        for row in range(8):
            for k in range(row + 1, 9):
                constraint1 = (row, col, k, col)
                constraint2 = (k, col, row, col)
                queue.append(constraint1)
                queue.append(constraint2)
                if (k, col) not in neighbours[(row, col)]:
                    neighbours[(row, col)].append((k, col))
                if (row, col) not in neighbours[(k, col)]:
                    neighbours[(k, col)].append((row, col))
    # all box
    for row in range(3):
        for col in range(3):
            for row2 in range(3):
                for col2 in range(3):
                    if row != row2 and col != col2:
                        constraint1 = (row, col, row2, col2)
                        constraint2 = (row2, col2, row, col)
                        # if constraint1 not in queue and constraint2 not in queue:
                        for i in range(3):
                            for j in range(3):
                                r1 = row + 3 * i
                                c1 = col + 3 * j
                                r2 = row2 + 3 * i
                                c2 = col2 + 3 * j
                                t = (r1, c1, r2, c2)
                                queue.append(t)
                                queue.append((r2, c2, r1, c1))
                                if (r2, c2) not in neighbours[(r1, c1)]:
                                    neighbours[(r1, c1)].append((r2, c2))
                                if (r1, c1) not in neighbours[(r2, c2)]:
                                    neighbours[(r2, c2)].append((r1, c1))
    queue = list(set(queue))
    return queue


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
    domain1 = domains[i1][j1]
    domain2 = domains[i2][j2]
    for num in domain1:
        if len(domain2 - {num}) == 0:
            domains[i1][j1].remove(num)  # revises domain
            return True
    return False


def solve(board):
    printBoard(board)
    initializeNeighbours()
    queue = initializeQueue()
    AC3(queue)
    applyDomain(board)
    printBoard(board)


if __name__ == "__main__":
    readFile("input.txt")
    solve(board)
