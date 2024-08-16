import numpy as np
import streamlit as st
import plotly.graph_objects as go
from scipy.integrate import odeint

# Definição das funções diferenciais do modelo
def dX_dt(X, t, a, b, c, d):
    x, y = X
    dxdt = a * x - b * x * y 
    dydt = c * x * y - d * y
    return [dxdt, dydt]

# Criando a Interface do servidor da Streamlit
st.title("Plano de fases do modelo de Presa-Predador")

# Definir os parâmetros
a = st.number_input("Taxa de crescimento das presas na ausência de predadores", value=1.0, format="%.5f")
b = st.number_input("Taxa de mortalidade das presas dada a presença de predadores", value=0.1, format="%.5f")
c = st.number_input("Taxa de crescimento dos predadores dada a caça de presas", value=0.1, format="%.5f")
d = st.number_input("Taxa de mortalidade dos predadores dada a ausência de presas", value=1.0, format="%.5f")
t0 = st.number_input("Tempo inicial", value=0.0, format="%.5f")
tn = st.number_input("Tempo final", value=100.0, format="%.5f")
nb_points = 50

#Definir titulo

titulo = st.text_input("Título do gráfico: ")
predadores = st.text_input('Predador: ')
presas = st.text_input('presa: ')
# Parâmetros do sistema (para cada tempo t entre o intervalo [t0, tn] com espaçamento de 500 pontos)
t = np.linspace(t0, tn, 500)

# Calcular o ponto de equilíbrio explicitamente
equilibrium_point = [d/c, a/b]

# Gráficos de trajetórias e campos vetoriais
fig = go.Figure()

# Grade de pontos e campos vetoriais
x = np.linspace(0, 2 * equilibrium_point[0], nb_points)
y = np.linspace(0, 2 * equilibrium_point[1], nb_points)
X1, Y1 = np.meshgrid(x, y)

# Calcula o campo vetorial em cada ponto da grade
DX1, DY1 = np.array([dX_dt([X1[i, j], Y1[i, j]], 0, a, b, c, d) for i in range(nb_points) for j in range(nb_points)]).T
DX1 = DX1.reshape(nb_points, nb_points)
DY1 = DY1.reshape(nb_points, nb_points)

# Adicionar campo vetorial ao gráfico usando quiver
fig.add_trace(go.Cone(
    x=X1.flatten(),
    y=Y1.flatten(),
    u=DX1.flatten(),
    v=DY1.flatten(),
    sizemode="absolute",
    sizeref=2,
    showscale=False,
    colorscale="Blues",
    name="Campo Vetorial"
))

# Ponto de Equilíbrio
fig.add_trace(go.Scatter(x=[equilibrium_point[0]], y=[equilibrium_point[1]], mode='markers', name=f'Ponto de Equilíbrio ({equilibrium_point[0]:.2f}, {equilibrium_point[1]:.2f})', marker=dict(color='red', size=10)))

# Trajetórias que se aproximam do ponto de equilíbrio
initial_conditions = [
    (0.9 * equilibrium_point[0], 0.9 * equilibrium_point[1]),
    (1.2 * equilibrium_point[0], 1.2 * equilibrium_point[1]),
    (1.5 * equilibrium_point[0], 1.5 * equilibrium_point[1]),
    (1.8 * equilibrium_point[0], 1.8 * equilibrium_point[1]),
    (2 * equilibrium_point[0], 2 * equilibrium_point[1])
]

for X0 in initial_conditions:
    X = odeint(dX_dt, X0, t, args=(a, b, c, d))
    fig.add_trace(go.Scatter(x=X[:, 0], y=X[:, 1], mode='lines', line=dict(width=2), name=f'Trajetória a partir de ({X0[0]:.2f}, {X0[1]:.2f})'))

# Layout
fig.update_layout(
    title=f'{titulo}',
    xaxis_title=f'Número de {presas}',
    yaxis_title=f'Número de {predadores}',
    legend_title='Legenda',
    showlegend=True
)

st.plotly_chart(fig)

