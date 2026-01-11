# How to Connect to the Correct Database in pgAdmin

You are likely looking at a different database instance. The application is running inside a **Docker Container** on port `5432` with the database name **`postgres`**.

## Steps to Fix

1.  Open **pgAdmin**.
2.  Right-click on **Servers** > **Register** > **Server...**
3.  **General Tab**:
    *   **Name**: `Docker Local DB` (or any name you prefer)
4.  **Connection Tab**:
    *   **Host name/address**: `127.0.0.1` (or `localhost`)
    *   **Port**: `5432`
    *   **Maintenance database**: `postgres`
    *   **Username**: `postgres`
    *   **Password**: `password`
5.  Click **Save**.

## Verification
1.  Expand the new server (`Docker Local DB`).
2.  Expand **Databases** > **`postgres`** > **Schemas** > **public** > **Tables**.
3.  Right-click on **`users`** > **View/Edit Data** > **All Rows**.
4.  You should now see the 7 users that were listed in the terminal.

### Note
If you see a database named `lpr_db`, ignore it. The system is currently using the default `postgres` database container.
