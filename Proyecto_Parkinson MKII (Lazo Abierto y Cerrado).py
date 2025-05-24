# -*- coding: utf-8 -*-
"""
Created on Fri May 23 15:11:50 2025

@author: Dario
"""

# Librerias
import numpy as np
import math as m
import matplotlib.pyplot as plt 
import control

x0,t0,tF,dt = 0,0,10,1E-3
w, h = 6, 3
N = round((tF-t0)/dt)+1 
t = np.linspace(t0,tF,N)

frequency = 4 # Frecuencia en Hz
u = 5 * np.sin(2 * m.pi * frequency * t) # Función sinusoidal con frecuencia de 4 Hz y amplitud de 5V

def plotsignals(t,u,Signal):
    # Elementos del circuito RLC para el CONTROL
    C = 1E-2
    R1ctrl = 10
    R2ctrl = 15
    L = 1E-1
    num = [R1ctrl * C * R2ctrl]
    den = [(C)*(L)*(R1ctrl+R2ctrl)+(R1ctrl*R2ctrl*C)+R1ctrl+R2ctrl]
    sys = control.tf(num, den)
    
    # Elementos del circuito RLC para el CASO
    R1c = 1
    R2c = 0.5
    numC = [R1c * C * R2c]
    denC = [(C)*(L)*(R1c+R2c)+(R1c*R2c*C)+R1c+R2c]
    sysC = control.tf(numC, denC)
    
    # Controlador (Tratamiento)
    Re = 521.97
    Cr = 1E-6
    numI = [1]
    denI = [Re * Cr]
    I = control.tf(numI, denI)
    X = control.series(I, I)
    sysI = control.feedback(X, 1, sign = -1)
    
    # Salidas
    ts, Vs_control = control.forced_response(sys, t, u, x0)
    ts, Vs_case = control.forced_response(sysC, t, u, x0)
    ts, Vs_treatment = control.forced_response(sysI, t, u, x0)

    # Gráfica 1: Completa
    fig1 = plt.figure()
    plt.plot(t, u, "-", color=[0.5, 0.05, 0.05], label="$V_{e}(t)$")
    plt.plot((t - 0.01), Vs_control, "-", color=[0, 0.25, 0.4], label="$V_{s}(t)$: Control")
    plt.plot((t - 0.02), Vs_case, "-", color=[0.3, 0.5, 0.2], label="$V_{s}(t)$: Caso")
    plt.plot((t - 0.01), Vs_treatment, "--", color=[0.79, 0.79, 0.23], label="$V_{s}(t)$: Tratamiento")
    plt.title("Actividad neuronal. Caso: Parkinson.")
    plt.grid(True)
    plt.xlim(0,1)
    plt.ylim(-7,7)
    plt.xticks(np.arange(0,1.0001,0.1))
    plt.yticks(np.arange(-7,7.1,1))
    plt.xlabel('$t$ [segundos]')
    plt.ylabel('$V(t)$ [milivolts $(mV)$]')
    plt.title('$Sistema$ $nervioso$. $Reactividad$ $neuronal$.')
    plt.legend(bbox_to_anchor=(0.5, -0.23), loc='center', ncol=4)
    fig1.set_size_inches(10, 4)
    plt.tight_layout()
    plt.savefig('ActNeuronal.png', dpi=600)
    plt.savefig('ActNeuronal.pdf')
    plt.show()

    # Gráfica 2: Solo Caso y Control
    fig2 = plt.figure()
    plt.plot((t - 0.01), Vs_control, "-", color=[0, 0.25, 0.4], label="Control")
    plt.plot((t - 0.02), Vs_case, "-", color=[0.3, 0.5, 0.2], label="Caso")
    plt.grid(True)
    plt.xlim(0,1)
    plt.ylim(-7,7)
    plt.xticks(np.arange(0,1.0001,0.1))
    plt.yticks(np.arange(-7,7.1,1))
    plt.xlabel('$t$ [segundos]')
    plt.ylabel('$V(t)$ [milivolts $(mV)$]')
    plt.title('Comparación: Control vs Caso (sin tratamiento)')
    plt.legend(loc='upper right')
    fig2.set_size_inches(8, 3.5)
    plt.tight_layout()
    plt.savefig('Control_vs_Caso.png', dpi=600)
    plt.savefig('Control_vs_Caso.pdf')
    plt.show()

# Ejecutar
for i in range(1, 2):
    plotsignals(t, u, i)
