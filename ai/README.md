## AI App

### Purpose

The `ai` app provides **mock GPT‑style services**:

- Error analysis for wrong answers.
- Concept explanations.
- Hints.
- Mock exercise generation.

### Models

- **ErrorAnalysis**
  - `id`: `UUIDField`.
  - `user_answer`: `OneToOneField` → `exercises.UserAnswer`.
  - `ai_explanation`: textual explanation.
  - `helpful_hint`: actionable hint.
  - `generated_at`: `DateTimeField`.

### Exposed API Endpoints

- **POST `/api/ai/explain`**
  - **Auth**: required.
  - **Body**:
    - `question_text`
    - `student_answer`
  - **Response (200)**: structured explanation with steps.

- **POST `/api/ai/analyze-error`**
  - **Auth**: required.
  - **Body**:
    - `user_answer_id` (UUID)
  - **Response (201)**: `ErrorAnalysis` object for the given answer.

- **POST `/api/ai/generate-exercise`**
  - **Auth**: required.
  - **Body**:
    - `subject`
    - `grade_level`
    - `difficulty`
  - **Response (201)**: mock exercise description (no DB persistence).

- **POST `/api/ai/hint`**
  - **Auth**: required.
  - **Body**:
    - `question_text`
    - `current_progress` (optional, float)
  - **Response (200)**: context‑aware hint.

### Business Rules

- All AI responses are **mocked** – no external APIs are called.
- Error analyses are stored in DB for traceability.

### Verification Example

```bash
curl -X POST http://localhost:8000/api/ai/explain \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"question_text":"2+2 = ?","student_answer":"5"}'
```

