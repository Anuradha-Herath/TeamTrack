import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getSummary } from '../../api/dashboard'
import { Card } from '../../components/common/Card'
import { Spinner } from '../../components/common/Spinner'
import { ROUTES } from '../../utils/constants'
import { formatProgressPct } from '../../utils/formatters'

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getSummary()
      .then(setData)
      .catch((err) => setError(err?.message || 'Failed to load dashboard'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <Spinner />
      </div>
    )
  }

  if (error) {
    return (
      <div className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">
        {error}
      </div>
    )
  }

  const { total_tasks = 0, completed_tasks = 0, pending_tasks = 0, projects = [] } = data || {}

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>

      <div className="grid gap-4 sm:grid-cols-3">
        <Card>
          <p className="text-sm font-medium text-gray-500">Total tasks</p>
          <p className="mt-1 text-2xl font-semibold text-gray-900">{total_tasks}</p>
        </Card>
        <Card>
          <p className="text-sm font-medium text-gray-500">Completed</p>
          <p className="mt-1 text-2xl font-semibold text-green-600">{completed_tasks}</p>
        </Card>
        <Card>
          <p className="text-sm font-medium text-gray-500">Pending</p>
          <p className="mt-1 text-2xl font-semibold text-amber-600">{pending_tasks}</p>
        </Card>
      </div>

      <Card title="Progress by project">
        {projects.length === 0 ? (
          <p className="text-sm text-gray-500">No projects yet. Create a project to see progress.</p>
        ) : (
          <ul className="space-y-4">
            {projects.map((p) => (
              <li key={p.id} className="border-b border-gray-100 pb-4 last:border-0 last:pb-0">
                <div className="flex items-center justify-between">
                  <Link
                    to={ROUTES.PROJECT_DETAIL(p.id)}
                    className="font-medium text-primary-600 hover:text-primary-700"
                  >
                    {p.name}
                  </Link>
                  <span className="text-sm text-gray-600">
                    {p.completed_tasks} / {p.total_tasks} — {formatProgressPct(p.progress_pct)}
                  </span>
                </div>
                <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-gray-200">
                  <div
                    className="h-full rounded-full bg-primary-500 transition-all"
                    style={{ width: `${p.progress_pct ?? 0}%` }}
                  />
                </div>
              </li>
            ))}
          </ul>
        )}
      </Card>
    </div>
  )
}
