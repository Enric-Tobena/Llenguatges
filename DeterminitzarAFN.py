#!/usr/bin/python
# -*- coding: utf-8 -*-

class AFN:
    def __init__(self, AFN):
        self.AFN = AFN
        self.simbolosAlfabeto = self.simbolosLenguaje()

        self.AFD = self.determinizarAFN()

    def estadosIniciales(self):
        # El estado inicial se corresponde con aquel estado cuya tupla tenga el simbolo '>' en la última posición
        estadosIniciales = []

        for subLista in self.AFN:
            if subLista[-1] == '>':
                estadosIniciales.append(subLista)
        
        return estadosIniciales


        #return filter(lambda s: s[-1] == '>', self.AFN)  
    
    def simbolosLenguaje(self):
        # Los simbolos del lenguaje se corresponden al primer elemento (l[0]) de todas las tuplas de longitud 2 de cada estado.        
        simbolos = []
        
        for subLista in self.AFN[0]:
            if type(subLista) == list and len(subLista) == 2:
                simbolos.append(subLista[0])
        
        return simbolos
        
        #return [l[0] for l in filter(lambda s: len(s) == 2, self.AFN[-1])]

    def Transaccion(self, e, t):
        return filter(lambda s: s[0] == t, filter(lambda s: s[0] == e, self.AFN)[0])[0][1]
   
    def estadosTratados(self):
        # Lista que contiene los estados que ya se han tratado
        estadosTratados = []

        for estado in self.AFD:
            estadosTratados.append(estado[0])

        return estadosTratados

        #return [e[0] for e in self.AFD]  

    def EstadosNoTratados(self):
        return map(lambda e: e[1],
                   filter(lambda s: s[0] in self.simbolosAlfabeto and s[1] not in self.estadosTratados(),
                          self.AFD[-1]))

    def determinizarAFN(self):
        self.AFD = []
        listaIniciales = self.estadosIniciales()

        while len(listaIniciales) != 0:
            self.AFD.append(listaIniciales[0])
            for estado in self.EstadosNoTratados():  # se recorren todos los estados que no fueron tratados
                TransaccionDelAFD = []  # en este vector se calculara los  las transacciones del AFD resultantes
                for simbolo in self.simbolosAlfabeto:  # recorro para todos los simbolos del lenguaje
                    nuevoEstado = []  # defino nuevoEstado para armar el nuevo estado del AFD
                    for e in estado:  # calculo la union con los conjuntos de llegada de todos los estados
                        for t in self.Transaccion([e], simbolo):
                            if t not in nuevoEstado:
                                nuevoEstado.append(t)
                        nuevoEstado.sort()

                    TransaccionDelAFD.append([simbolo, nuevoEstado])

                listaIniciales.append([estado] + TransaccionDelAFD)

            listaIniciales.pop(0)

        # busco los estados de Aceptacion y le pongo el *
        estasdosDeAceptacion = [l[0][0] for l in
                                filter(lambda s: s[-1] == '*', self.AFN)]  # estados de Aceptacion
        for e in self.AFD:
            Aceptacion = False
            for ea in estasdosDeAceptacion:
                if not Aceptacion:
                    Aceptacion = ea in e[0]
            if Aceptacion and '*' not in e: e.append('*')

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
            tuplaEstado.append('>')
        elif tipoEstado == "F":
            tuplaEstado.append('*')

        AFNgeneral.append(tuplaEstado) 

    return AFNgeneral



print("================INSTRUCCIONES================")
print("- Cuando incluyamos el simbolo actual, hay que emplear comillas simples -> ('a', 'b', ...) ")
print("- Para identificar los estados se emplean números naturales (0, 1, 2...) ") 
print("- Para definir el tipo de estado (inicial, final o neutro) hay que incluir 'I', 'F' o 'N' respectivamente cuándo lo pida") 

print("================INSERTAR AUTOMATA================")
#AFNseleccionado = insertarAFN()
AUT = AFN(
  [
            [[1], ['a', [1]], ['b', [1, 2]], '>'],
            [[2], ['a', []], ['b', [3]]],
            [[3], ['a', [3]], ['b', [3]], '*']
  ]
)
"""
print("/------------------------AUTOMATA NO DETERMINIZADO------------------------/")
for line in AFNseleccionado:
    print(line)
"""
print("/------------------------AUTOMATA DETERMINIZADO------------------------/")
for line in AUT.AFD:
    print(line)   

