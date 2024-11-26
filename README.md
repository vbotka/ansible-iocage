# ansible-iocage

[![license](https://img.shields.io/badge/license-BSD-red.svg)](https://www.freebsd.org/doc/en/articles/bsdl-gpl/article.html)
[![GitHub tag](https://img.shields.io/github/v/tag/vbotka/ansible-iocage)](https://github.com/vbotka/ansible-iocage/tags)

[iocage](https://github.com/iocage/iocage) module for Ansible.


## Use current branch

[Upstream](https://github.com/fractalcells/ansible-iocage/pulls) is too late
with accepting PRs. No patches were accepted since September 2021. Therefore,
the development is not submitted to the upstream anymore. Use the current branch
https://github.com/vbotka/ansible-iocage/tree/current until this problem is
resolved.


## Description

This module is an Ansible 'wrapper' of the iocage command.

* Works with Python3 iocage
* Release of a jail is the same as the release of the host if not specified
* Release is automatically fetched if missing


## Requirements (on the node)

* lang/python >= 3.6
* sysutils/iocage


## Installation

The module can be installed either as a standalone module or as a part of the
collection [vbotka.freebsd](https://galaxy.ansible.com/vbotka/freebsd). Do not
mix the installations of the collection and the standalone module.


### Standalone installation

See [Adding modules and plugins locally](https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html#adding-modules-and-plugins-locally).

For example, put the file iocage.py to *DEFAULT_MODULE_PATH*

```sh
shell> ansible-config dump | grep DEFAULT_MODULE_PATH
DEFAULT_MODULE_PATH(default) = ['/home/admin/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
```

If you want to use the module
[for selected playbooks or a single role](https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html#adding-standalone-local-modules-for-selected-playbooks-or-a-single-role).
put it into the directory *library*. This is how the module is used by
the playbook *iocage_test.yml* in the directory *test*.


### Install the collection vbotka.freebsd from Ansible Galaxy

```sh
shell> ansible-galaxy collection install vbotka.freebsd
```


## Documentation

Only the inline documentation of the module is available. Run the command

```sh
shell> ansible-doc -t module iocage
```

Read the [iocage documentation at readthedocs.io](https://iocage.readthedocs.io/en/latest/)


## Example

The module requires no options. Without any option the module gathers
facts about the jails. For example, the play below

```yaml
shell> cat playbook.yml
- hosts: srv.example.net
  tasks:
    - iocage:
    - debug:
        msg: |-
          iocage_releases: {{ iocage_releases }}
          iocage_templates: {{ iocage_templates.keys() | list }}
          iocage_jails: {{ iocage_jails.keys() | list }}
          iocage_plugins: {{ iocage_plugins.keys() | list }}
```

gives

```yaml

shell> ansible-playbook playbook.yml
  ...
  msg: |-
    iocage_releases:
      - 13.3-RELEASE
      - 13.4-RELEASE

    iocage_templates:
      - test_basejail_13_4_RELEASE

    iocage_jails:
      - test_jail
      - 81c26e24
      - ebeb44d9

    iocage_plugins: []
```

See *test/tasks/debug.yml* and display the *iocage* lists. Fit
*my_hosts* to your needs

```bash
shell> ansible-playbook iocage_test.yml -t debug -e my_hosts=test_18 \
                                                 -e debug=true \
												 -e debug_iocage_lists=true
```


## Use-cases

* Fetch 14.1-RELEASE

```
iocage: state=fetched release=14.1-RELEASE
```

* Fetch host's RELEASE

```
iocage: state=fetched
```

* Fetch the base component of host's RELEASE only

```
iocage: state=fetched components=base.txz
```

* Fetch host's RELEASE, limited to base and doc components

```
iocage: state=fetched components=base.txz,doc.txz
```

* Create basejail

```
iocage: state=basejail name=foo release=14.1-RELEASE
```

* Create template

```yaml
iocage:
  state: template
  name: mytemplate
  properties:
    vnet: 'on'
    defaultrouter: 10.1.0.10
    ip4_addr: "vnet0|10.1.0.199/24"
    resolver: "nameserver 127.0.0.1"
```

* Clone existing jail

```yaml
iocage:
  state: present
  name: foo
  clone_from: mytemplate
  pkglist: /path/to/pkglist.json
  properties:
    vnet: 'on'
    defaultrouter: 10.1.0.10
    ip4_addr: "vnet0|10.1.0.199/24"
    boot: "on"
    allow_sysvipc: 1
    host_hostname: 'myjail.my.domain'
```

* Create jail (without cloning)

```yaml
iocage:
  state: present
  name: foo
  pkglist: /path/to/pkglist.json
  properties:
    vnet: 'on'
    defaultrouter: 10.1.0.10
    ip4_addr: "vnet0|10.1.0.199/24"
    boot: 'on'
    allow_sysvipc: 1
    host_hostname: 'myjail.my.domain'
```

* Ensure jail is started

```
iocage: state=started name=foo
```

* Ensure jail is stopped

```
iocage: state=stopped name=foo
```

* Restart existing jail

```
iocage: state=restarted name=foo
```

* Execute command *cmd* in running jail *myjail* as user *root*

```
iocage: state=exec name=foo user=root cmd="service sshd start"
```

* Destroy jail

```
iocage: state=absent name=foo
```

* Set attributes on jail

```yaml
iocage:
  state: set
  name: foo
  properties:
    template: 'yes'
```


## Tests

The project comes with a set of tests stored in the directory
*test*. It is expected that
[iocage](https://man.freebsd.org/cgi/man.cgi?iocage) has already been
installed and activated.


### Configure tests

Optionally, you can configure the tests. Take a look at the playbook
*configure.yml*, *templates*, and *vars*. The playbook *configure.yml*
creates:

* the playbook *iocage_test.yml* from the template *iocage_test.yml.j2*
* the test files *tasks/\** from the *templates* and variables in
  *vars/tests.d*
* the groups of test files *tasks/group_\** from the *templates* and
  variables in *vars/groups.d*

Note: Some files in the directory *tasks* are not created from a
template. You can recognize them by missing `# Ansible managed` first
line in the file. Update these file directly if you want to.

The play should be idempotent. You're encouraged to fit the *vars* and
*templates* to your needs and run

```bash
shell> ansible-playbook configure.yml
```

Feel free to [contribute](https://github.com/firstcontributions/first-contributions)
new tests.


### Run tests

Create inventory. For example,

```bash
shell> cat hosts
test_18
test_23

[bsd_141]
test_23 ansible_host=10.1.0.73

[bsd_141:vars]
ansible_connection=ssh
ansible_user=admin
ansible_python_interpreter=/usr/local/bin/python3.11

[bsd_131]
test_18 ansible_host=10.1.0.18

[bsd_131:vars]
ansible_connection=ssh
ansible_user=admin
ansible_python_interpreter=/usr/local/bin/python3.9
```

Create *group_vars* and fit the variables to your needs. For example,

```bash
shell> cat group_vars/all/iocage_test_defaults.yml
python_required: '3.11'
release: 14.0-RELEASE

jname: test_jail
properties: {}
iocage_environment:
  CRYPTOGRAPHY_OPENSSL_NO_LEGACY: '1'

label_default: "{{ release | regex_replace('[\\W]', '_') }}"
label: "{{ label_default }}"
basejail_default: "test_basejail_{{ label }}"
basejail: "{{ basejail_default }}"
```

Create *host_vars* and update host specific variables. For example,

```yaml
shell> cat host_vars/test_18/iocage_test.yml
release: 13.4-RELEASE
python_required: 3.9
cmd: /bin/ls -la /root
properties:
  vnet: 'on'
  defaultrouter: 10.1.0.10
  ip4_addr: "vnet0|10.1.0.199/24"

```
```yaml
shell> cat host_vars/test_23/iocage_test.yml
release: 14.1-RELEASE
python_required: 3.11
cmd: /bin/ls -la /root
properties:
  vnet: 'off'
  ip4_addr: "em0|10.1.0.199/24"
```
Take a look at the variables. For example,

```bash
shell> ansible-playbook iocage_test.yml -t debug -e debug=true -e my_hosts=test_23
  ...
ok: [test_23] =>
  msg: |-
    sanity: False

    python_required: 3.11
    release: 14.1-RELEASE

    jname: test_jail
    basejail: test_basejail_14_1_RELEASE
    label: 14_1_RELEASE

    properties:
      ip4_addr: em0|10.1.0.199/24
      vnet: 'off'
```

Note: See *tasks/debug.yml* on how to display *iocage* lists and all
*iocage_\** variables.

Fit the configuration *ansible.cfg* and inventory *hosts* to your needs and run
all tests except the group of all tasks *group_all*. For example, enable custom
stats at hosts *test_18* and *test_23*

```sh
shell> ANSIBLE_SHOW_CUSTOM_STATS=true ansible-playbook iocage_test.yml \
                                      -e my_hosts=test_18,test_23 \
									  --skip-tags group_all
```

This should display a report similar to this one

```sh
PLAY RECAP ***********************************************************************************
test_18: ok=358  changed=41   unreachable=0    failed=0    skipped=158  rescued=11   ignored=0
test_23: ok=361  changed=42   unreachable=0    failed=0    skipped=157  rescued=10   ignored=0

CUSTOM STATS: ********************************************************************************
test_18:   a1: Nov 26 16:35:09  a2: Nov 26 17:07:01  crash: fetch,  fail: base_exists,  ok: 71
test_23:   a1: Nov 26 16:35:09  a2: Nov 26 17:07:01  fail: base_exists,  ok: 72
```


## Advanced tests

Most of the tests and groups are generated from templates (see the directory
*templates*) using the dictionaries *iocage_test_db* and *iocage_group_db*
stored in the directories *vars/tests.d* and *vars/groups.d*. Do not edit these
tasks and groups manually. Instead, modify or create new templates and
dictionary entries. Then, run the playbook *configure.yml* and update or create
new tasks and groups. For example, add new group of existing tests in
*vars/groups.d/group_present_absent_restart.yml*

```yaml
group_present_absent_restart:
  template: group
  tests:
    - test: test_present
    - test: test_absent
    - test: test_restart_crash
```

Run playbook *configure.yml*, create the group
*tasks/group_present_absent_restart.yml* and import it in the playbook
*iocage_test.yml*

```sh
shell> ansible-playbook configure.yml -e my_groups=group_present_absent_restart \
                                      -t create_groups,create_iocage_test
...
TASK [Create group files in directory tasks] *************************************************
ok: [localhost] => (item=group_present_absent_restart)

TASK [Create playbook iocage_test.yml] *******************************************************
ok: [localhost]
```

Create file with the parameters of the tests. For example, run tests on the
nodes *test_18,test_23*, set strategy *free*, use jail *test_31*, and enable
debug

```yaml
shell> cat extra_vars/test_31-debug-n2.yml
my_hosts: test_18,test_23
my_strategy: free
jname: test_31
debug: true
```

Run the tests and display custom stats

```sh
shell> ANSIBLE_SHOW_CUSTOM_STATS=true ansible-playbook iocage_test.yml \
                                      -e @extra_vars/test_31-debug-n2.yml \
									  -t group_present_absent_restart
```

This should display a report similar to this abridged one

```yaml
PLAY RECAP ***********************************************************************************
test_18: ok=20   changed=2    unreachable=0    failed=0    skipped=2    rescued=1    ignored=0
test_23: ok=20   changed=2    unreachable=0    failed=0    skipped=2    rescued=1    ignored=0

CUSTOM STATS: ********************************************************************************
test_18:   a1: Nov 26 18:29:44  a2: Nov 26 18:30:09  ok: 3
test_23:   a1: Nov 26 18:29:44  a2: Nov 26 18:30:39  ok: 3
```


## Variables and parameters of the tests

There are more sources of the tests' variables in this framework

* Hard-coded variables in the test files and group files. If you want to
  customize them change the data in *vars/* and run the playbook
  *configure.yml*. You can also add you own tests and group files preferably in
  the form of the data in *vars/* and *templates/*. Add also templates if
  needed.

* The variables in *group_vars* and *host_vars*

* The variables in the playbook *iocage_test.yml*. If you want to customize them
  change the template *iocage_test.yml.j2* and run the playbook *configure.yml*.

* The extra vars on the command line. See the directory *extra_vars/*

Except for this, you can customize the variables at any other
[precedence](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable)
you want to, of course.


## See also

* [iocage - A FreeBSD Jail Manager - iocage documentation at readthedocs.io](https://iocage.readthedocs.io/en/latest/)
* [iocage - Jail manager using ZFS and VNET - FreeBSD System Manager's Manual](https://www.freebsd.org/cgi/man.cgi?query=iocage)
