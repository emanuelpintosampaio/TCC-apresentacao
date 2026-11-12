
""" manim -qh tcc_slides.py Titulo Agenda Introducao 

    manim-slides convert Titulo Agenda Introducao apresentacao.html

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
        r = MathTex(texto, font_size=22, color=CINZA_LINHA)
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
            r"\textbf{Avaliação de Simplificações do Modelo Físico e}",
            font_size=45, color=CINZA_TEXTO
        )

        titulo_tcc2 = MathTex(
            r"\textbf{Métodos de Integração Temporal Aplicados à}",
            font_size=45, color=CINZA_TEXTO,
        )

        titulo_tcc3 = MathTex(
            r"\textbf{Difusão de Gás em Gotículas Marinha}",
            font_size=45, color=CINZA_TEXTO,
        )



        titulo_tcc = VGroup(titulo_tcc1,titulo_tcc2,titulo_tcc3).arrange(DOWN, buff=0.15)
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
        self.play(FlashFade(titulo_tcc1,mode="IN", **kwargs),FlashFade(titulo_tcc2,mode="IN", **kwargs),FlashFade(titulo_tcc3,mode="IN", **kwargs))

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
                    r"\textbf{1.  Motivação e Introdução}",
                    r"\textbf{2.  Fundamentação Teórica}",
                    r"\textbf{3.  Modelo Completo vs Modelo Simplificado}",
                    r"\,\,\,\text{    3.1  Modelo de difusão de C}\text{O}_2",
                    r"\,\,\,\text{    3.2  Modelo de difusão de C}\text{O}_2 \text{ Simplificado}",
                    r"\,\,\,\text{    3.3  Métodos numéricos (Euler e Runge-Kutta)}",
                    r"\,\,\,\text{    3.4  Resultados}",
                    r"\textbf{4.  Tempo Computacional e Acurácia}",
                    r"\,\,\,\text{    4.1  Estratégias de avanço no tempo}",
                    r"\,\,\,\text{    4.2  Resultados}",
                    r"\textbf{5.  Conclusões}"
                ]
        grupo = self.lista(itens, font_size=32, buff=0.30)
        grupo.next_to(titulo_grp, DOWN, buff=0.35).to_edge(LEFT, buff=1.2)

        for linha in grupo:
            self.play(FadeIn(linha, shift=RIGHT * 0.15), run_time=0.35)
        self.next_slide()
        self.limpar()
# ========================================================================
# CAPÍTULO 1 — INTRODUÇÃO
# ========================================================================
class Introducao(BaseSlide):
    def construct(self):
        cap = r"\text{1. Motivação e Introdução}"
 
        # slide 1
        titulo_grp = self.entrar_titulo("A Importância do Gás Carbônico na Atmosfera", cap)
        texto = self.lista([
            r"\text{Regulação Térmica}"], font_size=40)
        texto.to_edge(LEFT).shift(0.2*LEFT)
        fig = ImageMobject("fig1.png").scale(0.8).to_corner(DR)
        border = SurroundingRectangle(
            fig,
            color=AZUL_PRINCIPAL,          # ou YELLOW, BLUE, etc.
            buff=0.0001,            # pequena margem ao redor
            stroke_width=3,       # grossura da borda
            stroke_opacity=1
        )
        fig2 = ImageMobject("fig2.png").scale(0.8).to_corner(DR)


        self.play(Write(texto))
        self.play(FlashFade(border, width=5, opacity=1, lag_ratio=0.4, duration=2),FadeIn(fig))
        self.play(FadeIn(border))
        self.next_slide()
        self.limpar()

        # slide 2
        titulo_grp = self.entrar_titulo("O Papel dos Oceanos", cap)
        texto = self.lista([
            r"\text{Sumidouros de C}\text{O}_2"], font_size=37)
        texto.to_edge(LEFT).shift(2.25*UP+0.4*LEFT)
        fig3 = ImageMobject("fig3.png").scale(0.8).to_corner(DR)
        border = SurroundingRectangle(
            fig3,
            color=AZUL_PRINCIPAL,          # ou YELLOW, BLUE, etc.
            buff=0.0001,            # pequena margem ao redor
            stroke_width=3,       # grossura da borda
            stroke_opacity=1
        )
        texto2 = self.lista([
            r"\text{Como a Troca Acontece}"], font_size=37)
        texto2.to_edge(LEFT).shift(0.4*LEFT)

        texto3 = MathTex(r"F = k \Delta c", font_size=47,color=CINZA_TEXTO).next_to(texto2,DOWN,buff=0.4)

        texto4 = self.lista([
            r"\text{Bolhas e Gotículas}"], font_size=37)
        texto4.to_edge(LEFT).shift(3*DOWN + 0.4*LEFT)
        fig4 = ImageMobject("fig4.png").scale(0.8).to_corner(DR)
        fig5 = ImageMobject("fig5.png").scale(0.8).to_corner(DR)


        self.play(Write(texto))
        self.play(FlashFade(border, width=5, opacity=1, lag_ratio=0.4, duration=2),FadeIn(fig3))
        self.play(FadeIn(border))
        self.next_slide()
        self.play(Write(texto2))
        self.play(Write(texto3), FadeOut(border))
        self.play(FlashFade(border, width=5, opacity=1, lag_ratio=0.4, duration=2),ReplacementTransform(fig3,fig4))
        self.play(FadeIn(border))
        self.next_slide()
        self.play(Write(texto4), FadeOut(border))
        self.play(FlashFade(border, width=5, opacity=1, lag_ratio=0.4, duration=2),ReplacementTransform(fig4,fig5))
        self.play(FadeIn(border))
        self.next_slide()
        self.limpar()

        

        cap = r"\text{2. Fundamentação Teórica}"
        # slide 1
        titulo_grp = self.entrar_titulo("Microfísica das Gotículas Espuma", cap)
        
        vetor = MathTex(
            r"\mathbf{y}(t) = ",r"\big[\,r(t),\; T(t),\; m(t)\,\big]^{\top}",
            font_size=60,color=CINZA_TEXTO
        )
        vetor[1][1:5].set_color_by_gradient("#0065ff")
        vetor[1][6:10].set_color_by_gradient("#0065ff")
        vetor[1][11:15].set_color_by_gradient("#0065ff")

        vetor.next_to(titulo_grp, DOWN, buff=0.7)

        legenda = self.lista([
            r"r(t)\text{:  raio da gotícula}",
            r"T(t)\text{:  temperatura da gotícula}",
            r"m(t)\text{:  massa de C}\text{O}_2 \text{ dissolvida}",
        ], font_size=45,largura=20)
        legenda.set_color("#0065ff")

        legenda.next_to(vetor, DOWN, buff=1)

        grp = VGroup(legenda)

        fig6 = ImageMobject("fig6.png").scale(0.8).to_corner(DR)
        border = SurroundingRectangle(
            fig6,
            color=AZUL_PRINCIPAL,          # ou YELLOW, BLUE, etc.
            buff=0.0001,            # pequena margem ao redor
            stroke_width=3,       # grossura da borda
            stroke_opacity=1
        )

        self.play(Write(legenda.shift(UP * 0.2+0.5*RIGHT)))

        self.play(grp.animate.shift(5.3*LEFT).scale(0.65))
        self.play(FlashFade(border, width=5, opacity=1, lag_ratio=0.4, duration=2),FadeIn(fig6))
        self.play(FadeIn(border))

        self.next_slide()

        self.limpar()

        cap = r"\text{3. Modelo Completo vs Modelo Simplificado}"
        # slide 1
        titulo_grp = self.entrar_titulo("Modelo de Difusão de CO₂ em Gotículas Espuma", cap)
        texto = self.lista([
            r"\text{Modelo de difusão em superfícies esféricas (} \textbf{Pruppacher e Klett (2010)}\text):}"],font_size= 39,largura=20)
        texto.to_edge(LEFT).shift(2.25*UP+0.4*LEFT)


        texto1 = MathTex(
            r"""
            \begin{cases}
                \dfrac{dm(t)}{dt}
                = 4\pi r(t) D_g^*
                \left(
                    C_{ar} - \dfrac{3m(t)}{4\,\pi \, r^3(t) \, H^* \, \Re \, T(t)} \right)
                \\[12pt]
                \dfrac{dr(t)}{dt}
                = \dfrac{\zeta}{r(t)\,\eta}
                \\[12pt]
                \dfrac{dT(t)}{dt} = \dfrac{3}{\rho_s \, c_{ps} \, r^2(t)}
                \left[ k'_a (T_a - T(t)) + L_{v} D'_{w} (\rho_{v} - \rho_{vr}) \right]
            \end{cases}
            """,
            font_size=55,
            color=CINZA_TEXTO,
        ).shift(1*DOWN)

        linha1 = MathTex(
            r"D_g^* \text{ é o coeficiente de difusão do CO}_2\text{, }"
            r"C_{ar} \text{ é a concentração de CO}_2\text{ no ar,}",
            font_size=40,
            color=CINZA_TEXTO
        ).shift(DOWN)

        linha2 = MathTex(
            r"H^* \text{ é a constante da lei Henry e }"
            r"\Re \text{ é a constante universal dos gases.}",
            font_size=40,
            color=CINZA_TEXTO
        ).next_to(linha1, DOWN, aligned_edge=LEFT, buff=0.2) 
        txtdmdt = VGroup(linha1,linha2)

        texto2 = self.lista([
            r"\text{Equação de evolução do raio de gotículas salinas (}}\textbf{Andreas (2005)}\text):}"],font_size= 39,largura=20)
        texto2.next_to(texto,DOWN,buff=3).shift(0.58*LEFT)
        texto3 = MathTex(r"\dfrac{d r(t)}{ d t}",r" =",r" \dfrac{\zeta}{r(t) \, \eta};", font_size=45,color=CINZA_TEXTO).shift(2.6*DOWN)
        texto4 = MathTex(r"\zeta = (f - 1) - \frac{2 M_w \sigma_{s}}{RT_{a} \rho_w r(t)} - \frac{v_{\text{ion}} \Phi_s m_s}{\left(4 \pi r^3(t) \rho_s /3\right) - m_s} \left( \frac{M_w}{M_s} \right);", font_size=45,color=CINZA_TEXTO).next_to(texto3,DOWN,buff=0.8)
        texto5 = MathTex(r"\eta = \frac{\rho_s RT_{a}}{D'_w M_w e_{\text{sat}}(T_{a})} + \frac{\rho_s L_v}{K'_a T_{a}} \left( \frac{L_v M_w}{RT_{a}} - 1 \right);", font_size=45,color=CINZA_TEXTO).next_to(texto3,DOWN,buff=0.8)
        

        self.play(Write(texto))
        self.play(Write(texto1[0][19:63].set_color_by_gradient("#000000")))
        #m
        #self.play(ReplacementTransform(texto1[0][20:24],texto1[0][20:24].set_color_by_gradient("#002aff")),ReplacementTransform(texto1[0][43:47],texto1[0][43:47].set_color_by_gradient("#002aff")))
        self.play(Write(txtdmdt))
        self.wait(0.5)
        self.next_slide()
        #r
        self.play(FadeOut(txtdmdt))
        #self.play(ReplacementTransform(texto1[0][30:34],texto1[0][30:34].set_color_by_gradient("#002aff")),ReplacementTransform(texto1[0][50:55],texto1[0][50:55].set_color_by_gradient("#002aff")),)
        self.play(Write(texto2))
        self.play(Indicate(texto1[0][30:34],scale_factor=1.5,color=["#002aff"]))
        self.play(TransformFromCopy(texto1[0][30:34],texto3))
        self.next_slide()
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.shift(4.5 * DOWN))
        self.play(Indicate(texto3[3][0:1],scale_factor=1.5,color=["#002aff"]))
        self.play(TransformFromCopy(texto3[3][0:1],texto4),)
        

        linha1 = MathTex(
            r"f \text{ é a umidade relativa, }"
            r"M_w \text{ é a massa molar da água, }"
            r"\sigma_s \text{ é a tensão superficial,}",
            font_size=33,
            color=CINZA_TEXTO
        ).next_to(texto4,DOWN,buff=0.8).shift(1*LEFT)

        linha2 = MathTex(
            r"R \text{ é a constante universal dos gases, }"
            r"T_a \text{ é a temperatura do ar, }"
            r"\rho_w \text{ é a densidade da água,}",
            font_size=33,
            color=CINZA_TEXTO
        ).next_to(linha1, DOWN, aligned_edge=LEFT, buff=0.2)

        linha3 = MathTex(
            r"v_{\mathrm{ion}} \text{ é o número de íons por molécula dissociada, }"
            r"\Phi_s \text{ é o coeficiente osmótico,}",
            font_size=33,
            color=CINZA_TEXTO
        ).next_to(linha2, DOWN, aligned_edge=LEFT, buff=0.2)

        linha4 = MathTex(
            r"m_s \text{ é a massa de sal dissolvido, }"
            r"\rho_s \text{ é a densidade da gotícula e }"
            r"M_s \text{ é a massa molar do NaCl.}",
            font_size=33,
            color=CINZA_TEXTO
        ).next_to(linha3, DOWN, aligned_edge=LEFT, buff=0.2)

        grp1 = VGroup(linha1, linha2, linha3, linha4)
        grp2 = VGroup(grp1,texto4)
        self.play(Write(grp1))
        self.wait(0.5)
        self.next_slide()
        self.play(FadeOut(grp2))


        linha11 = MathTex(
            r"\rho_s \text{ é a densidade da gotícula, }"
            r"R \text{ é a constante universal dos gases, }"
            r"T_a \text{ é a temperatura do ar,}",
            font_size=33,
            color=CINZA_TEXTO
        ).next_to(texto5,DOWN,buff=0.8)

        linha22 = MathTex(
            r"D_w^\text{'} \text{ é a difusividade modificada do vapor de água, }"
            r"M_w \text{ é a massa molar da água,}",
            font_size=33,
            color=CINZA_TEXTO
        ).next_to(linha11, DOWN, aligned_edge=LEFT, buff=0.2)

        linha33 = MathTex(
            r"e_{\mathrm{sat}} \text{ é a pressão de vapor de saturação, }"
            r"L_v \text{ é o calor latente de vaporização e }",
            font_size=33,
            color=CINZA_TEXTO
        ).next_to(linha22, DOWN, aligned_edge=LEFT, buff=0.2)

        linha44 = MathTex(
            r"k_a^\text{'} \text{ é a condutividade térmica modificada do ar.}",
            font_size=33,
            color=CINZA_TEXTO
        ).next_to(linha33, DOWN, aligned_edge=LEFT, buff=0.2)

        grp11 = VGroup(linha11, linha22, linha33,linha44)
        self.play(Indicate(texto3[3][6:7],scale_factor=1.5,color=["#002aff"]))

        self.play(TransformFromCopy(texto3[3][6:7],texto5))
        grp3 = VGroup(grp11,texto5,texto2)
        self.play(Write(grp11))
        self.wait(0.5)
        self.next_slide()
        self.play(Restore(self.camera.frame))
        self.play(FadeOut(grp3),FadeTransform(texto3,texto1[0][63:79]))



        texto6 = self.lista([
            r"\text{Para a temperatura da gotícula, a evolução temporal é determinada por }"],font_size= 39,largura=20)
        texto6.next_to(texto,DOWN,buff=4.2).shift(0.38*LEFT)
        texto7 = MathTex(r"\textbf{Pruppacher e Klett (1978)}\text{:}",color= CINZA_TEXTO,font_size= 39).next_to(texto6,DOWN,buff=0.3).shift(3.5*LEFT)
        texto8 = MathTex(r"\frac{dT(t)}{dt} = \frac{3}{\rho_s \, c_{ps} \, r^2(t)}\left[ k'_a (T_a - T(t)) + L_{v} D'_{w} (\rho_{v} - \rho_{vr}) \right]", font_size=50,color=CINZA_TEXTO).shift(5.5*DOWN)
        self.play(Write(texto6))
        self.play(Write(texto7))
        self.next_slide()
        self.play(Indicate(texto1[0][58:62],scale_factor=1.5,color=["#002aff"]))
        self.play(TransformFromCopy(texto1[0][58:62],texto8))
        self.play(self.camera.frame.animate.shift(5.8 * DOWN))

        linha111 = MathTex(
            r"\rho_s \text{ é a densidade da gotícula, }"
            r"c_{ps} \text{ é o calor específico da gotícula, }"
            ,
            font_size=35,
            color=CINZA_TEXTO
        ).next_to(texto8, DOWN, buff=1.5).shift(1.7*LEFT)

        linha222 = MathTex(
            r"k_a^\text{'} \text{ é a condutividade térmica modificada do ar, }"
            r"T_a \text{ é a temperatura do ar, }"
            ,
            font_size=35,
            color=CINZA_TEXTO
        ).next_to(linha111, DOWN, aligned_edge=LEFT, buff=0.2)

        linha333 = MathTex(
            r"L_v \text{ é o calor latente de vaporização, }"
            r"D_w^\text{'} \text{ é a difusividade modificada do vapor de água,}",
            font_size=35,
            color=CINZA_TEXTO
        ).next_to(linha222, DOWN, aligned_edge=LEFT, buff=0.2)

        linha444 = MathTex(
            r"\rho_v \text{ é a densidade de vapor no ar e }"
            r"\rho_{vr} \text{ é a densidade de vapor na superfície da gotícula.}",
            font_size=35,
            color=CINZA_TEXTO
        ).next_to(linha333, DOWN, aligned_edge=LEFT, buff=0.2)

        grpp = VGroup(linha111, linha222, linha333, linha444)
        self.play(Write(grpp))
        grp4 = VGroup(grpp,texto6,texto7)
        self.next_slide()
        self.wait(0.5)
        self.play(Restore(self.camera.frame),FadeOut(grp4),FadeTransform(texto8,texto1[0][79:129]),Write(texto1[0][0:19]))
        self.wait(0.5)
        self.next_slide()
        self.play(self.camera.frame.animate.shift(8 * DOWN))

        # slide 1
        
        textoo = MathTex(
            r"""
            \begin{cases}
            \dfrac{d\mathbf{y}(t)}{dt}
            =
            \mathbf{F}(t,\mathbf{y}),
            \qquad
            t\in[0,\tau_f]
            \\[6pt]
            \mathbf{y}(t_0)=\mathbf{y}_0
            \end{cases}
            """,
            font_size=55,
            color=CINZA_TEXTO,
        ).shift(5.5*DOWN)

        vetory = MathTex(
            r"\mathbf{y}(t) = \big[m(t),\; r(t),\; T(t)\big]^{\top}",
            font_size=55, color=CINZA_TEXTO).next_to(textoo,DOWN,buff=0.8)
        
        vetory0 = MathTex(
            r"\mathbf{y}_0 = [m_i,\; r_i,\; T_i]^\top",
            font_size=55, color=CINZA_TEXTO).next_to(vetory,DOWN,buff=0.8)
        
        vectorF = MathTex(
            r"""
            \mathbf{F}(t,\mathbf{y})=
            \begin{bmatrix}
                4\pi\,r(t)\,D_g^*
                \left(
                    C_{ar}
                    -
                    \dfrac{3m(t)}
                    {4\pi\,r^3(t)\,H^*\,\Re\,T(t)}
                \right)
                \\[12pt]
                \dfrac{\zeta}{r(t)\,\eta}
                \\[12pt]
                \dfrac{3}
                {\rho_s\,c_{ps}\,r^2(t)}
                \left[
                    k'_a\left(T_a-T(t)\right)
                    +
                    L_vD'_w
                    \left(
                        \rho_v-\rho_{vr}
                    \right)
                \right]
            \end{bmatrix}
            """,
            font_size=50,
            color=CINZA_TEXTO,
        ).next_to(vetory0, DOWN, buff=0.8)

        texto2 = MathTex(r'\tau_f',r'=',r'\frac{H_s}{2\,U_f}',font_size=50,color=CINZA_TEXTO).next_to(textoo, DOWN, buff=2.3)
        texto3 = MathTex(r'U_f',r' =',r'\frac{2\,r_i^2\,g}{9\,\nu_{ar}\!\left[1 + 0{,}158\!\left(\dfrac{2\,r_i\,U_f}{\nu_{ar}}\right)^{2/3}\right]}\!\left(\frac{\rho_w}{\rho_a} - 1\right)',font_size=50,color=CINZA_TEXTO).next_to(texto2, DOWN, buff=1.2)
        texto34= MathTex(r'U_f',r' -',r'\frac{2\,r_i^2\,g}{9\,\nu_{ar}\!\left[1 + 0{,}158\!\left(\dfrac{2\,r_i\,U_f}{\nu_{ar}}\right)^{2/3}\right]}\!\left(\frac{\rho_w}{\rho_a} - 1\right)',r'=',r'0',font_size=50,color=CINZA_TEXTO).next_to(texto2, DOWN, buff=1.2)
        texto34[0].set_color_by_gradient("#002aff")
        texto34[2][22:24].set_color_by_gradient("#002aff")

        texto6 = self.lista([
            r"\text{O tempo de vida da gotícula, é estimado por } \textbf{Gonçalves e Innocentini (2018)}\text{:}"],font_size= 35,largura=20)
        texto6.next_to(textoo,DOWN,buff=0.8)

        #dy/dt = [0][5:20]
        self.play(Write(textoo))
        self.wait(1)
        self.play(Indicate(textoo[0][4:8],scale_factor=1.5,color=["#002aff"]))
        self.play(TransformFromCopy(textoo[0][4:8],vetory))
        self.play(Indicate(textoo[0][33:35],scale_factor=1.5,color=["#002aff"]))
        self.play(TransformFromCopy(textoo[0][33:35],vetory0))
        self.next_slide()
        self.play(Indicate(textoo[0][12:18],scale_factor=1.5,color=["#002aff"]))
        self.play(self.camera.frame.animate.shift(4 * DOWN),TransformFromCopy(textoo[0][12:18],vectorF))
        self.next_slide()
        grp1 = VGroup(vectorF,vetory0,vetory)
        self.play(self.camera.frame.animate.shift(4*UP),FadeOut(grp1))
        self.play(Write(texto6))
        self.play(Indicate(textoo[0][24:26],scale_factor=1.5,color=["#002aff"]))
        self.play(TransformFromCopy(textoo[0][24:26],texto2))
        self.next_slide()
        self.play(Indicate(texto2[2][4:6],scale_factor=1.5,color=["#002aff"]))

        self.play(self.camera.frame.animate.shift(3 * DOWN),TransformFromCopy(texto2[2][4:6],texto3))
        self.wait(0.5)
        self.play(ReplacementTransform(texto3[0],texto3[0].set_color_by_gradient("#002aff")),
                  ReplacementTransform(texto3[2][22:24],texto3[2][22:24].set_color_by_gradient("#002aff")))
        self.wait(0.5)
        self.play(FadeTransform(texto3,texto34))
        self.next_slide()
        grp12=VGroup(texto34,texto2,texto6,textoo)
        self.play(FadeOut(grp12), Restore(self.camera.frame))
        self.next_slide()
        self.play(self.camera.frame.animate.shift(8 * DOWN))

        text8 = self.lista([
            r"\textbf{Andreas (1989) }\text{propôs aproximar a evolução temporal do raio e da}"],font_size= 40,largura=20)
        text8.next_to(texto1,DOWN,buff=0.9).shift(0.38*LEFT)
        texto9 = MathTex(r"\text{temperatura por um decaimento exponencial:}",color= CINZA_TEXTO,font_size= 40).next_to(texto1,DOWN,buff=1.5).shift(2.5*LEFT)
        texto10 = MathTex(r"\dfrac{r(t)-r_{eq}}{\left(r_i-r_{eq}\right)}=\exp\left(-\dfrac{t}{\tau_r}\right),",color= CINZA_TEXTO,font_size= 55).next_to(texto1,DOWN,buff=3.5)
        texto1010 = MathTex(r"r(t) = r_{\mathrm{eq}} + \left(r_i - r_{\mathrm{eq}}\right)\exp\!\left(-\dfrac{t}{\tau_r}\right),",color= CINZA_TEXTO,font_size= 55).next_to(texto1,DOWN,buff=3.5)
        texto11 = MathTex(r"\dfrac{T(t)-T_{eq}}{\left(T_i-T_{eq}\right)}",r"=",r"\exp\left(-\dfrac{t}{\tau_T}\right).",color= CINZA_TEXTO,font_size= 55).shift(1.5*DOWN).next_to(texto10,DOWN,buff=1)
        texto1111 = MathTex(r"T(t) = T_{\mathrm{eq}} + \left(T_i - T_{\mathrm{eq}}\right)\exp\!\left(-\dfrac{t}{\tau_T}\right).",color= CINZA_TEXTO,font_size= 55).next_to(texto10,DOWN,buff=1)


        self.play(Write(text8))
        self.play(Write(texto9))
        self.play(Write(texto10))
        self.play(Write(texto11))
        self.next_slide()
        self.play(FadeTransform(texto10,texto1010),FadeTransform(texto11,texto1111))
        self.next_slide()

        texto12 = MathTex(
            r"""
            \begin{cases}
                \dfrac{dm(t)}{dt}
                = 4\pi r(t) D_g^*
                \left(
                    C_{ar} - \dfrac{3m(t)}{4\,\pi \, r^3(t) \, H^* \, \Re \, T(t)} \right)
                \\[12pt]
                r(t) = r_{\mathrm{eq}} + \left(r_i - r_{\mathrm{eq}}\right)\exp\!\left(-\dfrac{t}{\tau_r}\right)
                \\[12pt]
                T(t) = T_{\mathrm{eq}} + \left(T_i - T_{\mathrm{eq}}\right)\exp\!\left(-\dfrac{t}{\tau_T}\right)
            \end{cases}
            """,
            font_size=55,
            color=CINZA_TEXTO,
        ).next_to(texto1,DOWN,buff=2.8)
        self.play(Write(texto12[0][0:63]), FadeTransform(texto1010,texto12[0][63:90]),FadeTransform(texto1111,texto12[0][90:]))
        self.wait(0.5)
        self.next_slide()
        grp5 = VGroup(text8,texto9,texto)
        self.play(self.camera.frame.animate.scale(1.9).shift(4.4*UP),FadeOut(grp5),texto1.animate,texto12.animate.shift(0.5*UP))

        mdlcplt = MathTex(r'\textbf{Modelo Completo}',font_size=65, color=CINZA_TEXTO).next_to(texto1,UP,buff=0.5)
        mdlsimpl = MathTex(r'\textbf{Modelo Simplificado}',font_size=65, color=CINZA_TEXTO).next_to(texto12,UP,buff=0.5)
        bluess = ["#002aff",]   
        reds = ["#ff0000", ]        

        kwargsa = dict(color=bluess, width=3, duration=2.5)
        kwargsv = dict(color=reds, width=3, duration=2.5)

        self.play(FlashFade(mdlcplt,mode="IN", **kwargsa),FlashFade(mdlsimpl,mode="IN", **kwargsv))
        self.next_slide()
        self.limpar()
        self.play(Restore(self.camera.frame))





        cap = r"\text{3. Modelo Completo vs Modelo Simplificado}"
        # slide 1
        titulo_grp = self.entrar_titulo("Runge-Kutta de 3ª ordem (SSPRK3)", cap) 
        eq1 = MathTex(
            r"\mathbf{y}_{n+1}",
            r"=",
            r"\mathbf{y}_n}",r"+",r"\Delta t\,",r"\left(\dfrac{1}{6}k_1 + \dfrac{1}{6}k_2 + \dfrac{2}{3}k_3\right) ",
            font_size=55,
            color=CINZA_TEXTO,
                ).shift(1.6*UP)


        k1 = MathTex(
            r"k_1",
            r"=",
            r"\mathbf{F}(t_n,\;y_n)",
            font_size=55,
            color=CINZA_TEXTO,
                )

        k2 = MathTex(
            r"k_2",
            r"=",
            r"\mathbf{F}\!\left(t_n+\Delta t,\;y_n+\Delta t\,k_1\right)",
            font_size=55,
            color=CINZA_TEXTO,
                )

        k3 = MathTex(
            r"k_3",
            r"=",
            r"\mathbf{F}\!\left(t_n+\dfrac{\Delta t}{2},\;y_n+\dfrac{\Delta t}{4}\,k_1+\dfrac{\Delta t}{4}\,k_2\right)",
            font_size=55,
            color=CINZA_TEXTO,
                )

        txt = VGroup(k1, k2, k3).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.35,
        ).next_to(eq1,DOWN,buff=0.7)
        self.play(Write(eq1))
        self.wait(0.5)
        self.play(Indicate(eq1[5][4:6],scale_factor=1.5,color=["#002aff"]),
                  Indicate(eq1[5][10:12],scale_factor=1.5,color=["#002aff"]),
                  Indicate(eq1[5][16:18],scale_factor=1.5,color=["#002aff"]))
        self.play(TransformFromCopy(eq1[5][4:6],txt[0]),
                  TransformFromCopy(eq1[5][10:12],txt[1]),
                  TransformFromCopy(eq1[5][16:18],txt[2]))
        self.camera.frame.save_state()


        ax = Axes(
            x_range = [-.5, 5],
            y_range = [-0.5, 5],
            x_length = 8,
            y_length = 5,
        ).set_color_by_gradient("#000000").shift(7.5*DOWN)

        def func(t):
            return t**2/4

        func_plot = ax.plot(
            lambda t: func(t),
            color = "#24F000"
        )
        self.next_slide()
        self.play(self.camera.frame.animate.shift(7 * DOWN))
        self.play(Write(ax), Write(func_plot))


        # SSPRK3 avalia em t_i, t_i + Δt/2 e t_i + Δt, os mesmos 3 pontos do eixo,
        # mas na ordem t_i -> t_i+Δt -> t_i+Δt/2: k2 usa o passo cheio e k3 volta
        # para o ponto médio, ao contrário do RK3 clássico.
        t_labels = VGroup(
            MathTex("t_i",color=CINZA_TEXTO).scale(0.6).move_to(ax.c2p(2, -0.5, 0)),
            MathTex("t_i + \\Delta t/2",color=CINZA_TEXTO).scale(0.6).move_to(ax.c2p(3, -0.5, 0)),
            MathTex("t_i + \\Delta t",color=CINZA_TEXTO).scale(0.6).move_to(ax.c2p(4, -0.5, 0))
        )
        self.play(Write(t_labels))

        # --------------------------------------------------------------
        # Estágios do SSPRK3 calculados exatamente pelas fórmulas:
        #   k1 = F(t_n, y_n)
        #   k2 = F(t_n + Δt, y_n + Δt * k1)
        #   k3 = F(t_n + Δt/2, y_n + Δt/4*k1 + Δt/4*k2)
        # com F(t, y) = t/2, a derivada da própria curva y(t) = t²/4.
        # --------------------------------------------------------------
        def f(t, y):
            return t / 2

        t_n, y_n = 2, func(2)
        dt = 2

        k1 = f(t_n, y_n)

        t2, y2 = t_n + dt, y_n + dt * k1
        k2 = f(t2, y2)

        t3, y3 = t_n + dt/2, y_n + dt/4*k1 + dt/4*k2
        k3 = f(t3, y3)

        y_next = y_n + dt/6 * (k1 + k2) + dt * 2/3 * k3  # = 4.0, exatamente func(4)

        start = ax.c2p(t_n, y_n)
        k2_point = ax.c2p(t2, y2)
        k3_point = ax.c2p(t3, y3)

        points = [start, k2_point, k3_point]

        dots = VGroup(
            *[Dot(color="#002aff").move_to(point) for point in points]
        )

        initial_label = MathTex("(t_i, y_i)").next_to(dots[0], UL).set_color("#002aff")

        connecting_lines = VGroup()
        for i in range(1, len(dots)):
            connecting_lines.add(
                DashedLine(
                    start = dots[0].get_center(),
                    end = dots[i].get_center()
                ).set_color("#FF0000")
            )

        line_labels = VGroup(
            MathTex("k_1").scale(0.6).next_to(dots[0], DR, buff = 0.1),
            MathTex("k_2").scale(0.6).next_to(dots[1], RIGHT, buff = 0.15),
            MathTex("k_3").scale(0.6).next_to(dots[2], DR, buff = 0.1),
        ).set_color("#FF0000")

        # Cada tangente é construída a partir de dois pontos em espaço de
        # dados (t0 ± Δ, y0 ± slope*Δ) convertidos via ax.c2p, garantindo
        # que a inclinação visual corresponda exatamente à inclinação
        # numérica de cada k_i (sem distorção pela razão de aspecto dos eixos).
        def tangente(t0, y0, slope, meia_largura=0.35):
            p1 = ax.c2p(t0 - meia_largura, y0 - slope*meia_largura)
            p2 = ax.c2p(t0 + meia_largura, y0 + slope*meia_largura)
            return Line(p1, p2).set_color("#FF0000")

        k1_line = Line(
            start = dots[0].get_center() - 0.3 * (dots[1].get_center() - dots[0].get_center()),
            end = dots[0].get_center() + 0.3 * (dots[1].get_center() - dots[0].get_center())
        ).set_color("#FF0000")

        slope_lines = VGroup(
            k1_line,                    # k1: o próprio passo de Euler já tem essa inclinação
            tangente(t2, y2, k2),       # k2: avaliado no passo cheio, t_i + Δt
            tangente(t3, y3, k3),       # k3: avaliado de volta no ponto médio
        )

        final_point = Dot(color = "#002aff").scale(1.2).move_to(ax.c2p(t_n + dt, y_next - 0.07))
        final_connection = Line(
            start = dots[0].get_center(),
            end = final_point.get_center()
        ).set_color("#002aff")
        final_label = MathTex("(t_{i+1}, y_{i+1})").next_to(final_point, DR).set_color("#002aff")

        #Animating
        self.wait(1)

        self.play(Create(dots[0]),Create(slope_lines[0]), Write(initial_label),Indicate(t_labels[0],scale_factor=1.5,color=["#002aff"]))
        self.wait(1)
        self.play(Create(connecting_lines[0]), Write(line_labels[0]))
        self.wait(1)

        # k2: salta para t_i + Δt (índice 2 em t_labels)
        self.play(Indicate(t_labels[2],scale_factor=1.5,color=["#002aff"]),Create(dots[1]))
        self.play(Create(slope_lines[1]), Write(line_labels[1]))
        self.wait()
        self.play(
            ReplacementTransform(slope_lines[1].copy(), connecting_lines[1])
        )
        self.wait()


        # k3: volta para t_i + Δt/2 (índice 1 em t_labels)
        self.play(Indicate(t_labels[1],scale_factor=1.5,color=["#002aff"]),Create(dots[2]))
        self.play(Create(slope_lines[2]), Write(line_labels[2]))
        self.wait()
        grp1 = VGroup(line_labels,slope_lines,dots[1],dots[2])

        self.play(
            *[Transform(mob, final_connection) for mob in connecting_lines],FadeOut(grp1)
        )
        self.wait()
        self.play(Create(final_point), Write(final_label))
        self.wait()
        self.next_slide()
        self.play(Restore(self.camera.frame))
        self.next_slide()
        self.limpar()

        cap = r"\text{3. Modelo Completo vs Modelo Simplificado}"
        # slide 1
        titulo_grp = self.entrar_titulo("Euler Explícito", cap) 
        eq1 = MathTex(r"\mathbf{y}_{n+1}",r" =",r"\mathbf{y}_n",r"+",r"\Delta t\,",r"\mathbf{F}(t_n,\,\mathbf{y}_n)",
            font_size=55,
            color=CINZA_TEXTO,
        ).shift(2*UP)

        self.play(Write(eq1))
        self.wait()

        self.next_slide()
        self.camera.frame.save_state()


        ax = Axes(
            x_range = [-.5, 5],
            y_range = [-0.5, 5],
            x_length = 8,
            y_length = 5,
        ).set_color_by_gradient("#000000").shift(2.1*DOWN)

        def func(t):
            return t**2/4

        func_plot = ax.plot(
            lambda t: func(t),
            color = "#24F000"
        )
        self.next_slide()
        self.play(self.camera.frame.animate.shift(1 * DOWN))
        self.play(Write(ax), Write(func_plot))

        # Euler Explícito avalia a derivada em um único ponto, t_i, e usa essa
        # inclinação constante para projetar diretamente até t_i + Δt.
        # Diferente do SSPRK3, não existem avaliações intermediárias: apenas
        # os dois pontos do eixo, sem o ponto médio.
        t_labels = VGroup(
            MathTex("t_i", color=CINZA_TEXTO).scale(0.6).move_to(ax.c2p(2, -0.5, 0)),
            MathTex("t_i + \\Delta t", color=CINZA_TEXTO).scale(0.6).move_to(ax.c2p(4, -0.5, 0))
        )
        self.play(Write(t_labels))

        # --------------------------------------------------------------
        # Euler Explícito:
        #   k1 = F(t_n, y_n)
        #   y_{n+1} = y_n + Δt * k1
        # com F(t, y) = t/2, a derivada da própria curva y(t) = t²/4.
        # --------------------------------------------------------------
        def f(t, y):
            return t / 2

        t_n, y_n = 2, func(2)
        dt = 2

        k1 = f(t_n, y_n)

        y_next = y_n + dt * k1  # aproximação de Euler (linear), com erro em relação a func(4)

        start = ax.c2p(t_n, y_n)

        dot_start = Dot(color="#002aff").move_to(start)

        initial_label = MathTex("(t_i, y_i)").next_to(dot_start, UL).set_color("#002aff")

        k1_label = MathTex("k_1").scale(0.6).next_to(dot_start, DR, buff=0.1).set_color("#FF0000")

        # Mesma técnica do k1_line/tangente no SSPRK3: a reta nasce centrada
        # no ponto (t_i, y_i), com um pedaço "antes" e outro "depois" do ponto,
        # reforçando que k1 é uma inclinação (tangente à curva), e não um
        # segmento que já sai esticado em direção ao próximo ponto.
        def tangente(t0, y0, slope, meia_largura=0.35):
            p1 = ax.c2p(t0 - meia_largura, y0 - slope*meia_largura)
            p2 = ax.c2p(t0 + meia_largura, y0 + slope*meia_largura)
            return Line(p1, p2).set_color("#FF0000")

        k1_tangent = tangente(t_n, y_n, k1)

        # Só depois a tangente curta se estende até virar o passo completo de
        # Euler, de (t_i, y_i) até (t_i + Δt, y_{i+1}). Diferente do SSPRK3,
        # essa reta É a própria conexão final: não há combinação de múltiplas
        # inclinações, apenas uma única projeção linear.
        euler_line = DashedLine(
            start = start,
            end = ax.c2p(t_n + dt, y_n + dt * k1)
        ).set_color("#FF0000")

        uler_line2 = Line(
            start = start,
            end = ax.c2p(t_n + dt, y_n + dt * k1)
        ).set_color("#002aff")

        final_point = Dot(color="#002aff").scale(1.2).move_to(ax.c2p(t_n + dt, y_next))
        final_label = MathTex("(t_{i+1}, y_{i+1})").next_to(final_point, DR).set_color("#002aff")

        # Segmento pontilhado evidenciando o erro de truncamento local: a
        # distância vertical entre a aproximação de Euler e a curva exata em t_i+Δt.
        error_line = DashedLine(
            start = ax.c2p(t_n + dt, y_next),
            end = ax.c2p(t_n + dt, func(t_n + dt))
        ).set_color(GRAY)

        error_label = MathTex("\\text{erro local}", color=GRAY).scale(0.5).next_to(error_line, RIGHT, buff=0.1)

        # --------------------------------------------------------------
        # Só para efeito de comparação: a partir do mesmo (t_i, y_i) e
        # reaproveitando o k1 já calculado, completamos os estágios do
        # SSPRK3 (k2, k3) e marcamos onde ele chegaria em t_i + Δt. Como as
        # três inclinações se combinam de forma a cancelar o erro de
        # truncamento (ver Acurácia Numérica), o ponto do SSPRK3 cai
        # praticamente em cima da curva exata, ao contrário do Euler
        # Explícito, cujo erro já foi evidenciado pela error_line.
        #   k2 = F(t_n + Δt, y_n + Δt * k1)
        #   k3 = F(t_n + Δt/2, y_n + Δt/4*k1 + Δt/4*k2)
        # --------------------------------------------------------------
        t2, y2 = t_n + dt, y_n + dt * k1
        k2 = f(t2, y2)

        t3, y3 = t_n + dt/2, y_n + dt/4*k1 + dt/4*k2
        k3 = f(t3, y3)

        y_next_rk3 = y_n + dt/6 * (k1 + k2) + dt * 2/3 * k3  # praticamente exato, = func(4)

        final_point_rk3 = Dot(color="#7300FF").scale(1.2).move_to(ax.c2p(t_n + dt, y_next_rk3))
        final_label_rk3 = MathTex("\\text{SSPRK3}", color="#7300FF").scale(0.5).next_to(final_point_rk3, UR, buff=0.15)

        # A reta azul representa o passo efetivo do SSPRK3, do ponto inicial
        # até o ponto final, na mesma convenção de cor do final_connection
        # do código original: k1/k2/k3 individuais em vermelho, mas o passo
        # combinado (a "trajetória" de fato) em azul.
        final_connection_rk3 = Line(
            start = start,
            end = final_point_rk3.get_center()
        ).set_color("#7300FF")

        # Animating
        self.wait(1)

        self.play(
            Create(dot_start),
            Write(initial_label),
            Indicate(t_labels[0], scale_factor=1.5, color=["#002aff"])
        )
        self.wait(1)

        self.play(Create(k1_tangent))

        self.play(
            Indicate(t_labels[1], scale_factor=1.5, color=["#002aff"]),
            Create(euler_line),
            Create(final_point),
            Write(final_label)
        )

        grp1 = VGroup(euler_line, k1_tangent)
        self.play(
            
            ReplacementTransform(grp1, uler_line2)
        )
        self.wait()
        self.next_slide()

        # Comparação final: onde o SSPRK3 chegaria, partindo do mesmo ponto,
        # com a reta azul mostrando o passo efetivo do método.
        self.play(Create(final_connection_rk3), Create(final_point_rk3), Write(final_label_rk3))
        self.wait()
        self.play(Restore(self.camera.frame))

        self.next_slide()
        self.limpar()
        self.limpar()

        cap = r"\text{3. Modelo Completo vs Modelo Simplificado}"
        # slide 1
        titulo_grp = self.entrar_titulo("1º Objetivo", cap) 

        tabela = MathTable(
            [
                [r"\text{SCONTROL}", r"\text{SSPRK3}", r"\text{Completo}"],
                [r"\text{ECONTROL}", r"\text{EE}",     r"\text{Completo}"],
                [r"\text{E3}",       r"\text{EE}",     r"\text{Simplificado}"],
            ],
            col_labels=[
                MathTex(r"\textbf{Experimento}"),
                MathTex(r"\textbf{Método}"),
                MathTex(r"\textbf{Sistema}"),
            ],
            include_outer_lines=False,
        ).set_color(BLACK).set_color_by_gradient("#000000").shift(0.5*DOWN)

        # Remove todas as linhas
        for line in tabela.get_vertical_lines():
            line.set_opacity(0)
        for line in tabela.get_horizontal_lines():
            line.set_opacity(0)

        # Apenas linha superior, abaixo do cabeçalho e inferior
        h = tabela.get_horizontal_lines()
        h[0].set_opacity(1)
        h[1].set_opacity(1)
        h[-1].set_opacity(1)

        

        self.play(Write(tabela))
        

        self.wait()
        self.next_slide()
        self.camera.frame.save_state()
                # --------------------- RAIO ---------------------
        raio30 = (
            ImageMobject("grafico_raio_ECONTROL_SCONTROL_E3_30.png")
            .scale(0.45)
            .move_to(5 * DOWN)
        )

        raio500 = (
            ImageMobject("grafico_raio_ECONTROL_SCONTROL_E3_500.png")
            .scale(0.45)
            .next_to(raio30, DOWN, buff=0.08)
        )

        # ------------------ TEMPERATURA ------------------
        temp30 = (
            ImageMobject("grafico_temperatura_ECONTROL_SCONTROL_E3_30.png")
            .scale(0.45)
            .move_to(13 * DOWN)
        )

        temp500 = (
            ImageMobject("grafico_temperatura_ECONTROL_SCONTROL_E3_500.png")
            .scale(0.45)
            .next_to(temp30, DOWN, buff=0.08)
        )

        # --------------------- MASSA ---------------------
        massa30 = (
            ImageMobject("grafico_massa_ECONTROL_SCONTROL_E3_30.png")
            .scale(0.45)
            .move_to(21 * DOWN)
        )

        massa500 = (
            ImageMobject("grafico_massa_ECONTROL_SCONTROL_E3_500.png")
            .scale(0.45)
            .next_to(massa30, DOWN, buff=0.08)
        )

  


        # ---------- RAIO ----------
        self.play(self.camera.frame.animate.move_to(7 * DOWN),FadeIn(raio30), FadeIn(raio500))

        self.wait()
        self.next_slide()

        # ------ TEMPERATURA -------
        self.play(self.camera.frame.animate.move_to(15 * DOWN),FadeIn(temp30), FadeIn(temp500))

        self.wait()
        self.next_slide()

        # --------- MASSA ----------
        self.play(self.camera.frame.animate.move_to(23 * DOWN),FadeIn(massa30), FadeIn(massa500))

        self.wait()
        self.next_slide()
        self.play(Restore(self.camera.frame),FadeOut(Group(massa500,massa30,temp30,temp500,raio30,raio500)))
        tabela2 = MathTable(
            [
                [
                    r"\text{SCONTROL}",
                    r"\text{SSPRK3}",
                    r"\text{Completo}",
                    r"\checkmark",
                    r"\checkmark",
                ],
                [
                    r"\text{ECONTROL}",
                    r"\text{EE}",
                    r"\text{Completo}",
                    r"\checkmark",
                    r"\checkmark",
                ],
                [
                    r"\text{E3}",
                    r"\text{EE}",
                    r"\text{Simplificado}",
                    r"\times",
                    r"\checkmark",
                ],
            ],
            col_labels=[
                MathTex(r"\textbf{Experimento}"),
                MathTex(r"\textbf{Método}"),
                MathTex(r"\textbf{Sistema}"),
                MathTex(r"\mathbf{r_i = 30\,\mu m}"),
                MathTex(r"\mathbf{r_i = 500\,\mu m}"),
            ],
            include_outer_lines=False,
        ).set_color(BLACK).scale(0.7).shift(0.5*DOWN)
        for line in tabela2.get_vertical_lines():
            line.set_opacity(0)
        for line in tabela2.get_horizontal_lines():
            line.set_opacity(0)

        # Apenas linha superior, abaixo do cabeçalho e inferior
        j = tabela2.get_horizontal_lines()
        j[0].set_opacity(1)
        j[1].set_opacity(1)
        j[-1].set_opacity(1)
        self.next_slide()

        self.play(FadeTransform(tabela,tabela2))
        self.wait()
        self.next_slide()

        tabela3 = MathTable(
            [
                [
                    r"\text{SCONTROL}",
                    r"500",
                     r"0,544"
                ],
                [
                    r"\text{ECONTROL}",
                    r"500",
                     r"0,388"
                ],
                [
                    r"\text{E3}",
                    r"500",
                     r"0,348",
                ],
            ],
            col_labels=[
                MathTex(r"\textbf{Experimento}"),
                MathTex(r"\textbf{Raio } (\mu \text{m})"),
                MathTex(r"\textbf{Tempo }\mathbf{(s)}"),
            ],
            include_outer_lines=False,
        ).set_color(BLACK).scale(0.9).shift(8.2*DOWN)
        for line in tabela3.get_vertical_lines():
            line.set_opacity(0)
        for line in tabela3.get_horizontal_lines():
            line.set_opacity(0)

        # Apenas linha superior, abaixo do cabeçalho e inferior
        k = tabela3.get_horizontal_lines()
        k[0].set_opacity(1)
        k[1].set_opacity(1)
        k[-1].set_opacity(1)

        self.next_slide()
        self.play(self.camera.frame.animate.move_to(8 * DOWN), Write(tabela3))
        self.wait()
        self.next_slide()
        self.play(self.camera.frame.animate.move_to(15 * DOWN),FadeIn(raio30.shift(8*DOWN)), FadeIn(temp30.next_to(raio30, DOWN, buff=0.08)))
        self.wait()
        self.next_slide()
        self.limpar()
        self.play(Restore(self.camera.frame))

        Text.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        Tex.set_default(color=BLACK)
        cap = r"\text{4. Tempo Computacional e Acurácia}"
        titulo_grp = self.entrar_titulo("Passo Fixo e Controle por Subpassos", cap)

        textoo = MathTex(
            r"""
            \begin{cases}
            \dfrac{d\mathbf{y}(t)}{dt}
            =
            \mathbf{F}(t,\mathbf{y}),
            \qquad
            t\in[0,\tau_f]
            \\[6pt]
            \mathbf{y}(t_0)=\mathbf{y}_0
            \end{cases}
            """,
            font_size=55,
            color=CINZA_TEXTO,
        ).shift(1.5*UP)
 
        # ------------------------------------------------------------
        # Parâmetros geométricos (mesmo espírito do slide de subpassos)
        # ------------------------------------------------------------
        L = 9.5          # comprimento do eixo
        H = -0.3         # altura do eixo único (processo de passo fixo)
        x0 = -L / 2
        x1 = L / 2
 
        N = 6             # número de subpassos (mesmo N do .tex)
        step = L / N
        xs = [x0 + step * i for i in range(N + 1)]
 
        # ------------------------------------------------------------
        # 1) Rótulo do processo + eixo do tempo
        # ------------------------------------------------------------
        proc_title = VGroup(
            MathTex(r"t", font_size=40, color=CINZA_TEXTO),
        ).arrange(DOWN, buff=0.15)
        proc_title.move_to([x0 - 1.7, H, 0])
 
        eixo = Arrow(
            start=[x0 - 0.2, H, 0], end=[x1 + 0.8, H, 0],
            buff=0, color=GREY_D, stroke_width=3,
            max_tip_length_to_length_ratio=0.03,
        ).shift(3*DOWN)
        eixo_label = MathTex(r"t", font_size=40, color=CINZA_TEXTO).next_to(
            eixo, LEFT, buff=0.15
        )
 

 
        # ------------------------------------------------------------
        # 2) Marcas dos extremos: t_inicial e t_final (+ t_0 e t_N)
        # ------------------------------------------------------------
        tick_i = Line([x0, H + 0.15, 0], [x0, H - 0.15, 0], color=GREY_D).shift(3*DOWN)
        tick_f = Line([x1, H + 0.15, 0], [x1, H - 0.15, 0], color=GREY_D).shift(3*DOWN)
        label_i_slow = MathTex(r"0", font_size=40, color=CINZA_TEXTO).next_to(tick_i, DOWN, buff=0.15)
        label_f_slow = MathTex(r"\tau_f", font_size=40, color=CINZA_TEXTO).next_to(tick_f, DOWN, buff=0.15)

        label_inicial = MathTex(r"t_{\text{inicial}}", font_size=26).next_to(
            tick_i, DOWN, buff=0.18
        )
        label_final = MathTex(r"t_{\text{final}}", font_size=26).next_to(
            tick_f, DOWN, buff=0.18
        )
        label_t0 = MathTex(r"t_0", font_size=26).next_to(
            label_inicial, DOWN, buff=0.15
        )
        label_tN = MathTex(r"t_N", font_size=26).next_to(
            label_final, DOWN, buff=0.15
        )
        self.play(FadeIn(textoo))
        self.play(Write(eixo), Write(eixo_label),Create(tick_i), Create(tick_f),Write(label_i_slow),Write(label_f_slow))
        self.wait(0.3)
        self.play(Write(label_t0), Write(label_tN))
        self.wait(0.3)
 
        # ------------------------------------------------------------
        # 3) Subpassos de tamanho fixo Delta t, aparecendo em sequência
        #    (mesma lógica do loop usado nos subpassos rápidos do bb.py,
        #     mas aqui todos os passos têm o MESMO tamanho)
        # ------------------------------------------------------------
        ticks_internos = VGroup(*[
            Line([xs[i], H + 0.1, 0], [xs[i], H - 0.1, 0], color=GREY_D)
            for i in range(1, N)
        ]).shift(3*DOWN)

        ticks_labels = VGroup()

        for i in range(1, N):
            if i == 1:
                label = MathTex(r"t_{1}", font_size=40, color=CINZA_TEXTO)
            elif i == 2:
                label = MathTex(r"t_{2}", font_size=40, color=CINZA_TEXTO)
            elif i == N - 1:
                label = MathTex(r"t_{N-1}", font_size=40, color=CINZA_TEXTO)
            elif i == N - 2:
                label = MathTex(r"\cdots", font_size=40, color=CINZA_TEXTO)
            elif i == 3:
                label = MathTex(r"t_{3}", font_size=40, color=CINZA_TEXTO)
            else:
                continue

            label.next_to(ticks_internos[i - 1], DOWN, buff=0.15)
            ticks_labels.add(label)
 
        dt_arrows = VGroup(*[
            Arrow(
                [xs[i], H + 0.45, 0], [xs[i + 1], H + 0.45, 0],
                buff=0.05, color=AZUL_PRINCIPAL, stroke_width=5,
                max_tip_length_to_length_ratio=0.1,
            ).shift(3.45*DOWN)
            for i in range(N)
        ])
        dt_labels = VGroup(*[
            MathTex(r"\Delta t", font_size=26, color=AZUL_PRINCIPAL).next_to(
                dt_arrows[i], UP, buff=0.08
            )
            for i in range(N)
        ])
 
        # Rótulos dos nós temporais internos: t_1, t_2, ..., t_n, ...
        node_texts = [r"t_1", r"t_2", r"\cdots", r"t_n", r"\cdots"]
        node_labels = VGroup(*[
            MathTex(txt, font_size=24).next_to([xs[i], H, 0], DOWN, buff=0.18)
            for i, txt in enumerate(node_texts, start=1)
        ])
        self.next_slide()

        label_i_sloww = MathTex(r"t_0", font_size=40, color=CINZA_TEXTO).next_to(tick_i, DOWN, buff=0.15)
        label_f_sloww = MathTex(r"t_N", font_size=40, color=CINZA_TEXTO).next_to(tick_f, DOWN, buff=0.15)
        #self.play(ReplacementTransform(label_i_slow,label_i_sloww),ReplacementTransform(label_f_slow,label_f_sloww))

  
        
        for tick, label in zip(ticks_internos, ticks_labels):
            self.play(
            Create(tick),
            Write(label),
            run_time=0.3)

        self.wait(0.3)
        txt = MathTex(r'\tau_f',r' =',r'N',r'\,',r' \Delta t', font_size=55, color=CINZA_TEXTO).next_to(textoo,DOWN,buff=1.2)
        self.play(TransformFromCopy(label_f_slow,txt[0]),Write(txt[1]))
        # Anima cada subpasso surgindo em sequência, como um passo se repetindo
        for i in range(N):
            anims = [GrowArrow(dt_arrows[i])]
            self.play(*anims, run_time=0.3)
        self.wait(0.3)
        self.play(TransformFromCopy(dt_arrows,txt[2]))
 
        # ------------------------------------------------------------
        # 4) Chave superior: Delta t = tau_f / N
        # ------------------------------------------------------------
        brace_top = Brace(
            Line([xs[1], H + 0.85, 0], [xs[2], H + 0.85, 0]),
            UP, color=AZUL_PRINCIPAL,
        ).shift(3.8*DOWN)
        label_top = MathTex(
            r"\Delta t =t_2 -t_1", font_size=40, color=AZUL_PRINCIPAL
        ).next_to(brace_top, UP, buff=0.12)
 
        self.play(GrowFromCenter(brace_top), Write(label_top))
        grp=VGroup(brace_top,label_top)
        self.wait(0.3)
        self.play(TransformFromCopy(grp,txt[4]))

  
        self.next_slide()
        txt1 = MathTex(r'\Delta t',r'=',r'\dfrac{\tau_f}{N}', font_size=55, color=CINZA_TEXTO).next_to(textoo,DOWN,buff=1.2)
        self.play(FadeTransform(txt,txt1))
        self.next_slide()

        self.wait()
 
        #AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII

        texto6 = self.lista([
            r"\text{Passo de tempo macro para variáveis lentas: }",r'\Delta t = \dfrac{\tau_f}{N}'],font_size= 55,largura=20)
        texto6.shift(1.4*LEFT+1.3*UP)
        self.play(FadeOut(textoo),Write(texto6[0]))
        self.play(ReplacementTransform(txt1,texto6[1]))

        grp1 = VGroup(brace_top,label_top,eixo,eixo_label,tick_i,tick_f,label_i_slow,label_f_slow,ticks_internos,ticks_labels)
        self.next_slide()
        faa = VGroup(ticks_labels[0],ticks_labels[1],label_top)
        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.scale(0.2).move_to(faa))



        m = 5
        step_zoom = (xs[2] - xs[1]) / m
        xs_zoom = [xs[1] + step_zoom * i for i in range(m + 1)]

        ticks_zoom = VGroup(*[
            Line([xs_zoom[i], H + 0.08, 0], [xs_zoom[i], H - 0.08, 0], color=GREY_D)
            for i in range(1, m)
        ]).shift(3*DOWN)
        labels_zoom = VGroup(
            MathTex(r"t_{1,1}", font_size=11, color=CINZA_TEXTO).next_to(
                ticks_zoom[0], DOWN, buff=0.12
            ),

            MathTex(r"t_{1,2}", font_size=11, color=CINZA_TEXTO).next_to(
                ticks_zoom[1], DOWN, buff=0.12
            ),

            MathTex(r"\cdots", font_size=11, color=CINZA_TEXTO).next_to(
                ticks_zoom[(m-1)//2], DOWN, buff=0.12
            ),

            MathTex(r"t_{1,M-1}", font_size=11, color=CINZA_TEXTO).next_to(
                ticks_zoom[-1], DOWN, buff=0.12
            ),
        )

        for tick, label in zip(ticks_zoom, labels_zoom):
            self.play(Create(tick), Write(label), run_time=0.3)

        dtau_arrows = VGroup(*[
            Arrow(
                [xs_zoom[i], H - 0.55, 0], [xs_zoom[i + 1], H - 0.55, 0],
                buff=0.05, color="#ff5100", stroke_width=25,
                max_tip_length_to_length_ratio=0.2,
            ).shift(2.45*DOWN).set_stroke(width=4)
            for i in range(m)
        ])
        for arrow in dtau_arrows:
            self.play(GrowArrow(arrow), run_time=0.3)

        brace_zoom = Brace(dtau_arrows[1], UP, color="#ff5100").stretch(0.5, dim=1).shift(0.2*DOWN)
        label_dtau = MathTex(r"\delta t", font_size=15, color="#ff5100").next_to(
            brace_zoom, UP, buff=0.01
        )
        adsada=VGroup(brace_zoom,label_dtau)
        #self.play(GrowFromCenter(brace_zoom), Write(label_dtau))
        label_topp = MathTex(
            r"\Delta t =", r'M',r'\delta t', font_size=40, color=AZUL_PRINCIPAL
        ).next_to(brace_top, UP, buff=0.12)
        label_topp[0][2:3].set_color_by_gradient("#000000")
        self.play(FadeTransform(label_top,label_topp[0]))

        self.play(TransformFromCopy(dtau_arrows,label_topp[1].set_color_by_gradient("#000000")))
        self.play(Write(brace_zoom),Write(label_dtau))

        self.play(TransformFromCopy(adsada,label_topp[2].set_color_by_gradient("#ff5100")))

        self.next_slide()
        self.play(Restore(self.camera.frame))
        texto7 = self.lista([
            r"\text{Passo de tempo micro para variável rápida: }",r'\delta t = \dfrac{\Delta t}{M}'],font_size= 55,largura=20)
        texto7.shift(1.5*LEFT+1.2*DOWN)
        self.play(Write(texto7[0]))
        self.play(TransformFromCopy(label_topp,texto7[1]))
        self.wait()
        self.next_slide()

        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.move_to(8 * DOWN))



        listing = Code( "bbbb.py",
            tab_width=4,
            formatter_style="monokai",
            background="rectangle",
            language="python",
            background_config={"stroke_color": BLACK},
            paragraph_config={"font": "Noto Sans Mono"},
        )
        listing.scale(1.05).shift(0.3*RIGHT+8 * DOWN)

        self.play(Write(listing))
        self.wait()
        self.next_slide()
        self.play(Restore(self.camera.frame))


        self.next_slide()
 
        self.limpar()




       
        cap = r"\text{4. Tempo Computacional e Acurácia}"
        # slide 1
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
        self.next_slide()



 
        self.limpar()

        cap = r"\text{4. Tempo Computacional e Acurácia}"
        # slide 1
        titulo_grp = self.entrar_titulo("2° Objetivo", cap) 
        tabela = MathTable(
            [
                [r"\text{SCONTROL}", r"\text{SSPRK3}", r"\text{Fixo}",      r"\text{Completo}"],
                [r"\text{ECONTROL}", r"\text{EE}",     r"\text{Fixo}",      r"\text{Completo}"],
                [r"\text{E1}",       r"\text{EE}",     r"\text{Subpassos}", r"\text{Completo}"],
                [r"\text{E2}",       r"\text{EE}",     r"\text{PID}",       r"\text{Completo}"],
                [r"\text{E3}",       r"\text{EE}",     r"\text{Fixo}",      r"\text{Simplificado}"],
                [r"\text{E4}",       r"\text{EE}",     r"\text{Subpassos}", r"\text{Simplificado}"],
                [r"\text{E5}",       r"\text{EE}",     r"\text{PID}",       r"\text{Simplificado}"],
            ],
            col_labels=[
                MathTex(r"\textbf{Experimento}"),
                MathTex(r"\textbf{Método}"),
                MathTex(r"\textbf{Estratégia de passo}"),
                MathTex(r"\textbf{Sistema}"),
            ],
            include_outer_lines=False,
            add_background_rectangles_to_entries=False,
        ).set_color(BLACK).shift(0.5 * DOWN).scale(1.2)
        # Remove todas as linhas verticais e horizontais padrão
        for line in tabela.get_vertical_lines():
            line.set_opacity(0)
        for line in tabela.get_horizontal_lines():
            line.set_opacity(0)

        # Exibe apenas a linha superior, abaixo do cabeçalho e inferior (estilo livro/booktabs)
        h = tabela.get_horizontal_lines()
        h[0].set_opacity(1)   # Topo
        h[1].set_opacity(1)   # Topo
        h[2].set_opacity(1)   # Topo
        h[3].set_opacity(1)   # Topo
        h[4].set_opacity(1)   # Topo
        h[5].set_opacity(1)   # Topo
        h[6].set_opacity(1)   # Topo

        tabela.scale(0.55)
        self.play(Write(tabela))

        self.wait()
        self.next_slide()
        self.camera.frame.save_state()
        
         


        caption_texto0 = self.lista([
            r"\textbf{Acurácia e Eficiência Computacional}",
        ], font_size=45, largura=20)
        caption_texto0.shift(2.5*LEFT + 12.5*DOWN)

        # 3. Tabela única: para cada raio -> Pontos, Tempo, Erro relativo
        tabela_unica = MathTable(
            [
                [r"\text{SCONTROL}", r"\text{265.950}", r"\text{9,041}", r"\text{ref}",              r"\text{7.223}", r"\text{0,544}", r"\text{ref}"],
                [r"\text{ECONTROL}", r"\text{265.950}", r"\text{2,984}", r"4{,}94 \times 10^{-7}", r"\text{7.223}", r"\text{0,388}", r"1{,}23 \times 10^{-7}"],
                [r"\text{E1}",       r"\text{26.597}",  r"\text{2,068}", r"5{,}08 \times 10^{-6}", r"\text{724}",   r"\text{0,361}", r"1{,}41 \times 10^{-5}"],
                [r"\text{E2}",       r"\text{8.702}",   r"\text{0,414}", r"1{,}69 \times 10^{-5}", r"\text{107}",   r"\text{0,309}", r"9{,}06 \times 10^{-6}"],
                [r"\text{E3}",       r"\text{265.950}", r"\text{1,395}", r"1{,}36 \times 10^{-1}", r"\text{7.223}", r"\text{0,348}", r"3{,}43 \times 10^{-4}"],
                [r"\text{E4}",       r"\text{26.597}",  r"\text{0,443}", r"1{,}36 \times 10^{-1}", r"\text{724}",   r"\text{0,312}", r"3{,}29 \times 10^{-4}"],
                [r"\text{E5}",       r"\text{10.052}",  r"\text{0,362}", r"1{,}36 \times 10^{-1}", r"\text{96}",    r"\text{0,313}", r"3{,}45 \times 10^{-4}"],
            ],
            col_labels=[
                MathTex(r"\textbf{Experimento}"),
                MathTex(r"\textbf{Pontos}"),
                MathTex(r"\textbf{Tempo (s)}"),
                MathTex(r"\epsilon_f"),
                MathTex(r"\textbf{Pontos}"),
                MathTex(r"\mathbf{Tempo (s)}"),
                MathTex(r"\epsilon_f"),
            ],
            include_outer_lines=False,
            add_background_rectangles_to_entries=False,
        ).scale(0.55).set_color_by_gradient('#000000').shift(16.5*DOWN)

        # Remove a opacidade de todas as linhas verticais
        for line in tabela_unica.get_vertical_lines():
            line.set_opacity(0)
        # Remove a opacidade de todas as linhas horizontais
        for line in tabela_unica.get_horizontal_lines():
            line.set_opacity(0)

        # Aplica o estilo clássico "booktabs" nas linhas horizontais
        h_lliness = tabela_unica.get_horizontal_lines()
        h_lliness[0].set_opacity(1)   # Linha do topo

        # --- Cabeçalho agrupado (simula \multicolumn do LaTeX) ---
        col_labels_row = tabela_unica.get_rows()[0]

        c1_left, c1_right = col_labels_row[1], col_labels_row[3]   # Pontos/Tempo/Erro r=30
        c2_left, c2_right = col_labels_row[4], col_labels_row[6]   # Pontos/Tempo/Erro r=500

        label_r30 = MathTex(r"r_i = 30\ \mu m").scale(0.6).set_color('#000000')
        label_r500 = MathTex(r"r_i = 500\ \mu m").scale(0.6).set_color('#000000')

        label_r30.next_to(VGroup(c1_left, c1_right), UP, buff=0.25)
        label_r500.next_to(VGroup(c2_left, c2_right), UP, buff=0.25)

        line_r30 = Line(c1_left.get_left(), c1_right.get_right(), color='#000000').next_to(label_r30, DOWN, buff=0.08)
        line_r500 = Line(c2_left.get_left(), c2_right.get_right(), color='#000000').next_to(label_r500, DOWN, buff=0.08)

        # --- "referência" mesclado nas colunas de erro da linha SCONTROL ---
        sc_row = tabela_unica.get_rows()[1]  # linha 0 = cabeçalho, linha 1 = SCONTROL
        erro30_cell = sc_row[3]
        erro500_cell = sc_row[6]

        erro30_cell.set_opacity(0)
        erro500_cell.set_opacity(0)

        referencia_texto30 = MathTex(r"\text{referência}").scale(0.5).set_color('#000000')
        referencia_texto30.move_to(erro30_cell.get_center())

        referencia_texto500 = MathTex(r"\text{referência}").scale(0.5).set_color('#000000')
        referencia_texto500.move_to(erro500_cell.get_center())

        grupo_tabela = VGroup(
            tabela_unica, label_r30, label_r500,
            line_r30, line_r500,
            referencia_texto30, referencia_texto500,
        )

        self.play(self.camera.frame.animate.move_to(16 * DOWN), Write(caption_texto0))
        self.play(
            Write(tabela_unica),
            Write(label_r30), Write(label_r500),
            Create(line_r30), Create(line_r500),
            Write(referencia_texto30), Write(referencia_texto500),
        )
        self.wait()

        self.next_slide()

        self.play(self.camera.frame.animate.move_to(17 * DOWN))
        textoo = MathTex(r' \epsilon_f = \left|\dfrac{m_\text{exp}(\tau_f) - m_\text{ref}(\tau_f)}{m_\text{ref}(\tau_f)}\right|',
            font_size=53,
            color=CINZA_TEXTO,
        ).next_to(tabela_unica,DOWN,buff=0.2)
        self.play(Write(textoo))
        
        self.next_slide()
        self.play(self.camera.frame.animate.move_to(16 * DOWN),Unwrite(textoo))
        self.next_slide()
        e2_row = tabela_unica.get_rows()[4]  # 0=header, 1=SCONTROL, 2=ECONTROL, 3=E1, 4=E2

        destaque_e2 = SurroundingRectangle(
                    e2_row,
                    color="#002aff",
                    buff=0.12,
                    corner_radius=0.05,
                    stroke_width=6,
                )
        self.play(Write(destaque_e2))
        self.wait()

        self.next_slide()

        self.limpar()
        self.play(Restore(self.camera.frame))

        
