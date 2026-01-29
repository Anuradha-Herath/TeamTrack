import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getTask } from '../../api/tasks'
import { getProject } from '../../api/projects'
import { Card } from '../../components/common/Card'
import { Spinner } from '../../components/common/Spinner'
import { ROUTES } from '../../utils/constants'
import { TASK_STATUS_LABELS, TASK_PRIORITY_LABELS } from '../../utils/constants'
import { formatDate } from '../../utils/formatters'

export default function TaskDetail() {
  const { projectId, taskId } = useParams()
  const [task, setTask] = useState(null)
  const [project, setProject] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!projectId || !taskId) return
    Promise.all([getTask(projectId, taskId), getProject(projectId)])
      .then(([t, p]) => {
        setTask(t)
        setProject(p)
      })
      .catch((err) => setError(err?.message || 'Failed to load task'))
      .finally(() => setLoading(false))
  }, [projectId, taskId])

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <Spinner />
      </div>
    )
  }

  if (error || !task) {
    return (
      <div className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">
        {error || 'Task not found'}
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link to={ROUTES.PROJECT_TASKS(projectId)} className="text-sm text-gray-500 hover:text-gray-700">
          ← Tasks
        </Link>
        <h1 className="text-2xl font-bold text-gray-900">{task.title}</h1>
        <span className="rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600">
          {TASK_STATUS_LABELS[task.status] ?? task.status}
        </span>
      </div>

      <Card title="Details">
        <dl className="space-y-2 text-sm">
          <div>
            <dt className="text-gray-500">Status</dt>
            <dd>{TASK_STATUS_LABELS[task.status] ?? task.status}</dd>
          </div>
          <div>
            <dt className="text-gray-500">Priority</dt>
            <dd>{TASK_PRIORITY_LABELS[task.priority] ?? task.priority}</dd>
          </div>
          <div>
            <dt className="text-gray-500">Due date</dt>
            <dd>{formatDate(task.due_date)}</dd>
          </div>
          <div>
            <dt className="text-gray-500">Assigned to</dt>
            <dd>{task.assigned_to_email || '—'}</dd>
          </div>
          <div>
            <dt className="text-gray-500">Created by</dt>
            <dd>{task.created_by_email || '—'}</dd>
          </div>
        </dl>
      </Card>

      <Card title="Description">
        <p className="whitespace-pre-wrap text-sm text-gray-600">{task.description || 'No description'}</p>
      </Card>
    </div>
  )
}
