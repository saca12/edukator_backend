## Offline App

### Purpose

The `offline` app tracks content synchronized for offline usage and exposes sync endpoints.

### Models

- **OfflineContent**
  - `id`: `UUIDField`.
  - `student`: `ForeignKey` → `accounts.Student`.
  - `content_type`: e.g. `Lesson` or `Exercise`.
  - `related_entity_id`: UUID of the related object.
  - `local_file_path`: path on the device.
  - `last_synced`: `DateTimeField`.
  - **Indexes**: `(student, content_type)` for filtering.

### Exposed API Endpoints

- **POST `/api/sync/download`**
  - **Auth**: required.
  - **Body**:
    - `content_type`
    - `related_entity_id`
    - `local_file_path`
  - **Response (201)**: created `OfflineContent` record.

- **POST `/api/sync/upload`**
  - **Auth**: required.
  - **Body**: free‑form payload (e.g. device progress data).
  - **Response (200)**: `{ "status": "uploaded" }`.

- **GET `/api/sync/status`**
  - **Auth**: required.
  - **Response (200)**:
    - `offline_items`: count of offline content rows for the student.

### Verification Example

```bash
curl -X POST http://localhost:8000/api/sync/download \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"content_type":"Lesson","related_entity_id":"<UUID>","local_file_path":"/path/to/file"}'
```

