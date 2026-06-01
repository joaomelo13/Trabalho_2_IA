import random

def calcular_conflitos(solução):
    conflitos = 0
    for i in range(len(solução)):
        for j in range(i+1, len(solução)):
           
            if solução[i] == solução[j]:
                conflitos+=1
            if abs(solução[i] - solução[j]) == abs(i-j):
                conflitos+=1

    return conflitos

def criar_individuo():
    individuo = []

    for i in range(24):
        bit = random.randint(0, 1)
        individuo.append(bit)

    return individuo

def criar_populacao(tamanho_populacao):
    populacao = []

    for i in range(tamanho_populacao):
        individuo = criar_individuo()
        populacao.append(individuo)

    return populacao

def binario_para_vetor(individuo):
    solucao = []

    for i in range(0, 24, 3):
        grupo_bits = individuo[i:i+3]

        valor = grupo_bits[0] * 4 + grupo_bits[1] * 2 + grupo_bits[2] * 1

        solucao.append(valor)

    return solucao

def calcular_fitness(individuo):
    solucao = binario_para_vetor(individuo)

    conflitos = calcular_conflitos(solucao)

    fitness = 1 / (1 + conflitos)

    return fitness

def selecao_roleta(populacao):
    soma_fitness = 0

    for individuo in populacao:
        soma_fitness += calcular_fitness(individuo)

    ponto_sorteado = random.uniform(0, soma_fitness)

    acumulado = 0

    for individuo in populacao:
        acumulado += calcular_fitness(individuo)

        if acumulado >= ponto_sorteado:
            return individuo
        
def cruzamento(pai1, pai2, taxa_cruzamento):
    if random.random() < taxa_cruzamento:
        ponto_corte = random.randint(1, 23)

        filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
        filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]

        return filho1, filho2

    else:
        return pai1.copy(), pai2.copy()

def mutacao(individuo, taxa_mutacao):
    novo_individuo = individuo.copy()

    for i in range(len(novo_individuo)):
        if random.random() < taxa_mutacao:

            if novo_individuo[i] == 0:
                novo_individuo[i] = 1
            else:
                novo_individuo[i] = 0

    return novo_individuo

def melhor_individuo(populacao):
    melhor = populacao[0]
    melhor_fitness = calcular_fitness(melhor)

    for individuo in populacao:
        fitness = calcular_fitness(individuo)

        if fitness > melhor_fitness:
            melhor = individuo
            melhor_fitness = fitness

    return melhor

def ordenar_por_fitness(populacao):
    return sorted(populacao, key=calcular_fitness, reverse=True)

def algoritmo_genetico():
    tamanho_populacao = 20
    taxa_cruzamento = 0.80
    taxa_mutacao = 0.03
    max_geracoes = 1000
    quantidade_elite = 2

    populacao = criar_populacao(tamanho_populacao)

    melhor_global = melhor_individuo(populacao)

    for geracao in range(1, max_geracoes + 1):

        populacao_ordenada = ordenar_por_fitness(populacao)

        melhor_atual = populacao_ordenada[0]

        if calcular_fitness(melhor_atual) > calcular_fitness(melhor_global):
            melhor_global = melhor_atual

        solucao_melhor = binario_para_vetor(melhor_global)
        conflitos_melhor = calcular_conflitos(solucao_melhor)

        if conflitos_melhor == 0:
            return melhor_global, solucao_melhor, conflitos_melhor, geracao

        nova_populacao = []

        for i in range(quantidade_elite):
            nova_populacao.append(populacao_ordenada[i])

        while len(nova_populacao) < tamanho_populacao:

            pai1 = selecao_roleta(populacao)
            pai2 = selecao_roleta(populacao)

            filho1, filho2 = cruzamento(pai1, pai2, taxa_cruzamento)

            filho1 = mutacao(filho1, taxa_mutacao)
            filho2 = mutacao(filho2, taxa_mutacao)

            nova_populacao.append(filho1)

            if len(nova_populacao) < tamanho_populacao:
                nova_populacao.append(filho2)

        populacao = nova_populacao

    solucao_melhor = binario_para_vetor(melhor_global)
    conflitos_melhor = calcular_conflitos(solucao_melhor)

    return melhor_global, solucao_melhor, conflitos_melhor, max_geracoes

melhor_ind, melhor_solucao, conflitos, geracao = algoritmo_genetico()

print("Melhor indivíduo binário:", melhor_ind)
print("Melhor solução:", melhor_solucao)
print("Conflitos:", conflitos)
print("Parou na geração:", geracao)