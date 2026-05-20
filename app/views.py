from django.shortcuts import render
from queue import PriorityQueue

# Costos
costos = {

    'Empresa1': {
        'T': 20,
        'H': 30,
        'V': 20,
        'W': 40
    },

    'Empresa2': {
        'T': 50,
        'H': 50,
        'V': 40,
        'W': 50
    },

    'Empresa3': {
        'T': 60,
        'H': 55,
        'V': 50,
        'W': 60
    },

    'Empresa4': {
        'T': 100,
        'H': 80,
        'V': 60,
        'W': 70
    }
}

tipos = ['T', 'H', 'V', 'W']
empresas = list(costos.keys())


def heuristica(asignados, indice_tipo):

    restantes = tipos[indice_tipo:]

    disponibles = [
        e for e in empresas
        if e not in asignados
    ]

    h = 0

    for tipo in restantes:

        minimo = min(
            costos[e][tipo]
            for e in disponibles
        )

        h += minimo

    return h


def a_estrella():

    frontera = PriorityQueue()

    frontera.put((0, 0, []))

    while not frontera.empty():

        f, g, asignacion = frontera.get()

        indice_tipo = len(asignacion)

        if indice_tipo == len(tipos):

            return asignacion, g

        tipo_actual = tipos[indice_tipo]

        for empresa in empresas:

            if empresa not in asignacion:

                nueva_asignacion = (
                    asignacion + [empresa]
                )

                nuevo_g = (
                    g +
                    costos[empresa][tipo_actual]
                )

                nuevo_h = heuristica(
                    nueva_asignacion,
                    indice_tipo + 1
                )

                nuevo_f = nuevo_g + nuevo_h

                frontera.put((
                    nuevo_f,
                    nuevo_g,
                    nueva_asignacion
                ))


def inicio(request):

    solucion, costo_total = a_estrella()

    resultados = []

    for i in range(len(tipos)):

        resultados.append({

            'tipo': tipos[i],
            'empresa': solucion[i]

        })

    return render(request, 'index.html', {

        'resultados': resultados,
        'costo_total': costo_total

    })