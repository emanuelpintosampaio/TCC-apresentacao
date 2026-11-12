# Algoritmo Multiescala (Euler Explícito)
def passo_multiescala(r, T, m, t, Δ𝑡, M):

    𝛿t = Δ𝑡 / M

    # Subpassos rápidos (temperatura)
    for j in range(M):
        T = Euler(f_rapido, T, 𝛿t, r)

    # Passo lento (raio e massa) 
    r, m = Euler(f_lento, [r, m], Δ𝑡, T)

    return r, T, m

while t < t_final:

    r, T, m = passo_multiescala(r, T, m, t, Δ𝑡, M)

    t = t + Δ𝑡