import { Routes, Route, Navigate } from 'react-router-dom'
import { ProtectedRoute } from './ProtectedRoute'
import { AuthLayout } from '../layouts/AuthLayout'
import { DashboardLayout } from '../layouts/DashboardLayout'
import { ROUTES } from '../utils/constants'

// Auth pages
import Login from '../pages/auth/Login'
import Register from '../pages/auth/Register'

// App pages (lazy or direct for now)
import Dashboard from '../pages/dashboard/Dashboard'
import ProjectList from '../pages/projects/ProjectList'
import ProjectDetail from '../pages/projects/ProjectDetail'
import TaskList from '../pages/tasks/TaskList'
import TaskDetail from '../pages/tasks/TaskDetail'
import Profile from '../pages/users/Profile'
import UserList from '../pages/users/UserList'
import NotFound from '../pages/NotFound'

export function AppRoutes() {
  return (
    <Routes>
      <Route element={<AuthLayout />}>
        <Route path={ROUTES.LOGIN} element={<Login />} />
        <Route path={ROUTES.REGISTER} element={<Register />} />
      </Route>

      <Route
        element={
          <ProtectedRoute>
            <DashboardLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/" element={<Navigate to={ROUTES.DASHBOARD} replace />} />
        <Route path={ROUTES.DASHBOARD} element={<Dashboard />} />
        <Route path={ROUTES.PROJECTS} element={<ProjectList />} />
        <Route path="/projects/:projectId" element={<ProjectDetail />} />
        <Route path="/projects/:projectId/tasks" element={<TaskList />} />
        <Route path="/projects/:projectId/tasks/:taskId" element={<TaskDetail />} />
        <Route path={ROUTES.PROFILE} element={<Profile />} />
        <Route
          path={ROUTES.USERS}
          element={
            <ProtectedRoute requireAdmin>
              <UserList />
            </ProtectedRoute>
          }
        />
      </Route>

      <Route path="/404" element={<NotFound />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}
