import { useAuth } from '../../store/authStore'

export function Navbar() {
  const { user } = useAuth()

  return (
    <header className="sticky top-0 z-30 flex h-14 items-center justify-between border-b border-gray-200 bg-white px-4 shadow-sm">
      <div className="flex items-center gap-2">
        <button
          type="button"
          className="rounded-lg p-2 text-gray-600 hover:bg-gray-100 lg:hidden"
          onClick={() => {
            const sidebar = document.getElementById('sidebar')
            const backdrop = document.getElementById('sidebar-backdrop')
            if (sidebar) sidebar.classList.toggle('-translate-x-full')
            if (backdrop) backdrop.classList.toggle('hidden')
          }}
          aria-label="Toggle menu"
        >
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <span className="text-sm font-medium text-gray-600">TeamTrack</span>
      </div>
      <div className="flex items-center gap-3">
        <span className="hidden text-sm text-gray-600 sm:inline">{user?.email}</span>
        <span className="rounded-full bg-primary-100 px-2 py-0.5 text-xs font-medium text-primary-800">
          {user?.role === 'ADMIN' ? 'Admin' : 'Member'}
        </span>
      </div>
    </header>
  )
}
