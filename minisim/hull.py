
from minisim.config import DEFAULT_OUTPUT_DIR
from minisim.render.plot2d import plot_hull_views, animate_hull_views
from minisim.world.environment import waveField
from minisim.simulator import Simulator
from minisim.ship import Ship
import math

def load_obj(path):
    vertices = []
    faces = []
    with open(path, encoding = "utf-8") as file:
        for line in file:
            parts = line.split()
            if not parts:continue
            if parts[0] == "v":
                vertex = (float(parts[1]), float(parts[2]), float(parts[3]))
                vertices.append(vertex)
            if parts[0] == "f":
                face = []
                for v in parts[1:]:
                    face.append(int(v) - 1)
                faces.append(face)
    return vertices, faces

if __name__ == "__main__":
    vertices, faces = load_obj("3d/first/MiniShipSim_Hull.obj")
    print("顶点数：", len(vertices))
    print("面数：", len(faces))
    print("第一个顶点：", vertices[0])
    print("第一个面：", faces[0])

    ship = Ship()
    wave = waveField(amplitude=0.3, wavelength=8.0, speed=1.0, direction= math.pi/4)
    sim = Simulator(ship, wave)
    sim.run(dt = 0.1, steps = 100)

    pose_a = sim.history[0]
    pose_b = sim.history[20]

    plot_hull_views(
        vertices,
        faces,
        DEFAULT_OUTPUT_DIR / "hull_t0.png",
        pose = pose_a,
        wave = wave
    )

    plot_hull_views(
        vertices,
        faces,
        DEFAULT_OUTPUT_DIR / "hull_t2.png",
        pose = pose_b,
        wave = wave
    )

    animate_hull_views(vertices, faces, sim.history, wave=wave)

