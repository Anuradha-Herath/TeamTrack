import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getProjects } from '../../api/projects'
import { Card } from '../../components/common/Card'
import { Button } from '../../components/common/Button'
import { Spinner } from '../../components/common/Spinner'
import { ROUTES } from '../../utils/constants'
import { PROJECT_STATUS_LABELS } from '../../utils/constants'

export default function ProjectList() {
  const [payload, setPayload] = useState({ results: [], pagination: null })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getProjects()
      .then(setPayload)
      .catch((err) => setError(err?.message || 'Failed to load projects'))
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
      <div className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>
    )
  }

  const projects = payload?.results ?? []

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Projects</h1>
      </div>

      <Card>
        {projects.length === 0 ? (
          <p className="text-sm text-gray-500">No projects yet.</p>
        ) : (
          <ul className="divide-y divide-gray-200">
            {projects.map((p) => (
              <li key={p.id} className="flex items-center justify-between py-3 first:pt-0">
                <div>
                  <Link
                    to={ROUTES.PROJECT_DETAIL(p.id)}
                    className="font-medium text-primary-600 hover:text-primary-700"
                  >
                    {p.name}
                  </Link>
                  <p className="text-sm text-gray-500">
                    {p.description || 'No description'} · {p.member_count ?? 0} members ·{' '}
                    {PROJECT_STATUS_LABELS[p.status] ?? p.status}
                  </p>
                </div>
                <span className="rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600">
                  {p.member_count ?? 0} tasks
                </span>
              </li>
            ))}
          </ul>
        )}
      </Card>
    </div>
  )
}
