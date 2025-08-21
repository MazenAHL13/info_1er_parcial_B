import arcade
from typing import Protocol, Union


class Tool(Protocol):
    name: str
    def draw_traces(self, traces: list[list[int]]):
        pass

    def get_name(self):
        return self.name


class PencilTool(Tool):
    name = "PENCIL"
    line_width = 2

    def draw_traces(self, traces: list[dict[str]]):
        for trace in traces:
            if trace["tool"] == self.name:
                arcade.draw_line_strip(trace["trace"], 
                                       trace["color"], 
                                       line_width=self.line_width
                                       )
class MarkerTool(PencilTool):
    name = "MARKER"
    line_width = 5

class SprayTool(Tool):
    name = "SPRAY"
    point_size = 2
    
    def draw_traces(self, traces):
        for trace in traces:
            if trace["tool"] == self.name and len(trace["trace"]) >= 1:
                arcade.draw_points(
                    trace["trace"],       # lista de puntos sueltos
                    trace["color"],
                    size=self.point_size
                )

class EraserTool(MarkerTool):
    name = "ERASER"
    line_width = 20
    bg_color = arcade.color.WHITE  # Color de fondo para el borrador

    def draw_traces(self, traces: list[dict]):
        # Dibuja SIEMPRE con el color de fondo, ignorando trace["color"]
        for trace in traces:
            if trace["tool"] == self.name and len(trace["trace"]) >= 2:
                arcade.draw_line_strip(
                    trace["trace"],
                    self.bg_color,           # <--- color del fondo
                    line_width=self.line_width
                )