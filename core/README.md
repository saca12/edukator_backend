## Core App

### Purpose

The `core` app groups shared infrastructure pieces:

- Base models and mixins.
- Shared permission classes.

### Models

- **TimeStampedModel**
  - Abstract model providing:
    - `created_at`
    - `updated_at`
  - Used across most domain models for consistent auditing.

### Permissions

- **IsAuthenticatedOrCreate**
  - Allows unauthenticated `POST` requests (used for registration).
  - Requires authentication for all other methods.

- **IsOwnerOrReadOnly**
  - Object‑level permission: owner can modify, others have read‑only access.
  - Works with objects exposing `user` or `student.user`.

### Endpoints

The `core` app does not expose its own endpoints; it is consumed by other apps.

