# php-fpm

[![Build Status](https://travis-ci.org/infOpen/ansible-role-php-fpm.svg?branch=master)](https://travis-ci.org/Temelio/ansible-role-php-fpm)
[![License](https://img.shields.io/badge/license-MIT%20License-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Updates](https://pyup.io/repos/github/Temelio/ansible-role-php-fpm/shield.svg)](https://pyup.io/repos/github/Temelio/ansible-role-php-fpm/)
[![Python 3](https://pyup.io/repos/github/Temelio/ansible-role-php-fpm/python-3-shield.svg)](https://pyup.io/repos/github/Temelio/ansible-role-php-fpm/)
[![Ansible Role](https://img.shields.io/ansible/role/12562.svg)](https://galaxy.ansible.com/Temelio/php-fpm/)
[![GitHub tag](https://img.shields.io/github/tag/temelio/ansible-role-php-fpm.svg)](https://github.com/cloudalchemy/ansible-role-php-fpm/tags)

Install php-fpm package.

## Requirements

This role requires Ansible 2.4 or higher,
and platform requirements are listed in the metadata file.

## Testing

This role use [Molecule](https://github.com/metacloud/molecule/) to run tests.

Locally, you can run tests on Docker (default driver) or Vagrant.
Travis run tests using Docker driver only.

Currently, tests are done on:
- Ubuntu Xenial
- Ubuntu Bionic

and use:
- Ansible 2.4.x
- Ansible 2.5.x
- Ansible 2.6.x
- Ansible 2.7.x

### Running tests

#### Automatically with Travis

Tests runs automatically on Travis on push, release, pr, ... using docker testing containers

#### Using Docker driver

```
$ tox
```

## Role Variables

### Default role variables

``` yaml
# Packages management
php_fpm_apt_update_cache: True
php_fpm_apt_cache_valid_time: 3600
php_fpm_packages: "{{ _php_fpm_packages }}"

# Binaries
php_fpm_binary_name: "{{ _php_fpm_binary_name }}"

# Service management
php_fpm_disable_default_service: False
php_fpm_init_file_set_user: False
php_fpm_init_file_process_user: "{{ php_fpm_instance.fpm_pools[0].user }}"
php_fpm_init_file_timeout: 30

# Paths
php_fpm_binary_check_config_file_path: "{{ _php_fpm_binary_check_config_file_path }}"
php_fpm_binary_file_path: "{{ _php_fpm_binary_file_path }}"
php_fpm_config_base_path: "{{ _php_fpm_config_base_path }}"
php_fpm_init_base_path: '/etc/init.d'
php_fpm_init_file_path: "{{ _php_fpm_init_file_path }}"
php_fpm_log_base_path: "{{ _php_fpm_log_base_path }}"
php_fpm_run_base_path: "{{ _php_fpm_run_base_path }}"
php_fpm_systemd_base_path: "{{ _php_fpm_systemd_base_path | default('') }}"

# Files
php_fpm_error_log_file_path: "{{ _php_fpm_error_log_file_path }}"
php_fpm_pid_file_path: "{{ _php_fpm_pid_file_path }}"

# Permissions
php_fpm_config_owner: 'root'
php_fpm_config_group: 'root'
php_fpm_config_directories_mode: '0700'
php_fpm_config_files_mode: '0644'
php_fpm_init_files_mode: '0755'

# Instance management
php_fpm_instance:
  name: 'fpm'
  service_name: "{{ _php_fpm_service_name }}"
  fpm_config:
    - section: 'global'
      option: 'pid'
      value: "{{ php_fpm_pid_file_path }}"
    - section: 'global'
      option: 'error_log'
      value: "{{ php_fpm_error_log_file_path }}"
    - section: 'global'
      option: 'include'
      value: "{{ php_fpm_config_base_path }}/fpm/pool.d/*.conf"
  fpm_pools:
    - name: 'www'
      user: 'www-data'
      group: 'www-data'
      listen: "/var/run/{{ _php_fpm_service_name }}.sock"
      listen.owner: 'www-data'
      listen.group: 'www-data'
      chdir: '/'
  php_config: []
  php_modules: []

# php.ini configuration file configuration
php_fpm_shared_php_enabled: True
php_fpm_shared_php_force_unlink: False
php_fpm_shared_php_master_file: "{{ php_fpm_config_base_path }}/fpm/php.ini"
php_fpm_shared_php_master_confd: "{{ php_fpm_config_base_path }}/fpm/conf.d"

# Pools default settings
php_fpm_pool_defaults:
  pm: dynamic
  pm.max_children: 5
  pm.start_servers: 2
  pm.min_spare_servers: 1
  pm.max_spare_servers: 3
  pm.status_path: /status

# Logrotate configuration
php_fpm_manage_logrotate_config: True
php_fpm_logrotate_config:
  filename: "/etc/logrotate.d/{{ php_fpm_instance.service_name }}"
  log_pattern: "{{ php_fpm_error_log_file_path }}"
  options:
    - 'rotate 54'
    - 'weekly'
    - 'missingok'
    - 'notifempty'
    - 'compress'
    - 'delaycompress'
    - 'postrotate'
    - "[ -r '{{ php_fpm_pid_file_path }}' ] && kill -USR1 $(cat '{{ php_fpm_pid_file_path }}') > /dev/null"
    - 'endscript'
```

## How ...

### Force init.d service stop to only managed processes run by a user

* Set 'php_fpm_init_file_set_user' key to True (default: False)
* Set 'php_fpm_init_file_process_user' key with username

### Disable default service and only use custom instances

* Set 'php_fpm_disable_default_service' key to True

### Use a common PHP configuration between instances

* Set 'php_fpm_shared_php_enabled' to True (default)
* Use a dedicated role (ex: infOpen.php) to manage php configuration.

When use this setting, conf.d folder and php.ini file will be symlinks from:
* php_fpm_shared_php_master_file target
* php_fpm_shared_php_master_confd target

### Define custom settings for php.ini or php-fpm.conf files

You can define custom settings for php.ini or php-fpm.conf using:
* php.ini: 'php_config' key of php_fpm_instance
* php-fpm.conf: 'fpm_config' key of php_fpm instance

Note: PHP configuration will be managed only if 'php_fpm_shared_php_enabled' is set to False
``` yaml
- section: 'global'
  option: 'my_option'
  value: 'my_value'
  state: 'present'
```

### Define pools configuration

Each instance can manage multiple pools, usng this format. Pool settings will be merged with 'php_fpm_pool_defaults' dict
```yaml
- name: 'foobar'
  user: 'www-data'
  group: 'www-data'
  listen: '/var/run/php5-fpm-foobar.sock'
  listen.owner: 'www-data'
  listen.group: 'www-data'
```

### Define php modules

Note: PHP modules will be managed only if 'php_fpm_shared_php_enabled' is set to False
```yaml
- 'json'
```

## Dependencies

None

## Example Playbook

    - hosts: servers
      roles:
         - { role: Temelio.php-fpm }

## License

MIT

## Author Information

L Machetel (for Temelio company)
Fork from: Alexandre Chaussier (for Infopen company)
