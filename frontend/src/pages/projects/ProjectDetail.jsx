import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getProject } from '../../api/projects'
import { Card } from '../../components/common/Card'
import { Button } from '../../components/common/Button'
import { Spinner } from '../../components/common/Spinner'
import { ROUTES } from '../../utils/constants'
import { PROJECT_STATUS_LABELS, PROJECT_MEMBER_ROLE_LABELS } from '../../utils/constants'

export default function ProjectDetail() {
  const { projectId } = useParams()
  const [project, setProject] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!projectId) return
    getProject(projectId)
      .then(setProject)
      .catch((err) => setError(err?.message || 'Failed to load project'))
      .finally(() => setLoading(false))
  }, [projectId])

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <Spinner />
      </div>
    )
  }

  if (error || !project) {
    return (
      <div className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">
        {error || 'Project not found'}
      </div>
    )
  }

  const members = project.members ?? []

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link to={ROUTES.PROJECTS} className="text-sm text-gray-500 hover:text-gray-700">
          ← Projects
        </Link>
        <h1 className="text-2xl font-bold text-gray-900">{project.name}</h1>
        <span className="rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600">
          {PROJECT_STATUS_LABELS[project.status] ?? project.status}
        </span>
      </div>

      <Card title="Description">
        <p className="text-sm text-gray-600">{project.description || 'No description'}</p>
      </Card>

      <Card title="Tasks">
        <Link
          to={ROUTES.PROJECT_TASKS(project.id)}
          className="inline-flex items-center rounded-lg bg-primary-600 px-3 py-2 text-sm font-medium text-white hover:bg-primary-700"
        >
          View tasks
        </Link>
      </Card>

      <Card title="Members">
        {members.length === 0 ? (
          <p className="text-sm text-gray-500">No members</p>
        ) : (
          <ul className="space-y-2">
            {members.map((m) => (
              <li key={m.id} className="flex items-center justify-between text-sm">
                <span>{m.email}</span>
                <span className="text-gray-500">{PROJECT_MEMBER_ROLE_LABELS[m.role] ?? m.role}</span>
              </li>
            ))}
          </ul>
        )}
      </Card>
    </div>
  )
}
