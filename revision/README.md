## Revision App

### Purpose

The `revision` app manages **revision sessions** that group lessons requiring additional work.

### Models

- **RevisionSession**
  - `id`: `UUIDField`.
  - `student`: `ForeignKey` → `accounts.Student`.
  - `created_at`: `DateTimeField`.
  - `is_completed`: `BooleanField`.

### Exposed API Endpoints

- **POST `/api/revision/session`**
  - **Auth**: required.
  - **Body**: empty.
  - **Response (201)**:
    - `session`: serialized session.
    - `lessons`: list of `{ id, title }` for lessons needing revision (delegated to `progress` app).

### Business Rules

- A revision session snapshot is created from the current `Progress` state.
- Currently sessions are light‑weight: they are recorded with a timestamp and completion flag.

### Verification Example

```bash
curl -X POST http://localhost:8000/api/revision/session \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

