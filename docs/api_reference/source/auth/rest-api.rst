
.. _auth-rest-api:

==============================
MLForge Authentication REST API
==============================


The MLForge Authentication REST API allows you to create, get, update, and delete users,
manage user permissions, and manage roles and role-based access control (RBAC).
The API supports both legacy ``2.0`` endpoints for user management and new ``3.0``
endpoints for unified permission and role management introduced in MLForge 3.13.0.
The API is hosted under the ``/api`` route on the MLForge tracking server. For example, to create
a user on a tracking server hosted at ``http://localhost:5000``, access
``http://localhost:5000/api/2.0/MLForge/users/create``.

.. important::
    The MLForge REST API requires content type ``application/json`` for all POST requests.

.. contents:: Table of Contents
    :local:
    :depth: 1

===========================

.. _MLForgeAuthServiceCreateUser:

Create User
===========

+-----------------------------+-------------+
|          Endpoint           | HTTP Method |
+=============================+=============+
| ``2.0/MLForge/users/create`` | ``POST``    |
+-----------------------------+-------------+

.. _MLForgeCreateUser:

Request Structure
-----------------

+------------+------------+-------------+
| Field Name |    Type    | Description |
+============+============+=============+
| username   | ``STRING`` | Username.   |
+------------+------------+-------------+
| password   | ``STRING`` | Password.   |
+------------+------------+-------------+

.. _MLForgeCreateUserResponse:

Response Structure
------------------

+------------+-------------------+----------------+
| Field Name |       Type        |  Description   |
+============+===================+================+
| user       | :ref:`MLForgeUser` | A user object. |
+------------+-------------------+----------------+

===========================

.. _MLForgeAuthServiceGetUser:

Get User
========

+--------------------------+-------------+
|         Endpoint         | HTTP Method |
+==========================+=============+
| ``2.0/MLForge/users/get`` | ``GET``     |
+--------------------------+-------------+

.. _MLForgeGetUser:

Request Structure
-----------------

+------------+------------+-------------+
| Field Name |    Type    | Description |
+============+============+=============+
| username   | ``STRING`` | Username.   |
+------------+------------+-------------+

.. _MLForgeGetUserResponse:

Response Structure
------------------

+------------+-------------------+----------------+
| Field Name |       Type        |  Description   |
+============+===================+================+
| user       | :ref:`MLForgeUser` | A user object. |
+------------+-------------------+----------------+

===========================

.. _MLForgeAuthServiceUpdateUserPassword:

Update User Password
====================

+--------------------------------------+-------------+
|               Endpoint               | HTTP Method |
+======================================+=============+
| ``2.0/MLForge/users/update-password`` | ``PATCH``   |
+--------------------------------------+-------------+

.. _MLForgeUpdateUserPassword:

Request Structure
-----------------

+------------+------------+---------------+
| Field Name | Type       | Description   |
+============+============+===============+
| username   | ``STRING`` | Username.     |
+------------+------------+---------------+
| password   | ``STRING`` | New password. |
+------------+------------+---------------+

===========================

.. _MLForgeAuthServiceUpdateUserAdmin:

Update User Admin
=================

+-----------------------------------+-------------+
|             Endpoint              | HTTP Method |
+===================================+=============+
| ``2.0/MLForge/users/update-admin`` | ``PATCH``   |
+-----------------------------------+-------------+

.. _MLForgeUpdateUserAdmin:

Request Structure
-----------------

+------------+-------------+-------------------+
| Field Name |    Type     |    Description    |
+============+=============+===================+
| username   | ``STRING``  | Username.         |
+------------+-------------+-------------------+
| is_admin   | ``BOOLEAN`` | New admin status. |
+------------+-------------+-------------------+

===========================

.. _MLForgeAuthServiceDeleteUser:

Delete User
===========

+-----------------------------+-------------+
|          Endpoint           | HTTP Method |
+=============================+=============+
| ``2.0/MLForge/users/delete`` | ``DELETE``  |
+-----------------------------+-------------+

.. _MLForgeDeleteUser:

Request Structure
-----------------

+------------+------------+-------------+
| Field Name |    Type    | Description |
+============+============+=============+
| username   | ``STRING`` | Username.   |
+------------+------------+-------------+

===========================

.. _MLForgeAuthServiceListUsers:

List Users
==========

+-----------------------------+-------------+
|          Endpoint           | HTTP Method |
+=============================+=============+
| ``2.0/MLForge/users/list``   | ``GET``     |
+-----------------------------+-------------+

.. _MLForgeListUsersResponse:

Response Structure
------------------

+------------+---------------------------+------------------+
| Field Name |           Type            |   Description    |
+============+===========================+==================+
| users      | An array of               | A list of all    |
|            | :ref:`MLForgeUser`         | user objects.    |
+------------+---------------------------+------------------+

===========================

.. _MLForgeAuthServiceGetCurrentUser:

Get Current User
================

+--------------------------------+-------------+
|           Endpoint             | HTTP Method |
+================================+=============+
| ``2.0/MLForge/users/current``   | ``GET``     |
+--------------------------------+-------------+

.. _MLForgeGetCurrentUserResponse:

Response Structure
------------------

+------------+-------------------+------------------------------+
| Field Name |       Type        |         Description          |
+============+===================+==============================+
| user       | :ref:`MLForgeUser` | The current user object.     |
+------------+-------------------+------------------------------+

===========================

.. _MLForgeAuthServiceGrantUserPermission:

Grant User Permission
=====================

+------------------------------------------+-------------+
|                 Endpoint                 | HTTP Method |
+==========================================+=============+
| ``3.0/MLForge/users/permissions/grant``   | ``POST``    |
+------------------------------------------+-------------+

.. _MLForgeGrantUserPermission:

Request Structure
-----------------

+---------------+------------+---------------------------+
|  Field Name   |    Type    |        Description        |
+===============+============+===========================+
| username      | ``STRING`` | Username.                 |
+---------------+------------+---------------------------+
| resource_type | ``STRING`` | Resource type             |
|               |            | (``experiment`` or        |
|               |            | ``registered_model``).    |
+---------------+------------+---------------------------+
| resource_id   | ``STRING`` | Resource ID or name.      |
+---------------+------------+---------------------------+
| permission    | ``STRING`` | Permission to grant       |
|               |            | (``READ``, ``EDIT``,      |
|               |            | ``MANAGE``,               |
|               |            | ``USE``).                 |
+---------------+------------+---------------------------+

===========================

.. _MLForgeAuthServiceRevokeUserPermission:

Revoke User Permission
======================

+------------------------------------------+-------------+
|                 Endpoint                 | HTTP Method |
+==========================================+=============+
| ``3.0/MLForge/users/permissions/revoke``  | ``POST``    |
+------------------------------------------+-------------+

.. _MLForgeRevokeUserPermission:

Request Structure
-----------------

+---------------+------------+---------------------------+
|  Field Name   |    Type    |        Description        |
+===============+============+===========================+
| username      | ``STRING`` | Username.                 |
+---------------+------------+---------------------------+
| resource_type | ``STRING`` | Resource type             |
|               |            | (``experiment`` or        |
|               |            | ``registered_model``).    |
+---------------+------------+---------------------------+
| resource_id   | ``STRING`` | Resource ID or name.      |
+---------------+------------+---------------------------+

===========================

.. _MLForgeAuthServiceGetUserPermission:

Get User Permission
===================

+------------------------------------------+-------------+
|                 Endpoint                 | HTTP Method |
+==========================================+=============+
| ``3.0/MLForge/users/permissions/get``     | ``GET``     |
+------------------------------------------+-------------+

.. _MLForgeGetUserPermission:

Request Structure
-----------------

+---------------+------------+---------------------------+
|  Field Name   |    Type    |        Description        |
+===============+============+===========================+
| username      | ``STRING`` | Username.                 |
+---------------+------------+---------------------------+
| resource_type | ``STRING`` | Resource type             |
|               |            | (``experiment`` or        |
|               |            | ``registered_model``).    |
+---------------+------------+---------------------------+
| resource_id   | ``STRING`` | Resource ID or name.      |
+---------------+------------+---------------------------+

.. _MLForgeGetUserPermissionResponse:

Response Structure
------------------

+------------+-------------+------------------------------+
| Field Name |    Type     |         Description          |
+============+=============+==============================+
| allowed    | ``BOOLEAN`` | Whether the user is allowed  |
|            |             | to access the resource.      |
+------------+-------------+------------------------------+
| permission | ``STRING``  | The effective permission     |
|            |             | for the user on the          |
|            |             | specified resource.          |
+------------+-------------+------------------------------+

===========================

.. _MLForgeAuthServiceListUserPermissions:

List User Permissions
=====================

+------------------------------------------+-------------+
|                 Endpoint                 | HTTP Method |
+==========================================+=============+
| ``3.0/MLForge/users/permissions/list``    | ``GET``     |
+------------------------------------------+-------------+

.. _MLForgeListUserPermissions:

Request Structure
-----------------

+------------+------------+-------------+
| Field Name |    Type    | Description |
+============+============+=============+
| username   | ``STRING`` | Username.   |
+------------+------------+-------------+

.. _MLForgeListUserPermissionsResponse:

Response Structure
------------------

+-------------+------------+--------------------------------+
|  Field Name |    Type    |          Description           |
+=============+============+================================+
| permissions | ``ARRAY``  | List of permissions for        |
|             |            | the user across all resources. |
+-------------+------------+--------------------------------+

===========================

.. _MLForgeAuthServiceListCurrentUserPermissions:

List Current User Permissions
==============================

+--------------------------------------------------+-------------+
|                    Endpoint                      | HTTP Method |
+==================================================+=============+
| ``3.0/MLForge/users/current/permissions``         | ``GET``     |
+--------------------------------------------------+-------------+

.. _MLForgeListCurrentUserPermissionsResponse:

Response Structure
------------------

+-------------+------------+----------------------------------------+
|  Field Name |    Type    |              Description               |
+=============+============+========================================+
| permissions | ``ARRAY``  | List of permissions for the            |
|             |            | currently authenticated user.          |
+-------------+------------+----------------------------------------+

===========================

.. _MLForgeAuthServiceCreateRole:

Create Role
===========

+--------------------------------+-------------+
|           Endpoint             | HTTP Method |
+================================+=============+
| ``3.0/MLForge/roles/create``    | ``POST``    |
+--------------------------------+-------------+

.. _MLForgeCreateRole:

Request Structure
-----------------

+-------------+------------+----------------------+
| Field Name  |    Type    |     Description      |
+=============+============+======================+
| name        | ``STRING`` | Role name.           |
+-------------+------------+----------------------+
| description | ``STRING`` | Role description.    |
+-------------+------------+----------------------+
| workspace   | ``STRING`` | Workspace the role   |
|             |            | belongs to.          |
+-------------+------------+----------------------+

.. _MLForgeCreateRoleResponse:

Response Structure
------------------

+------------+--------------------+----------------+
| Field Name |        Type        |  Description   |
+============+====================+================+
| role       | :ref:`MLForgeRole`  | A role object. |
+------------+--------------------+----------------+

===========================

.. _MLForgeAuthServiceGetRole:

Get Role
========

+-----------------------------+-------------+
|          Endpoint           | HTTP Method |
+=============================+=============+
| ``3.0/MLForge/roles/get``    | ``GET``     |
+-----------------------------+-------------+

.. _MLForgeGetRole:

Request Structure
-----------------

+------------+-------------+-------------+
| Field Name |    Type     | Description |
+============+=============+=============+
| role_id    | ``INTEGER`` | Role ID.    |
+------------+-------------+-------------+

.. _MLForgeGetRoleResponse:

Response Structure
------------------

+------------+--------------------+----------------+
| Field Name |        Type        |  Description   |
+============+====================+================+
| role       | :ref:`MLForgeRole`  | A role object. |
+------------+--------------------+----------------+

===========================

.. _MLForgeAuthServiceListRoles:

List Roles
==========

+-----------------------------+-------------+
|          Endpoint           | HTTP Method |
+=============================+=============+
| ``3.0/MLForge/roles/list``   | ``GET``     |
+-----------------------------+-------------+

.. _MLForgeListRolesResponse:

Response Structure
------------------

+------------+---------------------------+------------------+
| Field Name |           Type            |   Description    |
+============+===========================+==================+
| roles      | An array of               | A list of all    |
|            | :ref:`MLForgeRole`         | role objects.    |
+------------+---------------------------+------------------+

===========================

.. _MLForgeAuthServiceUpdateRole:

Update Role
===========

+------------------------------+-------------+
|           Endpoint           | HTTP Method |
+==============================+=============+
| ``3.0/MLForge/roles/update``  | ``PATCH``   |
+------------------------------+-------------+

.. _MLForgeUpdateRole:

Request Structure
-----------------

+-------------+-------------+----------------------+
| Field Name  |    Type     |     Description      |
+=============+=============+======================+
| role_id     | ``INTEGER`` | Role ID.             |
+-------------+-------------+----------------------+
| description | ``STRING``  | New role description.|
+-------------+-------------+----------------------+

.. _MLForgeUpdateRoleResponse:

Response Structure
------------------

+------------+--------------------+----------------+
| Field Name |        Type        |  Description   |
+============+====================+================+
| role       | :ref:`MLForgeRole`  | The updated    |
|            |                    | role object.   |
+------------+--------------------+----------------+

===========================

.. _MLForgeAuthServiceDeleteRole:

Delete Role
===========

+------------------------------+-------------+
|           Endpoint           | HTTP Method |
+==============================+=============+
| ``3.0/MLForge/roles/delete``  | ``DELETE``  |
+------------------------------+-------------+

.. _MLForgeDeleteRole:

Request Structure
-----------------

+------------+-------------+-------------+
| Field Name |    Type     | Description |
+============+=============+=============+
| role_id    | ``INTEGER`` | Role ID.    |
+------------+-------------+-------------+

===========================

.. _MLForgeAuthServiceAssignRole:

Assign Role
===========

+------------------------------+-------------+
|           Endpoint           | HTTP Method |
+==============================+=============+
| ``3.0/MLForge/roles/assign``  | ``POST``    |
+------------------------------+-------------+

.. _MLForgeAssignRole:

Request Structure
-----------------

+------------+-------------+-------------------+
| Field Name |    Type     |    Description    |
+============+=============+===================+
| username   | ``STRING``  | Username.         |
+------------+-------------+-------------------+
| role_id    | ``INTEGER`` | Role ID to assign.|
+------------+-------------+-------------------+
| workspace  | ``STRING``  | Workspace context.|
+------------+-------------+-------------------+

.. _MLForgeAssignRoleResponse:

Response Structure
------------------

+------------+-------------+--------------------------+
| Field Name |    Type     |       Description        |
+============+=============+==========================+
| assignment | ``OBJECT``  | The assignment object,   |
|            |             | containing id, role_id,  |
|            |             | and user_id.             |
+------------+-------------+--------------------------+

===========================

.. _MLForgeAuthServiceUnassignRole:

Unassign Role
=============

+--------------------------------+-------------+
|           Endpoint             | HTTP Method |
+================================+=============+
| ``3.0/MLForge/roles/unassign``  | ``DELETE``  |
+--------------------------------+-------------+

.. _MLForgeUnassignRole:

Request Structure
-----------------

+------------+-------------+--------------------+
| Field Name |    Type     |    Description     |
+============+=============+====================+
| username   | ``STRING``  | Username.          |
+------------+-------------+--------------------+
| role_id    | ``INTEGER`` | Role ID to         |
|            |             | unassign.          |
+------------+-------------+--------------------+

===========================

.. _MLForgeAuthServiceAddRolePermission:

Add Role Permission
===================

+------------------------------------------+-------------+
|                 Endpoint                 | HTTP Method |
+==========================================+=============+
| ``3.0/MLForge/roles/permissions/add``     | ``POST``    |
+------------------------------------------+-------------+

.. _MLForgeAddRolePermission:

Request Structure
-----------------

+------------------+-------------+---------------------------+
|    Field Name    |    Type     |        Description        |
+==================+=============+===========================+
| role_id          | ``INTEGER`` | Role ID.                  |
+------------------+-------------+---------------------------+
| resource_type    | ``STRING``  | Resource type             |
|                  |             | (``experiment`` or        |
|                  |             | ``registered_model``).    |
+------------------+-------------+---------------------------+
| resource_pattern | ``STRING``  | Resource pattern. Use     |
|                  |             | ``*`` to match all        |
|                  |             | resources of this type.   |
+------------------+-------------+---------------------------+
| permission       | ``STRING``  | Permission to add.        |
+------------------+-------------+---------------------------+

.. _MLForgeAddRolePermissionResponse:

Response Structure
------------------

+----------------+--------------------------+-------------------------+
|   Field Name   |          Type            |       Description       |
+================+==========================+=========================+
| role_permission| ``OBJECT``               | The created permission, |
|                |                          | containing id, role_id, |
|                |                          | resource_type,          |
|                |                          | resource_pattern, and   |
|                |                          | permission.             |
+----------------+--------------------------+-------------------------+

===========================

.. _MLForgeAuthServiceRemoveRolePermission:

Remove Role Permission
======================

+------------------------------------------+-------------+
|                 Endpoint                 | HTTP Method |
+==========================================+=============+
| ``3.0/MLForge/roles/permissions/remove``  | ``DELETE``  |
+------------------------------------------+-------------+

.. _MLForgeRemoveRolePermission:

Request Structure
-----------------

+---------------------+-------------+----------------------+
|     Field Name      |    Type     |     Description      |
+=====================+=============+======================+
| role_permission_id  | ``INTEGER`` | Role permission ID.  |
+---------------------+-------------+----------------------+

===========================

.. _MLForgeAuthServiceListRolePermissions:

List Role Permissions
=====================

+------------------------------------------+-------------+
|                 Endpoint                 | HTTP Method |
+==========================================+=============+
| ``3.0/MLForge/roles/permissions/list``    | ``GET``     |
+------------------------------------------+-------------+

.. _MLForgeListRolePermissions:

Request Structure
-----------------

+------------+-------------+-------------+
| Field Name |    Type     | Description |
+============+=============+=============+
| role_id    | ``INTEGER`` | Role ID.    |
+------------+-------------+-------------+

.. _MLForgeListRolePermissionsResponse:

Response Structure
------------------

+-------------------+-----------+----------------------------------+
|    Field Name     |   Type    |           Description            |
+===================+===========+==================================+
| role_permissions  | ``ARRAY`` | List of permissions for the      |
|                   |           | role across all resources.       |
+-------------------+-----------+----------------------------------+

===========================

.. _MLForgeAuthServiceUpdateRolePermission:

Update Role Permission
======================

+------------------------------------------+-------------+
|                 Endpoint                 | HTTP Method |
+==========================================+=============+
| ``3.0/MLForge/roles/permissions/update``  | ``PATCH``   |
+------------------------------------------+-------------+

.. _MLForgeUpdateRolePermission:

Request Structure
-----------------

+---------------------+-------------+---------------------+
|     Field Name      |    Type     |     Description     |
+=====================+=============+=====================+
| role_permission_id  | ``INTEGER`` | Role permission ID. |
+---------------------+-------------+---------------------+
| permission          | ``STRING``  | New permission.     |
+---------------------+-------------+---------------------+

.. _MLForgeUpdateRolePermissionResponse:

Response Structure
------------------

+-----------------+------------+-------------------------+
|   Field Name    |    Type    |       Description       |
+=================+============+=========================+
| role_permission | ``OBJECT`` | The updated permission, |
|                 |            | containing id, role_id, |
|                 |            | resource_type,          |
|                 |            | resource_pattern, and   |
|                 |            | permission.             |
+-----------------+------------+-------------------------+

===========================

.. _MLForgeAuthServiceListUserRoles:

List User Roles
===============

+----------------------------------+-------------+
|            Endpoint              | HTTP Method |
+==================================+=============+
| ``3.0/MLForge/users/roles/list``  | ``GET``     |
+----------------------------------+-------------+

.. _MLForgeListUserRoles:

Request Structure
-----------------

+------------+------------+-------------+
| Field Name |    Type    | Description |
+============+============+=============+
| username   | ``STRING`` | Username.   |
+------------+------------+-------------+

.. _MLForgeListUserRolesResponse:

Response Structure
------------------

+------------+---------------------------+----------------------+
| Field Name |           Type            |     Description      |
+============+===========================+======================+
| roles      | An array of               | List of roles        |
|            | :ref:`MLForgeRole`         | assigned to user.    |
+------------+---------------------------+----------------------+

===========================

.. _MLForgeAuthServiceListRoleUsers:

List Role Users
===============

+----------------------------------+-------------+
|            Endpoint              | HTTP Method |
+==================================+=============+
| ``3.0/MLForge/roles/users/list``  | ``GET``     |
+----------------------------------+-------------+

.. _MLForgeListRoleUsers:

Request Structure
-----------------

+------------+-------------+-------------+
| Field Name |    Type     | Description |
+============+=============+=============+
| role_id    | ``INTEGER`` | Role ID.    |
+------------+-------------+-------------+

.. _MLForgeListRoleUsersResponse:

Response Structure
------------------

+-------------+-----------+----------------------------------+
| Field Name  |   Type    |           Description            |
+=============+===========+==================================+
| assignments | ``ARRAY`` | List of role assignments,        |
|             |           | each containing id, role_id,     |
|             |           | and user_id.                     |
+-------------+-----------+----------------------------------+

===========================

.. _auth-rest-struct:

Data Structures
===============


.. _MLForgeUser:

User
----

+------------------------------+----------------------------------------------------+------------------------------------------------------------------+
|          Field Name          |                        Type                        |                            Description                           |
+==============================+====================================================+==================================================================+
| id                           | ``STRING``                                         | User ID.                                                         |
+------------------------------+----------------------------------------------------+------------------------------------------------------------------+
| username                     | ``STRING``                                         | Username.                                                        |
+------------------------------+----------------------------------------------------+------------------------------------------------------------------+
| is_admin                     | ``BOOLEAN``                                        | Whether the user is an admin.                                    |
+------------------------------+----------------------------------------------------+------------------------------------------------------------------+
| roles                        | An array of :ref:`MLForgeRole`                      | Roles assigned to the user.                                      |
+------------------------------+----------------------------------------------------+------------------------------------------------------------------+

.. note::
    The ``roles`` field is only included in the response from
    ``users/list``. It is not present when calling ``users/get``
    or ``users/current``. The ``users/current`` endpoint also
    includes an additional ``is_basic_auth`` boolean field.

.. _MLForgePermission:

Permission
----------

Permission level for a user on a resource.

+----------------+--------------------------------------+
|      Name      |             Description              |
+================+======================================+
| READ           | Can read.                            |
+----------------+--------------------------------------+
| EDIT           | Can read and update.                 |
+----------------+--------------------------------------+
| MANAGE         | Can read, update, delete and manage. |
+----------------+--------------------------------------+
| NO_PERMISSIONS | No permissions.                      |
+----------------+--------------------------------------+

.. _MLForgeRole:

Role
----

+-------------+-------------+---------------------------+
| Field Name  |    Type     |        Description        |
+=============+=============+===========================+
| id          | ``INTEGER`` | Role ID.                  |
+-------------+-------------+---------------------------+
| name        | ``STRING``  | Role name.                |
+-------------+-------------+---------------------------+
| description | ``STRING``  | Role description.         |
+-------------+-------------+---------------------------+
| workspace   | ``STRING``  | Workspace the role        |
|             |             | belongs to.               |
+-------------+-------------+---------------------------+
| permissions | ``ARRAY``   | List of permissions       |
|             |             | associated with the role. |
+-------------+-------------+---------------------------+
