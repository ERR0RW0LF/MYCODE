from manim import *

# Short explanation of the Lorentz force in German on physics level with a simple example and a animation of the force acting on a moving charge in a magnetic field.
# all the text should be in German
# the animation should be in a 3D coordinate system
# all the elements should have there name be displayed in the animation next to them (e.g. the magnetic field should have the name "Magnetfeld" next to it)
class Erklärung(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        force = Arrow3D(start=ORIGIN, end=RIGHT, color=RED)
        electronic_current = Arrow3D(start=ORIGIN, end=UP, color=GREEN)
        magnetic_field = Arrow3D(start=ORIGIN, end=OUT, color=BLUE)
        
        force_text = Text("Lorentzkraft", font="Arial").scale(0.4).next_to(force, RIGHT, buff=0.1).rotate(75*DEGREES, axis=UP).rotate(30*DEGREES, axis=OUT).rotate(90*DEGREES, axis=OUT, about_point=force.get_center())
        electronic_current_text = Text("Stromfluss", font="Arial").scale(0.4).next_to(electronic_current, UP, buff=0.1).rotate(75*DEGREES, axis=UP).rotate(30*DEGREES, axis=OUT)
        magnetic_field_text = Text("Magnetfeld", font="Arial").scale(0.4).next_to(magnetic_field, OUT, buff=0.1).rotate(75*DEGREES, axis=UP).rotate(30*DEGREES, axis=OUT)
        # q: how do i rotate the text so it is always facing the camera?
        # a: use the rotate method with the axis parameter
        
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.play(Create(axes))
        self.play(Create(force),Create(force_text))
        self.play(Create(electronic_current),Create(electronic_current_text))
        self.play(Create(magnetic_field),Create(magnetic_field_text))
        self.wait(1)
