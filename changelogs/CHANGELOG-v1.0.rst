=======================================
vbotka.ansible-iocage 1.0 Release Notes
=======================================

.. contents:: Topics


1.2.6
=====

Release Summary
---------------
Maintenance update.

Minor Changes
-------------
* Update README.
* Simplify conditions in jail_create
* Update docs. Template can not boot.


1.2.5
=====

Release Summary
---------------
Maintenance incl. README update.

Minor Changes
-------------
* Complete all attributes of jails, templates, and plugins.
* Update test playbook template. Show simple progess. Add var dry_run
  default=true


1.2.4
=====

Release Summary
---------------
Bugfixes.

Bugfixes
--------
* Fix clone cmd.
* Fix doc. Building docsite crashes on bupdate return value (RV).
* Fix use provided properties in basejail.
* Fix documentation notes.


1.2.3
=====

Release Summary
---------------
Maintenance update.

Major Changes
-------------

Minor Changes
-------------
* Update DOCUMENTATION.
* Move changelog to changelogs.
* Fix ansible-lint yaml[truthy]: Truthy value should be one of false, true


1.2.2
=====

Release Summary
---------------
Maintenance update.

Major Changes
-------------

Minor Changes
-------------
* Update test/configure.yml play name
* Add SPDX-License-Identifier: BSD-2-Clause


1.2.1
=====

Release Summary
---------------
Maintenance update.

Major Changes
-------------

Minor Changes
-------------
* Update README


1.2.0
=====

Release Summary
---------------
Feature update.

Major Changes
-------------
* Add state get.
* Update documentation.
* Update tests

Minor Changes
-------------
* Update README

Bugfixes
--------
* Fix iocage.py strings formatting.
* Fix `re.match(r'(\d+|-|None)', _jid)`


1.1.2
=====

Release Summary
---------------
Maintenance update.

Major Changes
-------------
* Remove CHANGELOG.md
* Add changelog/CHANGELOG-v1.0.rst
* Update LICENSE 2021-2024

Minor Changes
-------------
* Update README.md

Bugfixes
--------

Breaking Changes / Porting Guide
--------------------------------
