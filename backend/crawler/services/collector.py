from urllib.parse import urljoin
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from robotexclusionrulesparser import RobotFileParserLookalike

from crawler.models import Link
from crawler.models import Task

robot_parser = RobotFileParserLookalike()


def collect_links(task: Task):
    target_url = task.site_url
    base_url = _get_base_url(target_url)
    if not _is_robot_spec_allow_crawl(base_url, target_url):
        return

    response = requests.get(target_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    found_results = []
    visited_urls = set()
    for link in soup.find_all('a'):
        rel_value = link.get('rel')
        if rel_value == "nofollow":
            continue

        href = link.get('href')
        if href:
            result_url = ''
            if href.startswith('http'):
                result_url = href
            elif href.startswith('/'):
                result_url = urljoin(base_url, href)

            if result_url and result_url not in visited_urls:
                result = Link(origin=target_url, url=result_url, task=task, parent_id=None)
                found_results.append(result)
                visited_urls.add(result_url)

    Link.objects.bulk_create(found_results)


def _get_base_url(target_url):
    base_url = target_url
    if '/' in urlparse(base_url).path:
        base_url = base_url.rsplit('/', 1)[0]
    return base_url


def _is_robot_spec_allow_crawl(base_url, target_url):
    robots_url = urljoin(base_url, '/robots.txt')
    robot_parser.fetch(robots_url)
    return robot_parser.can_fetch('*', target_url)
