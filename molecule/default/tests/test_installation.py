"""
Role tests
"""

import os
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner(
        os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_user(host):
    user = host.user('root')
    assert user.group == 'root'
