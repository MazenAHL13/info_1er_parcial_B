import arcade
from tool import PencilTool, MarkerTool, SprayTool, EraserTool
import math, random  # para spray
import utils
import json, os

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
        if load_path is not None and os.path.exists(load_path):
            with open(load_path, "r") as f:
                self.traces = json.load(f)
        else:
            self.traces = []

        # Inicializamos used_tools con todas las herramientas que aparecen en los trazos
        self.used_tools = {}
        for trace in self.traces:
            if trace["tool"] == "PENCIL":
                self.used_tools["PENCIL"] = PencilTool()
            elif trace["tool"] == "MARKER":
                self.used_tools["MARKER"] = MarkerTool()
            elif trace["tool"] == "SPRAY":
                self.used_tools["SPRAY"] = SprayTool()
            elif trace["tool"] == "ERASER":
                eraser = EraserTool()
                eraser.bg_color = self.background_color
                self.used_tools["ERASER"] = eraser

        # Aseguramos que la herramienta inicial (PENCIL) siempre exista en el diccionario
        self.used_tools[self.tool.name] = self.tool

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
        # -------- Guardado y Carga --------
        elif symbol == arcade.key.KEY_0:
            utils.save_traces(self.traces)  # guarda en "traces.json"
            return
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
        elif symbol == arcade.key.F:
            if self.tool.name != "ERASER":
                self.color = arcade.color.BLACK
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
        # 1) Dibujar los trazos
        for trace in self.traces:
            tool = self.used_tools.get(trace["tool"])
            if tool:
                tool.draw_traces([trace])

        # 2) Título (usar argumentos posicionales)
        arcade.draw_text(
            "El Paint de Mazen",
            WIDTH // 2, HEIGHT - 8,           # x, y
            arcade.color.BLACK, 20,           # color, font_size
            anchor_x="center", anchor_y="top"
        )

        # 3) Lista simple de atajos
        start_x = WIDTH - 220 + 10
        start_y = HEIGHT - 40
        line_h = 22
        lines = [
            "1 = Pencil",
            "2 = Marker",
            "3 = Spray",
            "4 = Eraser",
            "A = Red",
            "S = Green",
            "D = Blue",
            "F = Black",
            "0 = Guardar",
        ]
        for i, label in enumerate(lines):
            y = start_y - i * line_h
            arcade.draw_text(
                label,
                start_x, y,                     # x, y
                arcade.color.BLACK, 14,         # color, font_size
                anchor_x="left", anchor_y="center"
            )
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
