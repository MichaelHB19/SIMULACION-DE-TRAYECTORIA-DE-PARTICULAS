import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

#Los valores constantes (datos)
q_default = 1.0  # Carga de la particula
m_default = 1.0  # Masa de la particula
E_default = np.array([0.0, 0.0, 1.0])  # Campo Electrico
B_default = np.array([0.0, 0.0, 1.0])  # Campo magnetico


#Función para calcular la aceleración con Lorentz y componente estocástica
def calcular(v, ruido):
    F = q * (E + np.cross(v, B)) + ruido
    return F / m


#Función para ejecutar la simulación y graficar
def simular():
    try:
        # Leer variables de las entradas
        global q, m, E, B
        q = float(entry_q.get())
        m = float(entry_m.get())
        E = np.array([float(x) for x in entry_e.get().split(',')])
        B = np.array([float(x) for x in entry_b.get().split(',')])

        tiempo = float(entry_tiempo.get())
        num_par = int(entry_num_par.get())
        p_t = float(entry_p_t.get())
        num_steps = int(tiempo / p_t)
        num_sim = int(entry_num_sim.get())

        #Inicializamos las posiciones y velocidades
        global all_positions
        all_positions = np.zeros((num_sim, num_par, num_steps, 3))
        global colores
        colores = plt.get_cmap('tab10', num_par)  #Le ponemos color a cada particula

        for sim in range(num_sim):
            posi = np.zeros((num_par, num_steps, 3))
            vel = np.random.normal(0, 1, (num_par, 3))

            #Montecarlo
            for t in range(num_steps):
                for i in range(num_par):
                    ruido = np.random.normal(0, 0.1, 3)  #El ruido estocástico
                    a = calcular(vel[i], ruido)  # Aceleracion

                    #Se actualiza la velocidad y la posicion
                    vel[i] += a * p_t
                    posi[i, t, :] = posi[i, t - 1, :] + vel[i] * p_t if t > 0 else vel[i] * p_t

            all_positions[sim] = posi

        #Crear el gráfico inicial
        actualizar_grafico()

        #Actualizar las opciones en el selector de partículas
        particula_selector['values'] = ["Todas las partículas"] + list(range(1, num_par+1))
        particula_selector.current(0)  #Se selecciona "Todas las partículas" por defecto

    except ValueError:
        print("Por favor, ingrese valores válidos.")


#Función para actualizar el gráfico basado en la partícula que se seleccionada
def actualizar_grafico(*args):
    try:
        seleccion = particula_selector.get()
        if seleccion == "Todas las partículas":
            particula = -1
        else:
            particula = int(seleccion) -1
    except ValueError:
        return  #Si la selección no es válida, no hace nada

    #Limpiamos el gráfico anterior
    ax.cla()
    ax.set_title("Simulación de una partícula")  # Titulo del grafico interno

    if particula == -1:
        for sim in range(all_positions.shape[0]):
            for i in range(all_positions.shape[1]):
                ax.plot(all_positions[sim, i, :, 0], all_positions[sim, i, :, 1], all_positions[sim, i, :, 2],
                        color=colores(i))
    else:
        for sim in range(all_positions.shape[0]):
            ax.plot(all_positions[sim, particula, :, 0], all_positions[sim, particula, :, 1],
                    all_positions[sim, particula, :, 2], color=colores(particula))

    canvas.draw()

#Funcion para reiniciar valores son salir del programa(accion del boton)
def reiniciar():
    #Limpiamos el gráfico
    ax.cla()
    canvas.draw()

#Configuración de la interfaz gráfica con tkinter
root = tk.Tk()
root.title("Simulación de Movimiento de Partículas con Montecarlo")

frame = ttk.Frame(root, padding="10 10 10 10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

#Variables de entrada pra el programa
entry_tiempo = tk.StringVar()
entry_num_par = tk.StringVar()
entry_p_t = tk.StringVar()
entry_num_sim = tk.StringVar()

entry_q = tk.StringVar(value=str(q_default))
entry_m = tk.StringVar(value=str(m_default))
entry_e = tk.StringVar(value=','.join(map(str, E_default)))
entry_b = tk.StringVar(value=','.join(map(str, B_default)))

#Etiquetas y entradas de la interfaz
ttk.Label(frame, text="Carga (q):").grid(column=1, row=1, sticky=tk.W)
ttk.Entry(frame, textvariable=entry_q).grid(column=2, row=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Masa (m):").grid(column=1, row=2, sticky=tk.W)
ttk.Entry(frame, textvariable=entry_m).grid(column=2, row=2, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Campo Eléctrico (E):").grid(column=1, row=3, sticky=tk.W)
ttk.Entry(frame, textvariable=entry_e).grid(column=2, row=3, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Campo Magnético (B):").grid(column=1, row=4, sticky=tk.W)
ttk.Entry(frame, textvariable=entry_b).grid(column=2, row=4, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Tiempo:").grid(column=4, row=1, sticky=tk.W)
ttk.Entry(frame, textvariable=entry_tiempo).grid(column=5, row=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Número de Partículas:").grid(column=4, row=2, sticky=tk.W)
ttk.Entry(frame, textvariable=entry_num_par).grid(column=5, row=2, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Paso de Tiempo:").grid(column=4, row=3, sticky=tk.W)
ttk.Entry(frame, textvariable=entry_p_t).grid(column=5, row=3, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Número de Simulaciones:").grid(column=4, row=4, sticky=tk.W)
ttk.Entry(frame, textvariable=entry_num_sim).grid(column=5, row=4, sticky=(tk.W, tk.E))

#Botón de simular
ttk.Button(frame, text="Simular", command=simular).grid(column=2, row=5, sticky=tk.E)

#Boton para reiniciar
ttk.Button(frame, text="Reiniciar", command=reiniciar).grid(column=5, row=5, sticky=tk.E)

#Selector de partícula
ttk.Label(frame, text="Seleccionar Partícula:").grid(column=1, row=6, sticky=tk.W)
particula_selector = ttk.Combobox(frame)
particula_selector.grid(column=2, row=6, sticky=(tk.W, tk.E))
particula_selector.bind("<<ComboboxSelected>>", actualizar_grafico)

#Crear el gráfico con matplotlib
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Simulación de una partícula") #Titulo del grafico interno
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0, row=12, columnspan=3)

#Botón de salir
ttk.Button(frame, text="Salir", command=root.quit).grid(column=2, row=13, sticky=tk.E)

root.mainloop()
