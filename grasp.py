import random
def calcularConflitos(solução):
    conflitos = 0
    for i in range(len(solução)):
        for j in range(i+1, len(solução)):
           
            if solução[i] == solução[j]:
                conflitos+=1
            if abs(solução[i] - solução[j]) == abs(i-j):
                conflitos+=1

    return conflitos

def construcao_gulosa_randomizada(tamanho_rcl):
    solução = []
    for coluna in range(8):
        candidatos = []
        for linha in range(8):
            solução_teste = solução + [linha]
            conflitos = calcularConflitos(solução_teste)
            candidatos.append((linha,conflitos))
        candidatos.sort()
        rcl = candidatos[:tamanho_rcl]
        escolhido = random.choice(rcl)
        linha_escolhida = escolhido[0]
        solução.append(linha_escolhida)

    return solução

def gerar_vizinhos(solucao):
    vizinhos = []

    for coluna in range(8):
        linha_atual = solucao[coluna]

        for nova_linha in range(8):

            if nova_linha != linha_atual:
                vizinho = solucao.copy()

                vizinho[coluna] = nova_linha

                vizinhos.append(vizinho)

    return vizinhos

def busca_local_melhor_vizinho(solucao):
    solucao_atual = solucao.copy()

    conflitos_atual = calcularConflitos(solucao_atual)

    melhorou = True

    while melhorou:
        melhorou = False

        melhor_vizinho = solucao_atual
        conflitos_melhor_vizinho = conflitos_atual

        vizinhos = gerar_vizinhos(solucao_atual)

        for vizinho in vizinhos:
            conflitos_vizinho = calcularConflitos(vizinho)

            if conflitos_vizinho < conflitos_melhor_vizinho:
                melhor_vizinho = vizinho
                conflitos_melhor_vizinho = conflitos_vizinho

        if conflitos_melhor_vizinho < conflitos_atual:
            solucao_atual = melhor_vizinho
            conflitos_atual = conflitos_melhor_vizinho
            melhorou = True

    return solucao_atual

def grasp(max_iteracoes, tamanho_rcl):
    melhor_solucao = None

    melhor_conflitos = float("inf")

    iteracao_melhor = 0

    for iteracao in range(1, max_iteracoes + 1):

        solucao_inicial = construcao_gulosa_randomizada(tamanho_rcl)

        solucao_melhorada = busca_local_melhor_vizinho(solucao_inicial)

        conflitos = calcularConflitos(solucao_melhorada)

        if conflitos < melhor_conflitos:
            melhor_solucao = solucao_melhorada
            melhor_conflitos = conflitos
            iteracao_melhor = iteracao

        if melhor_conflitos == 0:
            break

    return melhor_solucao, melhor_conflitos, iteracao_melhor




melhor_solucao, melhor_conflitos, iteracao = grasp(100, 3)

print("Melhor solução:", melhor_solucao)
print("Conflitos:", melhor_conflitos)
print("Iteração da melhor solução:", iteracao)
