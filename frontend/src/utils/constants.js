/**
 * Route paths and API-related constants.
 * No magic strings in components.
 */

export const ROUTES = {
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  PROJECTS: '/projects',
  PROJECT_DETAIL: (id) => `/projects/${id}`,
  PROJECT_TASKS: (id) => `/projects/${id}/tasks`,
  TASK_DETAIL: (projectId, taskId) => `/projects/${projectId}/tasks/${taskId}`,
  PROFILE: '/profile',
  USERS: '/users',
  USER_DETAIL: (id) => `/users/${id}`,
}

export const TASK_STATUS = {
  TODO: 'TODO',
  IN_PROGRESS: 'IN_PROGRESS',
  DONE: 'DONE',
}

export const TASK_STATUS_LABELS = {
  TODO: 'Todo',
  IN_PROGRESS: 'In Progress',
  DONE: 'Done',
}

export const TASK_PRIORITY = {
  LOW: 'LOW',
  MEDIUM: 'MEDIUM',
  HIGH: 'HIGH',
}

export const TASK_PRIORITY_LABELS = {
  LOW: 'Low',
  MEDIUM: 'Medium',
  HIGH: 'High',
}

export const PROJECT_STATUS = {
  ACTIVE: 'ACTIVE',
  ARCHIVED: 'ARCHIVED',
}

export const PROJECT_STATUS_LABELS = {
  ACTIVE: 'Active',
  ARCHIVED: 'Archived',
}

export const USER_ROLE = {
  ADMIN: 'ADMIN',
  TEAM_MEMBER: 'TEAM_MEMBER',
}

export const USER_ROLE_LABELS = {
  ADMIN: 'Admin',
  TEAM_MEMBER: 'Team Member',
}

export const PROJECT_MEMBER_ROLE = {
  PROJECT_ADMIN: 'PROJECT_ADMIN',
  MEMBER: 'MEMBER',
}

export const PROJECT_MEMBER_ROLE_LABELS = {
  PROJECT_ADMIN: 'Project Admin',
  MEMBER: 'Member',
}
