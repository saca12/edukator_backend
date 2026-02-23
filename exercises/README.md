## Exercises App

### Purpose

The `exercises` app handles:

- Exercise metadata (difficulty, type).
- Exercises, questions and answers.
- User submissions with auto‑correction.
- Recommended exercises list.

### Models

- **Difficulty**
  - `id`: `UUIDField`.
  - `level_name`: human label (e.g. `Facile`).
  - `value`: `PositiveSmallIntegerField` used for ordering.

- **ExerciseType**
  - `id`: `UUIDField`.
  - `name`: enum `QCM | TEXT | TRUE_FALSE`.

- **Exercise**
  - `id`: `UUIDField`.
  - `title`, `instructions`.
  - `difficulty`: `ForeignKey` → `Difficulty`.
  - `type`: `ForeignKey` → `ExerciseType`.
  - `lesson`: optional `ForeignKey` → `education.Lesson`.

- **Question**
  - `id`: `UUIDField`.
  - `exercise`: `ForeignKey` → `Exercise`.
  - `question_text`: `TextField`.
  - `points`: `FloatField`.

- **Answer**
  - `id`: `UUIDField`.
  - `question`: `ForeignKey` → `Question`.
  - `choice_text`: `CharField`.
  - `is_correct_option`: `BooleanField`.
  - **Rule**: for QCM, exactly one answer per question has `is_correct_option=True`.

- **UserAnswer**
  - `id`: `UUIDField`.
  - `student`: `ForeignKey` → `accounts.Student`.
  - `question`: `ForeignKey` → `Question`.
  - `answer`: optional `ForeignKey` → `Answer` for choice‑based types.
  - `response_text`: `TextField` for TEXT exercises.
  - `is_correct_submission`: `BooleanField`.
  - `submission_date`: `DateTimeField`.
  - **Indexes**: `(student, submission_date)` for history queries.

### Exposed API Endpoints

- **GET `/api/exercises`**
  - **Auth**: required.
  - **Response (200)**: list of exercises with difficulty, type and nested questions/answers.

- **GET `/api/exercises/{id}`**
  - **Auth**: required.
  - **Response (200)**: exercise detail.

- **POST `/api/exercises/{id}/submit`**
  - **Auth**: required.
  - **Body**:
    - `answers`: array of:
      - `question_id` (UUID)
      - `answer_id` (UUID, optional for TEXT)
      - `response_text` (for TEXT)
  - **Response (201)**: list of created `UserAnswer` objects.

- **GET `/api/exercises/{id}/correction`**
  - **Auth**: required.
  - **Response (200)**:
    - `exercise_id`
    - `earned_points`
    - `total_points`
    - `percentage`

- **GET `/api/exercises/recommended`**
  - **Auth**: required.
  - **Response (200)**: list of recommended exercises (mock: latest ordered by difficulty).

### Business Rules

- Auto‑correction is performed in `exercises.services.auto_correct_answer`:
  - QCM/TRUE_FALSE: correctness comes from `Answer.is_correct_option`.
  - TEXT: correctness is simulated by non‑empty `response_text`.
- `submit_answers` persists submissions, auto‑corrects and returns `UserAnswer` objects.

### Verification Example

```bash
curl http://localhost:8000/api/exercises \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

curl -X POST http://localhost:8000/api/exercises/<EX_ID>/submit \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"answers":[{"question_id":"<Q_ID>","answer_id":"<A_ID>"}]}'
```

