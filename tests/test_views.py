def test_add_pet(client, jwt):
    r = client.post(
        "/pets",
        json=dict(
            pet_type="cat",
            name="tospik",
            breed="persian",
            owner="emreisikligil"
        ),
        headers=dict(Authorization=f"Bearer {jwt}")
    )
    assert r.status_code == 201
    body = r.json
    assert body["id"]
    assert body["name"] == "tospik"
    assert body["breed"] == "persian"
    assert body["owner"] == "emreisikligil"


def test_get_pets(client, jwt):
    r = client.get(
        "/pets",
        headers=dict(Authorization=f"Bearer {jwt}")
    )

    assert r.status_code == 200
    body = r.json
    assert len(body) == 1
    assert body[0]["id"]
    assert body[0]["name"] == "tospik"
    assert body[0]["breed"] == "persian"
    assert body[0]["owner"] == "emreisikligil"
