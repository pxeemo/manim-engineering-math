import numpy as np
from manim import *


def square_wave_fourier(t, N, omega=1.0, A=1.0):
    """
    S_N(t) = (4A/π) · Σ_{k=0}^{N-1} sin((2k+1)·ω·t) / (2k+1)

    Non-integer N: newest harmonic enters with weight = frac(N),
    so the curve deforms continuously during an animation.
    """
    t = np.asarray(t, dtype=float)
    if N <= 0:
        return np.zeros_like(t)

    N_int = int(N)
    if N_int > 0:
        n_vals = np.arange(1, 2 * N_int, 2, dtype=float)  # [1,3,…,2N_int-1]
        sin_nt = np.sin(np.outer(n_vals * omega, t))  # shape (N_int, len(t))
        total = (sin_nt / n_vals[:, None]).sum(axis=0)
    else:
        total = np.zeros_like(t)

    frac = N - N_int
    if frac > 0:
        n_new = 2 * N_int + 1
        total = total + frac * np.sin(n_new * omega * t) / n_new

    return (4 * A / PI) * total


def harmonic_component(t, n, A=1.0):
    """The single n-th sine term alone: (4A/π)·sin(nt)/n."""
    t = np.asarray(t, dtype=float)
    return (4 * A / PI) * np.sin(n * t) / n


class FourierGibbsStepByStep(Scene):
    def construct(self):
        # ---------- Axes ----------
        axes = Axes(
            x_range=[-2.5 * PI, 2.5 * PI, PI],
            y_range=[-1.5, 1.5, 1.0],
            axis_config={"color": LIGHT_GRAY},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
            x_length=8,
            y_length=4,
        ).shift(DOWN * 0.2)

        x_tick_tex = {
            -PI: r"-\pi",
            PI: r"\pi",
        }
        x_labels = VGroup(
            MathTex(tex, font_size=24).next_to(axes.c2p(v, 0), DOWN, buff=0.15)
            for v, tex in x_tick_tex.items()
        )
        axes_labels = VGroup(
            MathTex("t", font_size=30).next_to(axes.x_axis.get_end(), RIGHT),
            MathTex("f(t)", font_size=30).next_to(axes.y_axis.get_end(), UP),
        )

        ideal = axes.plot(
            lambda x: np.sign(np.sin(x)),
            color=GRAY,
            stroke_width=2,
            use_smoothing=False,
            discontinuities=[2 * -PI, -PI, 0, PI, 2 * PI],
        ).set_stroke(opacity=0.5)

        # ---------- Title + general formula (with ω) ----------
        title = Text(
            "سری فوریۀ موج مربعی و پدیدۀ گیبس",
            # "Fourier Series of a Square Wave and the Gibbs Phenomenon",
            font_size=42,
            font="IRNazanin",
            weight=MEDIUM,
        )
        general_formula = MathTex(
            r"S_N(t) = \frac{4",
            r"A",
            r"}{\pi} \sum_{k=0}^{N-1} \frac{\sin\big((2k+1)\,",
            r"\omega",
            r"t\big)}{2k+1}",
            r",\quad \omega = \frac{2\pi}{T}",
            font_size=30,
        ).next_to(title, DOWN, buff=0.5)
        simplified_general_formula = MathTex(
            r"S_N(t) = \frac{4",
            r"}{\pi} \sum_{k=0}^{N-1} \frac{\sin\big((2k+1)\,",
            r"t\big)}{2k+1}",
            font_size=30,
        ).next_to(title, DOWN, buff=0.5)

        opened_general_formula = MathTex(
            r"S_N(t) = \frac{4",
            r"A",
            r"}{\pi} \left(\sin(",
            r"\omega",
            r"t) + \frac{\sin(3",
            r"\omega",
            r"t)}{3} + \frac{\sin(5",
            r"\omega",
            r"t)}{5} + \cdots + \frac{\sin\big((2N-1)",
            r"\omega",
            r"t\big)}{2N-1} \right)",
            font_size=30,
        ).next_to(general_formula, DOWN, buff=0.5)
        simplified_opened_general_formula = MathTex(
            r"S_N(t) = \frac{4",
            r"}{\pi} \left(\sin(",
            r"t) + \frac{\sin(3",
            r"t)}{3} + \frac{\sin(5",
            r"t)}{5} + \cdots + \frac{\sin\big((2N-1)",
            r"t\big)}{2N-1} \right)",
            font_size=30,
        ).next_to(general_formula, DOWN, buff=0.5)

        VGroup(
            title,
            general_formula,
            simplified_general_formula,
            opened_general_formula,
            simplified_opened_general_formula,
        ).center()

        # ---------- Tracker + labels ----------
        n_tracker = ValueTracker(1)

        n_display = always_redraw(
            lambda: MathTex(
                f"N = {round(n_tracker.get_value())}",
                font_size=36,
            ).to_corner(DL, buff=0.5)
        )

        def make_partial_sum(N, font_size=26):
            tokens = [rf"S_{{{N}}}(t) = ", r"\frac{4}{\pi}", r"\Big(", r"\sin(t)"]
            for k in range(1, N):
                n = 2 * k + 1
                tokens.append(rf"+ \frac{{\sin({n}t)}}{{{n}}}")
            tokens.append(r"\Big)")

            tex = MathTex(*tokens, font_size=font_size)
            tex.to_edge(DOWN, buff=0.4)

            if N > 1:
                tex[-2].set_color(YELLOW)  # highlight only the newest term
            return tex

        partial_sum_display = make_partial_sum(1)

        # ---------- Curve with ADAPTIVE resolution (the fix) ----------
        def make_curve(N):
            N_int = max(1, int(N))
            n_pts = min(4000, max(600, 10 * (2 * N_int + 1)))
            xs = np.linspace(-2.5 * PI, 2.5 * PI, n_pts)
            ys = square_wave_fourier(xs, N)
            pts = [axes.c2p(x, y) for x, y in zip(xs, ys)]
            curve = VMobject()
            curve.set_points_as_corners(pts)
            curve.set_stroke(color=BLUE, width=4)
            return curve

        sum_curve = always_redraw(lambda: make_curve(n_tracker.get_value()))

        # ---------- Intro ----------
        self.play(Write(title, reverse=True))
        self.add(title)
        self.wait(2)
        self.play(Write(general_formula))
        self.wait(3)
        self.play(Write(opened_general_formula))
        self.wait(3)
        self.play(TransformMatchingTex(general_formula, simplified_general_formula))
        self.play(
            TransformMatchingTex(
                opened_general_formula, simplified_opened_general_formula
            )
        )
        self.wait(3)
        self.play(
            title.animate.to_edge(UP, buff=0.5).scale(0.8),
            FadeOut(simplified_general_formula),
            FadeOut(simplified_opened_general_formula),
        )
        self.play(
            Write(axes),
            Write(x_labels),
            Write(axes_labels),
        )
        self.wait(1)
        self.play(Create(ideal), run_time=0.6)
        self.wait(3)
        self.play(
            Create(sum_curve).set_run_time(4),
            Write(n_display),
            Write(partial_sum_display),
        )
        self.wait(4)

        # ---------- 6 incremental adds: N = 1 → 7 ----------
        for target_N in range(2, 7):
            n_val = 2 * target_N - 1

            adding_tex = MathTex(
                rf"+\frac{{\sin({n_val}\,t)}}{{{n_val}}}",
                font_size=28,
                color=YELLOW,
            ).next_to(partial_sum_display, RIGHT, buff=0.4)

            new_display = make_partial_sum(target_N)

            new_harmonic = axes.plot(
                lambda x, n=n_val: harmonic_component(x, n),
                x_range=[-2.5 * PI, 2.5 * PI, PI / 100],
                color=YELLOW,
                stroke_width=2,
                use_smoothing=True,
            )

            self.play(
                Create(new_harmonic).set_run_time(4),
                Write(adding_tex),
            )
            self.play(
                n_tracker.animate.set_value(target_N),
                TransformMatchingTex(
                    VGroup(partial_sum_display, adding_tex), new_display
                ),
                FadeOut(new_harmonic),
                run_time=1.5,
                rate_func=smooth,
            )
            self.wait(2)
            partial_sum_display = new_display  # hand off the reference

        self.play(
            FadeOut(partial_sum_display),
        )

        self.wait(2)

        # ------------------------- Jump --------------------------------
        self.play(
            n_tracker.animate.set_value(50),
            run_time=2.0,
            rate_func=smooth,
        )

        self.wait(2)
