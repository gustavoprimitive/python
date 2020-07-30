def permute(seed):
    result = [[]]
    for i in range(len(seed)):
        result = [[a] + b for a in seed for b in result if a not in b]
    return result

def check(col, row, seed):
    #Recorrido de las posiciones anteriores de columna en que existe reina
    for c in range(col):
        #Validación de conlficto con otra reina:
        #1.- De fila y columna
        #2.- De diagonal descendente
        #3.- De diagonal ascendente
        if seed[c] == row or seed[c] - c == row - col or seed[c] + c == row + col:
            return False
    return True

def loopSeed(seed):
    for s in permute(seed):
        ok = 0
        for index, value in enumerate(s):
            if check(index, value, s):
                ok += 1
        if ok == n:
            paintResult(s)

def paintResult(result):
    global resultNum
    resultNum = resultNum + 1
    print("\nResult #" + str(resultNum))
    for i in result:
        row = ""
        for j in range(n):
            if j == i:
                row = row + " 1 "
            else:
                row = row + " 0 "
        print(row)

n = 8
resultNum = 0

seed = []
for i in range(0, n):
    seed.append(i)

loopSeed(seed)