## Progress App

### Purpose

The `progress` app tracks learner performance and exposes dashboards:

- Per‑lesson progress.
- Aggregated progress per subject.
- Lessons needing revision.

### Models

- **Progress**
  - `id`: `UUIDField`.
  - `student`: `ForeignKey` → `accounts.Student`.
  - `lesson`: `ForeignKey` → `education.Lesson`.
  - `completion_percentage`: `FloatField` (0–100).
  - `average_score`: `FloatField`.
  - `last_activity`: `DateTimeField`.
  - **Unique constraint**: `(student, lesson)`.
  - **Indexes**: `(student, last_activity)`.

### Exposed API Endpoints

- **GET `/api/progress/dashboard`**
  - **Auth**: required.
  - **Response (200)**:
    - `overview`: `{ total_lessons_tracked, average_completion }`
    - `by_subject`: list of `{ subject_id, subject_name, lessons_count, avg_completion }`.

- **GET `/api/progress/by-subject`**
  - **Auth**: required.
  - **Response (200)**: same `by_subject` slice as above.

- **GET `/api/revision/needed`**
  - **Auth**: required.
  - **Response (200)**: list of `Progress` entries for lessons needing revision (completion < 80%).

### Business Rules

- `update_lesson_progress` ensures a unique `Progress` row per `(student, lesson)`.
- Dashboard aggregation is done in the service layer, not in the views.

### Verification Example

```bash
curl http://localhost:8000/api/progress/dashboard \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

