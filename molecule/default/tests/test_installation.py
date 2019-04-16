"""
Role tests
"""

import os
import pytest
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner(
        os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_user(host):
    user = host.user('www-data')
    assert user.group == 'www-data'


@pytest.mark.parametrize('codename,item_type,path,user,group,mode', [
    (
        ['xenial'], 'directory',
        '/var/log/php7.0-fpm.log', 'root', 'root', 0o700
    ),
    (
        ['xenial'], 'directory',
        '/etc/php/7.0/fpm/pool.d/', 'www-data', 'www-data', 0o750
    ),
    (
        ['bionic'], 'directory',
        '/var/log/php7.2-fpm.log', 'root', 'root', 0o700
    ),
    (
        ['bionic'], 'directory',
        '/etc/php/7.2/fpm/pool.d/', 'www-data', 'www-data', 0o750
        ),
    (
        ['xenial'], 'file',
        '/etc/logrotate.d/php7.0-fpm', 'root', 'root', 0o755
        ),
    (
        ['bionic'], 'file',
        '/etc/logrotate.d/php7.2-fpm', 'root', 'root', 0o755
        ),
])
def test_paths_properties(host, codename, item_type, path, user, group, mode):
    """
    Test php-fpm folders and files properties
    """

    current_item = host.file(path)

    if host.system_info.distribution not in codename:
        pytest.skip('{} ({}) distribution not managed'.format(
            host.system_info.distribution, host.system_info.release))
    if item_type == 'directory':
        assert current_item.is_directory
    elif item_type == 'file':
        assert current_item.is_file

    assert current_item.exists
    assert current_item.user == user
    assert current_item.group == group
    assert current_item.mode == mode
