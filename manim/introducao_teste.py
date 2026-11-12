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
AZUL_PRINCIPAL = "#002aff"
AZUL_ESCURO = BLUE_E
AZUL_CLARO = BLUE_C
CINZA_TEXTO = "#000000"
CINZA_LINHA = "#9A9A9A"
VERDE_OK = "#1E8449"
VERMELHO_ALERTA = "#B03A2E"
LARANJA_DESTAQUE = "#CA6F1E"

FONTE_TITULO = 40
FONTE_SUBTITULO = 30
FONTE_CORPO = 27
FONTE_PEQUENA = 22
FONTE_TABELA = 55



class BaseSlide(MovingCameraScene,Slide):
    """Classe base com métodos utilitários usados por todos os capítulos."""

    def setup(self):
        super().setup()
        self.camera.background_color = WHITE

    def construct(self):
        # BaseSlide não é uma cena real — isso é só uma rede de segurança
        # caso ela seja renderizada por engano (via -a ou seletor interativo).
        self.wait(0.1)

    # ---------------- layout ----------------
    def titulo(self, texto, cor=CINZA_TEXTO, tamanho=FONTE_TITULO):
        t = Text(texto, font_size=tamanho, color=cor, weight=BOLD)
        t.to_edge(UP, buff=0.45)
        linha = Line(LEFT, RIGHT, color=AZUL_PRINCIPAL, stroke_width=3)
        linha.set_width(13.5)
        linha.next_to(t, DOWN, buff=0.18)
        return VGroup(t, linha)
 
    def rotulo_capitulo(self, texto):
        r = MathTex(texto, font_size=16, color=CINZA_LINHA)
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
            linha = VGroup(marcador, txt).arrange(RIGHT, buff=0.18)
            grupo.add(linha)
        grupo.arrange(DOWN, aligned_edge=LEFT, buff=buff)
        return grupo
        

    def tabela(self, dados, fonte=FONTE_TABELA, cor_cabecalho=AZUL_ESCURO,
               largura_max=12.3, altura_max=5.4):
        t = MathTable(
            dados,
            include_outer_lines=True,
            line_config={"stroke_width": 1.5, "color": CINZA_LINHA},
            element_to_mobject=MathTex,
            element_to_mobject_config={"font_size": fonte, "color": CINZA_TEXTO},
        )
        t.get_rows()[0].set_color("#002aff")
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
# CAPÍTULO 1 — INTRODUÇÃO
# ========================================================================
class Introducao(BaseSlide):
    def construct(self):
        cap = r"\text{4. Tempo Computacional e Acurácia}"
        # slide 1
        titulo_grp = self.entrar_titulo("Passo de Tempo Adaptativo com Controlador PID", cap) 


        # ------------------------------------------------------------
        # 2) Equação do controlador PID, construída termo a termo
        # ------------------------------------------------------------
        eq_pid = MathTex(
            r"\Delta t_{n+1} =",
            r"\left( \dfrac{e_{n-1}}{e_{n}} \right)^{k_P}",
            r"\left( \dfrac{1}{e_{n}} \right)^{k_I}",
            r"\left( \dfrac{e_{n-1}^{2}}{e_{n}\, e_{n-2}} \right)^{k_D}",
            r"\Delta t_{n}",
            font_size=55, color=CINZA_TEXTO,
        )
        eq_pid.move_to(ORIGIN).shift(1.6 * UP)


        self.play(Write(eq_pid))
        self.next_slide()

        label_P = MathTex(r"\text{Proporcional}", font_size=30, color="#ff0000")
        label_I = MathTex(r"\text{Integral}", font_size=30, color="#108500")
        label_D = MathTex(r"\text{Derivativo}", font_size=30, color="#2b00ff")
        label_P.next_to(eq_pid[1], DOWN, buff=0.9)
        label_I.next_to(eq_pid[2], DOWN, buff=0.9)
        label_D.next_to(eq_pid[3], DOWN, buff=0.9)

        seta_P = Arrow(eq_pid[1].get_bottom(), label_P.get_top(),
                        buff=0.08, color="#ff0000", stroke_width=2.5,
                        max_tip_length_to_length_ratio=0.15)
        seta_I = Arrow(eq_pid[2].get_bottom(), label_I.get_top(),
                        buff=0.08, color="#108500", stroke_width=2.5,
                        max_tip_length_to_length_ratio=0.15)
        seta_D = Arrow(eq_pid[3].get_bottom(), label_D.get_top(),
                        buff=0.08, color="#2b00ff", stroke_width=2.5,
                        max_tip_length_to_length_ratio=0.15)
        self.play(FadeTransform(eq_pid[1],eq_pid[1].set_color("#ff0000")),GrowArrow(seta_P), Write(label_P))
        self.play(FadeTransform(eq_pid[2],eq_pid[2].set_color("#108500")),GrowArrow(seta_I), Write(label_I))
        self.play(FadeTransform(eq_pid[3],eq_pid[3].set_color("#2b00ff")),GrowArrow(seta_D), Write(label_D))
        self.wait(0.3)
        self.next_slide()


        grupo_pid = VGroup(label_P, label_I, label_D,
                            seta_P, seta_I, seta_D )
        self.play(FadeOut(grupo_pid),FadeTransform(eq_pid,eq_pid.set_color("#000000")))

        # ------------------------------------------------------------
        # 3) Definição do erro relativo
        # ------------------------------------------------------------
        eq_en = MathTex(
            r"e_n = \max(e_r,\, e_T,\, e_m)",
            font_size=42, color=CINZA_TEXTO,
        ).next_to(eq_pid,DOWN,buff=0.8)

        eq_ey = MathTex(
            r"e_y = \dfrac{e_y^{\ast}}{\mathrm{tol}_y}",
            r"\, , \qquad",
            r"e_y^{\ast} = \dfrac{\left| y_{n} - y_{n-1} \right|}{\left| y_{n} \right|}",
            font_size=36, color=CINZA_TEXTO,
        ).next_to(eq_en, DOWN, buff=0.8)

        self.play(Write(eq_en))
        self.play(Write(eq_ey))

        nota_erro = self.lista([
            r"y \in \{r, T, m\} \text{: raio, temperatura e massa de CO}_2\text{ dissolvida.}",
            r"\text{O máximo garante que a variável mais rápida controle o passo.}",
        ], font_size=36, largura=11.2)
        nota_erro.next_to(eq_ey, DOWN, buff=0.6)
        self.play(Write(nota_erro))
        self.wait(0.3)
        self.next_slide()

        grupo_erro = VGroup(eq_en, eq_ey, nota_erro)
        self.next_slide()
 
        # ------------------------------------------------------------
        # 4) Parâmetros do controlador
        # ------------------------------------------------------------


        dados = [
            [r"\text{Parâmetro}", r"\text{Valor}"],
            [r"k_P", "0,075"],
            [r"k_I", "0,175"],
            [r"k_D", "0,01"],
        ]
        tab = self.tabela(dados, largura_max=5.5, altura_max=3.4).scale(1.2)
        tab.shift(8*DOWN)
        self.camera.frame.save_state()
        fig3 = ImageMobject("passo_adaptativo_pid.png").scale(0.4).shift(8*DOWN)

        self.play(self.camera.frame.animate.move_to(8 * DOWN),FadeIn(fig3))
        self.wait(0.3)
        self.next_slide()
        self.play(Restore(self.camera.frame))


        self.limpar()
        self.next_slide()