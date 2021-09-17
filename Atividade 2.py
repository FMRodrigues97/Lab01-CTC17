import numpy

tabuleiro = numpy.zeros((7, 7), dtype=str)

'''
    LEGENDA
    0, 1, 2, 3, 4: Quantidade de lâmpadas adjacentes
    L: lâmpada
    I: iluminado
    P: preto
    X: proibido
    '': Não Iluminada
'''

'''
# JOGO 1: https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html#7x7:dBiBb4e4aBeBb3i0d
tabuleiro[0][4] = 'P'
tabuleiro[2][0] = 'P'
tabuleiro[2][3] = '4'
tabuleiro[3][2] = '4'
tabuleiro[3][4] = 'P'
tabuleiro[4][3] = 'P'
tabuleiro[4][6] = '3'
tabuleiro[6][2] = '0'
'''

'''
# JOGO 2: https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html#7x7:d1c1aBaBa1g1c1gBa4aBa2c3d
tabuleiro[0][4] = '1'
tabuleiro[1][1] = '1'
tabuleiro[1][3] = 'P'
tabuleiro[1][5] = 'P'
tabuleiro[2][0] = '1'
tabuleiro[3][1] = '1'
tabuleiro[3][5] = '1'
tabuleiro[4][6] = 'P'
tabuleiro[5][1] = '4'
tabuleiro[5][3] = 'P'
tabuleiro[5][5] = '2'
tabuleiro[6][2] = '3'
'''

'''
# JOGO 3: https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html#7x7:c1lBa3bBe1b2a0l2c
tabuleiro[0][3] = '1'
tabuleiro[2][2] = 'P'
tabuleiro[2][4] = '3'
tabuleiro[3][0] = 'P'
tabuleiro[3][6] = '1'
tabuleiro[4][2] = '2'
tabuleiro[4][4] = '0'
tabuleiro[6][3] = '2'
'''

'''
# JOGO 4: https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html#7x7:b2h0c3a2bBbBaBb1bBa3c1hBb
tabuleiro[0][2] = '2'
tabuleiro[1][4] = '0'
tabuleiro[2][1] = '3'
tabuleiro[2][3] = '2'
tabuleiro[2][6] = 'P'
tabuleiro[3][2] = 'P'
tabuleiro[3][4] = 'P'
tabuleiro[4][0] = '1'
tabuleiro[4][3] = 'P'
tabuleiro[4][5] = '3'
tabuleiro[5][2] = '1'
tabuleiro[6][4] = 'P'
'''

# '''
# JOGO 5: https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/lightup.html#7x7:b1b1aBhBa1a1g0a0a0hBaBb0b
tabuleiro[0][2] = '1'
tabuleiro[0][5] = '1'
tabuleiro[1][0] = 'P'
tabuleiro[2][2] = 'P'
tabuleiro[2][4] = '1'
tabuleiro[2][6] = '1'
tabuleiro[4][0] = '0'
tabuleiro[4][2] = '0'
tabuleiro[4][4] = '0'
tabuleiro[5][6] = 'P'
tabuleiro[6][1] = 'P'
tabuleiro[6][4] = '0'
# '''

print('')
print(tabuleiro)
print('')


def iluminar(board):
    for line in range(0, 7):
        for column in range(0, 7):
            if board[line][column] == 'L':

                j = column
                # Iluminar linha à esquerda
                while j > 0 and (board[line][j - 1] == '' or board[line][j - 1] == 'I' or board[line][j - 1] == 'X'):
                    board[line][j - 1] = 'I'
                    j = j - 1

                j = column
                # Iluminar linha à direita
                while j < 6 and (board[line][j + 1] == '' or board[line][j + 1] == 'I' or board[line][j + 1] == 'X'):
                    board[line][j + 1] = 'I'
                    j = j + 1

                i = line
                # Iluminar coluna acima
                while i > 0 and (
                        board[i - 1][column] == '' or board[i - 1][column] == 'I' or board[i - 1][column] == 'X'):
                    board[i - 1][column] = 'I'
                    i = i - 1

                i = line
                # Iluminar coluna abaixo
                while i < 6 and (
                        board[i + 1][column] == '' or board[i + 1][column] == 'I' or board[i + 1][column] == 'X'):
                    board[i + 1][column] = 'I'
                    i = i + 1

    return board


def vazios_e_lampadas(line, column, board):
    vazios_vizinhos = 0
    lampadas_vizinhas = 0

    if line + 1 <= 6 and board[line + 1][column] == '':
        vazios_vizinhos += 1
    if column + 1 <= 6 and board[line][column + 1] == '':
        vazios_vizinhos += 1
    if line >= 1 and board[line - 1][column] == '':
        vazios_vizinhos += 1
    if column >= 1 and board[line][column - 1] == '':
        vazios_vizinhos += 1

    if line + 1 <= 6 and board[line + 1][column] == 'L':
        lampadas_vizinhas += 1
    if column + 1 <= 6 and board[line][column + 1] == 'L':
        lampadas_vizinhas += 1
    if line >= 1 and board[line - 1][column] == 'L':
        lampadas_vizinhas += 1
    if column >= 1 and board[line][column - 1] == 'L':
        lampadas_vizinhas += 1

    return vazios_vizinhos, lampadas_vizinhas


def preenchimento_adjacencias(number, board):
    mudou = False
    for linha in range(0, 7):
        for coluna in range(0, 7):
            [v, l] = vazios_e_lampadas(linha, coluna, board)
            if board[linha][coluna] == number and v == int(tabuleiro[linha][coluna]) - l:
                if linha + 1 < 7 and tabuleiro[linha + 1][coluna] == '':
                    board[linha + 1][coluna] = 'L'
                    mudou = True
                if coluna + 1 < 7 and tabuleiro[linha][coluna + 1] == '':
                    board[linha][coluna + 1] = 'L'
                    mudou = True
                if linha - 1 >= 0 and tabuleiro[linha - 1][coluna] == '':
                    board[linha - 1][coluna] = 'L'
                    mudou = True
                if coluna - 1 >= 0 and tabuleiro[linha][coluna - 1] == '':
                    board[linha][coluna - 1] = 'L'
                    mudou = True
                board = iluminar(board)
    return board, mudou


def preenchimento(board):
    mudou1 = True
    mudou2 = True
    mudou3 = True
    mudou4 = True
    while mudou1 or mudou2 or mudou3 or mudou4:
        [board, mudou1] = preenchimento_adjacencias('4', board)
        [board, mudou2] = preenchimento_adjacencias('3', board)
        [board, mudou3] = preenchimento_adjacencias('2', board)
        [board, mudou4] = preenchimento_adjacencias('1', board)
    return board


def bloqueios(board):
    for linha in range(0, 7):
        for coluna in range(0, 7):
            # [viz, lamp] = vazios_e_lampadas(linha, coluna, board)
            lamp = vazios_e_lampadas(linha, coluna, board)[1]

            if board[linha][coluna] == '0':
                if linha + 1 < 7 and board[linha + 1][coluna] == '':
                    board[linha + 1][coluna] = 'X'
                if coluna + 1 < 7 and board[linha][coluna + 1] == '':
                    board[linha][coluna + 1] = 'X'
                if linha - 1 >= 0 and board[linha - 1][coluna] == '':
                    board[linha - 1][coluna] = 'X'
                if coluna - 1 >= 0 and board[linha][coluna - 1] == '':
                    board[linha][coluna - 1] = 'X'

            if board[linha][coluna] == '1' and lamp == 1:
                if linha + 1 < 7 and board[linha + 1][coluna] == '':
                    board[linha + 1][coluna] = 'X'
                if coluna + 1 < 7 and board[linha][coluna + 1] == '':
                    board[linha][coluna + 1] = 'X'
                if linha - 1 >= 0 and board[linha - 1][coluna] == '':
                    board[linha - 1][coluna] = 'X'
                if coluna - 1 >= 0 and board[linha][coluna - 1] == '':
                    board[linha][coluna - 1] = 'X'

            if board[linha][coluna] == '2' and lamp == 2:
                if linha + 1 < 7 and board[linha + 1][coluna] == '':
                    board[linha + 1][coluna] = 'X'
                if coluna + 1 < 7 and board[linha][coluna + 1] == '':
                    board[linha][coluna + 1] = 'X'
                if linha - 1 >= 0 and board[linha - 1][coluna] == '':
                    board[linha - 1][coluna] = 'X'
                if coluna - 1 >= 0 and board[linha][coluna - 1] == '':
                    board[linha][coluna - 1] = 'X'

            if board[linha][coluna] == '3' and lamp == 3:
                if linha + 1 < 7 and board[linha + 1][coluna] == '':
                    board[linha + 1][coluna] = 'X'
                if coluna + 1 < 7 and board[linha][coluna + 1] == '':
                    board[linha][coluna + 1] = 'X'
                if linha - 1 >= 0 and board[linha - 1][coluna] == '':
                    board[linha - 1][coluna] = 'X'
                if coluna - 1 >= 0 and board[linha][coluna - 1] == '':
                    board[linha][coluna - 1] = 'X'
    return board


# Analisar casas bloqueadas (marcadas com X)
def possibilidades_bloqueados(board):
    for linha in range(0, 7):
        for coluna in range(0, 7):
            if board[linha][coluna] == 'X':
                possibilidades = 0

                j = coluna
                # Buscar possibilidades na linha à esquerda
                while j > 0 and (board[linha][j - 1] == '' or board[linha][j - 1] == 'I' or board[linha][j - 1] == 'X'):
                    if board[linha][j - 1] == '':
                        possibilidades += 1
                        x = linha
                        y = j - 1
                    j = j - 1

                j = coluna
                # Buscar possibilidades na linha à direita
                while j < 6 and (board[linha][j + 1] == '' or board[linha][j + 1] == 'I' or board[linha][j + 1] == 'X'):
                    if board[linha][j + 1] == '':
                        possibilidades += 1
                        x = linha
                        y = j + 1
                    j = j + 1

                i = linha
                # Buscar possibilidades coluna acima
                while i > 0 and (
                        board[i - 1][coluna] == '' or board[i - 1][coluna] == 'I' or board[i - 1][coluna] == 'X'):
                    if board[i - 1][coluna] == '':
                        possibilidades += 1
                        x = i - 1
                        y = coluna
                    i = i - 1

                i = linha
                # Buscar possibilidades coluna abaixo
                while i < 6 and (
                        board[i + 1][coluna] == '' or board[i + 1][coluna] == 'I' or board[i + 1][coluna] == 'X'):
                    if board[i + 1][coluna] == '':
                        possibilidades += 1
                        x = i + 1
                        y = coluna
                    i = i + 1

                # Se houver só uma possibilidade, a lâmpada será colocada lá e X->I
                if possibilidades == 1:
                    board[x][y] = 'L'
                    board[linha][coluna] = 'I'
                    board = iluminar(board)

    return board


def finalizacao(board):
    for linha in range(0, 7):
        for coluna in range(0, 7):
            if board[linha][coluna] == '' or board[linha][coluna] == 'X':
                possibilidades = 0

                j = coluna
                # Buscar possibilidades na linha à esquerda
                while j > 0 and (board[linha][j - 1] == '' or board[linha][j - 1] == 'I' or board[linha][j - 1] == 'X'):
                    if board[linha][j - 1] == '':
                        possibilidades += 1
                        x = linha
                        y = j - 1
                    j = j - 1

                j = coluna
                # Buscar possibilidades na linha à direita
                while j < 6 and (board[linha][j + 1] == '' or board[linha][j + 1] == 'I' or board[linha][j + 1] == 'X'):
                    if board[linha][j + 1] == '':
                        possibilidades += 1
                        x = linha
                        y = j + 1
                    j = j + 1

                i = linha
                # Buscar possibilidades coluna acima
                while i > 0 and (
                        board[i - 1][coluna] == '' or board[i - 1][coluna] == 'I' or board[i - 1][coluna] == 'X'):
                    if board[i - 1][coluna] == '':
                        possibilidades += 1
                        x = i - 1
                        y = coluna
                    i = i - 1

                i = linha
                # Buscar possibilidades coluna abaixo
                while i < 6 and (
                        board[i + 1][coluna] == '' or board[i + 1][coluna] == 'I' or board[i + 1][coluna] == 'X'):
                    if board[i + 1][coluna] == '':
                        possibilidades += 1
                        x = i + 1
                        y = coluna
                    i = i + 1

                # Se houver só uma possibilidade, a lâmpada será colocada lá e X->I
                if board[linha][coluna] == 'X' and possibilidades == 1:
                    board[x][y] = 'L'
                    board[linha][coluna] = 'I'
                    board = iluminar(board)

                # Se não hoverem possibilidades, a lâmpada só pode estar lá
                if board[linha][coluna] == '' and possibilidades == 0:
                    board[linha][coluna] = 'L'
                    board = iluminar(board)

    return board


# Verificar se está correto
def is_correct(board):
    correct1 = True
    correct2 = True
    correct3 = True
    correct4 = True
    correct_vazio = True
    correct = False

    casas_vazias = 0

    for line in range(0, 7):
        for column in range(0, 7):
            x = line
            y = column

            if board[line][column] == '4' and vazios_e_lampadas(x, y, board)[1] != 4:
                correct4 = False
            if board[line][column] == '3' and vazios_e_lampadas(x, y, board)[1] != 3:
                correct3 = False
            if board[line][column] == '2' and vazios_e_lampadas(x, y, board)[1] != 2:
                correct2 = False
            if board[line][column] == '1' and vazios_e_lampadas(x, y, board)[1] != 1:
                correct1 = False

            if board[line][column] == '' or board[line][column] == 'X':
                correct_vazio = False
                casas_vazias += 1

    if correct1 and correct2 and correct3 and correct4 and correct_vazio:
        correct = True
        print("COMPLETO e CORRETO")

    else:
        print(f"INCOMPLETO: faltam {casas_vazias} casas")

    return correct


def chute_recursivo(board):
    lista_tabuleiros = [board]
    lista_chute_X = []
    lista_chute_Y = []

    for line in range(0, 7):
        for column in range(0, 7):
            casa = board[line][column]
            if casa in ('1', '2', '3') and vazios_e_lampadas(line, column, board)[1] < int(casa):
                if line - 1 >= 0 and board[line - 1][column] == '':
                    board[line - 1][column] = 'L'
                    board = atualizar_tabuleiro(board)

                    lista_tabuleiros.append(board)
                    lista_chute_X.append(line - 1)
                    lista_chute_Y.append(column)
                    return chute_recursivo(board)

                if column + 1 < 7 and board[line][column + 1] == '':
                    board[line][column + 1] = 'L'
                    board = atualizar_tabuleiro(board)
                    lista_tabuleiros.append(board)
                    lista_chute_X.append(line)
                    lista_chute_Y.append(column + 1)
                    return chute_recursivo(board)

                if line + 1 < 7 and board[line + 1][column] == '':
                    board[line + 1][column] = 'L'
                    board = atualizar_tabuleiro(board)

                    lista_tabuleiros.append(board)
                    lista_chute_X.append(line + 1)
                    lista_chute_Y.append(column)
                    return chute_recursivo(board)

                if column - 1 >= 0 and board[line][column - 1] == '':
                    board[line][column - 1] = 'L'
                    board = atualizar_tabuleiro(board)

                    lista_tabuleiros.append(board)
                    lista_chute_X.append(line)
                    lista_chute_Y.append(column - 1)

                    return chute_recursivo(board)

    board = atualizar_tabuleiro(board)

    return board


def atualizar_tabuleiro(board):
    board = preenchimento(board)
    board = bloqueios(board)
    board = possibilidades_bloqueados(board)

    board = preenchimento(board)
    board = bloqueios(board)
    board = possibilidades_bloqueados(board)

    board = preenchimento(board)
    board = bloqueios(board)
    board = possibilidades_bloqueados(board)

    board = preenchimento(board)
    board = bloqueios(board)
    board = possibilidades_bloqueados(board)

    board = finalizacao(board)

    return board


tabuleiro = atualizar_tabuleiro(tabuleiro)
print(tabuleiro)
print('')

tabuleiro = chute_recursivo(tabuleiro)
print(tabuleiro)
print('')

is_correct(tabuleiro)
