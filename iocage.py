#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2015, Perceivon Hosting Inc.
# Copyright 2021, Vladimir Botka <vbotka@gmail.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY [COPYRIGHT HOLDER] AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL [COPYRIGHT HOLDER] OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# SPDX-License-Identifier: BSD-2-Clause

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: iocage

short_description: FreeBSD iocage jail handling

description:
    - The M(iocage) module is wrapper to B(iocage) command.

options:
    state:
      description:
          - O(state) of the desired result.
          - State V(absent) by default force the destruction C(iocage destroy --force name).
      type: str
      choices: [absent, basejail, cloned, exec, facts, fetched, get, pkg,
                present, restarted, set, started, stopped, template,
                thickjail]
      default: facts
    name:
      description:
          - O(name) of the jail.
          - States V(started, stopped, restarted) accept V(ALL) to start, stop, or restart all jails.
          - States V(present, cloned, template, basejail, thickjail) will return RV(uuid) and RV(uuid_short)
            if O(name) is V(None) or empty.
      type: str
    pkglist:
      description:
          - Path to a JSON file containing packages to install. Only applicable when creating a jail.
      type: path
    properties:
      description:
          - O(properties) of the jail. The jail will restart if any of the properties B(ip4_addr,
            ip6_addr, template, interfaces, vnet, host_hostname) changes.
      type: dict
    args:
      description:
        - Additional arguments of M(iocage) applied to the O(state). They will be applied
          to the sub-command B(create) if the O(state) is V(basejail, thickjail, template, present).
          If the same Ansible task also fetches a release as apart of the creation
          the arguments will not be applied to the sub-command B(fetch). Use separate task
          B(state=fetched) and set O(args) there if needed.
      type: str
      default: ""
    user:
      description:
        - O(user) who runs the command O(cmd).
      type: str
      default: root
    cmd:
      description:
        - Execute the command O(cmd) inside the specified jail O(name).
      type: str
    clone_from:
      description:
        - Clone the jail O(clone_from) to O(name). Use O(properties) to configure the clone.
      type: str
    plugin:
      description:
        - Specify which plugin to fetch or update.
      type: str
    release:
      description:
        - Specify which RELEASE to fetch, update, or create a jail from. O(release) defaults to the
          release of the remote host if O(state) is one of V(basejail, thickjail, template, fetched,
          present). O(release) also defaults to the release of the remote host if V(bupdate=True).
      type: str
    bupdate:
      description:
        - Update the fetch to the latest patch level when B(state=fetched).
          Fetch and install binary updates when O(name) is defined. This will start the jail.
      type: bool
      default: False
    components:
      description:
        - Uses a local file directory for the root directory instead of HTTP to downloads and/or
          updates releases.
      type: list
      elements: path
      aliases: [files, component]
requirements:
  - lang/python >= 3.6
  - sysutils/iocage
notes:
  - Supports C(check_mode).
  - There is no mandatory option.
  - The module always creates facts B(iocage_releases), B(iocage_templates), and B(iocage_jails)
  - Returns B(module_args) when debugging is set E(ANSIBLE_DEBUG=true)
seealso:
  - name: iocage - A FreeBSD Jail Manager
    description: iocage 1.2 documentation
    link: https://iocage.readthedocs.io/en/latest/
  - name: iocage - jail manager using ZFS and VNET
    description: FreeBSD System Manager's Manual
    link: https://www.freebsd.org/cgi/man.cgi?query=iocage
author:
  - Johannes Meixner (@xmj)
  - Vladimir Botka (@vbotka)
  - dgeo (@dgeo)
  - Berend de Boer (@berenddeboer)
  - Dr Josef Karthauser (@Infiniverse)
  - Kevin P. Fleming (@kpfleming)
  - Ross Williams (@overhacked)
  - david8001 (@david8001)
  - luto (@luto)
  - Keve Müller (@kevemueller)
  - Mårten Lindblad (@martenlindblad)
'''

EXAMPLES = r'''
- name: Create Ansible facts iocage_*. This is the default state.
  iocage:
    state: facts

- name: Display lists of bases, plugins, templates, and jails
  debug:
    msg: |-
      {{ iocage_releases }}
      {{ iocage_plugins.keys()|list }}
      {{ iocage_templates.keys()|list }}
      {{ iocage_jails.keys()|list }}

- name: Fetch the remote host's version of base
  iocage:
    state: fetched

- name: Fetch base 13.0-RELEASE
  iocage:
    state: fetched
    release: 13.0-RELEASE

- name: Fetch only components base.txz and doc.txz of the base 13.0-RELEASE
  iocage:
    state: fetched
    release: 13.0-RELEASE
    components: 'base.txz,doc.txz'

- name: Fetch plugin Tarsnap. Keep jails on failure.
  iocage:
    state: fetched
    plugin: Tarsnap
    args: -k

- name: Update or fetch components base.txz and doc.txz of the remote host's release.
        Fetch plugin Tarsnap. Keep jails on failure.
  iocage:
    state: fetched
    bupdate: true
    components: 'base.txz,doc.txz'
    plugin: Tarsnap
    args: -k

- name: Update the jail. This will start the jail.
  iocage:
    state: present
    bupdate: true
    name: foo

- name: Start jail
  iocage:
    state: started
    name: foo

- name: Start all jails
  iocage:
    state: started
    name: ALL

- name: Start all jails with boot=on
  iocage:
    state: started
    args: '--rc'

- name: Stop jail
  iocage:
    state: stopped
    name: foo

- name: Stop all jails
  iocage:
    state: stopped
    name: ALL

- name: Stop all jails with boot=on
  iocage:
    state: stopped
    args: '--rc'

- name: Restart jail
  iocage:
    state: restarted
    name: foo

- name: Restart all jails
  iocage:
    state: restarted
    name: ALL

- name: Set IP address of the jail
  iocage:
    state: set
    name: foo
    properties:
      vnet: 'on'
      defaultrouter: 10.1.0.10
      ip4_addr: 'vnet0|10.1.0.199/24'

- name: Create jail without cloning, install packages, and set properties.
        Use release of the remote host.
  iocage:
    state: present
    name: foo
    pkglist: /path/to/pkglist.json
    properties:
      ip4_addr: 'vnet0|10.1.0.199/24'
      boot: true
      allow_sysvipc: true
      defaultrouter: '10.1.0.1'

- name: Create template, install packages, and set properties.
        Use release of the remote host.
  iocage:
    state: template
    name: tplfoo
    pkglist: /path/to/pkglist.json
    properties:
      ip4_addr: 'lo1|10.1.0.5'
      boot: true
      allow_sysvipc: true
      defaultrouter: '10.1.0.1'

- name: Create a cloned jail. Creates basejail if needed.
  iocage:
    state: present
    name: foo
    clone_from: tplfoo
    pkglist: /path/to/pkglist.json
    properties:
      ip4_addr: 'lo1|10.1.0.5'
      boot: true
      allow_sysvipc: true
      defaultrouter: '10.1.0.1'

- name: Create a cloned jail. Name is automatically generated.
  iocage:
    state: present
    clone_from: tplfoo
  register: result
- name: Set variable contains the name of the created jail.
  set_fact:
    jname: "{{ result.uuid_short }}"

- name: Execute command in running jail
  iocage:
    state: exec
    name: foo
    cmd: service sshd start

- name: Execute pkg command in running jail
  iocage:
    state: pkg
    name: foo
    cmd: info

- name: Destroy jail
  iocage:
    state: absent
    name: foo
'''

RETURN = r'''
uuid:
  description: Automatically generated unique ID of a jail.
  returned: States I(present, cloned, template, basejail, thickjail) if I(name) is C(None) or empty.
  type: str
uuid_short:
  description: First 8 characters of I(uuid). Set as a name of the jail.
  returned: States I(present, cloned, template, basejail, thickjail) if I(name) is C(None) or empty.
  type: str
ansible_facts:
  description: Facts to add to ansible_facts.
  returned: always
  type: dict
  contains:
    iocage_releases:
      description: List of all bases.
      returned: always
      type: list
      elements: str
      sample: ['13.3-RELEASE', '13.4-RELEASE']
    iocage_templates:
      description: Dictionary of all templates.
      returned: always
      type: dict
      sample: {}
    iocage_jails:
      description: Dictionary of all jails.
      returned: always
      type: dict
      sample: {}
    iocage_plugins:
      description: Dictionary of all plugins.
      returned: always
      type: dict
      sample: {}
module_args:
  description: Information on how the module was invoked.
  returned: debug
  type: dict
'''

import json
import re

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_bytes


def _all_jails_started(facts):
    '''Test all jail started.'''
    states = set([facts['iocage_jails'][jail]['state'] for jail in facts['iocage_jails'].keys()])
    return len(states) == 1 and next(iter(states)) == 'up'


def _all_jails_stopped(facts):
    '''Test all jail stopped.'''
    states = set([facts['iocage_jails'][jail]['state'] for jail in facts['iocage_jails'].keys()])
    return len(states) == 1 and next(iter(states)) == 'down'


def _props_to_str(props):
    '''Convert dictionary of properties to iocage arguments'''

    argstr = ""
    for _prop in props:
        _val = props[_prop]
        if _val == '-' or _val == '' or _val is None:
            continue
        if _val in ['yes', 'on', True]:
            argstr += f"{_prop}=1 "
        elif _val in ['no', 'off', False]:
            argstr += f"{_prop}=0 "
        elif isinstance(_val, str):
            argstr += f'{_prop}="{_val}" '
        else:
            argstr += f"{_prop}={str(_val)} "

    return argstr


def _command_fail(module, label, cmd, rc, stdout, stderr):
    '''Command fail. Create message and terminate module.'''
    module.fail_json(msg=f"{label}\ncmd: '{cmd}' return: {rc}\nstdout: '{stdout}'\nstderr: '{stderr}'")


def _get_iocage_facts(module, iocage_path, artifact='all', name=None):
    '''Collect facts.'''

    opt = dict(jails="list -hl",
               plugins="list -hP",
               templates="list -hlt",
               releases="list -hr",
               init="list -h")

    if artifact == 'all':
        # _init = _get_iocage_facts(module, iocage_path, "init")
        _jails = _get_iocage_facts(module, iocage_path, 'jails')
        _plugins = _get_iocage_facts(module, iocage_path, 'plugins')
        _templates = _get_iocage_facts(module, iocage_path, 'templates')
        _releases = _get_iocage_facts(module, iocage_path, 'releases')
        return dict(iocage_jails=_jails,
                    iocage_plugins=_plugins,
                    iocage_templates=_templates,
                    iocage_releases=_releases)

    if artifact in opt:
        cmd = f"{iocage_path} {opt[artifact]}"
    else:
        module.fail_json(msg=f"_get_iocage_facts(artifact={artifact}): argument not understood.")

    rc, out, err = module.run_command(to_bytes(cmd, errors='surrogate_or_strict'),
                                      errors='surrogate_or_strict')
    if rc != 0 and artifact != 'init':
        _command_fail(module, "Function _get_iocage_facts failed.", cmd, rc, out, err)
    elif artifact == 'init':
        return {}

    if artifact == 'releases':
        releases = [line.strip() for line in out.splitlines()]
        return releases

    elif artifact == 'jails' or artifact == 'templates' or artifact == 'plugins':
        _items = {}
        try:
            for line in out.splitlines():
                _jid = line.split('\t')[0]
                if _jid == '---':
                    # non-iocage jails: skip all
                    break
                if re.match(r'(\d+|-|None)', _jid):
                    _fragments = line.split('\t')
                    if artifact == 'jails' or artifact == 'templates':
                        if len(_fragments) == 10:
                            (_jid, _name, _boot, _state, _type, _release, _ip4, _ip6, _template, _basejail) = _fragments
                        else:
                            (_jid, _name, _boot, _state, _type, _release, _ip4, _ip6, _template) = _fragments
                        if _name != '':
                            _properties = _jail_get_properties(module, iocage_path, _name)
                            _items[_name] = {'jid': _jid, 'name': _name, 'state': _state, 'properties': _properties}
                    elif artifact == 'plugins':
                        (_jid, _name, _boot, _state, _type, _release, _ip4, _ip6, _template, _portal, _doc_url) = _fragments
                        _keys = ('jid', 'name', 'boot', 'state', 'type', 'release', 'ip4', 'ip6', 'template', 'portal', 'doc_url')
                        _items[_name] = dict(zip(_keys, _fragments))
                else:
                    module.fail_json(msg=f"_get_iocage_facts(artifact={artifact}):\nUnreadable stdout line from cmd '{cmd}':\n'{line}'")
        except ValueError:
            module.fail_json(msg=f"unable to parse {out}")

        if name is not None:
            if name in _items:
                return _items[name]
            return {}

        return _items


def _jail_get_properties(module, iocage_path, name):

    if name is not None and name != "":
        properties = {}
        cmd = f"{iocage_path} get --all {name}"
        rc, out, err = module.run_command(to_bytes(cmd, errors='surrogate_or_strict'),
                                          errors='surrogate_or_strict')
        if rc == 0:
            _properties = [line.strip() for line in out.strip().split('\n')]
            for p in _properties:
                for _property in [p.split(':', 1)]:
                    if len(_property) == 2:
                        properties[_property[0]] = _property[1]
                    else:
                        module.fail_json(msg=f"error parsing property {p} from {str(properties)}")
        else:
            _command_fail(module, f"_jail_get_properties({name})", cmd, rc, out, err)
    else:
        module.fail_json(msg=f"_jail_get_properties:\njail {name} not found.")

    return properties


def jail_started(module, iocage_path, name):
    '''Test jail name is started(up) or not(down). Return Boolean.'''

    cmd = f"{iocage_path} list -h"
    rc, out, err = module.run_command(to_bytes(cmd, errors='surrogate_or_strict'),
                                      errors='surrogate_or_strict')
    if rc != 0:
        _command_fail(module, f"jail_started({name})", cmd, rc, out, err)

    st = None
    for line in out.splitlines():
        u = line.split('\t')[1]
        if u == name:
            s = line.split('\t')[2]
            if s == 'up':
                st = True
                break
            if s == 'down':
                st = False
                break
            module.fail_json(msg=f"Jail '{name}' unknown state: {line}")

    return st


def jail_exists(module, iocage_path, name):
    '''Test jail name exists. Return Boolean.'''

    cmd = f"{iocage_path} get host_hostuuid {name}"
    rc, out, err = module.run_command(to_bytes(cmd, errors='surrogate_or_strict'),
                                      errors='surrogate_or_strict')

    if rc == 0:
        st = True
    elif rc == 1:
        st = False
    else:
        _command_fail(module, f"jail_exists({name})", cmd, rc, out, err)

    return st


def jail_start(module, iocage_path, name=None, args=""):
    '''Starts the specified jails or ALL. Multiple names are not supported. If you want to start a list of
       jails iterate the module.

       # iocage start help
       Usage:  [OPTIONS] [JAILS]...
       Options:
         --rc          Will start all jails with boot=on, in the specified order with
                       smaller value for priority starting first.
         -i, --ignore  Suppress exceptions for jails which fail to start
         --help        Show this message and exit.
    '''

    if name is None and not args:
        module.fail_json(msg="jail_start do not know what to start. Name is not defined and there are no arguments.")

    _changed = True
    cmd = f"{iocage_path} start"
    if args:
        cmd += f" {args}"
    if name is not None:
        cmd += f" {name}"

    if not module.check_mode:
        rc, out, err = module.run_command(to_bytes(cmd, errors='surrogate_or_strict'),
                                          errors='surrogate_or_strict')
        if rc != 0:
            _command_fail(module, "Jail(s) not started.", cmd, rc, out, err)
        if name is not None:
            if name == "ALL":
                _msg = f"All jails started.\n{cmd}\n{out}"
            else:
                _msg = f"Jail '{name}' started.\n{cmd}\n{out}"
        else:
            _msg = f"Jail(s) started.\n{cmd}\n{out}"
    else:
        out = ""
        err = ""
        if name is not None:
            if name == 'ALL':
                _msg = f"All jails would start.\n{cmd}"
            else:
                _msg = f"Jail '{name}' would start.\n{cmd}"
        else:
            _msg = f"Jail(s) would start.\n{cmd}"

    return _changed, _msg, out, err


def jail_stop(module, iocage_path, name=None, args=""):
    '''Stops the specified jails or ALL. Multiple names are not supported. If you want to stop a list of
       jails iterate the module.

       $ iocage stop --help
       Usage: iocage stop [OPTIONS] [JAILS]...
       Options:
         --rc          Will stop all jails with boot=on, in the specified order with
                       higher value for priority stopping first.
         -f, --force   Skips all pre-stop actions like stop services. Gently shuts
                       down and kills the jail process.
         -i, --ignore  Suppress exceptions for jails which fail to stop
         --help        Show this message and exit.
    '''

    if name is None and not args:
        module.fail_json(msg="jail_stop do not know what to stop. Name is not defined and there are no arguments.")

    _changed = True
    cmd = f"{iocage_path} stop"
    if args:
        cmd += f" {args}"
    if name is not None:
        cmd += f" {name}"

    if not module.check_mode:
        rc, out, err = module.run_command(to_bytes(cmd, errors='surrogate_or_strict'),
                                          errors='surrogate_or_strict')
        if rc != 0:
            _command_fail(module, "Jail(s) not stopped.", cmd, rc, out, err)
        if name is not None:
            if name == 'ALL':
                _msg = f"All jails stopped.\n{cmd}\n{out}"
            else:
                _msg = f"Jail '{name}' stopped.\n{cmd}\n{out}"
        else:
            _msg = f"Jail(s) stopped.\n{cmd}\n{out}"
    else:
        out = ""
        err = ""
        if name is not None:
            if name == "ALL":
                _msg = f"All jails would stop.\n{cmd}"
            else:
                _msg = f"Jail '{name}' would stop.\n{cmd}"
        else:
            _msg = f"Jail(s) would stop.\n{cmd}"

    return _changed, _msg, out, err


def jail_restart(module, iocage_path, name=None, args=""):
    '''Restarts the specified jails or ALL.

       $ iocage restart --help
       Usage: iocage restart [OPTIONS] JAIL
       Options:
         -s, --soft  Restarts the jail but does not tear down the network stack.
         --help      Show this message and exit.
    '''

    _changed = True
    cmd = f"{iocage_path} restart"
    if args:
        cmd += f" {args}"
    cmd += f" {name}"

    if not module.check_mode:
        rc, out, err = module.run_command(to_bytes(cmd, errors='surrogate_or_strict'),
                                          errors='surrogate_or_strict')
        if rc != 0:
            _command_fail(module, "Jail(s) not restarted.", cmd, rc, out, err)
        if name == 'ALL':
            _msg = f"ALL jails restarted.\n{cmd}\n{out}"
        else:
            _msg = f"Jail '{name}' restarted.\n{cmd}\n{out}"
    else:
        out = ""
        err = ""
        if name == 'ALL':
            _msg = f"ALL jails would restart.\n{cmd}"
        else:
            _msg = f"Jail '{name}' would restart.\n{cmd}"

    return _changed, _msg, out, err


def release_fetch(module, iocage_path, bupdate=False, release=None, components=None, plugin=None, args=""):
    '''Fetch a version of FreeBSD for jail usage or a preconfigured plugin.

       $ iocage fetch --help
       Usage: iocage fetch [OPTIONS] [PROPS]...
       (cont.)
    '''

    _changed = True
    if bupdate:
        args += " -U"
    if release is not None:
        args += f" -r {release}"
    if components is not None:
        for _component in components:
            if _component != '':
                args += f" -F {_component}"
    if plugin is not None:
        args += f" -P {plugin}"
    cmd = f"{iocage_path} fetch {args}"

    if not module.check_mode:
        rc, out, err = module.run_command(to_bytes(cmd, errors='surrogate_or_strict'),
                                          errors='surrogate_or_strict')
        if rc != 0:
            _command_fail(module, "Function release_fetch failed.", cmd, rc, out, err)
        if bupdate:
            _msg = f"Successfully fetched and updated.\n{cmd}\n{out}"
        else:
            _msg = f"Successfully fetched.\n{cmd}\n{out}"
    else:
        out = ""
        err = ""
        if bupdate:
            _msg = f"Would fetch and update.\n{cmd}"
        else:
            _msg = f"Would fetch.\n{cmd}"

    return _changed, _msg, out, err


def jail_exec(module, iocage_path, name, user='root', _cmd='/usr/bin/true'):
    '''Run a command inside a specified jail.

       $ iocage exec --help
       Usage: iocage exec [OPTIONS] JAIL [COMMAND]...
       Options:
         -u, --host_user TEXT  The host user to use.
         -U, --jail_user TEXT  The jail user to use.
         -f, --force           Start the jail if it's not running.
         --help                Show this message and exit.
    '''

    _changed = True
    cmd = f"{iocage_path} exec -u {user} {name} -- {_cmd}"

    if not module.check_mode:
        rc, out, err = module.run_command(to_bytes(cmd, errors='surrogate_or_strict'),
                                          errors='surrogate_or_strict')
        if rc != 0:
            _command_fail(module, f"Command '{_cmd}' not executed.", cmd, rc, out, err)
        _msg = f"Jail '{name}' executed command '{_cmd}'\n{cmd}\nrc: {rc}\nstdout:\n{out}\nstderr:\n{err}"
    else:
        out = ""
        err = ""
        _msg = f"Jail '{name}' would execute command '{_cmd}'\n{cmd}"

    return _changed, _msg, out, err


def jail_pkg(module, iocage_path, name, _cmd='info'):
    '''Use pkg inside a specified jail.

       $ iocage pkg --help
       Usage: iocage pkg [OPTIONS] JAIL [COMMAND]...
       Options:
         --help  Show this message and exit.
    '''

    _changed = True
    cmd = f"{iocage_path} pkg {name} {_cmd}"

    if not module.check_mode:
        rc, out, err = module.run_command(to_bytes(cmd, errors='surrogate_or_strict'),
                                          errors='surrogate_or_strict')
        if rc != 0:
            _command_fail(module, f"Command 'pkg {_cmd}' not executed.", cmd, rc, out, err)
        _msg = f"Jail '{name}' executed command 'pkg {_cmd}'\n{cmd}\nrc: {rc}\nstdout:\n{out}\nstderr:\n{err}"
    else:
        out = ""
        err = ""
        _msg = f"Jail '{name}' would execute command 'pkg {_cmd}'\n{cmd}"

    return _changed, _msg, out, err


def jail_set(module, iocage_path, name, properties=None):
    '''Sets the specified property.

       $ iocage set --help
       Usage: iocage set [OPTIONS] [PROPS]... JAIL
       Options:
         -P, --plugin  Set the specified key for a plugin jail, if accessing a nested key use . as a
                         separator. Example: iocage set -P foo.bar.baz=VALUE PLUGIN
         --help        Show this message and exit.
    '''

    if properties is None:
        properties = {}
    _existing_props = _jail_get_properties(module, iocage_path, name)
    _props_to_be_changed = {}

    for _property in properties:
        if _property not in _existing_props:
            continue
        if _existing_props[_property] == '-' and not properties[_property]:
            continue
        if _property == 'template':
            continue
        _val = properties[_property]
        _oval = _existing_props[_property]
        if _val in [0, 'no', 'off', False]:
            propval = 0
        elif _val in [1, 'yes', 'on', True]:
            propval = 1
        elif isinstance(_oval, str):
            if _val == '':
                propval = 'none'
            else:
                propval = f'{_val}'
        else:
            module.fail_json(msg="Unable to set attribute {0} to {1} for jail {2}"
                             .format(_property, str(_val).replace("'", "'\\''"), name))
        if 'CHECK_NEW_JAIL' in _existing_props or \
           (str(_existing_props[_property]) != str(propval) and propval is not None):
            _props_to_be_changed[_property] = propval

    if len(_props_to_be_changed) > 0:
        _changed = True
        if len(list(set(_props_to_be_changed.keys()) & set(['ip4_addr', 'ip6_addr', 'template', 'interfaces', 'vnet', 'host_hostname']))) > 0:
            need_restart = jail_started(module, iocage_path, name)
        else:
            need_restart = False

        cmd = f"{iocage_path} set {_props_to_str(_props_to_be_changed)} {name}"

        if not module.check_mode:
            if need_restart:
                jail_stop(module, iocage_path, name)
            rc, out, err = module.run_command(to_bytes(cmd, errors='surrogate_or_strict'),
                                              errors='surrogate_or_strict')
            if need_restart:
                jail_start(module, iocage_path, name)
            if rc != 0:
                _command_fail(module, "properties not set.", cmd, rc, out, err)
            _msg = f"properties {str(_props_to_be_changed.keys())} were set in jail '{name}'\n{cmd}"
        else:
            _msg = f"properties {str(_props_to_be_changed.keys())} would be set in jail '{name}'\n{cmd}"
            _msg += str(_props_to_be_changed)

    else:
        _changed = False
        _msg = f"properties {properties.keys()} already set in jail '{name}'"

    return _changed, _msg


def jail_create(module, iocage_path, name=None, properties=None, clone_from_name=None,
                clone_from_template=None, release=None, basejail=False, thickjail=False,
                pkglist=None, args=""):
    '''Create a jail.

       $ iocage create --help
       Usage: iocage create [OPTIONS] [PROPS]...
       (cont.)
    '''

    _changed = True
    _uuid = ""
    _uuid_short = ""

    if clone_from_name is None and clone_from_template is None:
        if name is None or len(name) == 0:
            cmd = f"{iocage_path} create -r {release}"
        else:
            cmd = f"{iocage_path} create -n {name} -r {release}"
        if basejail:
            cmd += " -b"
        elif thickjail:
            cmd += " -T"
        if pkglist is not None:
            cmd += f" -p {pkglist}"
        if args:
            cmd += f" {args}"

    elif clone_from_template is not None:
        if name is None or len(name) == 0:
            cmd = f"{iocage_path} create -t {clone_from_template}"
        else:
            cmd = f"{iocage_path} create -n {name} -t {clone_from_template}"
        if pkglist is not None:
            cmd += f" -p {pkglist}"
        if args:
            cmd += f" {args}"

    elif clone_from_name is not None:
        if name is None or len(name) == 0:
            cmd = f"{iocage_path} clone {clone_from_name}"
        else:
            cmd = f"{iocage_path} clone {clone_from_name} -n {name}"
        if args:
            cmd += f" {args}"

    if properties is not None:
        cmd += f" {_props_to_str(properties)}"

    if not module.check_mode:
        rc, out, err = module.run_command(to_bytes(cmd, errors='surrogate_or_strict'),
                                          errors='surrogate_or_strict')
        if rc != 0:
            _command_fail(module, "Jail not created.", cmd, rc, out, err)
        _msg = f"'Jail was created.\n{cmd}\n{out}"
        if name is None or len(name) == 0:
            _uuid = out.split()[0]
            _uuid_short = _uuid.split('-')[0]
            name = _uuid_short
            cmd = f"{iocage_path} rename {_uuid} {_uuid_short}"
            rc, out, err = module.run_command(to_bytes(cmd, errors='surrogate_or_strict'),
                                              errors='surrogate_or_strict')
            if rc != 0:
                _command_fail(module, "Jail not renamed.", cmd, rc, out, err)
        if not jail_exists(module, iocage_path, name):
            module.fail_json(msg=f"'{name}' not created ???\ncmd: {cmd}\nstdout:\n{out}\nstderr:\n{err}")
    else:
        _msg = f"Jail would be created.\n{cmd}"

    return _changed, _msg, _uuid, _uuid_short


def jail_update(module, iocage_path, name):
    '''Run freebsd-update to update a specified jail to the latest patch level.

       $ iocage update --help
       Usage: iocage update [OPTIONS] JAIL
       Options:
         -P, --pkgs  Decide whether or not to update the pkg repositories and all
                     installed packages in jail( this has no effect for plugins ).
         --help      Show this message and exit.
    '''

    _changed = True
    cmd = f"{iocage_path} update {name}"

    if not module.check_mode:
        rc, out, err = module.run_command(to_bytes(cmd, errors='surrogate_or_strict'),
                                          errors='surrogate_or_strict')
        if "No updates needed" in out:
            _changed = False
            _msg = f"Jail '{name}' is up-to-date.\n{out}"
        elif rc != 0:
            _command_fail(module, f"Jail '{name}' not updated.", cmd, rc, out, err)
        # elif "updating to" in out:
        #     nv = re.search(r' ([^ ]*):$', filter((lambda x: 'updating to' in x), out.split('\n'))[0]).group(1)
        #     _msg = f"Jail '{name}' was updated to {nv}\n{out}"
        else:
            _msg = f"Jail '{name}' was updated\n{out}"
    else:
        _msg = f"Jail '{name}' would be updated.\n{cmd}"

    return _changed, _msg


def jail_destroy(module, iocage_path, name, args=""):
    '''Destroy specified jail(s).

       $ iocage destroy --help
       Usage: iocage destroy [OPTIONS] [JAILS]...
       Options:
         -f, --force      Destroy the jail without warnings or more user input.
         -r, --release    Destroy a specified RELEASE dataset.
         -R, --recursive  Bypass the children prompt, best used with --force (-f).
         -d, --download   Destroy the download dataset of the specified RELEASE as
                          well.
         --help           Show this message and exit.
    '''

    _changed = True
    _args = '--force'
    if args:
        _args += f" {args}"
    cmd = f"{iocage_path} destroy {_args} {name}"

    if not module.check_mode:
        rc, out, err = module.run_command(to_bytes(cmd, errors='surrogate_or_strict'),
                                          errors='surrogate_or_strict')
        if rc != 0:
            _command_fail(module, f"'{name}' not destroyed.", cmd, rc, out, err)
        _msg = f"'{name}' was destroyed.\n{out}"
        if jail_exists(module, iocage_path, name):
            module.fail_json(msg=f"'{name}' not destroyed ???\ncmd: {cmd}\nstdout:\n{out}\nstderr:\n{err}")
    else:
        out = ""
        err = ""
        _msg = f"'{name}' would be destroyed.\n{cmd}"

    return _changed, _msg, out, err


def run_module():

    module_args = dict(
        state=dict(type='str', default='facts',
                   choices=['absent', 'basejail', 'cloned', 'exec', 'facts', 'fetched', 'get', 'pkg',
                            'present', 'restarted', 'set', 'started', 'stopped', 'template',
                            'thickjail']),
        name=dict(type='str'),
        pkglist=dict(type='path'),
        properties=dict(type='dict'),
        args=dict(type='str', default=''),
        user=dict(type='str', default='root'),
        cmd=dict(type='str'),
        clone_from=dict(type='str'),
        plugin=dict(type='str'),
        release=dict(type='str'),
        bupdate=dict(type='bool', default=False),
        components=dict(type='list', elements='path', aliases=['files', 'component']),)

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    iocage_path = module.get_bin_path('iocage', True)
    if not iocage_path:
        module.fail_json(msg="Utility iocage not found!")

    p = module.params
    name = p['name']
    properties = p['properties']
    cmd = p['cmd']
    args = p['args']
    clone_from = p['clone_from']
    user = p['user']
    plugin = p['plugin']
    release = p['release']
    bupdate = p['bupdate']
    components = p['components']
    pkglist = p['pkglist']

    # Gather facts

    _changed = False
    out = ""
    err = ""
    facts = _get_iocage_facts(module, iocage_path, 'all')
    facts['iocage_states'] = module_args['state']['choices']

    if p['state'] == 'facts':
        result = dict(ansible_facts=facts,
                      changed=_changed,
                      msg="",
                      stdout=out,
                      stderr=err,
                      )
        if module._debug:
            result['module_args'] = f"{(json.dumps(module.params, indent=4))}"
        module.exit_json(**result)

    jails = {}
    jails.update(facts['iocage_jails'])
    jails.update(facts['iocage_templates'])

    # Input validation

    # states that need name of jail
    if p['state'] in ['restarted', 'get', 'set', 'exec', 'pkg', 'absent']:
        if name is None:
            module.fail_json(msg=f"name needed for state {p['state']}")

    # states that need release defined
    if p['state'] in ['basejail', 'thickjail', 'template', 'fetched', 'present'] or bupdate:
        if release is None or release == '':
            rc, out, err = module.run_command("uname -r")
            if rc != 0:
                module.fail_json(msg="Unable to run uname -r ???")
            matches = re.match(r'(\d+\.\d+)\-(RELEASE|RC\d+).*', out.strip())
            if matches is not None:
                release = matches.group(1) + '-RELEASE'
            else:
                module.fail_json(msg=f"Release not recognised: {out}")

    # need existing jail
    if p['state'] in ['set', 'exec', 'pkg']:
        if name not in jails:
            module.fail_json(msg=f"Jail '{name}' doesn't exist.")
    if name is not None and bupdate:
        if name not in jails:
            module.fail_json(msg=f"Jail '{name}' doesn't exist.")

    # states that need running jail
    if p['state'] in ['exec', 'pkg']:
        if jails[name]['state'] != 'up':
            module.fail_json(msg=f"Jail '{name}' not running.")

    # Execution of states

    msgs = []
    _uuid = ''
    _uuid_short = ''

    if p['state'] == 'started':
        if name is not None and name != 'ALL' and name not in jails:
            module.fail_json(msg=f"Jail '{name}' doesn't exist.")
        if name is not None and name == 'ALL' and _all_jails_started(facts):
            msgs.append("All jails already started.")
        if name is not None and name != 'ALL' and jails[name]['state'] == 'up':
            msgs.append(f"Jail '{name}' already started.")
        else:
            _changed, _msg, out, err = jail_start(module, iocage_path, name, args)
            msgs.append(_msg)
        if not module.check_mode:
            facts['iocage_jails'] = _get_iocage_facts(module, iocage_path, 'jails')
            jails.update(facts['iocage_jails'])
            if name is not None and name == 'ALL' and not _all_jails_started(facts):
                module.fail_json(msg=f"ALL jails are not started.\n{out}\n{err}")
            if name is not None and name != 'ALL' and jails[name]['state'] != 'up':
                module.fail_json(msg=f"Jail '{name}' is not started.\n{out}\n{err}")

    elif p['state'] == 'stopped':
        if name is not None and name != 'ALL' and name not in jails:
            module.fail_json(msg=f"Jail '{name}' doesn't exist.")
        if name is not None and name == 'ALL' and _all_jails_stopped(facts):
            msgs.append("All jails already stopped.")
        if name is not None and name != 'ALL' and jails[name]['state'] == 'down':
            msgs.append(f"Jail '{name}' already stopped.")
        else:
            _changed, _msg, out, err = jail_stop(module, iocage_path, name, args)
            msgs.append(_msg)
        if not module.check_mode:
            facts['iocage_jails'] = _get_iocage_facts(module, iocage_path, 'jails')
            jails.update(facts['iocage_jails'])
            if name is not None and name == 'ALL' and not _all_jails_stopped(facts):
                module.fail_json(msg=f"ALL jails are not stopped.\n{out}\n{err}")
            if name is not None and name != 'ALL' and jails[name]['state'] != 'down':
                module.fail_json(msg=f"Jail '{name}' is not stopped.\n{out}\n{err}")

    elif p['state'] == 'restarted':
        if name is None:
            module.fail_json(msg="Jail name or ALL is required to restart jail(s).")
        if name != 'ALL' and name not in jails:
            module.fail_json(msg=f"Jail '{name}' doesn't exist.")
        else:
            _changed, _msg, out, err = jail_restart(module, iocage_path, name, args)
            msgs.append(_msg)
        if not module.check_mode:
            facts['iocage_jails'] = _get_iocage_facts(module, iocage_path, 'jails')
            jails.update(facts['iocage_jails'])
            if name == 'ALL' and not _all_jails_started(facts):
                module.fail_json(msg=f"ALL jails are not up.\n{out}\n{err}")
            if name != 'ALL' and jails[name]['state'] != 'up':
                module.fail_json(msg=f"Restarting jail '{name}' failed.\n{out}\n{err}")

    elif p['state'] == 'exec':
        _changed, _msg, out, err = jail_exec(module, iocage_path, name, user, cmd)
        msgs.append(_msg)

    elif p['state'] == 'pkg':
        _changed, _msg, out, err = jail_pkg(module, iocage_path, name, cmd)
        msgs.append(_msg)

    elif p['state'] == 'fetched':
        # Fetch or update release and componenets. The var release is always defined.
        if bupdate or release not in facts['iocage_releases']:
            _changed, _msg, out, err = release_fetch(module, iocage_path, bupdate, release, components, None, args)
            msgs.append(_msg)
            if not module.check_mode:
                facts['iocage_releases'] = _get_iocage_facts(module, iocage_path, 'releases')
                if release not in facts['iocage_releases']:
                    module.fail_json(msg=f"Fetching release {release} failed.\n{out}\n{err}")
        else:
            msgs.append(f"Release {release} already fetched.")
        # Fetch or update plugin if defined
        if plugin is not None:
            if bupdate or plugin not in facts['iocage_plugins']:
                _changed, _msg, out, err = release_fetch(module, iocage_path, bupdate, None, None, plugin, args)
                msgs.append(_msg)
                if not module.check_mode:
                    facts['iocage_plugins'] = _get_iocage_facts(module, iocage_path, 'plugins')
                    if plugin not in facts['iocage_plugins']:
                        module.fail_json(msg=f"Fetching plugin {plugin} failed.\n{out}\n{err}")
            else:
                msgs.append(f"Plugin {plugin} already fetched.")

    elif p['state'] == 'get':
        facts['iocage_properties'] = _jail_get_properties(module, iocage_path, name)

    elif p['state'] == 'set':
        _changed, _msg = jail_set(module, iocage_path, name, properties)
        msgs.append(_msg)
        if not module.check_mode:
            facts['iocage_jails'] = _get_iocage_facts(module, iocage_path, 'jails')

    elif p['state'] in ['present', 'cloned', 'template', 'basejail', 'thickjail']:

        do_basejail = False
        do_thickjail = False
        clone_from_name = None
        clone_from_template = None

        if p['state'] != 'cloned' and release not in facts['iocage_releases']:
            _changed, _msg = release_fetch(module, iocage_path, bupdate, release, components)
            msgs.append(_msg)
            if _changed:
                facts['iocage_releases'] = _get_iocage_facts(module, iocage_path, 'releases')

        if p['state'] == 'template':
            if properties is None:
                properties = {}
            properties['template'] = 1
            properties['boot'] = 0

        elif p['state'] == 'basejail':
            do_basejail = True

        elif p['state'] == 'thickjail':
            do_thickjail = True

        elif clone_from is not None:
            if clone_from in facts['iocage_jails']:
                clone_from_name = clone_from
            elif clone_from in facts['iocage_templates']:
                clone_from_template = clone_from
            else:
                if module.check_mode:
                    msgs.append(f"Jail would be cloned from (nonexisting) jail or template '{clone_from}'")
                else:
                    module.fail_json(msg=f"Unable to create jail.\nbasejail '{clone_from}' doesn't exist.")

        if name is None or len(name) == 0 or name not in jails:
            _changed, _msg, _uuid, _uuid_short = jail_create(module, iocage_path, name, properties, clone_from_name,
                                                             clone_from_template, release, do_basejail, do_thickjail,
                                                             pkglist, args)
            msgs.append(_msg)
        else:
            msgs.append("Jail already exists.")
            _changed, _msg = jail_set(module, iocage_path, name, properties)
            if _changed:
                msgs.append(_msg)

        if bupdate:
            if release not in facts['iocage_releases']:
                _changed, _msg = release_fetch(module, iocage_path, bupdate, release, components)
                if _changed:
                    msgs.append(_msg)
                    facts['iocage_releases'] = _get_iocage_facts(module, iocage_path, 'releases')
            _changed, _msg = jail_update(module, iocage_path, name)
            msgs.append(_msg)

        if _changed:
            if p['state'] == 'template':
                facts['iocage_templates'] = _get_iocage_facts(module, iocage_path, 'templates')
            else:
                facts['iocage_jails'] = _get_iocage_facts(module, iocage_path, 'jails')

    elif p['state'] == 'absent':
        if name not in jails:
            _msg = f"'{name}' already destroyed."
            msgs.append(_msg)
        else:
            if jails[name]['state'] == 'up':
                _changed, _msg, out, err = jail_stop(module, iocage_path, name)
                msgs.append(_msg)
            _changed, _msg, out, err = jail_destroy(module, iocage_path, name, args)
            msgs.append(_msg)
        if not module.check_mode:
            facts['iocage_jails'] = _get_iocage_facts(module, iocage_path, 'jails')
            facts['iocage_templates'] = _get_iocage_facts(module, iocage_path, 'templates')
            if name in facts['iocage_jails'] or name in facts['iocage_templates']:
                module.fail_json(msg=f"'{name}' not destroyed.\n{out}\n{err}")

    result = dict(ansible_facts=facts,
                  changed=_changed,
                  msg=", ".join(msgs),
                  stdout=out,
                  stderr=err,
                  )
    if module._debug:
        result['module_args'] = f"{(json.dumps(module.params, indent=4))}"
    if len(_uuid) > 0:
        result['uuid'] = f"{_uuid}"
        result['uuid_short'] = f"{_uuid_short}"

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
