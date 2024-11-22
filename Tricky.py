import tkinter as tk
import random

# Función para verificar si alguien ha ganado
def ha_ganado(tablero, jugador):
    for i in range(3):
        if all([tablero[i][j] == jugador for j in range(3)]) or \
           all([tablero[j][i] == jugador for j in range(3)]):
            return True
    if tablero[0][0] == tablero[1][1] == tablero[2][2] == jugador or \
       tablero[0][2] == tablero[1][1] == tablero[2][0] == jugador:
        return True
    return False

# Función para obtener las posiciones disponibles en el tablero
def obtener_posiciones_libres(tablero):
    return [(i, j) for i in range(3) for j in range(3) if tablero[i][j] == " "]

# Algoritmo Minimax para calcular el mejor movimiento
def minimax(tablero, profundidad, es_maximizar, jugador, oponente):
    if ha_ganado(tablero, jugador):
        return 1
    if ha_ganado(tablero, oponente):
        return -1
    if not obtener_posiciones_libres(tablero):
        return 0

    if es_maximizar:
        mejor_valor = -float('inf')
        for fila, col in obtener_posiciones_libres(tablero):
            tablero[fila][col] = jugador
            valor = minimax(tablero, profundidad + 1, False, jugador, oponente)
            tablero[fila][col] = " "
            mejor_valor = max(mejor_valor, valor)
        return mejor_valor
    else:
        mejor_valor = float('inf')
        for fila, col in obtener_posiciones_libres(tablero):
            tablero[fila][col] = oponente
            valor = minimax(tablero, profundidad + 1, True, jugador, oponente)
            tablero[fila][col] = " "
            mejor_valor = min(mejor_valor, valor)
        return mejor_valor

# Función para encontrar el mejor movimiento
def mejor_movimiento(tablero, jugador, oponente):
    mejor_valor = -float('inf')
    movimiento = None
    for fila, col in obtener_posiciones_libres(tablero):
        tablero[fila][col] = jugador
        valor = minimax(tablero, 0, False, jugador, oponente)
        tablero[fila][col] = " "
        if valor > mejor_valor:
            mejor_valor = valor
            movimiento = (fila, col)
    return movimiento

# Función para manejar el clic en el botón
def hacer_movimiento(fila, col):
    global turno
    if tablero[fila][col] == " ":
        tablero[fila][col] = jugador
        botones[fila][col].config(text=jugador)
        if ha_ganado(tablero, jugador):
            mostrar_mensaje("¡Felicidades, has ganado!")
            return
        turno = oponente
        if not obtener_posiciones_libres(tablero):
            mostrar_mensaje("¡Es un empate!")
            return
        mover_ia()

# Función para que la IA haga su movimiento
def mover_ia():
    global turno
    fila, col = mejor_movimiento(tablero, oponente, jugador)
    tablero[fila][col] = oponente
    botones[fila][col].config(text=oponente)
    if ha_ganado(tablero, oponente):
        mostrar_mensaje("La IA ha ganado. ¡Mejor suerte la próxima vez!")
        return
    turno = jugador
    if not obtener_posiciones_libres(tablero):
        mostrar_mensaje("¡Es un empate!")

# Función para mostrar un mensaje
def mostrar_mensaje(mensaje):
    mensaje_label.config(text=mensaje)

# Inicializar la ventana principal
ventana = tk.Tk()
ventana.title("Tres en Raya")

# Inicializar el tablero
tablero = [[" " for _ in range(3)] for _ in range(3)]
jugador = "X"
oponente = "O"
turno = jugador

# Crear botones para el tablero
botones = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        botones[i][j] = tk.Button(ventana, text=" ", font=('Arial', 24), width= 5, height=2, command=lambda fila=i, col=j: hacer_movimiento(fila, col))
        botones[i][j].grid(row=i, column=j)

# Label para mostrar mensajes
mensaje_label = tk.Label(ventana, text="", font=('Arial', 16))
mensaje_label.grid(row=3, column=0, columnspan=3)

# Iniciar la ventana
ventana.mainloop()