from manim import *

class LorentzForce(Scene):
    def construct(self):
        # --- Introduction ---
        title = Tex("The Lorentz Force").scale(1.5)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # --- Electric Field ---
        electric_field_text = Tex("Electric Field (E)").to_corner(UP + LEFT)
        self.play(Write(electric_field_text))

        electric_field_lines = VGroup(*[
            Line(start=[-3, i, 0], end=[3, i, 0]).set_color(YELLOW) for i in np.linspace(-2, 2, 5)
        ])
        self.play(Create(electric_field_lines))

        self.wait(1)

        # --- Magnetic Field ---
        magnetic_field_text = Tex("Magnetic Field (B)").to_corner(UP + RIGHT)
        self.play(Write(magnetic_field_text))

        magnetic_field_dots = VGroup(*[
            Dot(point=[i, j, 0], color=BLUE) for i in np.linspace(-2,2,5) for j in np.linspace(-2,2,5)
        ])
        self.play(Create(magnetic_field_dots))
        self.wait(1)

        # --- Moving Charged Particle (Electron) ---
        charged_particle = Dot(color=BLUE, radius=0.2)
        charged_particle.move_to([-4,0,0])
        charge_label = Tex("-e").scale(0.7).next_to(charged_particle, RIGHT)
        self.play(Create(charged_particle),Write(charge_label))

        self.wait(1)

        # --- Electric Force Only ---
        electric_force_text = Tex("Electric Force (F$_E$)").to_edge(DOWN+LEFT)
        self.play(Write(electric_force_text))
        self.play(charged_particle.animate.shift([-4,0,0])) # Changed direction
        electric_force_arrow=Arrow(start=charged_particle.get_center(),end = charged_particle.get_center() +[-4,0,0], color= YELLOW) # Changed direction
        self.play(Create(electric_force_arrow))
        self.wait(1)
        self.play(FadeOut(electric_force_arrow),FadeOut(electric_force_text))

        # --- Magnetic Force Only ---
        magnetic_force_text = Tex("Magnetic Force (F$_B$)").to_edge(DOWN+RIGHT)
        self.play(Write(magnetic_force_text))
        self.play(charged_particle.animate.shift([4,0,0])) # Changed direction

        # Now the magnetic force will be inwards from the screen (due to negative charge)
        magnetic_force_arrow = Arrow(start = charged_particle.get_center(), end = charged_particle.get_center() + [0,0,-0.5] , color = BLUE).rotate(PI/2,axis = RIGHT) # Changed direction
        self.play(Create(magnetic_force_arrow))

        self.wait(1)
        self.play(FadeOut(magnetic_force_arrow), FadeOut(magnetic_force_text))

        # --- Lorentz Force ---
        lorentz_force_text = Tex("Lorentz Force (F)").to_edge(DOWN)
        self.play(Write(lorentz_force_text))

        self.play(charged_particle.animate.shift([-4,0,0]))# Changed direction

        lorentz_force_arrow = Arrow(start = charged_particle.get_center(), end = charged_particle.get_center() + [-4, -0.5, -0.5], color=GREEN).rotate(PI/2, axis=RIGHT) # Changed direction
        self.play(Create(lorentz_force_arrow))
        self.wait(1)

        self.play(FadeOut(lorentz_force_arrow), FadeOut(lorentz_force_text), FadeOut(electric_field_lines),
                    FadeOut(magnetic_field_dots),FadeOut(charge_label),FadeOut(charged_particle),FadeOut(magnetic_field_text),
                    FadeOut(electric_field_text))


        # --- Conclusion ---
        conclusion = Tex("Lorentz Force: F = q(E + v x B)").scale(1.2)
        self.play(Write(conclusion))
        self.wait(3)