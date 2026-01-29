import { useEffect, useState } from 'react'
import { getUsers, updateUser } from '../../api/users'
import { Card } from '../../components/common/Card'
import { Spinner } from '../../components/common/Spinner'
import { USER_ROLE_LABELS } from '../../utils/constants'
import { formatDateTime } from '../../utils/formatters'

export default function UserList() {
  const [payload, setPayload] = useState({ results: [], pagination: null })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [updating, setUpdating] = useState(null)

  useEffect(() => {
    getUsers()
      .then(setPayload)
      .catch((err) => setError(err?.message || 'Failed to load users'))
      .finally(() => setLoading(false))
  }, [])

  const handleToggleActive = async (user) => {
    setUpdating(user.id)
    try {
      await updateUser(user.id, { is_active: !user.is_active })
      setPayload((prev) => ({
        ...prev,
        results: prev.results.map((u) => (u.id === user.id ? { ...u, is_active: !u.is_active } : u)),
      }))
    } catch (err) {
      setError(err?.message || 'Failed to update')
    } finally {
      setUpdating(null)
    }
  }

  const handleRoleChange = async (user, newRole) => {
    setUpdating(user.id)
    try {
      await updateUser(user.id, { role: newRole })
      setPayload((prev) => ({
        ...prev,
        results: prev.results.map((u) => (u.id === user.id ? { ...u, role: newRole } : u)),
      }))
    } catch (err) {
      setError(err?.message || 'Failed to update')
    } finally {
      setUpdating(null)
    }
  }

  const users = payload?.results ?? []

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <Spinner />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Users (Admin)</h1>

      {error && (
        <div className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>
      )}

      <Card>
        {users.length === 0 ? (
          <p className="text-sm text-gray-500">No users</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 text-sm">
              <thead>
                <tr>
                  <th className="px-4 py-2 text-left font-medium text-gray-700">Email</th>
                  <th className="px-4 py-2 text-left font-medium text-gray-700">Name</th>
                  <th className="px-4 py-2 text-left font-medium text-gray-700">Role</th>
                  <th className="px-4 py-2 text-left font-medium text-gray-700">Active</th>
                  <th className="px-4 py-2 text-left font-medium text-gray-700">Joined</th>
                  <th className="px-4 py-2 text-left font-medium text-gray-700">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {users.map((u) => (
                  <tr key={u.id}>
                    <td className="px-4 py-2">{u.email}</td>
                    <td className="px-4 py-2">{[u.first_name, u.last_name].filter(Boolean).join(' ') || '—'}</td>
                    <td className="px-4 py-2">
                      <select
                        value={u.role}
                        onChange={(e) => handleRoleChange(u, e.target.value)}
                        disabled={updating === u.id}
                        className="rounded border border-gray-300 px-2 py-1 text-sm"
                      >
                        {Object.entries(USER_ROLE_LABELS).map(([k, v]) => (
                          <option key={k} value={k}>{v}</option>
                        ))}
                      </select>
                    </td>
                    <td className="px-4 py-2">{u.is_active ? 'Yes' : 'No'}</td>
                    <td className="px-4 py-2 text-gray-500">{formatDateTime(u.date_joined)}</td>
                    <td className="px-4 py-2">
                      <button
                        type="button"
                        onClick={() => handleToggleActive(u)}
                        disabled={updating === u.id}
                        className="rounded-lg border border-gray-300 bg-white px-2 py-1 text-xs font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
                      >
                        {u.is_active ? 'Deactivate' : 'Activate'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  )
}
