import arcade
from tool import PencilTool, MarkerTool, SprayTool, EraserTool
import math, random  # para spray

SPRAY_POINTS = 100 # cuántos puntos por tick
SPRAY_RADIUS = 20 # radio del spray

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
        self.prev_color = None  # <-- para restaurar color al salir del borrador
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
    # -------- Herramientas --------
        if symbol == arcade.key.KEY_1:
            # si venimos del eraser, restaurar color anterior
            if self.tool.name == "ERASER" and self.prev_color is not None:
                self.color = self.prev_color
                self.prev_color = None
            self.tool = PencilTool()
            self.used_tools[self.tool.name] = self.tool

        elif symbol == arcade.key.KEY_2:
            if self.tool.name == "ERASER" and self.prev_color is not None:
                self.color = self.prev_color
                self.prev_color = None
            self.tool = MarkerTool()
            self.used_tools[self.tool.name] = self.tool

        elif symbol == arcade.key.KEY_3:
            if self.tool.name == "ERASER" and self.prev_color is not None:
                self.color = self.prev_color
                self.prev_color = None
            self.tool = SprayTool()
            self.used_tools[self.tool.name] = self.tool

        elif symbol == arcade.key.KEY_4:
            # al entrar al eraser, guardamos el color actual una sola vez
            if self.prev_color is None:
                self.prev_color = self.color # guardamos el color de antes en prev_color
            self.tool = EraserTool()
            self.tool.bg_color = self.background_color  # el eraser pinta del color del fondo
            self.color = self.background_color          # y forzamos el color actual a fondo
            self.used_tools[self.tool.name] = self.tool

        # -------- Colores (A/S/D) --------
        elif symbol == arcade.key.A:
            if self.tool.name != "ERASER":
                self.color = arcade.color.RED
            else:
                # si estás en eraser, mantén el color del fondo
                self.color = self.background_color
        elif symbol == arcade.key.S:
            if self.tool.name != "ERASER":
                self.color = arcade.color.GREEN
            else:
                self.color = self.background_color
        elif symbol == arcade.key.D:
            if self.tool.name != "ERASER":
                self.color = arcade.color.BLUE
            else:
                self.color = self.background_color
        
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
        # recorre todos los trazos en el orden que se hicieron
        for trace in self.traces:
            tool = self.used_tools.get(trace["tool"])
            if tool:
                tool.draw_traces([trace])

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
