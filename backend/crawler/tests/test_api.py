from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from crawler.models import Task
from optifino.asgi import app

client = TestClient(app)

base_url = "/api/crawler/"


@pytest.mark.django_db
def test_post_task_with_correct_url():
    test_url = "https://www.test.com"
    # Act
    response = client.post(base_url + "tasks/", json={"site_url": test_url})
    # Assert
    assert response.status_code == HTTPStatus.CREATED
    task_payload = response.json()
    assert task_payload['id'] > 0
    assert task_payload['created_at'] is not None
    assert task_payload['status'] == "pending"
    assert task_payload['site_url'] == test_url


@pytest.mark.django_db(transaction=True)
def test_get_task_by_id():
    test_url = "https://www.test.com"
    task = Task.objects.create(site_url=test_url)
    # Act
    response = client.get(base_url + f"tasks/{task.id}")
    # Assert
    assert response.status_code == HTTPStatus.OK
    task_payload = response.json()
    assert task_payload['id'] == task.id
    assert task_payload['created_at'] is not None
    assert task_payload['status'] == "pending"
    assert task_payload['site_url'] == test_url
