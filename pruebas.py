import numpy as np
import matplotlib.pyplot as plt

def graficar_restricciones(coeficientes, maximizar, xmin, xmax, ymin, ymax, numpoints=100):
    # Crear un arreglo de puntos para graficar
    x = np.linspace(xmin, xmax, numpoints)
    y = np.linspace(ymin, ymax, numpoints)
    X, Y = np.meshgrid(x, y)
    Z = coeficientes[0][0] * X + coeficientes[0][1] * Y
    for i in range(1, len(coeficientes)):
        Z = np.minimum(Z, (coeficientes[i][0] * X + coeficientes[i][1] * Y) / -coeficientes[i][2])
    if not maximizar:
        Z = -Z

    # Encontrar los puntos de intersección
    puntos_interseccion = []
    for i in range(len(coeficientes) - 1):
        for j in range(i + 1, len(coeficientes)):
            A = np.array([coeficientes[i][:2], coeficientes[j][:2]])
            b = np.array([-coeficientes[i][2], -coeficientes[j][2]])
            punto = np.linalg.solve(A, b)
            if xmin <= punto[0] <= xmax and ymin <= punto[1] <= ymax:
                puntos_interseccion.append(punto)

    # Graficar la región factible
    fig, ax = plt.subplots()
    ax.contourf(X, Y, Z, levels=20, alpha=0.5, cmap='coolwarm')
    ax.contour(X, Y, Z, levels=10, colors='black')
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    # Graficar los puntos de intersección
    if puntos_interseccion:
        x_interseccion = [p[0] for p in puntos_interseccion]
        y_interseccion = [p[1] for p in puntos_interseccion]
        ax.scatter(x_interseccion, y_interseccion, color='black', s=50)

# Mostrar la gráfica
plt.show()