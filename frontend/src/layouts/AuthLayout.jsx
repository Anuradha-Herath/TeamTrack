import { Outlet, Navigate } from 'react-router-dom'
import { useAuth } from '../store/authStore'
import { ROUTES } from '../utils/constants'

/**
 * Centered card layout for login/register. No sidebar/navbar.
 * Redirect to dashboard if already authenticated.
 */
export function AuthLayout() {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-100">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary-500 border-t-transparent" />
      </div>
    )
  }

  if (user) {
    return <Navigate to={ROUTES.DASHBOARD} replace />
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100 px-4">
      <main className="w-full max-w-md">
        <Outlet />
      </main>
    </div>
  )
}
