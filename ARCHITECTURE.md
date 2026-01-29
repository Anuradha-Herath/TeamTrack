# TeamTrack – Architecture Design Document

**Project:** Project & Task Management System (Jira-lite)  
**Purpose:** Production-grade architecture reference (frozen for the whole project)  
**No code in this document — structure and design only.**

---

## 1️⃣ BACKEND (DJANGO)

### 1.1 Recommended Django Project Structure

```
backend/
├── config/                    # Project configuration (formerly "project name")
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py            # Shared settings
│   │   ├── development.py     # Dev overrides
│   │   └── production.py      # Prod overrides
│   ├── urls.py                # Root URLconf
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── users/
│   ├── projects/
│   ├── tasks/
│   └── dashboard/
├── core/                      # Shared cross-app utilities
│   ├── __init__.py
│   ├── exceptions.py          # Custom exception classes
│   ├── middleware.py          # Custom middleware (e.g. request ID, logging)
│   ├── pagination.py          # Default pagination classes
│   └── permissions.py         # Base permission classes (if shared)
├── manage.py
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
└── .env.example
```

**Why this structure:**  
- `config/` holds all Django settings; splitting by environment keeps secrets and dev-only options out of production.  
- `apps/` groups domain apps; each app is self-contained (models, serializers, services, permissions, views).  
- `core/` holds shared code (exceptions, middleware, base pagination) so apps stay DRY and consistent.

---

### 1.2 App Structure (per app)

Each domain app under `apps/` follows the same layout:

```
apps/<app_name>/
├── __init__.py
├── admin.py
├── apps.py
├── models/
│   ├── __init__.py            # Exports all models for imports
│   └── <model_name>.py        # One file per model (optional; can use models.py)
├── serializers/
│   ├── __init__.py
│   └── <entity>_serializer.py # One or more serializer files
├── services/
│   ├── __init__.py
│   └── <entity>_service.py    # Business logic only
├── permissions/
│   ├── __init__.py
│   └── <entity>_permissions.py
├── views/
│   ├── __init__.py
│   └── <entity>_views.py      # Request/response handling only
├── urls.py
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_services.py
    └── test_views.py
```

**App roles:**

| App        | Responsibility |
|-----------|----------------|
| **users** | User model (or extend AbstractUser), profile, auth-related logic (register, password reset). No JWT issuance here—that stays in a dedicated auth app or in users with a clear “auth” sub-namespace. |
| **projects** | Project CRUD, project membership (who is in which project with which role). |
| **tasks** | Task CRUD, status/priority/due date/assignee, comments (if present), link to project. |
| **dashboard** | Read-only aggregations: counts, progress per project, etc. No business rules; uses services from projects/tasks. |

**Alternative:** If you prefer a single `models.py` per app instead of `models/` folder, keep one `models.py` and the same structure for serializers, services, permissions, and views.

---

### 1.3 Where to Put What

| Concern | Location | Notes |
|--------|----------|--------|
| **JWT auth** | Dedicated app, e.g. `apps/users/` with an `auth` submodule, or `apps/authentication/`. | Token issuance (access + refresh), blacklisting (if used), and JWT validation. Use one place for all JWT logic so middleware and views only “consume” tokens. |
| **Role-based access control** | `core/permissions.py` for base classes; `apps/<app>/permissions/` for app-specific rules. | Base: “is authenticated”, “is admin”. App-level: “is project member”, “is project admin”, “can edit task”. Permissions receive request + object (for object-level checks). |
| **Logging** | `config/settings/base.py` for log level and handlers; `core/middleware.py` or a logging utility for request/response or audit logs. | Structure logs (e.g. request_id, user_id, view name). Do not log secrets or full tokens. |
| **Error handling** | `core/exceptions.py` for custom exception classes; a custom exception handler in DRF (in settings) to map exceptions to HTTP responses; optional middleware for uncaught errors. | Views and services raise domain exceptions; the handler returns consistent JSON and status codes. |
| **Filtering, search, pagination** | **Pagination:** `core/pagination.py` (default page size, max size). **Filtering/search:** either in `apps/<app>/views/` using DRF filter backends and a small `filters.py` per app, or in `apps/<app>/services/` if filters are complex. | Keep view layer thin: views pass query params to services or filter backends; business rules (e.g. “only tasks in projects I belong to”) live in services or querysets. |

---

## 2️⃣ FRONTEND (REACT + VITE)

### 2.1 Complete Folder Structure

```
frontend/
├── public/
├── src/
│   ├── api/
│   │   ├── client.js          # Axios instance (base URL, interceptors)
│   │   ├── auth.js
│   │   ├── users.js
│   │   ├── projects.js
│   │   ├── tasks.js
│   │   └── dashboard.js
│   ├── components/
│   │   ├── common/            # Buttons, inputs, cards, modals, table
│   │   ├── layout/            # Sidebar, Navbar, MainLayout
│   │   └── features/          # TaskCard, ProjectCard, CommentList, etc.
│   ├── pages/
│   │   ├── auth/
│   │   │   ├── Login.jsx
│   │   │   └── Register.jsx
│   │   ├── dashboard/
│   │   │   └── Dashboard.jsx
│   │   ├── projects/
│   │   │   ├── ProjectList.jsx
│   │   │   ├── ProjectDetail.jsx
│   │   │   └── ProjectForm.jsx
│   │   ├── tasks/
│   │   │   ├── TaskList.jsx
│   │   │   ├── TaskDetail.jsx
│   │   │   └── TaskForm.jsx
│   │   └── NotFound.jsx
│   ├── layouts/
│   │   ├── AuthLayout.jsx     # Centered card, no sidebar
│   │   ├── DashboardLayout.jsx # Sidebar + Navbar + outlet
│   │   └── PublicLayout.jsx   # Optional; marketing/landing
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useProjects.js
│   │   ├── useTasks.js
│   │   └── usePagination.js
│   ├── utils/
│   │   ├── constants.js       # Status, priority enums; route paths
│   │   ├── formatters.js      # Dates, numbers
│   │   └── storage.js        # Token get/set/remove; key names
│   ├── store/                 # If using global state (e.g. Zustand/Redux)
│   │   ├── authStore.js
│   │   └── index.js
│   ├── routes/
│   │   ├── index.jsx          # Router setup + route list
│   │   └── ProtectedRoute.jsx
│   ├── App.jsx
│   └── main.jsx
├── index.html
├── vite.config.js
├── tailwind.config.js         # or MUI theme
└── .env.example
```

**Conventions:**  
- `api/`: only HTTP calls; no UI.  
- `components/`: reusable UI; they receive data and callbacks as props (or use hooks that call `api/`).  
- `pages/`: composition of components + route-level data fetching (or hooks).  
- `store/`: only if you need global auth or cross-page state; otherwise keep state in pages/hooks.

---

### 2.2 Layout System

- **AuthLayout:** Full-screen, centered card (login/register). No sidebar or navbar.  
- **DashboardLayout:**  
  - **Sidebar:** Logo, nav links (Dashboard, Projects, etc.), user block, logout.  
  - **Navbar:** Top bar (breadcrumb, user menu, notifications placeholder).  
  - **Main content:** Outlet for current page (e.g. dashboard, project list, task list).  
- **Main content area:** Scrollable; sidebar and navbar stay fixed (or collapse on small screens).

Routing: auth routes use `AuthLayout`; all authenticated app routes use `DashboardLayout`.

---

### 2.3 Routing Structure

- **Public (no auth):** `/login`, `/register` → `AuthLayout`.  
- **Protected (auth required):** `/`, `/dashboard`, `/projects`, `/projects/:id`, `/projects/:id/tasks`, `/projects/:id/tasks/:taskId` → `DashboardLayout` + `ProtectedRoute`.  
- **Role-based:** Same routes; visibility of menu items or actions (e.g. “Delete project”) is controlled by role (Admin vs Team Member) in the UI; backend enforces via permissions.  
- **Fallback:** `/404` or catch-all → `NotFound.jsx`.

Route definitions live in `routes/index.jsx`; `ProtectedRoute` checks token (and optionally role) and redirects to `/login` if unauthenticated.

---

### 2.4 Auth Flow (Frontend)

- **Login/Register:** Pages call `api/auth.js`; on success, store access (and optionally refresh) token in memory or `localStorage`/cookie; redirect to `/dashboard` or `/`.  
- **Protected routes:** `ProtectedRoute` (or equivalent) runs before rendering; if no valid token, redirect to `/login`.  
- **Role-based pages:** No separate route tree for roles; same URLs. Admin-only sections (e.g. “Users”, “Settings”) are hidden or disabled for non-admins; backend returns 403 for unauthorized actions.  
- **Token refresh:** If using refresh tokens, an Axios response interceptor catches 401, calls refresh endpoint, retries request; on refresh failure, clear storage and redirect to login.  
- **Logout:** Clear tokens and auth state; redirect to `/login`.

---

## 3️⃣ DATABASE DESIGN

### 3.1 Entities

| Entity | Purpose |
|--------|--------|
| **User** | Identity and auth (extends Django AbstractUser). Fields: email (or username), password, role (Admin / Team Member), name, avatar (optional), timestamps. |
| **Project** | A project container. Fields: name, description, status (e.g. Active/Archived), created_by (FK User), timestamps. |
| **ProjectMember** | Many-to-many between User and Project with role. Fields: user (FK), project (FK), role (e.g. Admin/Member), joined_at. Unique on (user, project). |
| **Task** | Work item under a project. Fields: project (FK), title, description, status (Todo/In Progress/Done), priority, due_date, assigned_to (FK User, nullable), created_by (FK User), timestamps. |
| **Comment** (optional) | Task comments. Fields: task (FK), author (FK User), body, timestamps. |
| **ActivityLog** (optional) | Audit trail. Fields: user (FK, nullable), action (e.g. task_created), target_type (e.g. task), target_id, project (FK, nullable), metadata (JSON), created_at. |

---

### 3.2 Relationships

- **User ↔ Project:** Many-to-many via **ProjectMember** (user can be in many projects; project has many members).  
- **Project → Task:** One-to-many (project has many tasks; task belongs to one project).  
- **Task → User:** Many-to-one for `assigned_to` and `created_by`.  
- **Comment → Task, User:** Many-to-one (task has many comments; each comment has one author).  
- **ActivityLog → User, Project:** Optional FKs for “who” and “in which project”.

Cascade: Deleting a project should cascade or restrict to tasks (and comments) per product rules; deleting a user may set `assigned_to`/`created_by` to null or restrict depending on policy.

---

### 3.3 Important Fields

- **User.role:** Admin vs Team Member; used for global permissions.  
- **ProjectMember.role:** Project-level role (e.g. Project Admin vs Member) for scoped permissions.  
- **Task.status:** Todo / In Progress / Done (filtering, dashboard).  
- **Task.priority:** For ordering and filtering.  
- **Task.due_date:** For filters and overdue indicators.  
- **Timestamps:** `created_at`, `updated_at` on main entities for ordering and auditing.

---

### 3.4 Indexes and Constraints

- **Unique:** (User, Project) on ProjectMember; unique constraints on auth identifier (e.g. email).  
- **Indexes:**  
  - Task: `project_id`, `status`, `assigned_to_id`, `due_date` (for list/filter performance).  
  - ProjectMember: `user_id`, `project_id`.  
  - ActivityLog: `created_at`, `project_id`, `user_id` if queried often.  
- **Foreign keys:** All FKs with appropriate ON DELETE behavior (e.g. SET_NULL for assignee, CASCADE for task → project if business rule is “delete project deletes tasks”).

---

## 4️⃣ AUTHENTICATION & AUTHORIZATION FLOW

### 4.1 Login

- Client sends credentials (e.g. email + password) to `/api/auth/login/`.  
- Backend validates, returns access token (short-lived) and refresh token (longer-lived).  
- Frontend stores tokens and user payload; uses access token in `Authorization` header for subsequent requests.

### 4.2 Register

- Client sends email, password, name (and optionally role if allowed).  
- Backend creates user (default role Team Member unless overridden); may return tokens or require login.  
- Frontend either logs in automatically or redirects to login.

### 4.3 JWT Access Token

- Short-lived (e.g. 15–60 minutes).  
- Contains: user id, role, and any needed claims.  
- Used in `Authorization: Bearer <token>` for every API request.  
- Validated by backend middleware/DRF auth class; invalid/expired → 401.

### 4.4 Refresh Token

- Long-lived (e.g. days), stored securely (httpOnly cookie or secure storage).  
- Endpoint: e.g. `POST /api/auth/refresh/` with refresh token in body or cookie.  
- Returns new access (and optionally new refresh) token.  
- Optional: refresh token rotation or blacklisting on logout.

### 4.5 Role-Based Permissions

- **Admin (global):** Can manage users, all projects, and system-wide settings.  
- **Team Member:** Can access only projects they are in; create/edit tasks according to project role.  
- **Project-level:** ProjectMember.role (e.g. Project Admin) can manage members and project settings; Member can manage tasks only.  
- Backend: every mutation and sensitive read checks permission (project membership + role); returns 403 when not allowed.

### 4.6 Frontend–Backend Interaction

- Frontend sends access token in header; backend validates JWT and loads user.  
- On 401: frontend tries refresh; on success retries; on failure redirects to login.  
- On 403: frontend shows “not allowed” and does not retry with same token.  
- Login/register and token refresh are the only endpoints that do not require a Bearer token.

---

## 5️⃣ API DESIGN

### 5.1 REST Endpoint Structure (by module)

**Auth**  
- `POST /api/auth/register/` — register.  
- `POST /api/auth/login/` — login (returns access + refresh).  
- `POST /api/auth/refresh/` — refresh access token.  
- `POST /api/auth/logout/` — optional; invalidate refresh token if blacklist used.

**Users**  
- `GET /api/users/me/` — current user profile.  
- `PATCH /api/users/me/` — update profile.  
- Admin-only: `GET /api/users/`, `GET /api/users/:id/`, `PATCH /api/users/:id/` (and optionally role management).

**Projects**  
- `GET /api/projects/` — list (filtered by membership for non-admin).  
- `POST /api/projects/` — create.  
- `GET /api/projects/:id/` — detail.  
- `PATCH /api/projects/:id/`, `DELETE /api/projects/:id/` — update, delete (with permission check).  
- `GET /api/projects/:id/members/`, `POST /api/projects/:id/members/`, `DELETE /api/projects/:id/members/:userId/` — membership.

**Tasks**  
- `GET /api/projects/:projectId/tasks/` — list tasks (with filters: status, priority, assignee, due date; search by title/description).  
- `POST /api/projects/:projectId/tasks/` — create.  
- `GET /api/projects/:projectId/tasks/:id/` — detail.  
- `PATCH /api/projects/:projectId/tasks/:id/`, `DELETE /api/projects/:projectId/tasks/:id/` — update, delete.  
- Optional: `GET /api/projects/:projectId/tasks/:id/comments/`, `POST /api/projects/:projectId/tasks/:id/comments/`.

**Dashboard**  
- `GET /api/dashboard/summary/` — totals (tasks, completed, pending) and progress per project (for current user’s projects).

---

### 5.2 Naming Conventions

- **URLs:** Plural nouns (`/projects/`, `/tasks/`); kebab-case if multi-word.  
- **IDs:** Path params for resource identity (`/projects/123/`, `/projects/123/tasks/456/`).  
- **Query params:** Snake_case for filters (`status`, `priority`, `assigned_to`, `due_date_from`, `search`).  
- **HTTP methods:** GET (read), POST (create), PATCH (partial update), DELETE (delete).  
- **JSON:** Snake_case in request/response body to match Django/DB convention.

---

### 5.3 Versioning Strategy

- **Prefix:** `/api/v1/` for all endpoints.  
- **Future:** New behavior in `/api/v2/` when breaking changes are needed; keep v1 supported for a deprecation period.  
- **No version in URL:** Acceptable for small team if you promise no breaking changes; then version only when necessary.

---

## 6️⃣ ENGINEERING DECISIONS

### 6.1 Why This Structure Is Scalable

- **Apps and core:** New features become new apps or new modules inside an app; core stays small and stable.  
- **Service layer:** New business rules go in services; views stay thin, so adding endpoints or changing responses does not duplicate logic.  
- **Permissions in one place:** Adding a new role or project-level role is a new permission class or condition, not scattered if/else in views.  
- **Frontend:** New pages add components and api modules; routing and layout stay the same.  
- **API versioning:** Allows breaking changes without breaking existing clients.

### 6.2 Avoiding Spaghetti Code

- **Backend:** Views only parse request, call service, return serializer response. Services contain all business logic and call repositories (Django ORM). No business logic in serializers beyond validation and simple transforms.  
- **Frontend:** Pages compose components and hooks; hooks call `api/` and expose data and actions. No direct API calls inside generic UI components.  
- **Single responsibility:** Each file has one clear purpose (e.g. one view set per resource, one service per aggregate).

### 6.3 Keeping Business Logic Out of Views

- **Views:** Validate request (e.g. via serializer), resolve IDs to objects (project, task), call `SomeService.do_something(user, project, data)`, then return serialized result or appropriate status code.  
- **Services:** Contain rules (e.g. “only project admin can add members”, “task status transitions”), create/update/delete operations, and calls to other services if needed.  
- **Permissions:** Only “can this user perform this action on this object?”; no business logic inside permission classes beyond access checks.

### 6.4 Keeping Frontend Maintainable

- **Central API client:** One Axios instance; base URL, interceptors (auth, refresh, error handling) in one place.  
- **Constants:** Routes, status and priority labels, and API paths in `utils/constants.js` to avoid magic strings.  
- **Reusable components:** Common UI in `components/common/`; feature-specific in `components/features/`.  
- **Hooks:** Data fetching and mutation in hooks so pages stay declarative; easy to add loading/error states and reuse across pages.  
- **No business rules in UI:** Validations that must hold are enforced by backend; frontend validates for UX only.

---

## Document Status

- **Frozen:** This architecture is the single source of truth for the project.  
- **Implementation:** All code (backend and frontend) must follow this structure and these decisions.  
- **Changes:** Any change to this document should be explicit and agreed (e.g. new app, new entity, new auth flow) so the rest of the codebase can be updated consistently.
