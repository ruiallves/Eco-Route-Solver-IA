from Model.Veiculo import Carro, Mota, Bicicleta
from View.Menus import *
from Model.Estafeta import *
import random

def criar_frota(tipo, qtd, frota, estafetas):
    if tipo == "Carro":
        for i in range(qtd):
            v = Carro()
            frota.append(v)
            v.set_estafeta(gera_random_estafeta(v, estafetas))

    elif tipo == "Mota":
        for i in range(qtd):
            v = Mota()
            frota.append(v)
            v.set_estafeta(gera_random_estafeta(v, estafetas))

    elif tipo == "Bicicleta":
        for i in range(qtd):
            v = Bicicleta()
            frota.append(v)
            v.set_estafeta(gera_random_estafeta(v, estafetas))


def adicionar_frota_ui(frota,estafetas):
    spacer()
    tipo = ""
    quantidade = 0

    while tipo != "Carro" and tipo != "Mota" and tipo != "Bicicleta":
        print("Que Tipo de Veiculo quer adicionar?")
        tipo = input()
        tipo = tipo.lower()
        tipo = tipo.capitalize()

    try:
        print("Quantos Veiculos deste tipo deseja adicionar?")
        quantidade = int(input())
    except ValueError:
        print("Input inválido. Adição de Veiculo cancelada, Voltando ao menu principal")
        siga()
        input()

    criar_frota(tipo, quantidade, frota, estafetas)
    print("Sucesso!")
    print(f"Foram criadas {quantidade} {tipo}"f"s")
    siga()
    input()


def remover_frota(frota):
    for v in frota:
        v.display()
    print("Qual o Id a remover?")
    id_rem = int(input())
    i = 0
    for v in frota:
        if v.get_last_id() == id_rem:
            frota = frota.pop(i)
        i += 1


def sys_default_frota(frota, estafetas):
    criar_frota("Carro", 1, frota, estafetas)
    criar_frota("Mota", 2, frota, estafetas)
    criar_frota("Bicicleta", 3, frota, estafetas)


def organiza_frota(frota):
    frota_bicicleta = []
    frota_mota = []
    frota_carro = []

    for f in frota:
        if isinstance(f, Bicicleta):
            frota_bicicleta.append(f)
        elif isinstance(f, Mota):
            frota_mota.append(f)
        elif isinstance(f, Carro):
            frota_carro.append(f)

    frota.clear()
    frota.extend(frota_bicicleta)
    frota.extend(frota_mota)
    frota.extend(frota_carro)


def gera_random_estafeta(veiculo, estafetas):
    id = len(estafetas) + 1
    idade = random.randint(18, 65)
    peso = random.randint(50, 150)
    ranking = 5

    estafeta = Estafeta(id, idade, peso, ranking, veiculo)
    estafetas.append(estafeta)

    return estafeta
