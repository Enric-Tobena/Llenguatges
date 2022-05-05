#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

class AFN:
    def __init__(self, AFN):
        self.AFN = AFN
        self.simbolosAlfabeto = self.simbolosLenguaje()

        self.AFD = self.determinizarAFN()

    def estadosIniciales(self):
        # El estado inicial se corresponde con aquel estado cuya tupla tenga el simbolo '->' en la última posición
        estadosIniciales = []

        for estado in self.AFN:
            if estado[-1] == '->':
                estadosIniciales.append(estado)

        return estadosIniciales

    def estadosFinales(self):
        # El estado final se corresponde con aquel estado cuya tupla tenga el simbolo '|-' en la última posición
        estadosFinales = []

        for estado in self.AFN:
            if estado[-1] == '|-':
                estadosFinales.append(estado[0][0])

        return estadosFinales

    def simbolosLenguaje(self):
        # Los simbolos del lenguaje se corresponden al primer elemento (l[0]) de todas las tuplas de longitud 2 de cada estado.
        simbolos = []

        for subLista in self.AFN[0]:
            if type(subLista) == list and len(subLista) == 2:
                simbolos.append(subLista[0])

        return simbolos

    def transicion(self, e, t):
        # A partir de un simbolo 'a' y un estado 'n' del que salimos como parámetros de entrada devuelve los estados destino
        for subLista in range(0, len(self.AFN)):
            if self.AFN[subLista][0] == e:
                for indexSimbolo in range(1, len(self.AFN[subLista])):
                    if self.AFN[subLista][indexSimbolo][0] == t:
                        return self.AFN[subLista][indexSimbolo][1]

    def estadosExaminados(self):
        # Lista que contiene los estados que ya se han tratado
        estadoExaminados = []

        for estado in self.AFD:
            estadoExaminados.append(estado[0])

        return estadoExaminados

    def estadosNoExaminados(self):
        return map(lambda e:e[1],filter(lambda s:s[0] in self.simbolosAlfabeto and s[1] not in self.estadosExaminados(),self.AFD[-1]))



    def determinizarAFN(self):
        self.AFD = []
        listaIniciales = self.estadosIniciales()

        while len(listaIniciales) != 0:
            self.AFD.append(listaIniciales[0])
            print(self.estadosNoExaminados())
            for estado in self.estadosNoExaminados():  # se recorren todos los estados que no fueron tratados
                nuevaTransaccion = []  # en este vector se calculara los  las transacciones del AFD resultantes

                for simbolo in self.simbolosAlfabeto:  # recorro para todos los simbolos del lenguaje
                    nuevoEstado = []  # defino nuevoEstado para armar el nuevo estado del AFD

                    for estadoNuevo in estado:  # calculo la union con los conjuntos de llegada de todos los estados
                        for tr in self.transicion([estadoNuevo], simbolo):
                            if tr not in nuevoEstado:
                                nuevoEstado.append(tr)

                        nuevoEstado.sort()
                    nuevaTransaccion.append([simbolo, nuevoEstado])
                listaIniciales.append([estado] + nuevaTransaccion)
            listaIniciales.pop(0)

        # busco los estados de Aceptacion y le pongo el |-
        estadosFinales = self.estadosFinales()

        for estadoNuevo in self.AFD:
            aceptado = False
            for estadoFinal in estadosFinales:
                if not aceptado:
                    aceptado = estadoFinal in estadoNuevo[0]
            if aceptado and '|-' not in estadoNuevo: estadoNuevo.append('|-')

        return self.AFD


def insertarAFN():
    AFNgeneral = []
    numEstados = int(input("Numero de estados del automata: "))
    numSimbolos = int(input("Numero de simbolos del automata: "))

    for i in range(0, numEstados):
        tuplaEstado = []
        estadoActual = int(input("Numero del estado actual: "))

        listaProvisional = []
        listaProvisional.append(estadoActual)
        tuplaEstado.append(listaProvisional)

        for j in range(0, numSimbolos):
            tuplaSimbolo = []
            tuplaEstadosDestino = []

            simboloActual = str(input("Simbolo actual: "))
            posiblesEstadosDestino = int(input("Numero de estados destino posibles: "))
            for k in range(0, posiblesEstadosDestino):
                estadoDestino = int(input("Estado destino: "))
                tuplaEstadosDestino.append(estadoDestino)

            tuplaSimbolo.append(simboloActual)
            tuplaSimbolo.append(tuplaEstadosDestino)
            tuplaEstado.append(tuplaSimbolo)

        tipoEstado = str(input("Tipo de estado (I/F/N): "))
        if tipoEstado == "I":
            tuplaEstado.append('->')
        elif tipoEstado == "F":
            tuplaEstado.append('|-')

        AFNgeneral.append(tuplaEstado)

    return AFNgeneral

def print_aut(aut):
    for line in aut:
        print(line)

print("================AFN================")
print("W --> Escribe por terminal el AFN")
print("D --> AFN por defecto")
print("Q --> Salir")
command1 = raw_input('')
if (command1.lower() == "c"):
    print("================INSTRUCCIONES================")
    print("- Cuando incluyamos el simbolo actual, hay que emplear comillas simples -> ('a', 'b', ...) ")
    print("- Para identificar los estados se emplean números naturales (0, 1, 2...) ")
    print(
        "- Para definir el tipo de estado (inicial, final o neutro) hay que incluir 'I', 'F' o 'N' respectivamente cuándo lo pida")
    AFNinsertado = insertarAFN()

if (command1.lower() == "d"):
    AFNinsertado = AFN(
        [
            [[1], ['a', [1]], ['b', [1, 2]], '->'],
            [[2], ['a', []], ['b', [3]]],
            [[3], ['a', [3]], ['b', [3]], '|-']
        ]
    )

if (command1.lower() == "q"):
    os.kill(0, 1)

print("================OPCIONES AFN================")
print("N --> Muestra AFN")
print("D --> Determinizar AFN")
print("Q --> Salir")
print(AFNinsertado.AFN)

while (1):
    command= raw_input('')
    if(command.lower()=="n"):
        print_aut(AFNinsertado.AFN)

    if(command.lower()=="d"):
        print("/------------------------AUTOMATA DETERMINIZADO------------------------/")
        print_aut(AFNinsertado.AFD)
    if(command.lower()=="q"):
        os.kill(0,1)
