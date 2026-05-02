# e-Citizen Mobile API Guide

## Base URL

```
https://ecitizen.go.ke/api/v1/
```

For development: `http://127.0.0.1:9000/api/v1/`

## Authentication

e-Citizen uses JWT (JSON Web Tokens) for mobile authentication. Tokens expire after 60 minutes (access) and 24 hours (refresh).

### Register (Create Account)

```
POST /api/v1/auth/register/
Content-Type: application/json

{
    "username": "janedoe",
    "email": "jane@example.com",
    "first_name": "Jane",
    "last_name": "Wanjiku",
    "password": "securepassword123",
    "id_number": "12345678",
    "phone": "0712345678",
    "county": 1
}
```

Response (201):
```json
{
    "access": "eyJ...",
    "refresh": "eyJ...",
    "user": { "id": 1, "username": "janedoe", "email": "jane@example.com", ... },
    "profile": { "id": "...", "id_number": "12345678", "phone": "0712345678", ... }
}
```

### Login

```
POST /api/v1/auth/login/
Content-Type: application/json

{
    "username": "janedoe",
    "password": "securepassword123"
}
```

Response (200):
```json
{
    "access": "eyJ...",
    "refresh": "eyJ...",
    "user": { ... }
}
```

### Refresh Token

```
POST /api/v1/token/refresh/
Content-Type: application/json

{
    "refresh": "eyJ..."
}
```

Response (200):
```json
{
    "access": "eyJ..."
}
```

### Authenticated Requests

Include the access token in the Authorization header:
```
Authorization: Bearer eyJ...
```

## Core Endpoints

### Profile

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/auth/profiles/` | List profiles (staff) or own profile |
| GET | `/api/v1/auth/profiles/{id}/` | Profile detail |
| PUT | `/api/v1/auth/profiles/{id}/` | Update profile |
| POST | `/api/v1/auth/profiles/upload_avatar/` | Upload profile photo (multipart) |

### Wallet

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/payments/wallet/` | Get wallet details + recent transactions |
| POST | `/api/v1/payments/wallet/top_up/` | Top up wallet (`{"amount": 1000, "method": "M-Pesa"}`) |

### Bank Accounts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/payments/bank-accounts/` | List linked bank accounts |
| POST | `/api/v1/payments/bank-accounts/` | Link a bank account |

### Payments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/payments/transactions/` | List payment transactions |
| POST | `/api/v1/payments/transactions/` | Create payment transaction |

### Notifications

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/notifications/notifications/` | List notifications |
| POST | `/api/v1/notifications/notifications/mark_all_read/` | Mark all read |

### Push Notification Tokens

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/notifications/device-tokens/` | List registered device tokens |
| POST | `/api/v1/notifications/device-tokens/` | Register device for push (`{"platform": "ios", "token": "fcm-token..."}`) |

### Counties

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/counties/` | All 47 counties with sub-counties, wards |
| GET | `/api/v1/counties/sub-counties/?county=001` | Sub-counties filtered by county code |
| GET | `/api/v1/counties/wards/?sub_county=1` | Wards filtered by sub-county ID |

### Services

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/services/` | Browse service catalog |
| GET | `/api/v1/services/{id}/` | Service detail |

### Applications

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/applications/` | List user's applications |
| POST | `/api/v1/applications/` | Submit new application |

## Pagination

All list endpoints use cursor-based pagination. Response format:
```json
{
    "next": "http://...?cursor=...",
    "previous": null,
    "results": [ ... ]
}
```

## API Documentation

Full OpenAPI 3 docs available at:
- Swagger UI: `/api/v1/docs/`
- ReDoc: `/api/v1/redoc/`

## Error Responses

All errors follow this format:
```json
{
    "detail": "Error message here"
}
```

Validation errors:
```json
{
    "field_name": ["Error message 1", "Error message 2"]
}
```
