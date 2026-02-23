## Notifications App

### Purpose

The `notifications` app provides:

- Gamification achievements.
- A simple notification center.

### Models

- **Achievement**
  - `id`: `UUIDField`.
  - `student`: `ForeignKey` → `accounts.Student`.
  - `badge_name`: badge label.
  - `icon_url`: optional icon.
  - `date_earned`: `DateTimeField`.

- **Notification**
  - `id`: `UUIDField`.
  - `student`: `ForeignKey` → `accounts.Student`.
  - `message`: notification body.
  - `is_read`: `BooleanField`.
  - `created_at`: `DateTimeField`.

### Exposed API Endpoints

- **GET `/api/sync/status`**
  - **Auth**: required.
  - **Response (200)**:
    - `unread_notifications`: integer count of unread notifications for the student.

Additional helper endpoints exist (not strictly required by the spec) for listing notifications and achievements but can be wired later if needed.

### Verification Example

```bash
curl http://localhost:8000/api/sync/status \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

