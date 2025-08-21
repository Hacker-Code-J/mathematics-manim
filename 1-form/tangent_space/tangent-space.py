from manim import *

# To run this code, save it as a .py file and run:
# manim -pql your_file_name.py TangentSpaceVisualization

class TangentSpaceVisualization(MovingCameraScene):
    """
    A Manim scene to visualize the tangent space T_p(R^2) and its
    1-dimensional subspace T_p(C) spanned by the tangent vector.
    """
    def construct(self):
        # 1. SETUP: Define function, axes, and point of tangency
        axes = Axes(
            x_range=[-2, 4, 1],
            y_range=[-1, 6, 1],
            axis_config={"color": BLUE},
            x_length=8,
            y_length=8,
        )
        # Define a function f(x) and its derivative f'(x)
        f = lambda x: x**3 - 2*x**2 + 2
        f_prime = lambda x: 3*x**2 - 4*x

        # Create the curve from the function
        graph = axes.plot(f, color=YELLOW)
        graph_label = axes.get_graph_label(graph, label="C: y=f(x)")

        # Define the point 'p' on the curve
        a = 1.5
        p_coords = axes.c2p(a, f(a)) # Convert graph coords to screen coords
        p_dot = Dot(p_coords, color=RED)
        p_label = MathTex("p", color=RED).next_to(p_dot, DR)

        self.play(Create(axes))
        # self.play(FadeIn(axes.get_axis_labels(x_label="x", y_label="y")))
        self.play(Create(graph), Write(graph_label))
        self.play(FadeIn(p_dot), Write(p_label))
        self.wait(1)
        
        # Draw dashed lines from p to the x-axis and y-axis (projections)
        x_proj = DashedLine(p_coords, axes.c2p(a, 0), color=RED)
        y_proj = DashedLine(p_coords, axes.c2p(0, f(a)), color=RED)
        x_proj_dot = Dot(axes.c2p(a, 0), color=WHITE)
        y_proj_dot = Dot(axes.c2p(0, f(a)), color=WHITE)
        x_proj_label = MathTex(f"a").next_to(x_proj_dot, DOWN)
        y_proj_label = MathTex(f"f(a)").next_to(y_proj_dot, LEFT)

        self.play(Create(x_proj), Create(y_proj))
        self.play(FadeIn(x_proj_dot), FadeIn(y_proj_dot))
        self.play(Write(x_proj_label), Write(y_proj_label))
        self.wait(1)
        # self.play(FadeOut(x_proj), FadeOut(y_proj), FadeOut(x_proj_dot), FadeOut(y_proj_dot), FadeOut(x_proj_label), FadeOut(y_proj_label))

        # 2. VISUALIZE T_p(C): The 1D Tangent Line Subspace
        self.wait(1)
        # Define the tangent vector v_p = <1, f'(a)>
        v_p_vec = np.array([1, f_prime(a), 0])
        v_p_arrow = Arrow(p_coords, p_coords + v_p_vec, buff=0, color=ORANGE)
        v_p_label = MathTex(r"\vec{v}_p=\begin{pmatrix}1\\ f'(a) \end{pmatrix}", color=ORANGE).next_to(v_p_arrow.get_end(), RIGHT)
        self.play(GrowArrow(v_p_arrow), Write(v_p_label))
        self.wait(2)
        # self.play(FadeOut(v_p_label))

        # Create an infinite line that represents the span of v_p
        tangent_line = Line(
            p_coords - 3 * v_p_vec, 
            p_coords + 3 * v_p_vec, 
            color=ORANGE, 
            stroke_width=6
        )
        
        line_label = MathTex(r"T_pC = \text{span}\{\vec{v}_p\}", color=ORANGE, font_size=40)
        line_label.next_to(tangent_line.get_end(), UR)

        # # Fade out the plane's label to reduce clutter
        # self.play(FadeOut(plane_label))

        # Animate the tangent line and its defining vector
        self.play(Create(tangent_line))
        self.play(Write(line_label))
        self.wait(1)
        self.play(FadeOut(tangent_line), FadeOut(line_label),FadeOut(x_proj), FadeOut(y_proj), FadeOut(x_proj_dot), FadeOut(y_proj_dot), FadeOut(x_proj_label), FadeOut(y_proj_label))
        self.play(FadeOut(p_label))
        p_label = MathTex("p", color=RED).next_to(p_dot, DL)
        self.play(Write(p_label))
        self.wait(2)

        # 3. VISUALIZE T_p(R^2): The 2D Tangent Plane
        # Zoom in at point p
        frame = self.camera.frame
        frame.save_state()
        # Zoom in and scale up (make the view tighter and objects larger)
        self.play(
            frame.animate.move_to(p_coords).scale(0.75),  # scale < 1 zooms in
            run_time=2
        )
        self.wait(1)
        
        # Draw the basis vectors for T_p(R^2)
        basis_e1 = Arrow(p_coords, p_coords + RIGHT, buff=0, color=GREEN)
        basis_e2 = Arrow(p_coords, p_coords + UP, buff=0, color=GREEN)
        basis_e1_label = MathTex(r"\begin{pmatrix}1\\ 0\end{pmatrix}_p", color=GREEN).next_to(basis_e1, RIGHT)
        basis_e2_label = MathTex(r"\begin{pmatrix}0\\ 1\end{pmatrix}_p", color=GREEN).next_to(basis_e2, UP)

        self.play(
            GrowArrow(basis_e1),
            GrowArrow(basis_e2),
            Write(basis_e1_label),
            Write(basis_e2_label)
        )
        self.wait(1)
        
        # Create a transparent plane to represent the tangent space
        plane = Square(
            side_length=3,
            fill_color=GREEN,
            fill_opacity=0.3,
            stroke_width=1,
            stroke_color=WHITE
        ).move_to(p_coords)

        plane_label = MathTex(
            r"\text{span}\left\{\begin{pmatrix}1\\ 0\end{pmatrix}_p, \begin{pmatrix}0\\ 1\end{pmatrix}_p\right\} = T_p\mathbb{R}^2 \cong \mathbb{R}^2",
            font_size=48
        ).next_to(plane, DOWN, buff=0.00001)

        self.play(Create(plane))
        self.play(Write(plane_label))
        self.wait(1)
        
        # self.play(Write(local_axes_labels))
        self.play(FadeOut(v_p_arrow), FadeOut(v_p_label), FadeOut(basis_e1_label), FadeOut(basis_e2_label))
        v_p_label = MathTex(r"\vec{v}_p=1\cdot \begin{pmatrix}1\\ 0\end{pmatrix}_p+f'(a)\cdot \begin{pmatrix}0\\ 1\end{pmatrix}_p", color=ORANGE).next_to(v_p_arrow.get_end(), UP)
        self.play(GrowArrow(v_p_arrow), Write(v_p_label))
        
        # Draw new axes at p, treating p as the origin
        self.play(FadeOut(axes), FadeOut(graph_label), FadeOut(basis_e1), FadeOut(basis_e2))
        self.play(FadeOut(plane_label), FadeOut(p_label))
        plane_label = MathTex(
            r"T_p\mathbb{R}^2 \cong \mathbb{R}^2",
            font_size=48
        ).next_to(plane, DOWN, buff=0.00001)
        self.play(Write(plane_label))
        local_axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            axis_config={"color": PURPLE}
        ).move_to(p_coords)

        # local_axes_labels = local_axes.get_axis_labels(x_label="x_p", y_label="y_p")
        self.play(Create(local_axes))
        # self.play(Write(local_axes_labels))

        self.wait(1)

        # Further zoom in and center at p for a tighter fit
        # Zoom out but keep the origin at p (fit more of the plane around p)
        # Zoom in further on the local coordinates to make them appear larger
        self.play(
            frame.animate.move_to(p_coords).scale(0.75),  # scale < 1 zooms in more
            run_time=2
        )
        self.wait(1)

        # Draw projections dx(\vec{v}_p)=1 and dy(\vec{v}_p)=f'(a)
        dx_arrow = Arrow(
            p_coords,
            p_coords + RIGHT,
            buff=0,
            color=BLUE_B
        )
        dx_label = MathTex(r"dx(\vec{v}_p)=1", color=BLUE_B).next_to(dx_arrow, DOWN)

        dy_arrow = Arrow(
            p_coords,
            p_coords + f_prime(a) * UP,
            buff=0,
            color=TEAL
        )
        dy_label = MathTex(r"dy(\vec{v}_p)=f'(a)", color=TEAL).next_to(dy_arrow, LEFT)

        self.play(GrowArrow(dx_arrow), Write(dx_label))
        self.wait(0.5)
        self.play(GrowArrow(dy_arrow), Write(dy_label))
        self.wait(2)
        
        # Zoom out to original frame
        # self.play(FadeOut(plane), FadeOut(plane_label), FadeOut(local_axes))
        self.play(frame.animate.restore().scale(1.4), run_time=2)
        self.wait(1)

        self.play(FadeOut(v_p_label))
        v_p_label = MathTex(r"\vec{v}_p=dx(\vec{v}_p)\cdot \begin{pmatrix}1\\ 0\end{pmatrix}_p+dy(\vec{v}_p)\cdot \begin{pmatrix}0\\ 1\end{pmatrix}_p", color=ORANGE).next_to(v_p_arrow.get_end(), RIGHT)
        self.play(Write(v_p_label))
        
        