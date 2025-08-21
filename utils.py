import json

def save_traces(traces: list[dict]) -> None:
    """
    Guarda las trazas en un archivo JSON.
    
    :param traces: Lista de trazas a guardar.
    """
    with open("traces.json", "w") as file:
        json.dump(traces, file, indent=4)
        print("Trazas guardadas en 'traces.json'.")
