from .models import Probe

class InvalidCommandError(Exception):
    pass

ROTATE_LEFT = {
    "NORTH": "WEST",
    "WEST": "SOUTH",
    "SOUTH": "EAST",
    "EAST": "NORTH"
}

ROTATE_RIGHT = {
    "NORTH": "EAST",
    "EAST": "SOUTH",
    "SOUTH": "WEST",
    "WEST": "NORTH"
}

def move_probe(probe: Probe, commands: str) -> Probe:
    for c in commands.upper():
        if c not in "MLR":
            raise InvalidCommandError(f"Comando inválido: {c}")
        if c == "L":
            probe.direction = ROTATE_LEFT[probe.direction]
        elif c == "R":
            probe.direction = ROTATE_RIGHT[probe.direction]
        elif c == "M":
            if probe.direction == "NORTH" and probe.pos_y < probe.mesh_y:
                probe.pos_y += 1
            elif probe.direction == "SOUTH" and probe.pos_y > 0:
                probe.pos_y -= 1
            elif probe.direction == "EAST" and probe.pos_x < probe.mesh_x:
                probe.pos_x += 1
            elif probe.direction == "WEST" and probe.pos_x > 0:
                probe.pos_x -= 1
            else:
                raise InvalidCommandError("Movimento ultrapassa os limites do planalto")
    probe.save()
    return probe