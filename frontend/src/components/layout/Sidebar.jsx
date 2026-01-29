import { NavLink } from 'react-router-dom'
import { useAuth } from '../../store/authStore'
import { ROUTES } from '../../utils/constants'

const navItems = [
  { to: ROUTES.DASHBOARD, label: 'Dashboard', end: true },
  { to: ROUTES.PROJECTS, label: 'Projects', end: false },
  { to: ROUTES.PROFILE, label: 'Profile', end: true },
]
const adminItem = { to: ROUTES.USERS, label: 'Users', end: true }

export function Sidebar() {
  const { user, logout, isAdmin } = useAuth()

  return (
    <>
      {/* Mobile overlay */}
      <div id="sidebar-backdrop" className="fixed inset-0 z-40 bg-black/50 lg:hidden" aria-hidden="true" />

      <aside
        id="sidebar"
        className="fixed left-0 top-0 z-50 h-full w-64 -translate-x-full transform border-r border-gray-200 bg-white transition-transform lg:translate-x-0"
      >
        <div className="flex h-full flex-col">
          <div className="flex h-14 items-center border-b border-gray-200 px-4">
            <NavLink to={ROUTES.DASHBOARD} className="text-lg font-semibold text-primary-600">
              TeamTrack
            </NavLink>
          </div>
          <nav className="flex-1 space-y-0.5 p-3">
            {navItems.map(({ to, label, end }) => (
              <NavLink
                key={to}
                to={to}
                end={end}
                className={({ isActive }) =>
                  `block rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                    isActive ? 'bg-primary-50 text-primary-700' : 'text-gray-700 hover:bg-gray-100'
                  }`
                }
              >
                {label}
              </NavLink>
            ))}
            {isAdmin && (
              <NavLink
                to={adminItem.to}
                end={adminItem.end}
                className={({ isActive }) =>
                  `block rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                    isActive ? 'bg-primary-50 text-primary-700' : 'text-gray-700 hover:bg-gray-100'
                  }`
                }
              >
                {adminItem.label}
              </NavLink>
            )}
          </nav>
          <div className="border-t border-gray-200 p-3">
            <p className="truncate px-3 py-1 text-xs text-gray-500">{user?.email}</p>
            <button
              type="button"
              onClick={logout}
              className="w-full rounded-lg px-3 py-2 text-left text-sm font-medium text-gray-700 hover:bg-gray-100"
            >
              Log out
            </button>
          </div>
        </div>
      </aside>
    </>
  )
}
