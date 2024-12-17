from manim import *
import numpy as np

class LorentzForce3D(ThreeDScene):
    def construct(self):
        # Set up the scene and camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.renderer.background_color = WHITE

        # Title
        title = Text("Die Lorentzkraft", font_size=48, color=BLACK).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Magnetic field
        magnetic_field = ArrowVectorField(
            lambda p: np.array([0., 1., 0.]),
            x_range=[-5., 5., 1.],
            y_range=[-2., 4., 1.],
            z_range=[-2., 2., 1.],
            color=BLUE,
        ).scale(0.7)
        self.add(magnetic_field)

        b_field_label = Text("Magnetfeld (B)", font_size=24, color=BLUE).next_to(magnetic_field, UP, buff=0.2)
        self.play(Write(b_field_label))
        self.wait(1)

        # Charge
        charge = Sphere(radius=0.3, color=RED, resolution=(10,10))
        charge_label = Text("Positive Ladung (q)", font_size=24, color=RED).next_to(charge, LEFT, buff=0.2)
        self.play(Create(charge))
        self.play(Write(charge_label))
        self.wait(1)

        # Velocity vector
        velocity_arrow = Arrow(start=charge.get_center(), end=charge.get_center() + [1, 0, 0], color=GREEN, buff=0.1).set_length(1.5)
        velocity_label = Text("Geschwindigkeit (v)", font_size=24, color=GREEN).next_to(velocity_arrow.get_end(), RIGHT, buff=0.2)
        self.play(Create(velocity_arrow))
        self.play(Write(velocity_label))
        self.wait(1)

        # Lorentz force (calculated)
        force_vector = Arrow(start=charge.get_center(), end=charge.get_center() + [0, 0, -1], color=PURPLE, buff=0.1).set_length(1.5)
        force_label = Text("Lorentzkraft (F)", font_size=24, color=PURPLE).next_to(force_vector.get_end(), LEFT, buff=0.2)
        self.play(Create(force_vector))
        self.play(Write(force_label))
        self.wait(1)


        # Brief explanation text (German)
        explanation_1 = Text("Eine bewegte Ladung in einem Magnetfeld", font_size=24, color=BLACK).to_edge(DOWN, buff=1.2).shift(LEFT*1.5)
        explanation_2 = Text("erfährt eine Kraft, senkrecht zur Geschwindigkeit und zum Magnetfeld", font_size=24, color=BLACK).next_to(explanation_1, DOWN).shift(LEFT*1.5)

        self.play(Write(explanation_1))
        self.play(Write(explanation_2))
        self.wait(2)


        #Movement Simulation
        velocity_vector = np.array([1., 0., 0.])
        force_vector_np = np.array([0.,0.,-1.]) #Force direction


        def update_charge(mob, dt):
            nonlocal velocity_vector, force_vector_np
            force_norm = np.linalg.norm(force_vector_np)
            velocity_norm = np.linalg.norm(velocity_vector)
            velocity_vector_norm = velocity_vector/velocity_norm
            force_vector_norm = force_vector_np/force_norm
            mob.move_to(mob.get_center() + dt*(velocity_vector_norm + 0.1*force_vector_norm))

            # Update direction of velocity vector
            velocity_vector = velocity_vector + dt*0.1*force_vector_norm
            velocity_norm = np.linalg.norm(velocity_vector)
            velocity_arrow.become(Arrow(start=mob.get_center(), end=mob.get_center() + velocity_vector, color=GREEN, buff=0.1).set_length(1.5))

            # Update direction of force vector.
            force_vector_np = np.cross(velocity_vector,[0,1,0])
            force_norm = np.linalg.norm(force_vector_np)
            force_vector.become(Arrow(start=mob.get_center(), end=mob.get_center() + force_vector_np, color=PURPLE, buff=0.1).set_length(1.5))


        self.play(charge.animate.move_to(charge.get_center() + [1, 0, 0]))
        self.play(charge.animate.set_z(charge.get_z()-0.1))

        self.play(
                charge.animate.move_to(charge.get_center()+ [2, 0, 0]),
                UpdateFromFunc(charge,lambda mob : update_charge(mob, self.dt)),
                rate_func=linear, run_time=5
        )

        self.play(FadeOut(explanation_1,explanation_2,force_label,force_vector,velocity_label,velocity_arrow))

        self.wait(1)


        # Right hand rule (Flemings law)
        rule_text = Text("Rechte-Hand-Regel (Drei-Finger-Regel)", font_size=30, color=BLACK).to_edge(UP,buff=0.2)
        self.play(Transform(title, rule_text))

        hand_label = Text("Daumen: Kraftrichtung (F)", font_size=18, color=PURPLE).shift(LEFT*2+DOWN*2).scale(1.1).shift(LEFT*1)
        middle_label = Text("Zeigefinger: Magnetfeldrichtung (B)", font_size=18, color=BLUE).shift(RIGHT*2+DOWN*2).scale(1.1).shift(RIGHT*1)
        index_label = Text("Mittelfinger: Bewegungsrichtung (v)", font_size=18, color=GREEN).shift(DOWN*1).scale(1.1)
        self.play(Write(hand_label), Write(middle_label), Write(index_label))
        self.wait(1)


        hand_3d = Group(
            Line3D([-0.8,-1,0], [0.5,-0.5,0],color=PURPLE), # Thumb
            Line3D([0,0,0], [0,1.5,0],color=BLUE), #index
            Line3D([0,0,0],[1,0,0],color=GREEN), # middle
        ).rotate(PI/2,axis=[1,0,0]).move_to(ORIGIN).scale(1.5)
        self.play(self.camera.animate.set(zoom = 1.5,center = hand_3d.get_center()))

        self.add(hand_3d)
        self.wait(2)
        self.play(FadeOut(hand_label,middle_label,index_label, hand_3d),Transform(title, title),run_time = 1)
        self.play(self.camera.animate.set(zoom = 1,center = ORIGIN))
        self.wait(2)


        # Final thoughts
        final_text = Text("Die Lorentzkraft ist fundamental für Elektromotoren und viele andere Technologien.",
                          font_size=24, color=BLACK).to_edge(DOWN, buff=1)

        self.play(Write(final_text))
        self.wait(3)
        self.play(FadeOut(final_text,title,magnetic_field,b_field_label, charge, charge_label))

        self.wait(1)