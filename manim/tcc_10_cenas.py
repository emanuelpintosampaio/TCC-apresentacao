# -*- coding: utf-8 -*-
"""
Slides para a defesa do TCC de Emanuel Pinto Sampaio
"Análise Comparativa de Modelos para a Difusão de Gás CO2
em Gotículas de Espuma Marinha"

Como renderizar e apresentar (manim-slides):

    manim -qh tcc_slides.py Titulo Agenda Introducao MicrofisicaGoticulas \
        ModeloDifusao MetodosNumericos EstrategiasTempo \
        ImplementacaoSimulacoes Resultados Conclusoes

    manim-slides convert Titulo Agenda Introducao MicrofisicaGoticulas \
        ModeloDifusao MetodosNumericos EstrategiasTempo \
        ImplementacaoSimulacoes Resultados Conclusoes apresentacao.html

    manim-slides present Titulo Agenda Introducao MicrofisicaGoticulas \
        ModeloDifusao MetodosNumericos EstrategiasTempo \
        ImplementacaoSimulacoes Resultados Conclusoes
"""

import numpy as np
from manim import *
from manim_slides import Slide
from mscene.plugins import *



# ----------------------------------------------------------------------
# Paleta de cores e tamanhos padrão
# ----------------------------------------------------------------------
AZUL_PRINCIPAL = "#0065ff"
AZUL_ESCURO = BLUE_E
AZUL_CLARO = BLUE_C
CINZA_TEXTO = "#2B2B2B"
CINZA_LINHA = "#9A9A9A"
VERDE_OK = "#1E8449"
VERMELHO_ALERTA = "#B03A2E"
LARANJA_DESTAQUE = "#CA6F1E"

FONTE_TITULO = 40
FONTE_SUBTITULO = 30
FONTE_CORPO = 27
FONTE_PEQUENA = 22
FONTE_TABELA = 24


class BaseSlide(Slide):
    """Classe base com métodos utilitários usados por todos os capítulos."""

    def setup(self):
        super().setup()
        self.camera.background_color = WHITE

    def construct(self):
        # BaseSlide não é uma cena real — isso é só uma rede de segurança
        # caso ela seja renderizada por engano (via -a ou seletor interativo).
        self.wait(0.1)

    # ---------------- layout ----------------
    def titulo(self, texto, cor=AZUL_ESCURO, tamanho=FONTE_TITULO):
        t = Text(texto, font_size=tamanho, color=cor, weight=BOLD)
        t.to_edge(UP, buff=0.45)
        linha = Line(LEFT, RIGHT, color=AZUL_PRINCIPAL, stroke_width=3)
        linha.set_width(11.5)
        linha.next_to(t, DOWN, buff=0.18)
        return VGroup(t, linha)
 
    def rotulo_capitulo(self, texto):
        r = Text(texto, font_size=16, color=CINZA_LINHA)
        r.to_corner(UP).shift(0.4*UP)
        return r
 
    def entrar_titulo(self, texto_titulo, texto_capitulo=None):
        grp = self.titulo(texto_titulo)
        mobs = [grp]
        if texto_capitulo is not None:
            cap = self.rotulo_capitulo(texto_capitulo)
            mobs.append(cap)
        self.play(*[FadeIn(m, shift=UP * 0.2) for m in mobs])
        return VGroup(*mobs)


    def limpar(self):
        if self.mobjects:
            self.play(FadeOut(Group(*self.mobjects)))

    def ajustar(self, mob, largura_max=12.0, altura_max=5.6):
        escala = min(largura_max / mob.width, altura_max / mob.height)
        mob.scale(escala)
        return mob

    # ---------------- conteúdo ----------------
    def lista(self, itens, font_size=FONTE_CORPO, cor=CINZA_TEXTO, buff=0.38, largura=11.5):
        grupo = VGroup()
        for item in itens:
            marcador = Dot(color=AZUL_PRINCIPAL).scale(0.55)
            txt = MathTex(item, font_size=font_size, color=cor)
            if txt.width > largura:
                txt.set_width(largura)
            linha = VGroup(marcador, txt).arrange(RIGHT, buff=0.28)
            grupo.add(linha)
        grupo.arrange(DOWN, aligned_edge=LEFT, buff=buff)
        return grupo
        

    def tabela(self, dados, fonte=FONTE_TABELA, cor_cabecalho=AZUL_ESCURO,
               largura_max=12.3, altura_max=5.4):
        t = Table(
            dados,
            include_outer_lines=True,
            line_config={"stroke_width": 1.5, "color": CINZA_LINHA},
            element_to_mobject=Text,
            element_to_mobject_config={"font_size": fonte, "color": CINZA_TEXTO},
        )
        t.get_rows()[0].set_color(cor_cabecalho)
        self.ajustar(t, largura_max, altura_max)
        return t

    def caixa(self, texto, cor=AZUL_PRINCIPAL, fonte=FONTE_CORPO, largura=None):
        txt = Text(texto, font_size=fonte, color=CINZA_TEXTO)
        if largura:
            txt.set_width(largura)
        fundo = SurroundingRectangle(txt, color=cor, buff=0.35, stroke_width=2.5)
        return VGroup(fundo, txt)

    def fonte_rodape(self, texto):
        r = Text(texto, font_size=16, color=CINZA_LINHA, slant=ITALIC)
        r.to_corner(DL, buff=0.3)
        return r


# ========================================================================
# CAPA / TÍTULO
# ========================================================================
class Titulo(BaseSlide):
    def construct(self):
        # ---- slide de capa completa ----
        branco = Text('oi',color=WHITE,font_size=0.001)
        instituicao = Text(
            "Universidade Federal do Espírito Santo",
            font_size=26, color=CINZA_TEXTO, weight=BOLD,
        )
        centro = Text(
            "Centro Universitário Norte do Espírito Santo",
            font_size=22, color=CINZA_TEXTO,
        )
        curso = Text(
            "Curso de Bacharelado em Matemática Industrial",
            font_size=22, color=CINZA_TEXTO,
        )
        cabecalho = VGroup(instituicao, centro, curso).arrange(DOWN, buff=0.18)
        cabecalho.to_edge(UP, buff=0.7)

        titulo_tcc1 = MathTex(
            r"\text{Análise Comparativa de Modelos para a Difusão}",
            font_size=45, color=CINZA_TEXTO
        ).set_stroke(width=2.5)

        titulo_tcc2 = MathTex(
            r"\text{de Gás C}\text{O}_2 \text{ em Gotículas de Espuma Marinha}",
            font_size=45, color=CINZA_TEXTO,
        ).set_stroke(width=2.5)

        titulo_tcc = VGroup(titulo_tcc1,titulo_tcc2).arrange(DOWN, buff=0.15)
        titulo_tcc.move_to(ORIGIN + UP * 0.3)

        autor = Text("Emanuel Pinto Sampaio", font_size=26, color=CINZA_TEXTO)
        orientador = Text(
            "Orientador: Prof. Dr. Iury Ângelo Gonçalves",
            font_size=22, color=CINZA_TEXTO,
        )
        rodape = VGroup(autor, orientador).arrange(DOWN, buff=0.15)
        rodape.next_to(titulo_tcc, DOWN, buff=0.7)

        local1 = Text("São Mateus, ES", font_size=20, color=CINZA_TEXTO)
        local2 = Text("2026", font_size=20, color=CINZA_TEXTO)
        local = VGroup(local1, local2).arrange(DOWN, buff=0.15)

        local.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(branco))
        self.next_slide()
        self.play(FadeIn(cabecalho, shift=DOWN * 0.2))
        blues = [BLUE_A, BLUE_C, BLUE_E]        
        kwargs = dict(color=blues, width=3, duration=1.5)
        self.play(FlashFade(titulo_tcc1,mode="IN", **kwargs),FlashFade(titulo_tcc2,mode="IN", **kwargs))

        #self.play(Write(titulo_tcc))
        self.play(FadeIn(rodape, shift=UP * 0.2))
        self.play(FadeIn(local))
        self.next_slide()
        self.limpar()




# ========================================================================
# AGENDA
# ========================================================================
class Agenda(BaseSlide):
    def construct(self):
        titulo_grp = self.entrar_titulo("Estrutura da Apresentação")
        
        itens = [
                    r"\text{1.  Introdução e Motivação}",
                    r"\text{2.  Fundamentação Teórica}",
                    r"\,\,\,\text{    2.1  Microfísica das gotículas espuma}",
                    r"\,\,\,\text{    2.2  Modelo de difusão de C}\text{O}_2", # Seu CO2 em LaTeX!
                    r"\,\,\,\text{    2.3  Métodos numéricos (Euler e Runge-Kutta)}",
                    r"\,\,\,\text{    2.4  Estratégias de avanço no tempo}",
                    r"\text{3.  Implementação e Simulações Numéricas}",
                    r"\text{4.  Resultados e Discussão}",
                    r"\text{5.  Conclusões}"
                ]
        grupo = self.lista(itens, font_size=35, buff=0.30).set_stroke(width=1)
        grupo.next_to(titulo_grp, DOWN, buff=0.55).to_edge(LEFT, buff=1.2)

        for linha in grupo:
            self.play(FadeIn(linha, shift=RIGHT * 0.15), run_time=0.35)
        self.next_slide()
        self.limpar()
        self.next_slide()

# ========================================================================
# CAPÍTULO 1 — INTRODUÇÃO
# ========================================================================
class Introducao(BaseSlide):
    def construct(self):
        cap = "1. Introdução"

        # 1. Título com MathTex (permite o subscrito do CO2)
        t = MathTex(
            r"\textbf{A importância do gás C}\textbf{O}_2\textbf{ na atmosfera}",
            font_size=FONTE_TITULO,
            color=CINZA_TEXTO,
        )
        t.to_edge(UP, buff=0.45)

        # 2. Linha azul
        linha = Line(LEFT, RIGHT, color=AZUL_PRINCIPAL, stroke_width=3)
        linha.set_width(11.5)
        linha.next_to(t, DOWN, buff=0.18)

        # 3. Rótulo do capítulo
        rotulo = Text(cap, font_size=20, color=CINZA_LINHA)
        rotulo.to_corner(UR, buff=0.5)

        # 4. Agrupa título + linha + rótulo
        titulo_grp = VGroup(t, linha, rotulo)

        # 5. Anima entrada do cabeçalho
        self.play(*[FadeIn(m, shift=UP * 0.2) for m in titulo_grp])

        # ---- Lista de tópicos ----
        texto = self.lista([
            r"\text{C}\text{O}2 \text{é um dos principais gases responsáveis pela retenção de calor}",
            r"\text{Entender o balanço de C}\text{O}2 \text{é essencial para modelos climáticos}",
        ], font_size=27)

        texto.next_to(titulo_grp, DOWN, buff=0.6)
        self.play(FadeIn(texto, shift=UP * 0.2))

        # ---- Finalização ----
        self.next_slide()
        self.limpar()

        # ---- slide 2: oceano como sumidouro ----
        titulo_grp = self.entrar_titulo("O oceano como sumidouro de CO2", cap)
        eq = MathTex(r"F = k\,\Delta c", font_size=56, color=AZUL_PRINCIPAL)
        legenda = Text(
            "F: fluxo de gás    k: velocidade de transferência    Δc: diferença de concentração",
            font_size=22, color=CINZA_TEXTO,
        )
        bloco_eq = VGroup(eq, legenda).arrange(DOWN, buff=0.35)
        bloco_eq.next_to(titulo_grp, DOWN, buff=0.55)

        obs = self.lista([
            "O gás flui do meio mais concentrado para o menos concentrado",
            "O oceano é um dos principais sumidouros do CO2 atmosférico",
            "Em contrapartida, a absorção aumenta a acidez da água do mar",
        ], font_size=25)
        obs.next_to(bloco_eq, DOWN, buff=0.55)

        #self.play(Write(eq))
        #self.play(FadeIn(legenda))
        self.next_slide()
        #self.play(FadeIn(obs, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 3: dois mecanismos ----
        titulo_grp = self.entrar_titulo("Dois mecanismos de troca oceano-atmosfera", cap)

        # bolhas
        mar1 = Rectangle(width=4.6, height=1.0, color=AZUL_CLARO, fill_color=AZUL_CLARO,
                          fill_opacity=0.35, stroke_width=0)
        bolhas = VGroup(*[
            Circle(radius=0.10, color=AZUL_PRINCIPAL, stroke_width=2)
            for _ in range(6)
        ])
        for i, b in enumerate(bolhas):
            b.move_to(mar1.get_center() + UP * (0.15 + 0.12 * i) + RIGHT * (-1.5 + 0.5 * i))
        grupo1 = VGroup(mar1, bolhas)
        titulo1 = Text("1. Bolhas de ar", font_size=24, color=AZUL_ESCURO, weight=BOLD)
        desc1 = Text("Ondas quebram, aprisionam ar\ne liberam gás ao estourar",
                      font_size=20, color=CINZA_TEXTO, line_spacing=1.1)
        bloco1 = VGroup(titulo1, grupo1, desc1).arrange(DOWN, buff=0.25)

        # gotículas
        mar2 = Rectangle(width=4.6, height=1.0, color=AZUL_CLARO, fill_color=AZUL_CLARO,
                          fill_opacity=0.35, stroke_width=0)
        gotas = VGroup(*[
            Dot(radius=0.06, color=AZUL_PRINCIPAL)
            for _ in range(6)
        ])
        for i, g in enumerate(gotas):
            g.move_to(mar2.get_center() + UP * (0.5 + 0.15 * i) + RIGHT * (-1.4 + 0.55 * i))
        seta_vento = Arrow(LEFT * 2 + DOWN * 0.4, RIGHT * 1.6 + DOWN * 0.4,
                            color=LARANJA_DESTAQUE, buff=0)
        grupo2 = VGroup(mar2, gotas)
        titulo2 = Text("2. Gotículas de espuma", font_size=24, color=AZUL_ESCURO, weight=BOLD)
        desc2 = Text("Vento arranca gotículas da crista\ndas ondas (foco deste trabalho)",
                      font_size=20, color=CINZA_TEXTO, line_spacing=1.1)
        bloco2 = VGroup(titulo2, grupo2, desc2).arrange(DOWN, buff=0.25)

        mecanismos = VGroup(bloco1, bloco2).arrange(RIGHT, buff=1.3)
        mecanismos.next_to(titulo_grp, DOWN, buff=0.7)

        #self.play(FadeIn(bloco1, shift=RIGHT * 0.2))
        #self.next_slide()
        #self.play(FadeIn(bloco2, shift=LEFT * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 4: ciclo de vida da gotícula ----
        titulo_grp = self.entrar_titulo("Ciclo de vida de uma gotícula espuma", cap)

        p1 = Dot(color=AZUL_PRINCIPAL, radius=0.14).move_to(LEFT * 5 + DOWN * 1.0)
        p2 = Dot(color=AZUL_PRINCIPAL, radius=0.10).move_to(LEFT * 1.7 + UP * 1.2)
        p3 = Dot(color=AZUL_PRINCIPAL, radius=0.07).move_to(RIGHT * 1.7 + DOWN * 1.0)
        traj = VMobject(color=CINZA_LINHA, stroke_width=2)
        traj.set_points_smoothly([p1.get_center(), p2.get_center(), p3.get_center()])

        t1 = Text("1. Ejeção pelo vento", font_size=20, color=CINZA_TEXTO).next_to(p1, DOWN, buff=0.3)
        t2 = Text("2. Absorve CO2 por difusão\n(raio e temperatura variam)",
                   font_size=20, color=CINZA_TEXTO, line_spacing=1.1).next_to(p2, UP, buff=0.3)
        t3 = Text("3. Retorna ao oceano\ncarregando CO2", font_size=20,
                   color=CINZA_TEXTO, line_spacing=1.1).next_to(p3, DOWN, buff=0.3)

        cena = VGroup(traj, p1, p2, p3, t1, t2, t3)
        cena.next_to(titulo_grp, DOWN, buff=0.7)

        #self.play(Create(traj), FadeIn(p1), FadeIn(p2), FadeIn(p3))
        #self.play(FadeIn(t1))
        #self.play(FadeIn(t2))
        #self.play(FadeIn(t3))
        self.next_slide()

        tempo_vida = MathTex(
            r"\tau_f = \dfrac{H_s}{2\,U_f}",
            font_size=44, color=AZUL_PRINCIPAL,
        )
        legenda2 = Text(
            "τf: tempo de vida    Hs: altura significativa da onda    Uf: velocidade terminal",
            font_size=20, color=CINZA_TEXTO,
        )
        bloco_tf = VGroup(tempo_vida, legenda2).arrange(DOWN, buff=0.3)
        bloco_tf.to_edge(DOWN, buff=0.6)
        #self.play(FadeIn(bloco_tf, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 5: problema multiescala + objetivo ----
        titulo_grp = self.entrar_titulo("O problema central deste trabalho", cap)

        pergunta = self.caixa(
            "Vale a pena simplificar o modelo físico\npara ganhar velocidade computacional?",
            cor=LARANJA_DESTAQUE, fonte=27, largura=9.5,
        )
        pergunta.next_to(titulo_grp, DOWN, buff=0.6)

        comparacao = self.lista([
            "Sistema completo: 3 EDOs acopladas e não lineares (r, T, m)",
            "Sistema simplificado: r(t) e T(t) por fórmulas exponenciais analíticas",
            "Desafio extra: temperatura relaxa ~1000× mais rápido que o raio",
            "     (problema multiescala, τT ≪ τr)",
        ], font_size=24)
        comparacao.next_to(pergunta, DOWN, buff=0.55)

        self.play(FadeIn(pergunta, shift=UP * 0.2))
        self.next_slide()
        self.play(FadeIn(comparacao, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 6: objetivos ----
        titulo_grp = self.entrar_titulo("Objetivo geral", cap)
        objetivo = self.lista([
            "Comparar o sistema completo com a simplificação exponencial",
            "Método base: Euler Explícito (simples e barato por passo)",
            "Referência de alta precisão: SSPRK3 com passo fixo (SCONTROL)",
            "Avaliar o impacto na acurácia e no custo computacional",
        ], font_size=27)
        objetivo.next_to(titulo_grp, DOWN, buff=0.6)
        self.play(FadeIn(objetivo, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        titulo_grp = self.entrar_titulo("Objetivos específicos", cap)
        especificos = self.lista([
            "Estudar a microfísica de gotículas (raio e temperatura de equilíbrio)",
            "Estudar o modelo de difusão de CO2 em superfícies esféricas",
            "Implementar Euler Explícito e o método de referência SSPRK3",
            "Implementar controle por subpassos e passo adaptativo (PID)",
            "Avaliar o sistema simplificado como alternativa ao sistema completo",
            "Comparar acurácia e custo computacional em todos os cenários",
        ], font_size=23)
        especificos.next_to(titulo_grp, DOWN, buff=0.55)
        self.play(FadeIn(especificos, shift=UP * 0.2))
        self.next_slide()
        self.limpar()


# ========================================================================
# CAPÍTULO 2.1 — MICROFÍSICA DAS GOTÍCULAS
# ========================================================================
class MicrofisicaGoticulas(BaseSlide):
    def construct(self):
        cap = "2.1  Microfísica das gotículas"

        # ---- slide 1: variáveis de estado ----
        titulo_grp = self.entrar_titulo("Três variáveis descrevem a gotícula", cap)

        vetor = MathTex(
            r"\mathbf{y}(t) = \big[\,r(t),\; T(t),\; m(t)\,\big]^{\top}",
            font_size=48, color=AZUL_PRINCIPAL,
        )
        vetor.next_to(titulo_grp, DOWN, buff=0.7)

        legenda = self.lista([
            "r(t):  raio da gotícula",
            "T(t):  temperatura da gotícula",
            "m(t):  massa de CO2 dissolvida",
        ], font_size=26)
        legenda.next_to(vetor, DOWN, buff=0.6)

        obs = Text(
            "As três variáveis evoluem de forma acoplada e não linear",
            font_size=22, color=CINZA_LINHA, slant=ITALIC,
        )
        obs.next_to(legenda, DOWN, buff=0.55)

        self.play(Write(vetor))
        self.next_slide()
        self.play(FadeIn(legenda, shift=UP * 0.2))
        self.next_slide()
        self.play(FadeIn(obs))
        self.next_slide()
        self.limpar()

        # ---- slide 2: evolução da temperatura (modelo completo) ----
        titulo_grp = self.entrar_titulo("Evolução da temperatura — modelo completo", cap)

        eq_T = MathTex(
            r"\frac{dT}{dt} = \frac{3}{\rho_s\,c_{ps}\,r^2}"
            r"\Big[\,k_a'\,(T_a - T) + L_v D_w'\,(\rho_v - \rho_{vr})\,\Big]",
            font_size=38, color=AZUL_PRINCIPAL,
        )
        eq_T.next_to(titulo_grp, DOWN, buff=0.8)

        obs_T = self.lista([
            "Troca de calor por condução (com o ar) e por evaporação",
            "k'a, D'w, ρv, ρvr: propriedades físicas ajustadas pela curvatura da gotícula",
            "Fortemente acoplada ao raio r(t)",
        ], font_size=23)
        obs_T.next_to(eq_T, DOWN, buff=0.6)

        self.play(Write(eq_T))
        self.next_slide()
        self.play(FadeIn(obs_T, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 3: aproximação exponencial da temperatura ----
        titulo_grp = self.entrar_titulo("Simplificação: decaimento exponencial", cap)

        eq_Texp = MathTex(
            r"T(t) = T_{eq} + \big(T_i - T_{eq}\big)\,\exp\!\left(-\frac{t}{\tau_T}\right)",
            font_size=42, color=AZUL_PRINCIPAL,
        )
        eq_Texp.next_to(titulo_grp, DOWN, buff=0.8)

        obs_Texp = self.lista([
            "Solução analítica: dispensa integração numérica",
            "Teq: temperatura de equilíbrio (raiz de uma equação quadrática)",
            "τT: tempo característico de relaxação térmica",
            "Proposta por Andreas (1989) como alternativa de baixo custo",
        ], font_size=24)
        obs_Texp.next_to(eq_Texp, DOWN, buff=0.6)

        self.play(Write(eq_Texp))
        self.next_slide()
        self.play(FadeIn(obs_Texp, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 4: evolução do raio (modelo completo) ----
        titulo_grp = self.entrar_titulo("Evolução do raio — modelo completo", cap)

        eq_r = MathTex(
            r"\frac{dr}{dt} = \frac{\zeta(r)}{r\,\eta}\,,\qquad "
            r"\zeta(r) = (f - 1) - Y(r)",
            font_size=38, color=AZUL_PRINCIPAL,
        )
        eq_r.next_to(titulo_grp, DOWN, buff=0.8)

        obs_r = self.lista([
            "f: umidade relativa do ar     η: termo termodinâmico auxiliar",
            "Y(r): efeitos de curvatura (tensão superficial) e de salinidade",
            "Também acoplada à temperatura T(t) por meio de η e Y",
        ], font_size=24)
        obs_r.next_to(eq_r, DOWN, buff=0.6)

        self.play(Write(eq_r))
        self.next_slide()
        self.play(FadeIn(obs_r, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 5: aproximação exponencial do raio ----
        titulo_grp = self.entrar_titulo("Simplificação: decaimento exponencial do raio", cap)

        eq_rexp = MathTex(
            r"r(t) = r_{eq} + \big(r_i - r_{eq}\big)\,\exp\!\left(-\frac{t}{\tau_r}\right)",
            font_size=42, color=AZUL_PRINCIPAL,
        )
        eq_rexp.next_to(titulo_grp, DOWN, buff=0.8)

        obs_rexp = self.lista([
            "Válida sobretudo para t/τr ≤ 1",
            "req: raio de equilíbrio     τr: tempo característico de relaxação do raio",
            "Andreas (1989, p. 28): τT e τr diferem em ≈ 3 ordens de grandeza",
        ], font_size=24)
        obs_rexp.next_to(eq_rexp, DOWN, buff=0.6)

        self.play(Write(eq_rexp))
        self.next_slide()
        self.play(FadeIn(obs_rexp, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 6: raio de equilíbrio via Newton-Raphson ----
        titulo_grp = self.entrar_titulo("Raio de equilíbrio: ζ(r) = 0", cap)

        eq_newton = MathTex(
            r"r_{eq}^{\,n} = r_{eq}^{\,n-1} - \frac{\zeta\big(r_{eq}^{\,n-1}\big)}"
            r"{\zeta'\big(r_{eq}^{\,n-1}\big)}",
            font_size=40, color=AZUL_PRINCIPAL,
        )
        eq_newton.next_to(titulo_grp, DOWN, buff=0.7)

        obs_newton = self.lista([
            "Não há solução analítica: usa-se o Método de Newton-Raphson",
            "Ponto de partida seguro: ri = 1,1 · rig  (10% acima da singularidade física)",
            "Convergência obtida em poucas iterações (n ≈ 8 no exemplo do trabalho)",
        ], font_size=23)
        obs_newton.next_to(eq_newton, DOWN, buff=0.55)

        self.play(Write(eq_newton))
        self.next_slide()
        self.play(FadeIn(obs_newton, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 7: gráfico esquemático de ζ(r) ----
        titulo_grp = self.entrar_titulo("Convergência do método (esquema ilustrativo)", cap)

        eixos = Axes(
            x_range=[0, 10, 2],
            y_range=[-4, 5, 2],
            x_length=8.5,
            y_length=4.3,
            axis_config={"color": CINZA_LINHA, "font_size": 20},
            tips=False,
        )
        eixos.next_to(titulo_grp, DOWN, buff=0.45)

        curva = eixos.plot(
            lambda x: 4.0 / (x - 2.0) - 0.6 if x > 2.3 else -10,
            x_range=[2.4, 9.8],
            color=AZUL_PRINCIPAL,
            use_smoothing=False,
        )
        assintota = DashedLine(
            eixos.c2p(2.0, -4), eixos.c2p(2.0, 5), color=VERMELHO_ALERTA, stroke_width=2,
        )
        linha_zero = DashedLine(
            eixos.c2p(0, 0), eixos.c2p(10, 0), color=CINZA_LINHA, stroke_width=1.5,
        )
        raiz_x = 2.0 + 4.0 / 0.6
        ponto_raiz = Dot(eixos.c2p(raiz_x, 0), color=VERDE_OK, radius=0.09)

        rotulo_sing = Text("rig (limite físico)", font_size=18, color=VERMELHO_ALERTA)
        rotulo_sing.next_to(assintota, UP, buff=0.15)
        rotulo_raiz = Text("req (raiz de ζ)", font_size=18, color=VERDE_OK)
        rotulo_raiz.next_to(ponto_raiz, DOWN + RIGHT, buff=0.15)
        rotulo_curva = MathTex(r"\zeta(r)", font_size=26, color=AZUL_PRINCIPAL)
        rotulo_curva.next_to(eixos.c2p(8.5, 0.3), UP, buff=0.1)

        grafico = VGroup(eixos, curva, assintota, linha_zero, ponto_raiz,
                          rotulo_sing, rotulo_raiz, rotulo_curva)

        self.play(Create(eixos))
        self.play(Create(curva), Create(assintota), Create(linha_zero))
        self.play(FadeIn(rotulo_sing), FadeIn(rotulo_curva))
        self.next_slide()
        self.play(FadeIn(ponto_raiz, scale=1.5), FadeIn(rotulo_raiz))
        self.next_slide()
        self.limpar()


# ========================================================================
# CAPÍTULO 2.2 — MODELO DE DIFUSÃO DE CO2
# ========================================================================
class ModeloDifusao(BaseSlide):
    def construct(self):
        cap = "2.2  Modelo de difusão de CO2"

        # ---- slide 1: equação de difusão de massa ----
        titulo_grp = self.entrar_titulo("Difusão de CO2 na superfície da gotícula", cap)

        eq_m = MathTex(
            r"\frac{dm}{dt} = 4\pi\,r(t)\,D_g^{*}"
            r"\left[\,C_{ar} - \frac{3\,m(t)}{4\pi\,r^3(t)\,H^{*}\,\Re\,T(t)}\,\right]",
            font_size=34, color=AZUL_PRINCIPAL,
        )
        eq_m.next_to(titulo_grp, DOWN, buff=0.8)

        obs_m = self.lista([
            "Modelo de Pruppacher e Klett (2010) para gotícula esférica",
            "D*g: difusão molecular de CO2 modificada pela curvatura",
            "H*: constante de Henry, modificada por dissociação iônica (Weiss, 1974)",
            "Car: concentração de CO2 no ar     Re: constante universal dos gases",
        ], font_size=22)
        obs_m.next_to(eq_m, DOWN, buff=0.6)

        self.play(Write(eq_m))
        self.next_slide()
        self.play(FadeIn(obs_m, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 2: sistema acoplado completo ----
        titulo_grp = self.entrar_titulo("O sistema acoplado (PVI vetorial)", cap)

        pvi = MathTex(
            r"\frac{d\mathbf{y}}{dt} = \mathbf{F}(t, \mathbf{y})\,,"
            r"\qquad \mathbf{y}(0) = \big[r_i,\, T_i,\, m_i\big]^{\top}",
            font_size=36, color=AZUL_PRINCIPAL,
        )
        pvi.next_to(titulo_grp, DOWN, buff=0.8)

        F_vetor = MathTex(
            r"\mathbf{F}(t,\mathbf{y}) = "
            r"\begin{bmatrix} \zeta(r)/(r\,\eta) \\[4pt] "
            r"\dfrac{3}{\rho_s c_{ps} r^2}\big[k_a'(T_a-T) + L_v D_w'(\rho_v-\rho_{vr})\big] "
            r"\\[6pt] 4\pi r D_g^{*}\big[C_{ar} - \tfrac{3m}{4\pi r^3 H^* \Re T}\big] "
            r"\end{bmatrix}",
            font_size=26, color=AZUL_ESCURO,
        )
        F_vetor.next_to(pvi, DOWN, buff=0.55)

        self.play(Write(pvi))
        self.next_slide()
        self.play(FadeIn(F_vetor, shift=UP * 0.15))
        self.next_slide()
        self.limpar()

        # ---- slide 3: existência e unicidade ----
        titulo_grp = self.entrar_titulo("Existência e unicidade da solução", cap)

        obs = self.lista([
            "F(t, y) é contínua e satisfaz a condição de Lipschitz em y",
            "Domínio físico:  r > req > rig > 0,  T > 0,  m ≥ 0",
            "Singularidades (r = 0 e r = rig) ficam fora do domínio físico",
            "Pelo teorema de existência e unicidade, a solução do PVI é única",
        ], font_size=25)
        obs.next_to(titulo_grp, DOWN, buff=0.65)
        self.play(FadeIn(obs, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 4: completo x simplificado ----
        titulo_grp = self.entrar_titulo("Sistema completo × sistema simplificado", cap)

        dados = [
            ["", "Sistema completo", "Sistema simplificado"],
            ["r(t)", "EDO não linear", "Fórmula exponencial analítica"],
            ["T(t)", "EDO não linear", "Fórmula exponencial analítica"],
            ["m(t)", "EDO (integrada numericamente)", "EDO (integrada numericamente)"],
            ["Custo", "Maior (3 EDOs acopladas)", "Menor (1 EDO escalar)"],
        ]
        t = self.tabela(dados, fonte=22, largura_max=12.0, altura_max=4.6)
        t.next_to(titulo_grp, DOWN, buff=0.6)
        self.play(FadeIn(t))
        self.next_slide()
        self.limpar()


# ========================================================================
# CAPÍTULO 2.3 — MÉTODOS NUMÉRICOS
# ========================================================================
class MetodosNumericos(BaseSlide):
    def construct(self):
        cap = "2.3  Métodos numéricos"

        # ---- slide 1: discretização ----
        titulo_grp = self.entrar_titulo("Discretização do tempo", cap)

        malha = MathTex(
            r"t_n = n\,\Delta t\,,\qquad n = 0, 1, \dots, N",
            font_size=42, color=AZUL_PRINCIPAL,
        )
        malha.next_to(titulo_grp, DOWN, buff=0.8)

        obs = self.lista([
            "O intervalo contínuo [0, τf] é substituído por uma malha discreta",
            "yn ≈ y(tn): aproximação numérica da solução exata",
            "Δt fixo, por subpassos ou adaptativo — estratégias da Seção 2.4",
        ], font_size=25)
        obs.next_to(malha, DOWN, buff=0.6)

        self.play(Write(malha))
        self.next_slide()
        self.play(FadeIn(obs, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 2: Euler explícito ----
        titulo_grp = self.entrar_titulo("Método de Euler Explícito", cap)

        eq_euler = MathTex(
            r"\mathbf{y}_{n+1} = \mathbf{y}_n + \Delta t\,\mathbf{F}(t_n, \mathbf{y}_n)",
            font_size=42, color=AZUL_PRINCIPAL,
        )
        eq_euler.next_to(titulo_grp, DOWN, buff=0.75)

        obs_euler = self.lista([
            "Obtido truncando a série de Taylor após o termo linear",
            "Explícito: yn+1 depende apenas de valores já conhecidos em tn",
            "Erro local de truncamento:  O(Δt²)  →  ordem de precisão q = 1",
            "Erro global (acumulado): O(Δt) — reduzir Δt à metade reduz o erro à metade",
        ], font_size=23)
        obs_euler.next_to(eq_euler, DOWN, buff=0.55)

        self.play(Write(eq_euler))
        self.next_slide()
        self.play(FadeIn(obs_euler, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 3: Euler implícito e comparação ----
        titulo_grp = self.entrar_titulo("Euler Implícito × Euler Explícito", cap)

        eq_impl = MathTex(
            r"\mathbf{y}_{n+1} = \mathbf{y}_n + \Delta t\,\mathbf{F}(t_{n+1}, \mathbf{y}_{n+1})",
            font_size=36, color=AZUL_ESCURO,
        )
        eq_impl.next_to(titulo_grp, DOWN, buff=0.7)

        dados = [
            ["", "Euler Explícito", "Euler Implícito"],
            ["Ordem", "1", "1"],
            ["Custo por passo", "Baixo (1 avaliação)", "Alto (resolve sistema não linear)"],
            ["Estabilidade", "Condicional (Δt pequeno)", "Incondicional"],
            ["Uso neste trabalho", "Método principal", "Não utilizado"],
        ]
        t = self.tabela(dados, fonte=20, largura_max=11.7, altura_max=4.0)
        t.next_to(eq_impl, DOWN, buff=0.5)

        self.play(Write(eq_impl))
        self.next_slide()
        self.play(FadeIn(t))
        self.next_slide()
        self.limpar()

        # ---- slide 4: Runge-Kutta - ideia geral ----
        titulo_grp = self.entrar_titulo("Métodos de Runge-Kutta: a ideia", cap)

        obs = self.lista([
            "Euler usa 1 avaliação de F por passo → precisão limitada",
            "Runge-Kutta avalia F em vários pontos intermediários (estágios)",
            "A combinação ponderada desses estágios gera maior precisão",
            "Um método de s estágios é definido por coeficientes aij, bi, ci",
            "(organizados na tabela de Butcher)",
        ], font_size=25)
        obs.next_to(titulo_grp, DOWN, buff=0.65)
        self.play(FadeIn(obs, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 5: RK3 clássico ----
        titulo_grp = self.entrar_titulo("Runge-Kutta de 3ª ordem (RK3 clássico)", cap)

        estagios = MathTex(
            r"""
            \begin{aligned}
            k_1 &= f(t_n, y_n) \\
            k_2 &= f\!\left(t_n + \tfrac{\Delta t}{2},\; y_n + \tfrac{\Delta t}{2} k_1\right) \\
            k_3 &= f\big(t_n + \Delta t,\; y_n - \Delta t\, k_1 + 2\Delta t\, k_2\big)
            \end{aligned}
            """,
            font_size=32, color=AZUL_PRINCIPAL,
        )
        atualizacao = MathTex(
            r"y_{n+1} = y_n + \frac{\Delta t}{6}\big(k_1 + 4k_2 + k_3\big)",
            font_size=32, color=AZUL_ESCURO,
        )
        bloco = VGroup(estagios, atualizacao).arrange(DOWN, buff=0.45)
        bloco.next_to(titulo_grp, DOWN, buff=0.6)

        legenda = Text(
            "k1: início do intervalo   k2: ponto médio (peso 2/3)   k3: fim do intervalo",
            font_size=20, color=CINZA_TEXTO,
        )
        legenda.next_to(bloco, DOWN, buff=0.4)

        self.play(Write(estagios))
        self.next_slide()
        self.play(Write(atualizacao))
        self.play(FadeIn(legenda))
        self.next_slide()
        self.limpar()

        # ---- slide 6: SSPRK3 (referência) ----
        titulo_grp = self.entrar_titulo("SSPRK3 — solução de referência (SCONTROL)", cap)

        ssprk3 = MathTex(
            r"""
            \begin{aligned}
            \mathbf{y}^{(1)} &= \mathbf{y}_n + \Delta t\,\mathbf{F}(\mathbf{y}_n) \\
            \mathbf{y}^{(2)} &= \tfrac{3}{4}\mathbf{y}_n + \tfrac{1}{4}\big(\mathbf{y}^{(1)} + \Delta t\,\mathbf{F}(\mathbf{y}^{(1)})\big) \\
            \mathbf{y}_{n+1} &= \tfrac{1}{3}\mathbf{y}_n + \tfrac{2}{3}\big(\mathbf{y}^{(2)} + \Delta t\,\mathbf{F}(\mathbf{y}^{(2)})\big)
            \end{aligned}
            """,
            font_size=30, color=AZUL_PRINCIPAL,
        )
        ssprk3.next_to(titulo_grp, DOWN, buff=0.6)

        obs_ssprk3 = self.lista([
            "3ª ordem: erro de truncamento local O(Δt⁴), global O(Δt³)",
            "Amplamente usado em modelos atmosféricos (boa estabilidade)",
            "Adotado como SCONTROL: passo fixo Δt = 10⁻⁴ s, sistema completo",
            "Serve de referência de alta precisão para medir os demais erros",
        ], font_size=21)
        obs_ssprk3.next_to(ssprk3, DOWN, buff=0.45)

        self.play(Write(ssprk3))
        self.next_slide()
        self.play(FadeIn(obs_ssprk3, shift=UP * 0.2))
        self.next_slide()
        self.limpar()


# ========================================================================
# CAPÍTULO 2.4 — ESTRATÉGIAS DE AVANÇO NO TEMPO
# ========================================================================
class EstrategiasTempo(BaseSlide):
    def construct(self):
        cap = "2.4  Estratégias de avanço no tempo"

        # ---- slide 1: o problema multiescala ----
        titulo_grp = self.entrar_titulo("Um problema, duas velocidades", cap)

        comparacao = MathTex(
            r"\tau_T \ll \tau_r \qquad (\text{diferença de} \sim 10^3 \text{ vezes})",
            font_size=38, color=AZUL_PRINCIPAL,
        )
        comparacao.next_to(titulo_grp, DOWN, buff=0.8)

        obs = self.lista([
            "Temperatura relaxa quase instantaneamente (processo rápido)",
            "Raio e massa evoluem muito mais lentamente (processo lento)",
            "Usar um único Δt (ditado pela temperatura) desperdiça cálculo",
            "Duas soluções: controle por subpassos e passo adaptativo (PID)",
        ], font_size=24)
        obs.next_to(comparacao, DOWN, buff=0.6)

        self.play(Write(comparacao))
        self.next_slide()
        self.play(FadeIn(obs, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 2: controle por subpassos ----
        titulo_grp = self.entrar_titulo("Controle por subpassos", cap)

        formula = MathTex(r"\delta t = \frac{\Delta t}{M}", font_size=40, color=AZUL_PRINCIPAL)
        formula.next_to(titulo_grp, DOWN, buff=0.55)

        # diagrama temporal
        eixo_rapido = Line(LEFT * 5, RIGHT * 5, color=CINZA_TEXTO)
        marcas = VGroup(*[
            Line(UP * 0.08, DOWN * 0.08, color=CINZA_TEXTO).move_to(eixo_rapido.point_from_proportion(p))
            for p in [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        ])
        rotulo_rapido = Text("Processo rápido — T(t): M subpassos δt", font_size=20, color=AZUL_ESCURO)
        rotulo_rapido.next_to(eixo_rapido, UP, buff=0.35)
        bloco_rapido = VGroup(rotulo_rapido, eixo_rapido, marcas)

        eixo_lento = Line(LEFT * 5, RIGHT * 5, color=CINZA_TEXTO)
        seta_lenta = DoubleArrow(eixo_lento.get_left(), eixo_lento.get_right(),
                                  color=LARANJA_DESTAQUE, buff=0, stroke_width=3)
        rotulo_lento = Text("Processo lento — r(t), m(t): 1 passo macroscópico Δt",
                             font_size=20, color=LARANJA_DESTAQUE)
        rotulo_lento.next_to(eixo_lento, DOWN, buff=0.35)
        bloco_lento = VGroup(seta_lenta, rotulo_lento)

        diagrama = VGroup(bloco_rapido, bloco_lento).arrange(DOWN, buff=1.0)
        diagrama.next_to(formula, DOWN, buff=0.6)

        self.play(Write(formula))
        self.next_slide()
        self.play(Create(eixo_rapido), Create(marcas), FadeIn(rotulo_rapido))
        self.next_slide()
        self.play(GrowArrow(seta_lenta), FadeIn(rotulo_lento))
        self.next_slide()
        self.limpar()

        # ---- slide 3: passo adaptativo (motivação) ----
        titulo_grp = self.entrar_titulo("Passo adaptativo: ajustar Δt à dinâmica", cap)

        obs = self.lista([
            "Fase transiente: a solução varia rápido → precisa de Δt pequeno",
            "Fase de equilíbrio: a solução quase não muda → Δt pode crescer",
            "Um Δt fixo é sempre um compromisso ruim entre as duas fases",
            "Solução: ajustar Δt automaticamente a cada passo (controlador PID)",
        ], font_size=25)
        obs.next_to(titulo_grp, DOWN, buff=0.65)
        self.play(FadeIn(obs, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 4: controlador PID ----
        titulo_grp = self.entrar_titulo("Controlador Proporcional-Integral-Derivativo", cap)

        eq_pid = MathTex(
            r"\Delta t_{n+1} = \left(\frac{e_{n-1}}{e_n}\right)^{k_P}"
            r"\left(\frac{1}{e_n}\right)^{k_I}"
            r"\left(\frac{e_{n-1}^2}{e_n\,e_{n-2}}\right)^{k_D}\,\Delta t_n",
            font_size=32, color=AZUL_PRINCIPAL,
        )
        eq_pid.next_to(titulo_grp, DOWN, buff=0.65)

        eq_erro = MathTex(
            r"e_n = \max(e_r,\, e_T,\, e_m)\,,\qquad "
            r"e_y = \frac{|y_n - y_{n-1}|/|y_n|}{\text{tol}_y}",
            font_size=28, color=AZUL_ESCURO,
        )
        eq_erro.next_to(eq_pid, DOWN, buff=0.5)

        obs = self.lista([
            "Termo proporcional: reage à tendência do erro mais recente",
            "Termo integral: conduz o erro em direção à tolerância",
            "Termo derivativo: antecipa a curvatura do erro (suaviza o ajuste)",
        ], font_size=20)
        obs.next_to(eq_erro, DOWN, buff=0.45)

        self.play(Write(eq_pid))
        self.next_slide()
        self.play(Write(eq_erro))
        self.next_slide()
        self.play(FadeIn(obs, shift=UP * 0.2))
        self.next_slide()
        self.limpar()


# ========================================================================
# CAPÍTULO 3.1-3.2 — IMPLEMENTAÇÃO E VALIDAÇÃO
# ========================================================================
class ImplementacaoSimulacoes(BaseSlide):
    def construct(self):
        cap = "3.  Implementação e Simulações"

        # ---- slide 1: sete experimentos ----
        titulo_grp = self.entrar_titulo("Sete experimentos numéricos", cap)

        dados = [
            ["Experimento", "Método", "Estratégia de passo", "Sistema"],
            ["SCONTROL", "SSPRK3", "Fixo", "Completo"],
            ["ECONTROL", "Euler Explícito", "Fixo", "Completo"],
            ["E1", "Euler Explícito", "Subpassos", "Completo"],
            ["E2", "Euler Explícito", "PID (adaptativo)", "Completo"],
            ["E3", "Euler Explícito", "Fixo", "Simplificado"],
            ["E4", "Euler Explícito", "Subpassos", "Simplificado"],
            ["E5", "Euler Explícito", "PID (adaptativo)", "Simplificado"],
        ]
        t = self.tabela(dados, fonte=21, largura_max=12.3, altura_max=5.2)
        t.next_to(titulo_grp, DOWN, buff=0.5)
        self.play(FadeIn(t))
        self.next_slide()

        obs = self.lista([
            "SCONTROL: referência de alta precisão (não é comparado a si mesmo)",
            "ECONTROL × SCONTROL → isola o erro de truncamento do Euler",
            "E1/E2 × ECONTROL → efeito das estratégias de passo (sistema completo)",
            "E3/E4/E5 → efeito da simplificação exponencial",
        ], font_size=20)
        obs.next_to(t, DOWN, buff=0.4)
        self.play(FadeIn(obs, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 2: cenários de raio inicial ----
        titulo_grp = self.entrar_titulo("Dois cenários extremos de raio inicial", cap)

        gota_pequena = Circle(radius=0.35, color=AZUL_PRINCIPAL, fill_color=AZUL_PRINCIPAL,
                               fill_opacity=0.5)
        texto_pequena = Text("ri = 30 μm\ndinâmica rápida\ne fortemente não linear",
                              font_size=22, color=CINZA_TEXTO, line_spacing=1.2)
        bloco_pequena = VGroup(gota_pequena, texto_pequena).arrange(DOWN, buff=0.4)

        gota_grande = Circle(radius=0.9, color=AZUL_PRINCIPAL, fill_color=AZUL_PRINCIPAL,
                              fill_opacity=0.5)
        texto_grande = Text("ri = 500 μm\ndinâmica lenta\ne suave",
                             font_size=22, color=CINZA_TEXTO, line_spacing=1.2)
        bloco_grande = VGroup(gota_grande, texto_grande).arrange(DOWN, buff=0.4)

        cenarios = VGroup(bloco_pequena, bloco_grande).arrange(RIGHT, buff=1.8)
        cenarios.next_to(titulo_grp, DOWN, buff=0.9)

        self.play(FadeIn(bloco_pequena, shift=RIGHT * 0.2))
        self.next_slide()
        self.play(FadeIn(bloco_grande, shift=LEFT * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 3: escolha do passo de referência ----
        titulo_grp = self.entrar_titulo("Escolhendo o Δt de referência", cap)

        obs = self.lista([
            "Δt = 10⁻² s:  instável — E1 e E4 (subpassos) divergem (massa vira NaN)",
            "Δt = 10⁻³ s:  estável, mas mascara o ganho do PID (poucos pontos de sobra)",
            "Δt = 10⁻⁴ s:  escolha final — estável e evidencia a economia do PID",
        ], font_size=24)
        obs.next_to(titulo_grp, DOWN, buff=0.7)

        for linha in obs:
            self.play(FadeIn(linha, shift=RIGHT * 0.15))
        self.next_slide()

        nota = Text(
            "Nas Figuras usa-se Δt = 10⁻⁵ s apenas para suavizar visualmente as curvas\n"
            "(não altera os resultados quantitativos, obtidos com 10⁻⁴ s)",
            font_size=18, color=CINZA_LINHA, slant=ITALIC, line_spacing=1.2,
        )
        nota.next_to(obs, DOWN, buff=0.6)
        self.play(FadeIn(nota))
        self.next_slide()
        self.limpar()

        # ---- slide 4: validação numérica ----
        titulo_grp = self.entrar_titulo("Validação: comparação com Andreas (2005)", cap)

        dados_val = [
            ["Parâmetro", "Andreas (2005)", "Simulação realizada"],
            ["Temperatura de equilíbrio (Teq)", "17,08 °C", "17,07 °C"],
            ["Raio de equilíbrio (req)", "61,44 μm", "62,28 μm"],
            ["Tempo de relaxação térmica (τT)", "0,176 s", "0,177 s"],
            ["Tempo de decaimento do raio (τr)", "303 s", "304,30 s"],
        ]
        t = self.tabela(dados_val, fonte=21, largura_max=12.3, altura_max=4.2)
        t.next_to(titulo_grp, DOWN, buff=0.6)
        self.play(FadeIn(t))
        self.next_slide()

        conclusao = Text(
            "Resultados praticamente idênticos aos da literatura → implementação validada",
            font_size=22, color=VERDE_OK, weight=BOLD,
        )
        conclusao.next_to(t, DOWN, buff=0.5)
        self.play(FadeIn(conclusao, shift=UP * 0.2))
        self.next_slide()
        self.limpar()


# ========================================================================
# CAPÍTULO 3.3-3.4 — RESULTADOS E DISCUSSÃO
# ========================================================================
class Resultados(BaseSlide):
    def construct(self):
        cap = "4.  Resultados e Discussão"

        # ---- slide 1: eficiência computacional - ri = 30 micrômetros ----
        titulo_grp = self.entrar_titulo("Eficiência computacional — ri = 30 μm", cap)

        dados_30 = [
            ["Exp.", "Pontos", "T. real (s)", "T. user (s)", "T. sys (s)", "CPU (%)"],
            ["SCONTROL", "265 950", "9,041", "9,17", "0,90", "111"],
            ["ECONTROL", "265 950", "2,984", "3,25", "0,89", "138"],
            ["E1", "26 597", "2,068", "2,32", "0,90", "155"],
            ["E2", "8 702", "0,414", "0,68", "0,78", "353"],
            ["E3", "265 950", "1,395", "1,56", "0,83", "171"],
            ["E4", "26 597", "0,443", "0,74", "0,85", "358"],
            ["E5", "10 052", "0,362", "0,60", "0,75", "375"],
        ]
        t30 = self.tabela(dados_30, fonte=19, largura_max=12.5, altura_max=5.3)
        t30.next_to(titulo_grp, DOWN, buff=0.4)
        self.play(FadeIn(t30))
        self.next_slide()
        self.limpar()

        # ---- slide 2: eficiência computacional - ri = 500 micrômetros ----
        titulo_grp = self.entrar_titulo("Eficiência computacional — ri = 500 μm", cap)

        dados_500 = [
            ["Exp.", "Pontos", "T. real (s)", "T. user (s)", "T. sys (s)", "CPU (%)"],
            ["SCONTROL", "7 223", "0,544", "0,80", "0,85", "304"],
            ["ECONTROL", "7 223", "0,388", "0,67", "0,88", "400"],
            ["E1", "724", "0,361", "0,62", "0,91", "423"],
            ["E2", "107", "0,309", "0,58", "0,89", "475"],
            ["E3", "7 223", "0,348", "0,62", "0,90", "434"],
            ["E4", "724", "0,312", "0,57", "0,91", "472"],
            ["E5", "96", "0,313", "0,60", "0,88", "472"],
        ]
        t500 = self.tabela(dados_500, fonte=19, largura_max=12.5, altura_max=5.3)
        t500.next_to(titulo_grp, DOWN, buff=0.4)
        self.play(FadeIn(t500))
        self.next_slide()
        self.limpar()

        # ---- slide 3: discussão da eficiência ----
        titulo_grp = self.entrar_titulo("O que as tabelas mostram", cap)

        obs = self.lista([
            "SSPRK3 (SCONTROL) custa ≈ 3× mais que Euler (ECONTROL) por passo",
            "     — 3 avaliações do sistema por passo, contra apenas 1 do Euler",
            "Subpassos (E1) reduzem bastante o nº de pontos macroscópicos",
            "Sistema simplificado (E3) mantém os pontos mas reduz o custo por passo",
            "PID (E2 e E5) é sempre o mais econômico: concentra esforço",
            "     onde a dinâmica realmente varia",
        ], font_size=22)
        obs.next_to(titulo_grp, DOWN, buff=0.6)
        for linha in obs:
            self.play(FadeIn(linha, shift=RIGHT * 0.12), run_time=0.4)
        self.next_slide()
        self.limpar()

        # ---- slide 4: acurácia numérica ----
        titulo_grp = self.entrar_titulo("Erro relativo final (referência: SCONTROL)", cap)

        eq_erro = MathTex(
            r"\epsilon_f = \left|\frac{m_{\text{num}}(\tau_f) - m_{\text{ref}}(\tau_f)}"
            r"{m_{\text{ref}}(\tau_f)}\right|",
            font_size=34, color=AZUL_PRINCIPAL,
        )
        eq_erro.next_to(titulo_grp, DOWN, buff=0.5)

        dados_erro = [
            ["Experimento", "εf  (ri = 30 μm)", "εf  (ri = 500 μm)"],
            ["ECONTROL", "4,94 × 10⁻⁷", "1,23 × 10⁻⁷"],
            ["E1", "5,08 × 10⁻⁶", "1,41 × 10⁻⁵"],
            ["E2", "1,69 × 10⁻⁵", "9,06 × 10⁻⁶"],
            ["E3", "1,36 × 10⁻¹", "3,43 × 10⁻⁴"],
            ["E4", "1,36 × 10⁻¹", "3,29 × 10⁻⁴"],
            ["E5", "1,36 × 10⁻¹", "3,45 × 10⁻⁴"],
        ]
        t = self.tabela(dados_erro, fonte=21, largura_max=11.5, altura_max=4.4)
        t.next_to(eq_erro, DOWN, buff=0.4)

        self.play(Write(eq_erro))
        self.next_slide()
        self.play(FadeIn(t))
        self.next_slide()

        linhas_simplificado = VGroup(t.get_rows()[4], t.get_rows()[5], t.get_rows()[6])
        self.play(linhas_simplificado.animate.set_color(VERMELHO_ALERTA))
        destaque = Text(
            "Erro de 5 ordens de grandeza maior para gotas pequenas\n"
            "com o sistema simplificado (E3, E4, E5)",
            font_size=20, color=VERMELHO_ALERTA, weight=BOLD, line_spacing=1.2,
        )
        destaque.next_to(t, DOWN, buff=0.4)
        self.play(FadeIn(destaque, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 5: interpretação ----
        titulo_grp = self.entrar_titulo("De onde vem cada erro?", cap)

        card1 = self.caixa(
            "Erro de truncamento do Euler\n(ECONTROL, E1, E2)\n\n10⁻⁷ a 10⁻⁵\nDESPREZÍVEL",
            cor=VERDE_OK, fonte=22, largura=4.6,
        )
        card2 = self.caixa(
            "Erro da simplificação física\n(E3, E4, E5)\n\naté 1,36 × 10⁻¹\nCRÍTICO em gotas pequenas",
            cor=VERMELHO_ALERTA, fonte=22, largura=4.6,
        )
        cards = VGroup(card1, card2).arrange(RIGHT, buff=1.0)
        cards.next_to(titulo_grp, DOWN, buff=0.8)

        self.play(FadeIn(card1, shift=RIGHT * 0.2))
        self.next_slide()
        self.play(FadeIn(card2, shift=LEFT * 0.2))
        self.next_slide()

        conclusao = Text(
            "A perda de acurácia vem da física simplificada, não do integrador numérico",
            font_size=24, color=AZUL_ESCURO, weight=BOLD,
        )
        conclusao.next_to(cards, DOWN, buff=0.7)
        self.play(FadeIn(conclusao, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 6: esquema ilustrativo - gota pequena ----
        titulo_grp = self.entrar_titulo("Esquema ilustrativo — gota pequena (30 μm)", cap)
        sub = Text("(diagrama conceitual; não reproduz os dados numéricos exatos)",
                    font_size=18, color=CINZA_LINHA, slant=ITALIC)
        sub.next_to(titulo_grp, DOWN, buff=0.15)

        eixos1 = Axes(
            x_range=[0, 10, 5], y_range=[0, 1, 0.5],
            x_length=5.6, y_length=3.1,
            axis_config={"include_ticks": False, "color": CINZA_LINHA},
            tips=False,
        )
        titulo_eixo1 = Text("Temperatura T(t)", font_size=18, color=CINZA_TEXTO)
        titulo_eixo1.next_to(eixos1, UP, buff=0.15)
        curva_completa1 = eixos1.plot(lambda x: 0.15 + 0.8 * np.exp(-x), color=AZUL_PRINCIPAL)
        curva_simples1 = eixos1.plot(lambda x: 0.35 + 0.6 * np.exp(-x), color=VERMELHO_ALERTA,
                                      x_range=[0, 10])
        bloco1 = VGroup(titulo_eixo1, eixos1, curva_completa1, curva_simples1)

        eixos2 = Axes(
            x_range=[0, 10, 5], y_range=[0, 1, 0.5],
            x_length=5.6, y_length=3.1,
            axis_config={"include_ticks": False, "color": CINZA_LINHA},
            tips=False,
        )
        titulo_eixo2 = Text("Massa de CO2  m(t)", font_size=18, color=CINZA_TEXTO)
        titulo_eixo2.next_to(eixos2, UP, buff=0.15)
        curva_completa2 = eixos2.plot(lambda x: 0.1 + 0.85 * (1 - np.exp(-0.4 * x)), color=AZUL_PRINCIPAL)
        curva_simples2 = eixos2.plot(lambda x: 0.1 + 0.55 * (1 - np.exp(-0.4 * x)), color=VERMELHO_ALERTA)
        bloco2 = VGroup(titulo_eixo2, eixos2, curva_completa2, curva_simples2)

        graficos = VGroup(bloco1, bloco2).arrange(RIGHT, buff=0.8)
        graficos.next_to(sub, DOWN, buff=0.35)

        legenda_azul = VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color=AZUL_PRINCIPAL, stroke_width=4),
                               Text("Sistema completo", font_size=18, color=CINZA_TEXTO)
                               ).arrange(RIGHT, buff=0.2)
        legenda_verm = VGroup(Line(LEFT * 0.3, RIGHT * 0.3, color=VERMELHO_ALERTA, stroke_width=4),
                               Text("Sistema simplificado", font_size=18, color=CINZA_TEXTO)
                               ).arrange(RIGHT, buff=0.2)
        legenda = VGroup(legenda_azul, legenda_verm).arrange(RIGHT, buff=0.8)
        legenda.next_to(graficos, DOWN, buff=0.35)

        self.play(FadeIn(sub))
        self.play(Create(eixos1), Create(eixos2), FadeIn(titulo_eixo1), FadeIn(titulo_eixo2))
        self.play(Create(curva_completa1), Create(curva_completa2))
        self.next_slide()
        self.play(Create(curva_simples1), Create(curva_simples2), FadeIn(legenda))
        self.next_slide()

        obs_final = Text(
            "A curva simplificada (vermelha) se afasta da curva completa (azul):\n"
            "a aproximação exponencial subestima a temperatura final da gota pequena",
            font_size=20, color=CINZA_TEXTO, line_spacing=1.2,
        )
        obs_final.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(obs_final))
        self.next_slide()
        self.limpar()

        # ---- slide 7: passo adaptativo - colapso do PID ----
        titulo_grp = self.entrar_titulo("PID com sistema simplificado: um alerta", cap)

        obs = self.lista([
            "Para gotas pequenas, o controlador de E5 aumenta Δt rapidamente",
            "     (pois a exponencial 'acha' que T varia pouco)",
            "Quando a queda real de T se acentua, o erro local dispara",
            "     e o PID é forçado a reduzir Δt bruscamente (colapso do passo)",
            "O PID de E2 (sistema completo) não sofre esse colapso:",
            "     acompanha a dinâmica real de forma contínua",
        ], font_size=22)
        obs.next_to(titulo_grp, DOWN, buff=0.6)
        for linha in obs:
            self.play(FadeIn(linha, shift=RIGHT * 0.12), run_time=0.4)
        self.next_slide()

        nota = Text(
            "O colapso do passo não corrige o problema: só sinaliza que o modelo\n"
            "simplificado deixou de ser adequado para aquele regime físico",
            font_size=20, color=LARANJA_DESTAQUE, weight=BOLD, line_spacing=1.2,
        )
        nota.next_to(obs, DOWN, buff=0.5)
        self.play(FadeIn(nota, shift=UP * 0.2))
        self.next_slide()
        self.limpar()


# ========================================================================
# CAPÍTULO 4 — CONCLUSÕES
# ========================================================================
class Conclusoes(BaseSlide):
    def construct(self):
        cap = "5.  Conclusões"

        # ---- slide 1: síntese dos erros ----
        titulo_grp = self.entrar_titulo("Duas fontes de erro, dois pesos muito diferentes", cap)

        obs = self.lista([
            "Erro de truncamento do Euler Explícito: desprezível em ambos os cenários",
            "Erro da simplificação exponencial: grande, sobretudo em gotas pequenas",
            "Conclusão: a perda de acurácia vem da física simplificada,",
            "     não da escolha de um integrador numérico mais simples",
        ], font_size=25)
        obs.next_to(titulo_grp, DOWN, buff=0.65)
        for linha in obs:
            self.play(FadeIn(linha, shift=RIGHT * 0.15), run_time=0.4)
        self.next_slide()
        self.limpar()

        # ---- slide 2: custo computacional ----
        titulo_grp = self.entrar_titulo("Custo computacional", cap)

        obs = self.lista([
            "Euler Explícito é mais barato que o SSPRK3 no sistema completo",
            "     (1 avaliação do sistema por passo, contra 3)",
            "Entre as estratégias de avanço, o controle PID adaptativo",
            "     é sempre o mais econômico",
            "O PID concentra o esforço computacional apenas onde a",
            "     dinâmica realmente varia",
        ], font_size=24)
        obs.next_to(titulo_grp, DOWN, buff=0.6)
        for linha in obs:
            self.play(FadeIn(linha, shift=RIGHT * 0.15), run_time=0.4)
        self.next_slide()
        self.limpar()

        # ---- slide 3: recomendação final ----
        titulo_grp = self.entrar_titulo("Recomendação final", cap)

        destaque = self.caixa(
            "E2\n\nEuler Explícito + Sistema Completo\n+ Controle Adaptativo PID",
            cor=VERDE_OK, fonte=30, largura=8.5,
        )
        destaque.next_to(titulo_grp, DOWN, buff=0.7)

        motivos = self.lista([
            "Preserva a acurácia física do sistema completo",
            "É o mais rápido entre os experimentos com sistema completo",
            "Dispensa a simplificação exponencial em qualquer cenário de raio",
        ], font_size=23)
        motivos.next_to(destaque, DOWN, buff=0.55)

        self.play(FadeIn(destaque, scale=0.9))
        self.next_slide()
        self.play(FadeIn(motivos, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

        # ---- slide 4: contribuições ----
        titulo_grp = self.entrar_titulo("Contribuições deste trabalho", cap)

        obs = self.lista([
            "Implementação validada do modelo de Pruppacher e Klett (2010)",
            "Comparação sistemática entre sistema completo e simplificado",
            "Quantificação separada do erro numérico e do erro de modelagem",
            "Evidência de que o controle PID é a estratégia mais eficiente",
            "     sem custo de acurácia",
        ], font_size=24)
        obs.next_to(titulo_grp, DOWN, buff=0.6)
        for linha in obs:
            self.play(FadeIn(linha, shift=RIGHT * 0.15), run_time=0.4)
        self.next_slide()
        self.limpar()

        # ---- slide final: agradecimentos ----
        texto = Text("Obrigado!", font_size=72, color=AZUL_PRINCIPAL, weight=BOLD)
        subtexto = Text("Perguntas são bem-vindas", font_size=30, color=CINZA_TEXTO)
        bloco = VGroup(texto, subtexto).arrange(DOWN, buff=0.5)
        bloco.move_to(ORIGIN + UP * 0.6)

        self.play(Write(texto))
        self.play(FadeIn(subtexto, shift=UP * 0.2))
        self.next_slide()

        text_nome = MathTex(r"\text{Emanuel Pinto Sampaio}", font_size=60, color=AZUL_ESCURO)
        text_nome.next_to(bloco, DOWN, buff=0.9)
        self.play(FadeIn(text_nome, shift=UP * 0.2))
        self.next_slide()
        self.limpar()

