import os

import pytest

from crawler.models import Link
from crawler.models import Task
from crawler.models.task import TaskStatus
from crawler.services.collector import robot_parser
from crawler.tasks import parse_links


def read_file(filename):
    dir_path = os.path.dirname(__file__)
    file_path = os.path.join(dir_path, filename)
    with open(file_path, "r", encoding='utf-8') as f:
        return f.read()


@pytest.mark.django_db
def test_parse_links(requests_mock, mocker):
    stub_content = read_file('wiki_page.html')
    test_url = "https://en.wikipedia.org/wiki/Django_(web_framework)"
    requests_mock.get(test_url, text=stub_content)

    def mock_fetch(url, timeout=None):
        assert url == 'https://en.wikipedia.org/robots.txt'
        robot_content = read_file('robots.txt')
        robot_parser.parse(robot_content.splitlines())

    mocker.patch.object(robot_parser, 'fetch', side_effect=mock_fetch)

    task = Task.objects.create(site_url=test_url)
    # Act
    parse_links(task_id=task.id)
    # Assert
    task.refresh_from_db()
    assert task.status == TaskStatus.COMPLETED
    assert Link.objects.count() == 488
