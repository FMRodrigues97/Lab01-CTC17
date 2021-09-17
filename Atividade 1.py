# %%
# Importação de Biblioteca
import math
import os

import numpy
import pandas as pd
from geopy import distance

# Carregamento da base de dados
curr_path = os.path.dirname(os.path.abspath(__file__))
aus = pd.read_csv(os.path.join(curr_path, "australia.csv"))


# Criação do DB com os IDs dos vizinhos para cada cidade
def nid_db(ctr):
    max_row = len(ctr.index)
    neigh = numpy.zeros((max_row, 4), dtype=int)

    for id_city in ctr['id']:
        neigh[id_city - 1][0] = id_city

        if id_city % 2 == 0:  # ID par
            if id_city - 2 >= 1:
                neigh[id_city - 1][1] = id_city - 2
            if id_city - 1 >= 1:
                neigh[id_city - 1][2] = id_city - 1
            if id_city + 2 <= max_row:
                neigh[id_city - 1][3] = id_city + 2

        else:  # ID ímpar
            if id_city - 2 >= 1:
                neigh[id_city - 1][1] = id_city - 2
            if id_city + 1 <= max_row:
                neigh[id_city - 1][2] = id_city + 1
            if id_city + 2 <= max_row:
                neigh[id_city - 1][3] = id_city + 2

    neigh = pd.DataFrame(neigh, columns=['ID', 'Neighbor 1', 'Neighbor 2', 'Neighbor 3'])

    return neigh


# Criação do DB com as distâncias aos vizinhos para cada cidade
def ndist_db(ctr, id_db):
    max_row = len(ctr.index)
    dist = numpy.zeros((max_row, 4), dtype=float)

    for id_orig in ctr['id']:
        dist[id_orig - 1][0] = id_orig

        for i in range(1, 4):
            id_neigh = int(id_db[id_db['ID'] == id_orig]['Neighbor ' + str(i)])
            if id_neigh != 0:
                dist[id_orig - 1][i] = dist_cty(id_orig, id_neigh, ctr) * 1.1

    dist = pd.DataFrame(dist, columns=['ID', 'Neighbor 1', 'Neighbor 2', 'Neighbor 3'])

    return dist


# Calculadora de distância
def dist_cty(id_orig, id_fin, ctr):
    return float(distance.distance((float(ctr[ctr['id'] == id_orig]['lat']), float(ctr[ctr['id'] == id_orig]['lng'])),
                                   (float(ctr[ctr['id'] == id_fin]['lat']), float(ctr[ctr['id'] == id_fin]['lng']))).km)


# %%
# Função para encontrar um caminho dado uma Cidade Original até uma Cidade Final
# Passa-se, além dos banco de dados, o peso acumulado e o caminho já percorrido
def path_finder(dist_db, id_db, ctr, ini, fin, weight, path):
    path = [elem for elem in path]
    poss = []
    path_anl = []
    idx_aval = []
    no_go = []
    dist = 0

    # Até encontrar um caminho
    cty_org = ini
    cty_fin = fin
    curr = cty_org
    while curr != cty_fin:
        id_ch = 0
        wg_ch = math.inf
        arr_dist = dist_db.loc[dist_db.ID == curr].values.flatten().tolist()[1:]
        arr_id = id_db.loc[id_db.ID == curr].values.flatten().tolist()[1:]
        if (curr not in path):  # Checa se já não está no caminho
            path.append(curr)
        for i in range(1, 4):  # Escolhe o de menor falor f(n)
            if (arr_id[i - 1] > 0):
                dist_analy = weight + arr_dist[i - 1] + dist_cty(arr_id[i - 1], cty_fin, ctr)
                if (wg_ch > dist_analy and arr_id[i - 1] > 0 and (arr_id[i - 1] not in path) and arr_id[
                    i - 1] not in no_go):
                    dlock = True
                    for elem in id_db.loc[id_db.ID == arr_id[i - 1]].values.flatten().tolist()[1:]:
                        if elem not in path:
                            dlock = False
                    if (dlock == False):
                        id_ch = arr_id[i - 1]
                        wg_ch = dist + arr_dist[i - 1] + dist_cty(arr_id[i - 1], cty_fin, ctr)
        if (id_ch != 0):  # Se escolheu alguma cidade
            curr = id_ch
            aux = [elem for elem in path]
            for i in range(1, 4):
                if (id_ch != arr_id[i - 1] and arr_id[i - 1] > 0 and arr_id[i - 1] not in path):
                    # Passase-se as info de caminho até a cidade, a cidade, f(cidade) e peso acumulado da cidade
                    poss.append([aux, arr_id[i - 1], dist + arr_dist[i - 1] + dist_cty(arr_id[i - 1], cty_fin, ctr),
                                 dist + arr_dist[i - 1]])
            dist = 0
            for i in range(len(path) - 1):
                dist = dist + dist_cty(path[i], path[i + 1], ctr)
        else:  # Se não escolheu alguma cidade, checou num fim de linha. Volta o path e continua o processo
            path = path[0:-1]
            dist = 0
            for i in range(len(path) - 1):
                dist = dist + dist_cty(path[i], path[i + 1], ctr)
            no_go.append(curr)
            aux = [elem for elem in no_go]
            for i in range(len(aux) - 1):
                stay = True
                for elem in id_db.loc[id_db.ID == curr].values.flatten().tolist()[1:]:
                    if (elem not in path and elem not in no_go and elem > 0):
                        stay = False
                if (stay == False):
                    no_go.remove(aux[i])
            curr = path[-1]

    path.append(cty_fin)

    # Calculo do peso acumulado
    dist = 0
    for i in range(len(path) - 1):
        dist = dist + dist_cty(path[i], path[i + 1], ctr)
    weight = weight + dist

    # Verifica todos os outros caminhos possíveis
    for i in range(len(poss)):
        if (poss[i][2] < weight):
            idx_aval.append(i)
    for i in idx_aval:
        path_anl.append(poss[i])

    return path, path_anl, weight


# Analisa se o caminho passado consegue chegar na Cidade Final com o peso acumulado menor que o passado
def path_analyser(weight, dist_db, id_db, ctr, ini, fin, wg_ch):
    cty_org = ini
    cty_fin = fin
    path_aux = []
    no_go_aux = []
    dist = 0

    # Checa se consegue
    curr = cty_org
    path_aux.append(curr)
    while curr != cty_fin and weight - wg_ch > dist:
        id_ch = 0
        aux = math.inf
        arr_dist = dist_db.loc[dist_db.ID == curr].values.flatten().tolist()[1:]
        arr_id = id_db.loc[id_db.ID == curr].values.flatten().tolist()[1:]
        if (curr not in path_aux):
            path_aux.append(curr)
        for i in range(1, 4):  # Escolhe entre os vizinhos
            if (arr_id[i - 1] > 0):
                if (aux > wg_ch + arr_dist[i - 1] + dist_cty(arr_id[i - 1], cty_fin, ctr) and arr_id[
                    i - 1] not in path_aux and arr_id[i - 1] not in no_go_aux):
                    id_ch = arr_id[i - 1]
                    aux = dist + arr_dist[i - 1] + dist_cty(arr_id[i - 1], cty_fin, ctr)
        if (id_ch != 0):  # Se conseguiu escolher
            curr = id_ch
            dist = 0
            for i in range(len(path_aux) - 1):
                dist = dist + dist_cty(path_aux[i], path_aux[i + 1], ctr)
        else:  # Caso não conseguiu, chegou num fim de linha, volta o path e continua
            path_aux = path_aux[0:-1]
            dist = 0
            for i in range(len(path_aux) - 1):
                dist = dist + dist_cty(path_aux[i], path_aux[i + 1], ctr)
            no_go_aux.append(curr)
            aux = [elem for elem in no_go_aux]
            for i in range(len(aux) - 1):
                stay = True
                for elem in id_db.loc[id_db.ID == curr].values.flatten().tolist()[1:]:
                    if (elem not in path_aux and elem not in no_go_aux and elem > 0):
                        stay = False
                if (stay == False):
                    no_go_aux.remove(aux[i])
            curr = path_aux[-1]

    # Calculo do peso acumulado
    dist = 0
    for i in range(len(path_aux) - 1):
        dist = dist + dist_cty(path_aux[i], path_aux[i + 1], ctr)
    wg_ch = wg_ch + dist

    # Se chegou na Cidade Final com um peso acumulado menor, então retorna True
    if (curr == cty_fin):
        if (wg_ch < weight):
            return True
    return False


# Algoritmo de Busca A*
def a_algo(dist_db, id_db, ctr, ini, fin):
    cty_org = ini
    cty_fin = fin

    # Faz-se a primeira busca (Etapa 1)
    p_algo, p_anl_algo, w_algo = path_finder(dist_db, id_db, ctr, cty_org, cty_fin, 0, [])

    # Da primeira busca, analisa os caminhos possíveis (Etapa 2)
    find = False
    aux = [elem for elem in p_anl_algo]
    for i in range(len(aux) - 1, -1, -1):
        if (path_analyser(w_algo, dist_db, id_db, ctr, aux[i][1], fin, aux[i][3])):
            idx = i
            find = True
        else:
            p_anl_algo.remove(aux[i])

            # Caso tenha caminho possível, prossiga até continuar tendo melhoras possíveis (Etapa 3)
    while find:
        # Novas condições iniciais
        cty_org = aux[idx][1]
        p_algo = aux[idx][0]
        wg_ch = aux[idx][3]
        p_anl_algo.remove(aux[idx])

        # Novo caminho, novos possíveis caminhos e novo peso
        p_algo, p_anl_algo_aux, w_algo = path_finder(dist_db, id_db, ctr, cty_org, cty_fin, wg_ch, p_algo)

        # Atualiza os novos possíveis caminhos de acordo com o novo peso
        aux = [elem for elem in p_anl_algo_aux]
        for i in range(len(aux) - 1, -1, -1):
            if (w_algo < aux[i][2]):
                p_anl_algo_aux.remove(aux[i])
        aux = [elem for elem in p_anl_algo]
        for i in range(len(aux) - 1, -1, -1):
            if (w_algo < aux[i][2]):
                p_anl_algo.remove(aux[i])
        p_anl_algo = p_anl_algo + p_anl_algo_aux

        # Análise dos caminhos possíveis, caso tenha caminho de fato possível, find fica True e continua processo
        aux = [elem for elem in p_anl_algo]
        for i in range(len(aux) - 1, -1, -1):
            if path_analyser(w_algo, dist_db, id_db, ctr, aux[i][1], fin, aux[i][3]):
                find = True
                idx = i
            else:
                p_anl_algo.remove(aux[i])
        if (len(p_anl_algo) == 0):  # Continua até não ter mais caminhos possíveis
            find = False
    print("Feito")
    return p_algo, w_algo


neigh_id = nid_db(aus)
neigh_dist = ndist_db(aus, neigh_id)
p, w = a_algo(neigh_dist, neigh_id, aus, 5, 219)

# %%
dist = 0
for i in range(len(p) - 1):
    dist = dist + neigh_dist.loc[neigh_dist.ID == p[i]].values.flatten().tolist()[1:][
        neigh_id.loc[neigh_id.ID == p[i]].values.flatten().tolist()[1:].index(p[i + 1])]
print(dist)

# %%
# %%
dist = 0
for i in range(len(p) - 1):
    dist = dist + dist_cty(p[i], p[i + 1], aus)
dist
# %%
