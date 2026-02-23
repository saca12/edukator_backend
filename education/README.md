## Education App

### Purpose

The `education` app models the **pedagogical structure**:

- Grades and levels (primary/secondary).
- Subjects per grade.
- Chapters within subjects.
- Lessons and their rich content.

### Models

- **Grade**
  - `id`: `UUIDField`, primary key.
  - `name`: display name (e.g. `CM2`).
  - `level`: enum `PRIMARY | SECONDARY`, indexed.

- **Subject**
  - `id`: `UUIDField`.
  - `name`: subject name.
  - `icon_url`: optional icon.
  - `grade`: `ForeignKey` → `Grade`.
  - **Constraints**: unique per `(name, grade)`.

- **Chapter**
  - `id`: `UUIDField`.
  - `title`: chapter title.
  - `order_index`: numeric order.
  - `subject`: `ForeignKey` → `Subject`.
  - **Constraints**: unique `(subject, order_index)` to preserve ordering.

- **Lesson**
  - `id`: `UUIDField`.
  - `title`, `order_index`.
  - `is_completed`: boolean flag (global, used for content readiness).
  - `chapter`: `ForeignKey` → `Chapter`.

- **LessonContent**
  - `id`: `UUIDField`.
  - `lesson`: `OneToOneField` → `Lesson`.
  - `rich_text_content`: main narrative content.
  - `illustrations_url`, `audio_url`: optional media URLs.

### Exposed API Endpoints

- **GET `/api/subjects`**
  - **Auth**: required.
  - **Response (200)**: list of subjects with grade details.

- **GET `/api/subjects/{id}`**
  - **Auth**: required.
  - **Response (200)**: subject detail.

- **GET `/api/subjects/{id}/chapters`**
  - **Auth**: required.
  - **Response (200)**: list of chapters for a subject.

- **GET `/api/lessons`**
  - **Auth**: required.
  - **Response (200)**: list of lessons with chapter/subject info.

- **GET `/api/lessons/{id}`**
  - **Auth**: required.
  - **Response (200)**: lesson detail and content.

- **GET `/api/lessons/{id}/related`**
  - **Auth**: required.
  - **Response (200)**: lessons in the same chapter excluding the current one.

- **POST `/api/lessons/{id}/complete`**
  - **Auth**: required.
  - **Body**: empty.
  - **Response (200)**:
    - `lesson_id`
    - `completion_percentage`
    - `average_score`

### Business Rules

- `LessonContent` is 1‑to‑1 with `Lesson`.
- Marking a lesson as completed also updates the `Progress` entry via `progress.update_lesson_progress`.
- Relations are navigable from `Student` → `Grade` → `Subject` → `Chapter` → `Lesson`.

### Verification Example

```bash
curl http://localhost:8000/api/subjects \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

curl http://localhost:8000/api/lessons \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

