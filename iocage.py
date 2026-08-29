# Copyright 2015, Perceivon Hosting Inc.
# Copyright 2021-2026, Vladimir Botka <vbotka@gmail.com>
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
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# SPDX-License-Identifier: BSD-2-Clause

from __future__ import annotations

DOCUMENTATION = r"""
module: iocage
short_description: FreeBSD iocage jail handling
description:
  - A wrapper to C(iocage) command.
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
requirements:
  - lang/python >= 3.6
  - sysutils/iocage
options:
  state:
    description:
      - "O(state) of the desired result."
      - "State V(cloned) uses C(iocage create ...) if O(clone_from) is a template."
      - "State V(cloned) uses C(iocage clone ...) if O(clone_from) is a jail."
      - "State V(absent) by default forces destruction C(iocage destroy --force name)."
      - "V(started, stopped, restarted, get, set, exec, pkg, absent) require O(name)."
      - "V(started, stopped, restarted, get, set, exec, pkg) require existing jail."
      - "V(exec, pkg) requires running jail."
      - "For V(basejail, thickjail, template, fetched, present) the default O(release) is C('uname -r')."
      - "For O(bupdate) the default O(release) is C('uname -r')."
      - "O(bupdate) requires existing jail if O(name) is used."
      - "The choices below provide the command synopsis:"
      - "V(absent) - iocage destroy --force [args] <name>"
      - "V(basejail) - iocage create -b [-n name] [-r release] [-p pkglist] [args] [properties]"
      - "V(cloned) - iocage create -t <clone_from> [-n name] [-p pkglist] [args] [properties] or iocage clone <clone_from> [-n name] [args] [properties]"
      - "V(exec) - iocage exec -u <user> <name> -- <cmd>"
      - "V(facts) - iocage list -hl|-hP|-hlt|-hr"
      - "V(fetched) - iocage fetch [-U] [-r release] [-F components] [-P plugin]"
      - "V(get) - iocage get --all <name>"
      - "V(pkg) - iocage pkg <name> <cmd>"
      - "V(present) - iocage create [-n name] [-r release] [-p pkglist] [args] [properties]"
      - "V(restarted) - iocage restart [args] [name]"
      - "V(set) - iocage set <properties> <name>"
      - "V(started) - iocage start [args] [name]"
      - "V(stopped) - iocage stop [args] [name]"
      - "V(template) - iocage create [-n name] [-r release] [-p pkglist] [args] [properties] template=1 boot=0"
      - "V(thickjail) - iocage create -T [-n name] [-r release] [-p pkglist] [args] [properties]"
    type: str
    default: facts
    choices:
      - absent
      - basejail
      - cloned
      - exec
      - facts
      - fetched
      - get
      - pkg
      - present
      - restarted
      - set
      - started
      - stopped
      - template
      - thickjail
  name:
    description:
      - "O(name) of the jail."
      - "States V(started, stopped, restarted) accept V(ALL) to start, stop, or restart all jails."
      - "States V(present, cloned, template, basejail, thickjail) will return RV(uuid) and RV(uuid_short) if O(name) is
        V(None) or empty."
    type: str
  pkglist:
    description:
      - Path to a JSON file containing packages to install. Only applicable when creating a jail.
    type: path
  properties:
    description:
      - "O(properties) of the jail. The jail will restart if any of the properties B(ip4_addr,
        ip6_addr, template, interfaces, vnet, host_hostname) changes."
      - "The strings C('yes') and C('on'), and boolean C(True) or C(true) will be converted to C(1)."
      - "The strings C('no') and C('off'), and boolean C(False) or C(false) will be converted to C(0)."
    type: dict
  args:
    description:
      - Additional arguments of C(iocage) applied to the O(state). They will be applied
        to the sub-command B(create) if the O(state) is V(basejail, thickjail, template, present).
        If the same Ansible task also fetches a release as part of the creation
        the arguments will not be applied to the sub-command B(fetch). Use a separate task
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
      - Use B(state=cloned).
      - If O(clone_from) is a template C(create) the new jail C(uuid) or O(name) if defined.
      - If O(clone_from) is a jail C(clone) the new jail C(uuid) or O(name) if defined.
      - Use O(properties) to configure the new jail.
      - Use O(args) to configure the C(iocage) command.
      - Use O(pkglist) if O(clone_from) is a template.
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
      - Uses a local file directory for the root directory instead of HTTP to download and/or
        update releases.
    type: list
    elements: path
    aliases: [files, component]
notes:
  - Supports C(check_mode).
  - There is no mandatory option.
  - The module always creates facts B(iocage_releases), B(iocage_templates), B(iocage_jails), and
    B(iocage_plugins).
  - Returns B(module_args) when debugging is enabled.
seealso:
  - name: iocage - A FreeBSD Jail Manager
    description: iocage 1.2 documentation
    link: https://iocage.readthedocs.io/en/latest/
  - name: iocage - jail manager using ZFS and VNET
    description: FreeBSD System Manager's Manual
    link: https://www.freebsd.org/cgi/man.cgi?query=iocage
"""

EXAMPLES = r"""
- name: Create Ansible facts iocage_*. This is the default state.
  iocage:
    state: facts

- name: Display lists of bases, plugins, templates, and jails
  debug:
    msg: |-
      {{ ansible_facts.iocage_releases }}
      {{ ansible_facts.iocage_plugins.keys() | list }}
      {{ ansible_facts.iocage_templates.keys() | list }}
      {{ ansible_facts.iocage_jails.keys() | list }}

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
    components:
      - base.txz
      - doc.txz

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
    components:
      - base.txz
      - doc.txz
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
      ip4_addr: 'vnet0|10.1.0.5/24'
      boot: false
      allow_sysvipc: true
      defaultrouter: '10.1.0.1'

- name: Create the jail from the template tplfoo.
        Install packages and set properties.
  iocage:
    state: cloned
    name: foo
    clone_from: tplfoo
    pkglist: /path/to/add_pkglist.json
    properties:
      ip4_addr: 'vnet0|10.1.0.6/24'
      boot: true
      allow_sysvipc: true
      defaultrouter: '10.1.0.1'

- name: Create the jail from the template tplfoo.
        The name is automatically generated.
  iocage:
    state: cloned
    clone_from: tplfoo
  register: result

- name: Set variable contains the name of the created jail.
  ansible.builtin.set_fact:
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
"""

RETURN = r"""
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
"""

import re
import shlex
from ansible.module_utils.basic import AnsibleModule


RESTART_PROPERTIES = frozenset({
    'ip4_addr',
    'ip6_addr',
    'template',
    'interfaces',
    'vnet',
    'host_hostname',
})


def _all_jails_started(facts):
    """Test all jails are started."""
    states = {v['state'] for v in facts['iocage_jails'].values()}
    return states == {'up'}


def _all_jails_stopped(facts):
    """Test all jails are stopped."""
    states = {v['state'] for v in facts['iocage_jails'].values()}
    return states == {'down'}


def _props_to_args(props):
    """Convert dictionary of properties to list of iocage key=value argument pairs."""
    args = []
    for key, val in props.items():
        if val in ('-', '', None):
            continue
        if val in ('yes', 'on', True):
            args.append(f"{key}=1")
        elif val in ('no', 'off', False):
            args.append(f"{key}=0")
        else:
            args.append(f"{key}={val}")
    return args


def _command_fail(module, label, cmd, rc, stdout, stderr):
    """Command fail. Create message and terminate module."""
    cmd_str = ' '.join(cmd) if isinstance(cmd, list) else cmd
    module.fail_json(msg=f"{label}\ncmd: '{cmd_str}' return: {rc}\nstdout: '{stdout}'\nstderr: '{stderr}'")


def _get_iocage_facts(module, iocage_path, artifact='all', name=None):
    """Collect facts."""
    opt = {
        "jails": ["list", "-hl"],
        "plugins": ["list", "-hP"],
        "templates": ["list", "-hlt"],
        "releases": ["list", "-hr"],
        "init": ["list", "-h"],
    }

    if artifact == 'all':
        return dict(
            iocage_jails=_get_iocage_facts(module, iocage_path, 'jails'),
            iocage_plugins=_get_iocage_facts(module, iocage_path, 'plugins'),
            iocage_templates=_get_iocage_facts(module, iocage_path, 'templates'),
            iocage_releases=_get_iocage_facts(module, iocage_path, 'releases'),
        )

    if artifact not in opt:
        module.fail_json(msg=f"_get_iocage_facts(artifact={artifact}): argument not understood.")

    cmd = [iocage_path] + opt[artifact]
    rc, out, err = module.run_command(cmd)

    if rc != 0 and artifact != 'init':
        _command_fail(module, "Function _get_iocage_facts failed.", cmd, rc, out, err)
    elif artifact == 'init':
        return {}

    if artifact == 'releases':
        return [line.strip() for line in out.splitlines() if line.strip()]

    if artifact in ('jails', 'templates', 'plugins'):
        _items = {}
        try:
            for line in out.strip('\r\n').splitlines():
                line = line.strip()
                if not line:
                    continue
                _jid = line.split('\t')[0]
                if _jid == '---':
                    break
                if re.match(r'^(\d+|-|None)$', _jid):
                    _fragments = line.split('\t')
                    if artifact in ('jails', 'templates'):
                        if len(_fragments) == 10:
                            _keys = ('jid', 'name', 'boot', 'state', 'type', 'release', 'ip4', 'ip6', 'template', 'basejail')
                        else:
                            _keys = ('jid', 'name', 'boot', 'state', 'type', 'release', 'ip4', 'ip6', 'template')
                        _name = _fragments[1]
                        if _name:
                            _items[_name] = dict(zip(_keys, _fragments))
                            _items[_name]['properties'] = _jail_get_properties(module, iocage_path, _name)
                    elif artifact == 'plugins':
                        _keys = ('jid', 'name', 'boot', 'state', 'type', 'release', 'ip4', 'ip6', 'template', 'portal', 'doc_url')
                        _name = _fragments[1]
                        if _name:
                            _items[_name] = dict(zip(_keys, _fragments))
                else:
                    module.fail_json(msg=f"_get_iocage_facts(artifact={artifact}):\nUnreadable stdout line from cmd '{' '.join(cmd)}':\n'{line}'")
        except ValueError:
            module.fail_json(msg=f"unable to parse {out}")

        if name:
            return _items.get(name, {})

        return _items


def _jail_get_properties(module, iocage_path, name):
    if not name:
        module.fail_json(msg="_jail_get_properties:\njail name not specified.")

    properties = {}
    cmd = [iocage_path, "get", "--all", name]
    rc, out, err = module.run_command(cmd)
    if rc == 0:
        for line in out.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split(':', 1)
            if len(parts) == 2:
                properties[parts[0]] = parts[1]
            else:
                module.fail_json(msg=f"error parsing property {line} from {properties}")
    else:
        _command_fail(module, f"_jail_get_properties({name})", cmd, rc, out, err)

    return properties


def jail_started(module, iocage_path, name):
    """Test jail name is started(up) or not(down). Return Boolean."""
    cmd = [iocage_path, "list", "-h"]
    rc, out, err = module.run_command(cmd)
    if rc != 0:
        _command_fail(module, f"jail_started({name})", cmd, rc, out, err)

    for line in out.splitlines():
        parts = line.split('\t')
        if len(parts) >= 3 and parts[1] == name:
            state = parts[2]
            if state == 'up':
                return True
            if state == 'down':
                return False
            module.fail_json(msg=f"Jail '{name}' unknown state: {line}")

    return None


def jail_exists(module, iocage_path, name):
    """Test jail name exists. Return Boolean."""
    cmd = [iocage_path, "get", "host_hostuuid", name]
    rc, out, err = module.run_command(cmd)
    if rc == 0:
        return True
    if rc == 1:
        return False
    _command_fail(module, f"jail_exists({name})", cmd, rc, out, err)
    return False


def jail_start(module, iocage_path, name, args=""):
    _changed = True
    cmd = [iocage_path, "start"]
    if args:
        cmd.extend(shlex.split(args))
    cmd.append(name)

    if not module.check_mode:
        rc, out, err = module.run_command(cmd)
        if rc != 0:
            _command_fail(module, "Jail(s) not started.", cmd, rc, out, err)
        if name == "ALL":
            _msg = f"All jails started.\n{' '.join(cmd)}\n{out}"
        else:
            _msg = f"Jail '{name}' started.\n{' '.join(cmd)}\n{out}"
    else:
        out = ""
        err = ""
        if name == 'ALL':
            _msg = f"All jails would start.\n{' '.join(cmd)}"
        else:
            _msg = f"Jail '{name}' would start.\n{' '.join(cmd)}"

    return _changed, _msg, out, err


def jail_stop(module, iocage_path, name, args=""):
    _changed = True
    cmd = [iocage_path, "stop"]
    if args:
        cmd.extend(shlex.split(args))
    cmd.append(name)

    if not module.check_mode:
        rc, out, err = module.run_command(cmd)
        if rc != 0:
            _command_fail(module, "Jail(s) not stopped.", cmd, rc, out, err)
        if name == 'ALL':
            _msg = f"All jails stopped.\n{' '.join(cmd)}\n{out}"
        else:
            _msg = f"Jail '{name}' stopped.\n{' '.join(cmd)}\n{out}"
    else:
        out = ""
        err = ""
        if name == "ALL":
            _msg = f"All jails would stop.\n{' '.join(cmd)}"
        else:
            _msg = f"Jail '{name}' would stop.\n{' '.join(cmd)}"

    return _changed, _msg, out, err


def jail_restart(module, iocage_path, name, args=""):
    _changed = True
    cmd = [iocage_path, "restart"]
    if args:
        cmd.extend(shlex.split(args))
    cmd.append(name)

    if not module.check_mode:
        rc, out, err = module.run_command(cmd)
        if rc != 0:
            _command_fail(module, "Jail(s) not restarted.", cmd, rc, out, err)
        if name == 'ALL':
            _msg = f"ALL jails restarted.\n{' '.join(cmd)}\n{out}"
        else:
            _msg = f"Jail '{name}' restarted.\n{' '.join(cmd)}\n{out}"
    else:
        out = ""
        err = ""
        if name == 'ALL':
            _msg = f"ALL jails would restart.\n{' '.join(cmd)}"
        else:
            _msg = f"Jail '{name}' would restart.\n{' '.join(cmd)}"

    return _changed, _msg, out, err


def release_fetch(module, iocage_path, bupdate=False, release=None, components=None, plugin=None, args=""):
    _changed = True
    cmd = [iocage_path, "fetch"]
    if args:
        cmd.extend(shlex.split(args))
    if bupdate:
        cmd.append("-U")
    if release:
        cmd.extend(["-r", release])
    if components:
        for component in components:
            if component:
                cmd.extend(["-F", component])
    if plugin:
        cmd.extend(["-P", plugin])

    if not module.check_mode:
        rc, out, err = module.run_command(cmd)
        if rc != 0:
            _command_fail(module, "Function release_fetch failed.", cmd, rc, out, err)
        if bupdate:
            _msg = f"Successfully fetched and updated.\n{' '.join(cmd)}\n{out}"
        else:
            _msg = f"Successfully fetched.\n{' '.join(cmd)}\n{out}"
    else:
        out = ""
        err = ""
        if bupdate:
            _msg = f"Would fetch and update.\n{' '.join(cmd)}"
        else:
            _msg = f"Would fetch.\n{' '.join(cmd)}"

    return _changed, _msg, out, err


def jail_exec(module, iocage_path, name, user='root', _cmd='/usr/bin/true'):
    _changed = True
    cmd = [iocage_path, "exec", "-u", user, name, "--"]
    if isinstance(_cmd, list):
        cmd.extend(_cmd)
    else:
        cmd.extend(shlex.split(_cmd))

    if not module.check_mode:
        rc, out, err = module.run_command(cmd)
        if rc != 0:
            _command_fail(module, f"Command '{_cmd}' not executed.", cmd, rc, out, err)
        _msg = f"Jail '{name}' executed command '{_cmd}'\n{' '.join(cmd)}\nrc: {rc}\nstdout:\n{out}\nstderr:\n{err}"
    else:
        out = ""
        err = ""
        _msg = f"Jail '{name}' would execute command '{_cmd}'\n{' '.join(cmd)}"

    return _changed, _msg, out, err


def jail_pkg(module, iocage_path, name, _cmd='info'):
    _changed = True
    cmd = [iocage_path, "pkg", name]
    if isinstance(_cmd, list):
        cmd.extend(_cmd)
    else:
        cmd.extend(shlex.split(_cmd))

    if not module.check_mode:
        rc, out, err = module.run_command(cmd)
        if rc != 0:
            _command_fail(module, f"Command 'pkg {_cmd}' not executed.", cmd, rc, out, err)
        _msg = f"Jail '{name}' executed command 'pkg {_cmd}'\n{' '.join(cmd)}\nrc: {rc}\nstdout:\n{out}\nstderr:\n{err}"
    else:
        out = ""
        err = ""
        _msg = f"Jail '{name}' would execute command 'pkg {_cmd}'\n{' '.join(cmd)}"

    return _changed, _msg, out, err


def jail_set(module, iocage_path, name, properties=None):
    if properties is None:
        properties = {}
    _existing_props = _jail_get_properties(module, iocage_path, name)
    _props_to_be_changed = {}

    for prop_name, prop_val in properties.items():
        if prop_name not in _existing_props:
            continue
        if _existing_props[prop_name] == '-' and not prop_val:
            continue

        _oval = _existing_props[prop_name]
        if prop_val in (0, 'no', 'off', False):
            formatted_val = "0"
        elif prop_val in (1, 'yes', 'on', True):
            formatted_val = "1"
        elif isinstance(_oval, str):
            formatted_val = 'none' if prop_val == '' else str(prop_val)
        else:
            module.fail_json(msg=f"Unable to set attribute {prop_name} to {prop_val} for jail {name}")

        if 'CHECK_NEW_JAIL' in _existing_props or (str(_oval) != str(formatted_val) and formatted_val is not None):
            _props_to_be_changed[prop_name] = formatted_val

    if _props_to_be_changed:
        _changed = True
        need_restart = bool(RESTART_PROPERTIES.intersection(_props_to_be_changed.keys())) and jail_started(module, iocage_path, name)

        cmd = [iocage_path, "set"] + _props_to_args(_props_to_be_changed) + [name]

        if not module.check_mode:
            if need_restart:
                jail_stop(module, iocage_path, name)
            rc, out, err = module.run_command(cmd)
            if need_restart:
                jail_start(module, iocage_path, name)
            if rc != 0:
                _command_fail(module, "properties not set.", cmd, rc, out, err)
            _msg = f"properties {list(_props_to_be_changed.keys())} were set in jail '{name}'\n{' '.join(cmd)}"
        else:
            _msg = f"properties {list(_props_to_be_changed.keys())} would be set in jail '{name}'\n{' '.join(cmd)}\n{_props_to_be_changed}"
    else:
        _changed = False
        _msg = f"properties {list(properties.keys())} already set in jail '{name}'"

    return _changed, _msg


def jail_create(module, iocage_path, name=None, properties=None, clone_from_name=None,
                clone_from_template=None, release=None, basejail=False, thickjail=False,
                pkglist=None, args=""):
    _changed = True
    _uuid = ""
    _uuid_short = ""

    if clone_from_name is None and clone_from_template is None:
        cmd = [iocage_path, "create"]
        if name:
            cmd.extend(["-n", name])
        if release:
            cmd.extend(["-r", release])
        if basejail:
            cmd.append("-b")
        elif thickjail:
            cmd.append("-T")
        if pkglist:
            cmd.extend(["-p", pkglist])
        if args:
            cmd.extend(shlex.split(args))

    elif clone_from_template:
        cmd = [iocage_path, "create", "-t", clone_from_template]
        if name:
            cmd.extend(["-n", name])
        if pkglist:
            cmd.extend(["-p", pkglist])
        if args:
            cmd.extend(shlex.split(args))

    elif clone_from_name:
        cmd = [iocage_path, "clone", clone_from_name]
        if name:
            cmd.extend(["-n", name])
        if args:
            cmd.extend(shlex.split(args))

    if properties:
        cmd.extend(_props_to_args(properties))

    if not module.check_mode:
        rc, out, err = module.run_command(cmd)
        if rc != 0:
            _command_fail(module, "Jail not created.", cmd, rc, out, err)
        _msg = f"Jail was created.\n{' '.join(cmd)}\n{out}"
        if not name:
            _uuid = out.split()[0]
            _uuid_short = _uuid.split('-')[0]
            name = _uuid_short
            rename_cmd = [iocage_path, "rename", _uuid, _uuid_short]
            rc, out, err = module.run_command(rename_cmd)
            if rc != 0:
                _command_fail(module, "Jail not renamed.", rename_cmd, rc, out, err)
        if not jail_exists(module, iocage_path, name):
            module.fail_json(msg=f"'{name}' not created ???\ncmd: {' '.join(cmd)}\nstdout:\n{out}\nstderr:\n{err}")
    else:
        _msg = f"Jail would be created.\n{' '.join(cmd)}"

    return _changed, _msg, _uuid, _uuid_short


def jail_update(module, iocage_path, name):
    _changed = True
    cmd = [iocage_path, "update", name]

    if not module.check_mode:
        rc, out, err = module.run_command(cmd)
        if "No updates needed" in out:
            _changed = False
            _msg = f"Jail '{name}' is up-to-date.\n{out}"
        elif rc != 0:
            _command_fail(module, f"Jail '{name}' not updated.", cmd, rc, out, err)
        else:
            _msg = f"Jail '{name}' was updated\n{out}"
    else:
        _msg = f"Jail '{name}' would be updated.\n{' '.join(cmd)}"

    return _changed, _msg


def jail_destroy(module, iocage_path, name, args=""):
    _changed = True
    cmd = [iocage_path, "destroy", "--force"]
    if args:
        cmd.extend(shlex.split(args))
    cmd.append(name)

    if not module.check_mode:
        rc, out, err = module.run_command(cmd)
        if rc != 0:
            _command_fail(module, f"'{name}' not destroyed.", cmd, rc, out, err)
        _msg = f"'{name}' was destroyed.\n{out}"
        if jail_exists(module, iocage_path, name):
            module.fail_json(msg=f"'{name}' not destroyed ???\ncmd: {' '.join(cmd)}\nstdout:\n{out}\nstderr:\n{err}")
    else:
        out = ""
        err = ""
        _msg = f"'{name}' would be destroyed.\n{' '.join(cmd)}"

    return _changed, _msg, out, err


def run_module():
    module_args = dict(
        state=dict(
            type='str',
            default='facts',
            choices=[
                'absent', 'basejail', 'cloned', 'exec', 'facts', 'fetched', 'get', 'pkg',
                'present', 'restarted', 'set', 'started', 'stopped', 'template', 'thickjail',
            ],
        ),
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
        components=dict(type='list', elements='path', aliases=['files', 'component']),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    iocage_path = module.get_bin_path('iocage', required=True)

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

    _changed = False
    out = ""
    err = ""
    facts = _get_iocage_facts(module, iocage_path, 'all')
    facts['iocage_states'] = module_args['state']['choices']

    if p['state'] == 'facts':
        result = dict(
            ansible_facts=facts,
            changed=_changed,
            msg="",
            stdout=out,
            stderr=err,
        )
        module.exit_json(**result)

    jails = {}
    jails.update(facts['iocage_jails'])
    jails.update(facts['iocage_templates'])

    # Input validation
    if p['state'] in ('started', 'stopped', 'restarted', 'get', 'set', 'exec', 'pkg', 'absent') and name is None:
        module.fail_json(msg=f"name needed for state {p['state']}")

    if p['state'] in ('started', 'stopped', 'restarted'):
        if name != 'ALL' and name not in jails:
            module.fail_json(msg=f"Jail '{name}' doesn't exist.")

    if p['state'] in ('get', 'set', 'exec', 'pkg') and name not in jails:
        module.fail_json(msg=f"Jail '{name}' doesn't exist.")

    if name and bupdate and name not in jails:
        module.fail_json(msg=f"Jail '{name}' doesn't exist.")

    if p['state'] in ('exec', 'pkg') and jails[name]['state'] != 'up':
        module.fail_json(msg=f"Jail '{name}' not running.")

    if p['state'] in ('basejail', 'thickjail', 'template', 'fetched', 'present') or bupdate:
        if not release:
            rc, out, err = module.run_command(["uname", "-r"])
            if rc != 0:
                module.fail_json(msg="Unable to run uname -r ???")
            matches = re.match(r'^(\d+\.\d+)-(RELEASE|RC\d+).*', out.strip())
            if matches:
                release = matches.group(1) + '-RELEASE'
            else:
                module.fail_json(msg=f"Release not recognized: {out}")

    msgs = []
    _uuid = ''
    _uuid_short = ''

    if p['state'] == 'started':
        if name == 'ALL' and _all_jails_started(facts):
            msgs.append("All jails already started.")
        elif name != 'ALL' and jails[name]['state'] == 'up':
            msgs.append(f"Jail '{name}' already started.")
        else:
            _changed, _msg, out, err = jail_start(module, iocage_path, name, args)
            msgs.append(_msg)
        if not module.check_mode:
            facts['iocage_jails'] = _get_iocage_facts(module, iocage_path, 'jails')
            jails.update(facts['iocage_jails'])
            if name == 'ALL' and not _all_jails_started(facts):
                module.fail_json(msg=f"ALL jails are not started.\n{out}\n{err}")
            elif name != 'ALL' and jails[name]['state'] != 'up':
                module.fail_json(msg=f"Jail '{name}' is not started.\n{out}\n{err}")

    elif p['state'] == 'stopped':
        if name == 'ALL' and _all_jails_stopped(facts):
            msgs.append("All jails already stopped.")
        elif name != 'ALL' and jails[name]['state'] == 'down':
            msgs.append(f"Jail '{name}' already stopped.")
        else:
            _changed, _msg, out, err = jail_stop(module, iocage_path, name, args)
            msgs.append(_msg)
        if not module.check_mode:
            facts['iocage_jails'] = _get_iocage_facts(module, iocage_path, 'jails')
            jails.update(facts['iocage_jails'])
            if name == 'ALL' and not _all_jails_stopped(facts):
                module.fail_json(msg=f"ALL jails are not stopped.\n{out}\n{err}")
            elif name != 'ALL' and jails[name]['state'] != 'down':
                module.fail_json(msg=f"Jail '{name}' is not stopped.\n{out}\n{err}")

    elif p['state'] == 'restarted':
        _changed, _msg, out, err = jail_restart(module, iocage_path, name, args)
        msgs.append(_msg)
        if not module.check_mode:
            facts['iocage_jails'] = _get_iocage_facts(module, iocage_path, 'jails')
            jails.update(facts['iocage_jails'])
            if name == 'ALL' and not _all_jails_started(facts):
                module.fail_json(msg=f"ALL jails are not up.\n{out}\n{err}")
            elif name != 'ALL' and jails[name]['state'] != 'up':
                module.fail_json(msg=f"Restarting jail '{name}' failed.\n{out}\n{err}")

    elif p['state'] == 'exec':
        _changed, _msg, out, err = jail_exec(module, iocage_path, name, user, cmd)
        msgs.append(_msg)

    elif p['state'] == 'pkg':
        _changed, _msg, out, err = jail_pkg(module, iocage_path, name, cmd)
        msgs.append(_msg)

    elif p['state'] == 'fetched':
        if bupdate or release not in facts['iocage_releases']:
            _changed, _msg, out, err = release_fetch(module, iocage_path, bupdate, release, components, None, args)
            msgs.append(_msg)
            if not module.check_mode:
                facts['iocage_releases'] = _get_iocage_facts(module, iocage_path, 'releases')
                if release not in facts['iocage_releases']:
                    module.fail_json(msg=f"Fetching release {release} failed.\n{out}\n{err}")
        else:
            msgs.append(f"Release {release} already fetched.")

        if plugin:
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

    elif p['state'] in ('present', 'cloned', 'template', 'basejail', 'thickjail'):
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

        elif clone_from:
            if clone_from in facts['iocage_jails']:
                clone_from_name = clone_from
            elif clone_from in facts['iocage_templates']:
                clone_from_template = clone_from
            else:
                if module.check_mode:
                    msgs.append(f"Jail would be cloned from (nonexisting) jail or template '{clone_from}'")
                else:
                    module.fail_json(msg=f"Unable to create jail.\nbasejail '{clone_from}' doesn't exist.")

        if name not in jails:
            _changed, _msg, _uuid, _uuid_short = jail_create(
                module,
                iocage_path,
                name=name,
                properties=properties,
                clone_from_name=clone_from_name,
                clone_from_template=clone_from_template,
                release=release,
                basejail=do_basejail,
                thickjail=do_thickjail,
                pkglist=pkglist,
                args=args,
            )
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
            msgs.append(f"'{name}' already destroyed.")
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

    result = dict(
        ansible_facts=facts,
        changed=_changed,
        msg=", ".join(msgs),
        stdout=out,
        stderr=err,
    )
    if _uuid:
        result['uuid'] = _uuid
        result['uuid_short'] = _uuid_short

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
