from manim import *

# Paleta simples, coerente com o restante do TCC (preto/cinza sobre fundo branco)
config.background_color = WHITE
TXT_COLOR = BLACK
AXIS_COLOR = GREY_D
DASH_COLOR = GREY_B


class Subciclagem(Scene):
    def construct(self):
        Text.set_default(color=TXT_COLOR, font="sans-serif")
        MathTex.set_default(color=TXT_COLOR)
        Tex.set_default(color=TXT_COLOR)

        L = 8       # comprimento dos eixos
        y_top = 1.5   # altura do eixo "Processo Rápido"
        y_bot = -1.5   # altura do eixo "Processo Lento"
        x0 = -L / 2
        x1 = L / 2

        # ------------------------------------------------------------
        # 1) PROCESSO LENTO (base) — aparece primeiro
        # ------------------------------------------------------------
        slow_title = VGroup(
            Text("Processo Lento", weight=BOLD, font_size=25),
            MathTex(r"r(t)\ \text{e}\ m(t)", font_size=40),
        ).arrange(DOWN, buff=0.15).next_to(LEFT * (L / 2 + 0.6) + UP * y_bot, ORIGIN, buff=0)
        slow_title.move_to([x0 - 1.6, y_bot, 0])

        slow_axis = Arrow(
            start=[x0 - 0.2, y_bot, 0], end=[x1 + 0.8, y_bot, 0],
            buff=0, color=AXIS_COLOR, stroke_width=3, max_tip_length_to_length_ratio=0.03,
        )
        slow_axis_label = Text("Tempo", font_size=24).next_to(slow_axis, RIGHT, buff=0.15)

        tick_i_slow = Line([x0, y_bot + 0.15, 0], [x0, y_bot - 0.15, 0], color=AXIS_COLOR)
        tick_f_slow = Line([x1, y_bot + 0.15, 0], [x1, y_bot - 0.15, 0], color=AXIS_COLOR)
        label_i_slow = MathTex(r"t_{\text{inicial}}", font_size=28).next_to(tick_i_slow, DOWN, buff=0.15)
        label_f_slow = MathTex(r"t_{\text{final}}", font_size=28).next_to(tick_f_slow, DOWN, buff=0.15)

        self.play(Write(slow_title),Create(slow_axis), FadeIn(slow_axis_label),Create(tick_i_slow), Create(tick_f_slow),
            Write(label_i_slow), Write(label_f_slow),)
        self.wait(0.3)

        # Seta indicando o avanço em um único passo macroscópico
        macro_arrow = Arrow(
            [x0, y_bot + 0.5, 0], [x1, y_bot + 0.5, 0],
            buff=0, color="#002aff", stroke_width=4, max_tip_length_to_length_ratio=0.04,
        )

        macro_brace = Brace(Line([x0, y_bot - 0.9, 0], [x1, y_bot - 0.9, 0]), DOWN, color="#002aff")
        macro_label = MathTex(
            r"\text{Passo Macrosc\^opico: } \Delta t = t_{\text{final}} - t_{\text{inicial}}",
            font_size=30, color="#002aff",
        ).next_to(macro_brace, DOWN, buff=0.15)
        self.play(GrowArrow(macro_arrow),GrowFromCenter(macro_brace), Write(macro_label))
        self.wait(0.6)

        # ------------------------------------------------------------
        # 2) PROCESSO RÁPIDO (topo) — subciclagem dentro do mesmo Δt
        # ------------------------------------------------------------
        fast_title = VGroup(
            Text("Processo Rápido", weight=BOLD, font_size=25),
            MathTex(r"T(t)", font_size=40),
        ).arrange(DOWN, buff=0.15)
        fast_title.move_to([x0 - 1.6, y_top, 0])

        fast_axis = Arrow(
            start=[x0 - 0.2, y_top, 0], end=[x1 + 0.8, y_top, 0],
            buff=0, color=AXIS_COLOR, stroke_width=3, max_tip_length_to_length_ratio=0.03,
        )
        fast_axis_label = Text("Tempo", font_size=24).next_to(fast_axis, RIGHT, buff=0.15)

        self.play(Write(fast_title),Create(fast_axis), FadeIn(fast_axis_label))

        # Linhas tracejadas de acoplamento entre os dois eixos
        dash_left = DashedLine([x0, y_top, 0], [x0, y_bot, 0], color=DASH_COLOR, stroke_width=2)
        dash_right = DashedLine([x1, y_top, 0], [x1, y_bot, 0], color=DASH_COLOR, stroke_width=2)
        self.play(Create(dash_left), Create(dash_right))

        # Subpassos: N segmentos iguais dentro do intervalo [x0, x1]
        N = 5
        step = L / N
        xs = [x0 + step * i for i in range(N + 1)]

        ticks = VGroup(*[
            Line([x, y_top + 0.1, 0], [x, y_top - 0.1, 0], color=AXIS_COLOR)
            for x in xs
        ])

        sub_arrows = VGroup(*[
            Arrow(
                [xs[i], y_top + 0.45, 0], [xs[i + 1], y_top + 0.45, 0],
                buff=0.05, color="#002aff", stroke_width=3, max_tip_length_to_length_ratio=0.12,
            )
            for i in range(N)
        ])
        sub_labels = VGroup(*[
            MathTex(r"\delta t", font_size=26, color="#002aff").next_to(sub_arrows[i], UP, buff=0.08)
            for i in range(N)
        ])

        # Rótulos t0, t1, t2, ..., tM ao longo do eixo rápido
        node_labels = [
            MathTex(r"t_0", font_size=26),
            MathTex(r"t_1", font_size=26),
            MathTex(r"t_2", font_size=26),
            MathTex(r"\cdots", font_size=26),
            MathTex(r"\cdots", font_size=26),
            MathTex(r"t_M", font_size=26),
        ]
        for lbl, x in zip(node_labels, xs):
            lbl.next_to([x, y_top, 0], DOWN, buff=0.2)

        # Anima subpassos aparecendo em sequência, como um ciclo se repetindo
        for i in range(N):
            self.play(
                Create(ticks[i]),
                Write(node_labels[i]),
                run_time=0.2,
            )
            self.play(
                GrowArrow(sub_arrows[i]),
                Write(sub_labels[i]),
                run_time=0.2,
            )
        self.play(Create(ticks[N]), Write(node_labels[N]), run_time=0.2)
        self.wait(0.3)

        fast_brace = Brace(Line([xs[0], y_top + 0.95, 0], [xs[1], y_top + 0.95, 0]), UP, color="#002aff")
        fast_label = MathTex(r"\delta t = \Delta t / M", font_size=40, color="#002aff").next_to(
            fast_brace, UP, buff=0.12
        )
        self.play(GrowFromCenter(fast_brace), Write(fast_label))
        self.wait(1)

