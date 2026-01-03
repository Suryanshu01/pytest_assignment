import pytest


class TestPosts:

    def test_get_post_by_id(self, session, base_url):
        response = session.get(f"{base_url}/posts/1")
        assert response.status_code == 200

        data = response.json()
        assert {"userId", "id", "title", "body"} <= data.keys()
        assert data["id"] == 1

    @pytest.mark.parametrize(
        "payload",
        [
            {"title": "foo", "body": "bar", "userId": 1},
            {"title": "test", "body": "content", "userId": 10},
        ],
    )
    def test_create_post(self, session, base_url, payload):
        response = session.post(f"{base_url}/posts", json=payload)
        assert response.status_code == 201

        data = response.json()
        assert data["title"] == payload["title"]
        assert data["body"] == payload["body"]
        assert data["userId"] == payload["userId"]
        assert "id" in data

    @pytest.mark.parametrize(
        "post_id, payload",
        [
            (1, {"title": "updated", "body": "updated body", "userId": 1}),
            (2, {"title": "new title", "body": "new body", "userId": 2}),
        ],
    )
    def test_update_post(self, session, base_url, post_id, payload):
        response = session.put(f"{base_url}/posts/{post_id}", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == post_id

    def test_delete_post(self, session, base_url):
        response = session.delete(f"{base_url}/posts/1")
        assert response.status_code == 200

    def test_get_non_existing_post(self, session, base_url):
        response = session.get(f"{base_url}/posts/999999")
        assert response.status_code == 404
