import arcade
from tool import PencilTool, MarkerTool, SprayTool
import math, random  # para spray

SPRAY_POINTS = 20 # cuántos puntos por tick
SPRAY_RADIUS = 12 # radio del spray

WIDTH = 800
HEIGHT = 600
TITLE = "Paint"

COLORS = {
    "black": arcade.color.BLACK,
    "red": arcade.color.RED,
    "blue": arcade.color.BLUE,
    "yellow": arcade.color.YELLOW,
    "green": arcade.color.GREEN,
}


class Paint(arcade.View):
    def __init__(self, load_path: str = None):
        super().__init__()
        self.background_color = arcade.color.WHITE
        self.tool = PencilTool()
        self.used_tools = {self.tool.name: self.tool}
        self.color = arcade.color.BLUE
        if load_path is not None:
            ### IMPLEMENTAR CARGA DE DIBUJO ###
            self.traces = []
        else:
            self.traces = []

    def on_key_press(self, symbol: int, modifiers: int):
        # Selección de herramientas con las teclas numéricas
        if symbol == arcade.key.KEY_1:
            self.tool = PencilTool()
        elif symbol == arcade.key.KEY_2:
            self.tool = MarkerTool()
            # other tool
        elif symbol == arcade.key.KEY_3:
            self.tool = SprayTool()
        # Selección de color con teclas asd
        elif symbol == arcade.key.A:
            self.color = arcade.color.RED
        elif symbol == arcade.key.S:
            self.color = arcade.color.GREEN
        elif symbol == arcade.key.D:
            self.color = arcade.color.BLUE
        
        # Guardado del dibujo con la tecla O
        ### IMPLEMENTAR ###
        ####-----------####
        self.used_tools[self.tool.name] = self.tool
        print(self.used_tools, self.tool)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        print(x, y)
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.tool.name == "SPRAY":
                pts = self._spray_points(x, y, SPRAY_POINTS, SPRAY_RADIUS)
                self.traces.append({"tool": self.tool.name, "color": self.color, "trace": pts})
            else: # Pencil or Marker
                self.traces.append({"tool": self.tool.name, "color": self.color, "trace":[(x, y)]})

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        if self.traces:
            self.traces[-1]["trace"].append((x, y))

    def on_draw(self):
        self.clear()
        for tool in self.used_tools.values():
            tool.draw_traces(self.traces)


    def _spray_points(self, cx: int, cy: int, n: int, radius: int):
        pts = []
        for _ in range(n):
            # Generamos un punto aleatorio dentro de un cuadrado
            # centrado en (cx, cy) con lados de tamaño 2*radius
            px = random.randint(cx - radius, cx + radius)
            py = random.randint(cy - radius, cy + radius)
            pts.append((px, py))
        return pts

if __name__ == "__main__":
    import sys
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    # Invocación del programa en la forma: python main.py ruta/a/mi/archivo
    if len(sys.argv) > 1:
        app = Paint(sys.argv[1])
    else:
        app = Paint()
    window.show_view(app)
    arcade.run()
