
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, DirectionalLight, AmbientLight
from panda3d.core import NodePath
import random

class Boid:
    def __init__(self, model, position, velocity):
        self.model = model
        self.position = position
        self.velocity = velocity

    def update(self, dt):
        self.position += self.velocity * dt
        self.model.set_pos(self.position)
        # Make the model face the direction it's moving
        if self.velocity.length() > 0:
            self.model.look_at(self.position + self.velocity)

class BoidApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable default camera control so we can set our own
        self.disable_mouse()

        # Set camera position and look at center
        self.camera.set_pos(0, -50, 30)
        self.camera.look_at(0, 0, 0)

        # Lighting setup
        dlight = DirectionalLight('dlight')
        dlight.set_color((0.8, 0.8, 0.8, 1))
        dlight_np = self.render.attach_new_node(dlight)
        dlight_np.set_hpr(-30, -60, 0)
        self.render.set_light(dlight_np)

        alight = AmbientLight('alight')
        alight.set_color((0.2, 0.2, 0.2, 1))
        alight_np = self.render.attach_new_node(alight)
        self.render.set_light(alight_np)

        # Load a simple model for the boid (a cone)
        self.boids = []
        for _ in range(20):
            model = self.loader.load_model('models/misc/cone')  # built-in model in Panda3D
            model.reparent_to(self.render)
            model.set_scale(0.5)
            pos = Vec3(random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(0, 10))
            vel = Vec3(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-0.5, 0.5))
            boid = Boid(model, pos, vel)
            self.boids.append(boid)

        # Add the update task
        self.task_mgr.add(self.update, 'update')

    def update(self, task):
        dt = globalClock.get_dt()
        for boid in self.boids:
            boid.update(dt)
        return task.cont

if __name__ == '__main__':
    app = BoidApp()
    app.run()
