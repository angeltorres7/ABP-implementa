import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os

# Inicializar pygame
pygame.mixer.init()

# Nombre del archivo donde se guardará la playlist
ARCHIVO_PLAYLIST = "playlist.txt"

# Lista donde guardaremos las canciones (rutas completas)
canciones = []

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

# Reproducir canción seleccionada
def reproducir():
    seleccion = listbox.curselection()
    if seleccion:
        index = seleccion[0]
        pygame.mixer.music.load(canciones[index])
        pygame.mixer.music.play()
        etiqueta.config(text="Reproduciendo: " + os.path.basename(canciones[index]))

def pausar():
    pygame.mixer.music.pause()

def continuar():
    pygame.mixer.music.unpause()

def detener():
    pygame.mixer.music.stop()

def eliminar_cancion():
    seleccion = listbox.curselection()
    if seleccion:
        index = seleccion[0]
        canciones.pop(index)
        listbox.delete(index)
        guardar_playlist()
        etiqueta.config(text="Canción eliminada.")

# Crear ventana
ventana = tk.Tk()
ventana.title("🎶 Reproductor de Música con Playlist")
ventana.geometry("400x400")

# Etiqueta
etiqueta = tk.Label(ventana, text="No hay canción reproduciendo", wraplength=350)
etiqueta.pack(pady=10)

# Listbox para la playlist
listbox = tk.Listbox(ventana, width=50)
listbox.pack(pady=10)

# Botones
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=5)

tk.Button(frame_botones, text="Agregar 🎵", command=agregar_cancion).grid(row=0, column=0, padx=5)
tk.Button(frame_botones, text="Eliminar 🗑", command=eliminar_cancion).grid(row=0, column=1, padx=5)
tk.Button(frame_botones, text="Reproducir ▶", command=reproducir).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_botones, text="Pausar ⏸", command=pausar).grid(row=1, column=1, padx=5)
tk.Button(frame_botones, text="Continuar ⏯", command=continuar).grid(row=2, column=0, padx=5)
tk.Button(frame_botones, text="Detener ⏹", command=detener).grid(row=2, column=1, padx=5)

# Cargar canciones al iniciar
cargar_playlist()

ventana.mainloop()