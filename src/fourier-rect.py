import numpy as np
from manim import *


class FourierRect(Scene):
    def construct(self):

        # ================================================
        # 1. Fourier transform derivation
        # ================================================

        title = Text(
            "Fourier Transform of Rectangular Pulse",
            font_size=32,
        ).to_edge(UP, buff=0.35)

        self.play(Write(title))

        eq1 = MathTex(r"x(t)=\operatorname{rect}\left(\frac{t}{T}\right)")

        eq2 = MathTex(
            r"X(f)=\int_{-\infty}^{+\infty}"
            r"x(t)e^{-j2\pi ft}\,dt"
        )

        eq3 = MathTex(
            r"X(f)=\int_{-T/2}^{T/2}"
            r"e^{-j2\pi ft}\,dt"
        )

        eq4 = MathTex(
            r"X(f)="
            r"\left[\frac{e^{-j2\pi ft}}{-j2\pi f}"
            r"\right]_{-T/2}^{T/2}"
        )

        eq5 = MathTex(r"X(f)=\frac{\sin(\pi fT)}{\pi f}")

        eq6 = MathTex(r"X(f)=T\frac{\sin(\pi fT)}{\pi fT}")

        eq7 = MathTex(r"\operatorname{sinc}(u)=\frac{\sin(\pi u)}{\pi u}")

        eq8 = MathTex(r"\boxed{X(f)=T\operatorname{sinc}(Tf)}")

        derivation = (
            VGroup(eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8)
            .arrange(
                DOWN,
                aligned_edge=LEFT,
                buff=0.32,
            )
            .scale_to_fit_height(config.frame_height - 4 * title.height)
        )

        derivation.next_to(title, DOWN)

        # Show equations one by one, but keep previous ones
        for eq in derivation:
            self.play(
                Write(eq),
                run_time=1,
            )
            self.wait(0.6)

        self.wait(2)

        # Remove intermediate calculations only
        self.play(
            FadeOut(VGroup(*derivation[1:-1])),
            FadeOut(title),
            run_time=1,
        )

        # ================================================
        # 2. Dynamic plots
        # ================================================

        T = ValueTracker(2.5)

        # Time domain axes
        time_axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 1.3, 0.5],
            x_length=7.5,
            y_length=1.4,
            axis_config={
                "include_numbers": True,
                "font_size": 18,
            },
            tips=False,
        ).move_to(LEFT * 2.7 + UP * 1.65)

        # Frequency domain axes
        freq_axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 2.6, 0.5],
            x_length=7.5,
            y_length=1.4,
            axis_config={
                "include_numbers": True,
                "font_size": 18,
            },
            tips=False,
        ).move_to(LEFT * 2.7 + DOWN * 1.45)

        # ================================================
        # 3. Permanent titles
        # ================================================

        time_title = Text(
            "Time Domain",
            font_size=27,
            color=BLUE,
        ).next_to(time_axes, UP, buff=0.2)

        freq_title = Text(
            "Frequency Domain",
            font_size=27,
            color=YELLOW,
        ).next_to(freq_axes, UP, buff=0.2)

        time_formula = MathTex(
            r"x(t)=\operatorname{rect}\left(\frac{t}{T}\right)"
        ).scale(0.75)

        time_formula.move_to(RIGHT * 3.5 + UP * 1.65)

        freq_formula = MathTex(r"|X(f)|=T|\operatorname{sinc}(Tf)|").scale(0.75)

        freq_formula.move_to(RIGHT * 3.5 + DOWN * 1.45)

        # Transform the final derivation into the spectrum formula
        self.play(
            FadeTransformPieces(eq1, time_formula),
            FadeTransformPieces(eq8, freq_formula),
            run_time=1.5,
        )

        self.play(
            Create(time_axes),
            Create(freq_axes),
            Write(time_title),
            Write(freq_title),
            run_time=1.5,
        )

        # ================================================
        # 4. Rectangular pulse
        # ================================================

        def rect(t):
            return 1.0 if abs(t) < 0.5 else 0.0

        def make_pulse():
            width = T.get_value()

            return time_axes.plot(
                lambda t: rect(t / width),
                x_range=[-4, 4],
                color=BLUE,
                stroke_width=3,
                use_smoothing=False,
            )

        pulse = always_redraw(make_pulse)

        # ================================================
        # 5. Fourier spectrum
        # ================================================

        def make_spectrum():

            width = T.get_value()

            return freq_axes.plot(
                lambda f: width * abs(np.sinc(width * f)),
                x_range=[-4, 4],
                color=YELLOW,
                stroke_width=3,
            )

        spectrum = always_redraw(make_spectrum)

        # ================================================
        # 6. Dynamic width indicator
        # ================================================

        width_text = always_redraw(
            lambda: (
                MathTex(rf"T={T.get_value():.2f}")
                .scale(0.7)
                .to_edge(UP, buff=0.5)
            )
        )

        self.play(
            Write(pulse),
            Create(spectrum),
            FadeIn(width_text),
            run_time=1.5,
        )

        self.wait(2)

        # ================================================
        # 7. Time compression
        # ================================================

        compress_text = Text(
            "Time Compression",
            font_size=24,
            color=BLUE,
        ).to_edge(DOWN, buff=0.4)

        relation = (
            MathTex(
                r"\Delta t\downarrow"
                r"\quad\Longrightarrow\quad"
                r"\Delta f\uparrow"
            )
            .scale(0.85)
            .to_edge(DOWN, buff=0.4)
        )

        self.play(FadeIn(compress_text))

        self.play(
            T.animate.set_value(0.65),
            run_time=4,
            rate_func=smooth,
        )

        self.play(
            FadeOut(compress_text),
            Write(relation),
        )

        self.wait(2)

        # ================================================
        # 8. Time expansion
        # ================================================

        expand_text = Text(
            "Time Expansion",
            font_size=24,
            color=BLUE,
        ).to_edge(DOWN, buff=0.4)

        reverse_relation = (
            MathTex(
                r"\Delta t\uparrow"
                r"\quad\Longrightarrow\quad"
                r"\Delta f\downarrow"
            )
            .scale(0.85)
            .to_edge(DOWN, buff=0.4)
        )

        self.play(
            FadeOut(relation),
            FadeIn(expand_text),
        )

        self.play(
            T.animate.set_value(2.5),
            run_time=4,
            rate_func=smooth,
        )

        self.play(
            FadeOut(expand_text),
            Write(reverse_relation),
        )

        self.wait(3)
