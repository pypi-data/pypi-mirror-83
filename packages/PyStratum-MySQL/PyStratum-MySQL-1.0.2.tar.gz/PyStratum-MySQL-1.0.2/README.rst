PyStratum-MySQL
===============

MySQL & MariaDB Backend for PyStratum

+-----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------+
| Social                                                                                                                      | Release                                                                                            | Tests                                                                                                 | Code                                                                                                       |
+=============================================================================================================================+====================================================================================================+=======================================================================================================+============================================================================================================+
| .. image:: https://badges.gitter.im/SetBased/py-stratum.svg                                                                 | .. image:: https://badge.fury.io/py/PyStratum-MySQL.svg                                            | .. image:: https://travis-ci.org/DatabaseStratum/py-stratum-mysql.svg?branch=master                   | .. image:: https://scrutinizer-ci.com/g/DatabaseStratum/py-stratum-mysql/badges/quality-score.png?b=master |
|   :target: https://gitter.im/SetBased/py-stratum?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge  |   :target: https://badge.fury.io/py/PyStratum-MySQL                                                |   :target: https://travis-ci.org/DatabaseStratum/py-stratum-mysql                                     |   :target: https://scrutinizer-ci.com/g/DatabaseStratum/py-stratum-mysql/?branch=master                    |
|                                                                                                                             |                                                                                                    | .. image:: https://scrutinizer-ci.com/g/DatabaseStratum/py-stratum-mysql/badges/coverage.png?b=master |                                                                                                            |
|                                                                                                                             |                                                                                                    |   :target: https://scrutinizer-ci.com/g/DatabaseStratum/py-stratum-mysql/?branch=master               |                                                                                                            |
+-----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------+

Overview
========
PyStratum-MySQL is a package with the following mayor functionalities:

* Loading modified and new stored routines and removing obsolete stored routines into/from a MySQL and MariaDB instance. This MySQL or MariaDB instance can be part of your development or a production environment.
* Enhancing the (limited) syntax of MySQL & MariaDB stored routines with constants and custom types (based on actual table columns).
* Generating automatically a Python wrapper class for calling your stored routines. This wrapper class takes care about error handing and prevents SQL injections.
* Defining Python constants based on auto increment columns and column widths.

Documentation
=============

The documentation of PyStratum pgSQL is available at https://pystratum-mysql.readthedocs.io and the general documentation of all Stratum projects is available at https://stratum.readthedocs.io.

License
=======

This project is licensed under the terms of the MIT license.
