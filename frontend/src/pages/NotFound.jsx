import { Link } from 'react-router-dom'
import { ROUTES } from '../utils/constants'

export default function NotFound() {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center px-4">
      <h1 className="text-4xl font-bold text-gray-900">404</h1>
      <p className="mt-2 text-gray-600">Page not found</p>
      <Link
        to={ROUTES.DASHBOARD}
        className="mt-4 rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
      >
        Go to Dashboard
      </Link>
    </div>
  )
}
