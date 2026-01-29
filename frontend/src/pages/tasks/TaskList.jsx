import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getTasks } from '../../api/tasks'
import { getProject } from '../../api/projects'
import { Card } from '../../components/common/Card'
import { Spinner } from '../../components/common/Spinner'
import { ROUTES } from '../../utils/constants'
import { TASK_STATUS_LABELS, TASK_PRIORITY_LABELS } from '../../utils/constants'
import { formatDate } from '../../utils/formatters'

export default function TaskList() {
  const { projectId } = useParams()
  const [project, setProject] = useState(null)
  const [payload, setPayload] = useState({ results: [], pagination: null })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [filters, setFilters] = useState({ status: '', priority: '' })

  useEffect(() => {
    if (!projectId) return
    getProject(projectId).then(setProject).catch(() => setProject(null))
  }, [projectId])

  useEffect(() => {
    if (!projectId) return
    setLoading(true)
    const params = {}
    if (filters.status) params.status = filters.status
    if (filters.priority) params.priority = filters.priority
    getTasks(projectId, params)
      .then(setPayload)
      .catch((err) => setError(err?.message || 'Failed to load tasks'))
      .finally(() => setLoading(false))
  }, [projectId, filters.status, filters.priority])

  if (!projectId) return null

  const tasks = payload?.results ?? []

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link to={ROUTES.PROJECT_DETAIL(projectId)} className="text-sm text-gray-500 hover:text-gray-700">
          ← Project
        </Link>
        <h1 className="text-2xl font-bold text-gray-900">
          {project?.name ?? 'Project'} — Tasks
        </h1>
      </div>

      <Card>
        <div className="mb-4 flex flex-wrap gap-2">
          <select
            value={filters.status}
            onChange={(e) => setFilters((f) => ({ ...f, status: e.target.value }))}
            className="rounded-lg border border-gray-300 px-3 py-1.5 text-sm"
          >
            <option value="">All statuses</option>
            {Object.entries(TASK_STATUS_LABELS).map(([k, v]) => (
              <option key={k} value={k}>{v}</option>
            ))}
          </select>
          <select
            value={filters.priority}
            onChange={(e) => setFilters((f) => ({ ...f, priority: e.target.value }))}
            className="rounded-lg border border-gray-300 px-3 py-1.5 text-sm"
          >
            <option value="">All priorities</option>
            {Object.entries(TASK_PRIORITY_LABELS).map(([k, v]) => (
              <option key={k} value={k}>{v}</option>
            ))}
          </select>
        </div>

        {loading ? (
          <div className="flex justify-center py-8">
            <Spinner />
          </div>
        ) : error ? (
          <p className="text-sm text-red-600">{error}</p>
        ) : tasks.length === 0 ? (
          <p className="text-sm text-gray-500">No tasks</p>
        ) : (
          <ul className="divide-y divide-gray-200">
            {tasks.map((t) => (
              <li key={t.id} className="py-3 first:pt-0">
                <Link
                  to={ROUTES.TASK_DETAIL(projectId, t.id)}
                  className="font-medium text-primary-600 hover:text-primary-700"
                >
                  {t.title}
                </Link>
                <p className="mt-0.5 flex flex-wrap gap-2 text-sm text-gray-500">
                  <span>{TASK_STATUS_LABELS[t.status] ?? t.status}</span>
                  <span>{TASK_PRIORITY_LABELS[t.priority] ?? t.priority}</span>
                  {t.due_date && <span>Due {formatDate(t.due_date)}</span>}
                  {t.assigned_to_email && <span>→ {t.assigned_to_email}</span>}
                </p>
              </li>
            ))}
          </ul>
        )}
      </Card>
    </div>
  )
}
