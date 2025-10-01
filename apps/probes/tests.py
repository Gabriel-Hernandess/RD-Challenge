import pytest
from apps.probes.models import Probe

@pytest.mark.django_db
def test_create_probe(auth_client):
    data = {"direction": "NORTH", "mesh_x": 5, "mesh_y": 5}
    response = auth_client.post("/api/probes/", data, format="json")
    
    assert response.status_code == 201
    assert response.data["pos_x"] == 0
    assert response.data["pos_y"] == 0
    assert response.data["direction"] == "NORTH"

@pytest.mark.django_db
def test_move_probe(auth_client):
    probe = Probe.objects.create(direction="NORTH", mesh_x=5, mesh_y=5)
    response = auth_client.put(f"/api/probes/{probe.id}/move/", {"commands": "MRML"}, format="json")
    
    assert response.status_code == 200
    assert 0 <= response.data["pos_x"] <= probe.mesh_x
    assert 0 <= response.data["pos_y"] <= probe.mesh_y

@pytest.mark.django_db
def test_move_probe_invalid_command(auth_client):
    # Cria uma sonda
    probe = Probe.objects.create(direction="NORTH", mesh_x=5, mesh_y=5)
    
    # Comando inválido 'Z'
    response = auth_client.put(f"/api/probes/{probe.id}/move/", {"commands": "MRZL"}, format="json")
    
    # Deve retornar 400 com erro
    assert response.status_code == 400
    assert "error" in response.data

@pytest.mark.django_db
def test_move_probe_out_of_bounds(auth_client):
    probe = Probe.objects.create(direction="NORTH", mesh_x=1, mesh_y=1)
    response = auth_client.put(f"/api/probes/{probe.id}/move/", {"commands": "MMMM"}, format="json")
    
    assert response.status_code == 400
    assert "ultrapassa os limites" in response.data["error"]

@pytest.mark.django_db
def test_delete_probe(auth_client):
    probe = Probe.objects.create(direction="NORTH", mesh_x=5, mesh_y=5)
    response = auth_client.delete(f"/api/probes/{probe.id}/")
    
    assert response.status_code == 204
    assert not Probe.objects.filter(id=probe.id).exists()