# How to Use Authentication in Swagger UI

## Step-by-Step Guide

### 1. Register a New User (Optional - if you don't have an account)

1. Go to the `/api/auth/register` endpoint in Swagger UI
2. Click "Try it out"
3. Enter your details:
   ```json
   {
     "email": "your-email@example.com",
     "name": "Your Name",
     "password": "your-password"
   }
   ```
4. Click "Execute"
5. You should get a response with your user details

### 2. Login to Get Your JWT Token

1. Go to the `/api/auth/login` endpoint in Swagger UI
2. Click "Try it out"
3. Enter your credentials:
   ```json
   {
     "email": "your-email@example.com",
     "password": "your-password"
   }
   ```
4. Click "Execute"
5. Copy the `access_token` from the response. It will look like:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type": "bearer"
   }
   ```

### 3. Authorize in Swagger UI

1. Click the **"Authorize"** button (🔒 icon) at the top right of the Swagger UI page
2. In the authorization dialog, you'll see a "Bearer" section
3. Paste your `access_token` (the JWT token you got from login) into the "Value" field
4. Click **"Authorize"**
5. Click **"Close"**

### 4. Use Protected Endpoints

Now you can use any protected endpoint (like `/api/companies`, `/api/financial-snapshots`, etc.) without getting 401 errors.

## Important Notes

- **You don't need**: username, password, client_id, or client_secret in the Authorize dialog
- **You only need**: The JWT `access_token` from the login endpoint
- **Token expires**: After 30 minutes (configurable in `src/database.py`)
- **To refresh**: Just login again to get a new token

## Troubleshooting

- **401 Unauthorized**: Make sure you've copied the entire token (it's a long string)
- **Token expired**: Login again to get a new token
- **Can't see Authorize button**: Make sure you're on the Swagger UI page (`/docs`)

