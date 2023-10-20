=====================
Environment Variables
=====================

Medusa uses environment variables for configuration and customization. Below is a list of important environment variables you can set to tailor your application to your specific needs.

Application
-----------
- ``APP_NAME`` (str): The name of your application.
- ``APP_ENV`` (str): The environment in which your application is running.
  
  Options:
    - ``dev``
    - ``production``

- ``APP_DATABASE`` (bool): Set to `True` to enable the Database component of Medusa. Set to `False` to disable it.
- ``APP_SERVER`` (bool): Set to `True` to enable the Server component of Medusa. Set to `False` to disable it.
- ``APP_MASK`` (bool): Set to `True` to enable redacting sensitive data from logs.

Database
--------
These environment variables are used if ``APP_DATABASE`` is `True`.

- ``DATABASE_HOST`` (str): The host or IP address of your database server. Default is `localhost`.
- ``DATABASE_NAME`` (str): The name of the database Medusa should connect to. Default is `medusa`.
- ``DATABASE_USER`` (str): The username used to authenticate with the database.
- ``DATABASE_PASSWORD`` (str): The password for the database user. Ensure to keep this secure.
- ``DATABASE_PORT`` (int): The port number used for database connections. Default is `5432` for PostgreSQL.
- ``DATABASE_TYPE`` (str, required): The type of database to use.
  
  Options:
    - ``sqlite``
    - ``mysql``
    - ``postgresql``
    - ``oracle``
    - ``mssql+pymssql``
    - ``firebird``
    - ``memory``
  
- ``DATABASE_PATH`` (str): For SQLite databases, specify the path to the database file. Default is `storage`.

Logging
-------
- ``LOG_LEVEL`` (str): The log level for internal logging.
  
  Options:
    - ``debug``
    - ``info``
    - ``warning``
    - ``error``
  
- ``LOG_PATH``: The directory where log files should be stored.

Example
-------
.. code-block:: ini

    DATABASE_HOST=localhost
    DATABASE_NAME=medusa
    DATABASE_USER=user
    DATABASE_PASSWORD=password123
    DATABASE_PORT=5432
    DATABASE_TYPE=sqlite
    DATABASE_PATH=storage

    LOG_LEVEL=debug
    LOG_PATH=logs

    APP_NAME=Medusa
    APP_ENV=dev
    APP_DATABASE=True
    APP_SERVER=True
