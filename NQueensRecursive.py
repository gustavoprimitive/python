def permute(col):
    #Si se han procesado todas las posiciones del vector resultado (0->n-1), se pinta el mismo
    if col == n:
        paintResult()
    else:
        #Recorrido de posiciones posibles de fila para cada columna
        for row in range(n):
            #Si no hay conflicto con otras reinas
            if check(col, row):
                #Se guarda en el vector resultado la posición de la fila para la reina
                result[col] = row
                #Recursividad: se validan todos los valores de fila candidatos a reina por cada columna
                permute(col + 1)

def check(col, row):
    #Recorrido de las posiciones anteriores de columna en que existe reina
    for c in range(col):
        #Validación de conlficto con otra reina:
        #1.- De fila y columna
        #2.- De diagonal descendente
        #3.- De diagonal ascendente
        if result[c] == row or result[c] - c == row - col or result[c] + c == row + col:
            return False
    return True

def paintResult():
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
result = [0] * n

permute(0)