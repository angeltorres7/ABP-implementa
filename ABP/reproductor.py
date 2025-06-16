import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os
import random
import time

# Inicializar pygame
pygame.mixer.init()

# Nombre del archivo donde se guardará la playlist
ARCHIVO_PLAYLIST = "playlist.txt"

# Lista donde guardaremos las canciones (rutas completas)
canciones = []

# Modo aleatorio
modo_aleatorio = False  # Variable que controla si el modo aleatorio está activado o no

# Cargar la playlist desde archivo
def cargar_playlist():
    if os.path.exists(ARCHIVO_PLAYLIST):
        with open(ARCHIVO_PLAYLIST, "r") as f:
            for linea in f:
                ruta = linea.strip()
                if os.path.isfile(ruta):
                    canciones.append(ruta)
                    listbox.insert(tk.END, os.path.basename(ruta))

# Guardar la playlist actual
def guardar_playlist():
    with open(ARCHIVO_PLAYLIST, "w") as f:
        for cancion in canciones:
            f.write(cancion + "\n")

# Cargar una nueva canción
def agregar_cancion():
    archivo = filedialog.askopenfilename(filetypes=[("MP3", "*.mp3")])
    if archivo and archivo not in canciones:
        canciones.append(archivo)
        listbox.insert(tk.END, os.path.basename(archivo))
        guardar_playlist()

# Reproducir canción seleccionada o aleatoria
def reproducir():
    global modo_aleatorio
    if modo_aleatorio:
        # Seleccionar una canción aleatoria
        index = random.randint(0, len(canciones) - 1)
    else:
        seleccion = listbox.curselection()
        if seleccion:
            index = seleccion[0]
        else:
            return  # No hay selección y el modo aleatorio no está activado, no se reproduce nada

    pygame.mixer.music.load(canciones[index])
    pygame.mixer.music.play()
    etiqueta.config(text="Reproduciendo: " + os.path.basename(canciones[index]))

    # Configurar la barra de progreso con el tiempo total de la canción
    tiempo_total = pygame.mixer.Sound(canciones[index]).get_length()
    barra_progreso.config(to=tiempo_total, value=0)

    # Iniciar el proceso de actualización de la barra de progreso
    actualizar_barra_progreso()

# Pausar música
def pausar():
    pygame.mixer.music.pause()

# Continuar música
def continuar():
    pygame.mixer.music.unpause()

# Detener música
def detener():
    pygame.mixer.music.stop()

# Eliminar canción
def eliminar_cancion():
    seleccion = listbox.curselection()
    if seleccion:
        index = seleccion[0]
        canciones.pop(index)
        listbox.delete(index)
        guardar_playlist()
        etiqueta.config(text="Canción eliminada.")

# Activar o desactivar el modo aleatorio
def activar_aleatorio():
    global modo_aleatorio
    modo_aleatorio = not modo_aleatorio
    if modo_aleatorio:
        etiqueta.config(text="Modo aleatorio activado")
    else:
        etiqueta.config(text="Modo aleatorio desactivado")

# Actualizar la barra de progreso en tiempo real
def actualizar_barra_progreso():
    if pygame.mixer.music.get_busy():
        # Obtener el tiempo actual de la canción
        tiempo_actual = pygame.mixer.music.get_pos() / 1000  # Obtener en segundos
        barra_progreso.set(tiempo_actual)
        ventana.after(1000, actualizar_barra_progreso)  # Actualizar cada segundo

# Función para adelantar o retroceder la canción con la barra
def mover_progreso(event):
    tiempo_seleccionado = barra_progreso.get()
    pygame.mixer.music.set_pos(tiempo_seleccionado)  # Mover la canción a la posición seleccionada

# Crear ventana
ventana = tk.Tk()
ventana.title("🎶 Reproductor de Música con Playlist")
ventana.geometry("400x500")  # Aumentamos el tamaño para incluir la barra de progreso

# Cambiar el color de fondo de la ventana a negro
ventana.config(bg='#000000')  # Fondo negro

# Etiqueta
etiqueta = tk.Label(ventana, text="No hay canción reproduciendo", wraplength=350, fg='#FFFFFF', bg='#000000', font=("Arial", 12))
etiqueta.pack(pady=10)

# Listbox para la playlist
listbox = tk.Listbox(ventana, width=50, height=10, bg='#1F3A68', fg='#FFFFFF', selectmode=tk.SINGLE)
listbox.pack(pady=10)

# Barra de progreso
barra_progreso = tk.Scale(ventana, from_=0, to=100, orient=tk.HORIZONTAL, length=350, sliderlength=15, bg='#1F3A68', fg='#FFFFFF')
barra_progreso.pack(pady=10)
barra_progreso.bind("<ButtonRelease-1>", mover_progreso)  # Permite mover el progreso al soltar el clic

# Botones
frame_botones = tk.Frame(ventana, bg='#000000')
frame_botones.pack(pady=5)

# Estilo de los botones (colores de fondo y texto)
boton_color_fondo = '#1F3A68'  # Fondo azul fuerte
boton_color_texto = '#FFFFFF'  # Texto blanco

tk.Button(frame_botones, text="Agregar 🎵", command=agregar_cancion, bg=boton_color_fondo, fg=boton_color_texto).grid(row=0, column=0, padx=5)
tk.Button(frame_botones, text="Eliminar 🗑", command=eliminar_cancion, bg=boton_color_fondo, fg=boton_color_texto).grid(row=0, column=1, padx=5)
tk.Button(frame_botones, text="Reproducir ▶", command=reproducir, bg=boton_color_fondo, fg=boton_color_texto).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_botones, text="Pausar ⏸", command=pausar, bg=boton_color_fondo, fg=boton_color_texto).grid(row=1, column=1, padx=5)
tk.Button(frame_botones, text="Continuar ⏯", command=continuar, bg=boton_color_fondo, fg=boton_color_texto).grid(row=2, column=0, padx=5)
tk.Button(frame_botones, text="Detener ⏹", command=detener, bg=boton_color_fondo, fg=boton_color_texto).grid(row=2, column=1, padx=5)
tk.Button(frame_botones, text="Aleatorio 🔀", command=activar_aleatorio, bg=boton_color_fondo, fg=boton_color_texto).grid(row=3, column=0, columnspan=2, pady=5)

# Cargar canciones al iniciar
cargar_playlist()

ventana.mainloop()
