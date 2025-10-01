from django.db import models
import uuid

class Direction(models.TextChoices):
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"

class Probe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pos_x = models.PositiveIntegerField(default=0)
    pos_y = models.PositiveIntegerField(default=0)
    direction = models.CharField(
        max_length=5,
        choices=Direction.choices,
        default=Direction.NORTH
    )
    mesh_x = models.PositiveIntegerField(default=5)  # tamanho da malha X
    mesh_y = models.PositiveIntegerField(default=5)  # tamanho da malha Y
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Probe {self.id} at ({self.pos_x}, {self.pos_y}) facing {self.direction}"