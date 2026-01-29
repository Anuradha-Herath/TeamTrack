import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../store/authStore'
import { ROUTES } from '../utils/constants'

/**
 * Redirect unauthenticated users to login. Preserve intended URL in state for redirect after login.
 */
export function ProtectedRoute({ children, requireAdmin = false }) {
  const { user, loading } = useAuth()
  const location = useLocation()

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary-500 border-t-transparent" />
      </div>
    )
  }

  if (!user) {
    return <Navigate to={ROUTES.LOGIN} state={{ from: location }} replace />
  }

  if (requireAdmin && user.role !== 'ADMIN') {
    return <Navigate to={ROUTES.DASHBOARD} replace />
  }

  return children
}
