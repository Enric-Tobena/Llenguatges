#!/usr/bin/python
# -*- coding: utf-8 -*-

import os


class AFN:
    def __init__(self, AFN):
        self.AFN = AFN
        self.simbolosAlfabeto = self.simbolosLenguaje()

        self.AFD = self.determinizarAFN()

    def estadosIniciales(self):
        # El estado inicial se corresponde con aquel estado cuya tupla tenga el simbolo '->' en la última posicion
        estadosIniciales = []

        for subLista in self.AFN:
            if subLista[-1] == '->':
                estadosIniciales.append(subLista)

        return estadosIniciales

    def estadosFinales(self):
        # El estado final se corresponde con aquel estado cuya tupla tenga el simbolo '|-' en la última posición
        estadosFinales = []

        for subLista in self.AFN:
            if subLista[-1] == '|-':
                estadosFinales.append(subLista[0][0])

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
        estadosExaminados = []

        for estado in self.AFD:
            estadosExaminados.append(estado[0])

        return estadosExaminados

    def estadosNoExaminados(self):        
        estadosNoExaminados = [] 

        for estado in self.AFD:
            for i in range (1, len(estado)):
                if str(estado[i][0]) in self.simbolosAlfabeto and list(estado[i][1]) not in self.estadosExaminados():
                    estadosNoExaminados.append(estado[i])

        estadosNoExaminados = map(lambda estado: estado[1], estadosNoExaminados) 
        return estadosNoExaminados

    def determinizarAFN(self):
        self.AFD = []
        listaIniciales = self.estadosIniciales()
        
        while len(listaIniciales) > 0:            
            self.AFD.append(listaIniciales[0])
            for estado in self.estadosNoExaminados():  # Se recorren todos los estados que no fueron tratados
                nuevaTransaccion = []  # En este vector se calcularan las transacciones del AFD resultantes

                for simbolo in self.simbolosAlfabeto:  # Recorro para todos los simbolos del lenguaje
                    nuevoEstado = []  # Defino nuevoEstado para montar el nuevo estado del AFD

                    # Calculo la union con los conjuntos de llegada de todos los estados
                    for estadoNuevo in estado:  # Por cada estado en la lista de estados no examinados
                        for tr in self.transicion([estadoNuevo], simbolo): # Por cada transicion en la lista de transiciones
                            if tr not in nuevoEstado: # Si esta transaccion no esta en la lista de estados, añadimos  la transaccion a la lista de nuevos estados
                                nuevoEstado.append(tr) 

                    nuevaTransaccion.append([simbolo, nuevoEstado]) # Se añade a la lista nueva transaccion  el simbolo y el estado
                listaIniciales.append([estado] + nuevaTransaccion) # Se añade a la lista de iniciales el estado y la transaccin
            listaIniciales.pop(0)                        # Eliminamos el elemento en la posción 0 de la lista

            # CON ESTO CONSEGUIMOS:
            # [estado, [simbolo,nuevoestado],...,...,]
            # Quitamos de la lista de iniciales


        # AÑADIMOS LOS FINALES
        # Busco los estados finales y les añado el |-
        estadosFinales = self.estadosFinales()

        for estadoNuevo in self.AFD:
            final = False
            for estadoFinal in estadosFinales:
                if not final:
                    final = estadoFinal in estadoNuevo[0]
            if final and '|-' not in estadoNuevo: #si no tiene el |- lo añadimos
                estadoNuevo.append('|-') 

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

def checkear(estadoAnterior, estadoActual):
    if len(estadoAnterior) != len(estadoActual):
        return False
    else:
        return estadoAnterior[0] == estadoActual[0] 

while (1):
    print("")
    print("================COMANDOS POSIBLES================")
    print("W | w --> Escribe por terminal el AFN")
    print("D | d --> AFN por defecto")
    print("Q | q --> Salir")
    print("- Hay que incluir la letra de la funcion entre comillas simples --> ('w', 'd', 'q') ")
    command1 = input('')

    if command1.lower() == 'w':
        print("================INSTRUCCIONES================")
        print("- Cuando incluyamos el simbolo actual, hay que emplear comillas simples -> ('a', 'b', ...) ")
        print("- Para identificar los estados se emplean números naturales (0, 1, 2...) ")
        print(
            "- Para definir el tipo de estado (inicial, final o neutro) hay que incluir 'I', 'F' o 'N' respectivamente cuándo lo pida")

        AFNseleccionado = insertarAFN()
        AFNinsertado = AFN(AFNseleccionado)

        print("/------------------------AUTOMATA NO DETERMINIZADO------------------------/")
        for line in AFNseleccionado:
            print(line)

        print("/------------------------AUTOMATA DETERMINIZADO------------------------/")
        for i in range(0, len(AFNinsertado.AFD)):
            if i == 0:
                print(AFNinsertado.AFD[0])
            else:
                if not checkear(AFNinsertado.AFD[i - 1], AFNinsertado.AFD[i]):
                    print(AFNinsertado.AFD[i])

    elif command1.lower() == 'd':
        AFNdefecto = AFN(

            [               
                [[0], ['a', [0, 2]], ['b', [0, 1]], '->'],
                [[1], ['a', [2]], ['b', [2]]], 
                [[2], ['a', []], ['b', []], '|-']
            ]

        )

        print("/------------------------AUTOMATA NO DETERMINIZADO------------------------/")
        for line in AFNdefecto.AFN:
            print(line)

        print("/------------------------AUTOMATA DETERMINIZADO------------------------/")
        for i in range(0, len(AFNdefecto.AFD)):
            if i == 0:
                print(AFNdefecto.AFD[0])
            else:
                if not checkear(AFNdefecto.AFD[i - 1], AFNdefecto.AFD[i]):
                    print(AFNdefecto.AFD[i])

    elif command1.lower() == 'q':
        os.kill(0, 1)

    else:
        print("Comando incorrecto")