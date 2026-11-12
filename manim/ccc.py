# Algoritmo Adaptativo (Euler + Controlador PID)
def passo_adaptativo(r, T, m, t, Δt):
    # Passo de Euler
    r*, T*, m* = Euler(f, [r, T, m], Δt)
    # Estimativa do erro
    erro = estimar_erro(r*, T*, m*)
    if erro > ε_tol:
        # Passo rejeitado
        Δt = PID(erro, Δt)
        return r, T, m, t, Δt, False
    # Passo aceito
    Δt = PID(erro, Δt)
    return r*, T*, m*, t + Δt, Δt, True

while t < t_final:
    r, T, m, t, Δt, aceito = passo_adaptativo(
        r, T, m, t, Δt)