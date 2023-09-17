## Environment Variables

Medusa uses environment variables for configuration and customization. Below is a list of important environment variables you can set to tailor your application to your specific needs.

## Application Configuration

- **`APP_NAME`**: The name of your Medusa application.

- **`APP_ENV`**: The environment in which your application is running. 
    - Options: `dev`, `production`.

- **`APP_DATABASE`**: Set to `True` to enable the Database component of Medusa. Set to `False` to disable it.

- **`APP_SERVER`**: Set to `True` to enable the Server component of Medusa. Set to `False` to disable it.


## Database Configuration

These environment variables are used if `APP_DATABASE` is `True`

- **`DATABASE_HOST`**: The host or IP address of your database server. Default is `localhost`.

- **`DATABASE_NAME`**: The name of the database Medusa should connect to. Default is `medusa`.

- **`DATABASE_USER`**: The username used to authenticate with the database.

- **`DATABASE_PASSWORD`**: The password for the database user. Ensure to keep this secure.

- **`DATABASE_PORT`**: The port number used for database connections. Default is `5432` for PostgreSQL.

- **`DATABASE_TYPE`** (required): The type of database to use. 
    - Options: `sqlite`, `mysql`, `postgresql`, `oracle`, `mssql+pymssql`, `firebird`, `memory`.

- **`DATABASE_PATH`**: For SQLite databases, specify the path to the database file. Default is `storage`.

## Logging Configuration

- **`LOG_LEVEL`**: The log level for Medusa's internal logging. 
    - Options: `debug`, `info`, `warning`, `error`.

- **`LOG_PATH`**: The directory where log files should be stored.



## Sample
```ini
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
```