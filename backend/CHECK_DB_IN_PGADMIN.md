# Database Connection Details for pgAdmin

It seems like there was a confusion between `lpr_db` and `postgres`. Based on your Docker configuration and running scripts, your application is using the default **`postgres`** database.

Please use these exact settings in pgAdmin:

## Connection Settings

- **Name**: Local Docker DB (or any name you like)
- **Host name/address**: `127.0.0.1` (or `localhost`)
- **Port**: `5432`
- **Maintenance database**: `postgres`
- **Username**: `postgres`
- **Password**: `password`

## Validating Data

1. Expand **Servers** -> **[Your Server Name]** -> **Databases**.
2. Click on **`postgres`** (This is where your tables are!).
   - *Note: If you see `lpr_db`, it might be empty or unused.*
3. Go to **Schemas** -> **public** -> **Tables**.
4. You should see:
   - `users`
   - `complaints`
5. Right-click `users` -> **View/Edit Data** -> **All Rows** to confirm your registration.

## Why was there a mismatch?
Some previous configuration scripts attempted to use `lpr_db`, but the Docker container was initialized with the default `postgres` name. The backend has been automatically falling back to `postgres` to ensure it works, which is why your login/registration is successful.
