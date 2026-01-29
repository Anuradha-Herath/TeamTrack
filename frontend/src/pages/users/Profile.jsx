import { useEffect, useState } from 'react'
import { useAuth } from '../../store/authStore'
import { getMe, updateMe } from '../../api/users'
import { Card } from '../../components/common/Card'
import { Button } from '../../components/common/Button'
import { Input } from '../../components/common/Input'
import { Spinner } from '../../components/common/Spinner'
import { USER_ROLE_LABELS } from '../../utils/constants'
import { formatDateTime } from '../../utils/formatters'

export default function Profile() {
  const { user: authUser, updateUser } = useAuth()
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)
  const [edit, setEdit] = useState({ first_name: '', last_name: '' })

  useEffect(() => {
    getMe()
      .then((data) => {
        setUser(data)
        setEdit({ first_name: data.first_name ?? '', last_name: data.last_name ?? '' })
      })
      .catch((err) => setError(err?.message || 'Failed to load profile'))
      .finally(() => setLoading(false))
  }, [])

  const handleSave = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError(null)
    try {
      const updated = await updateMe(edit)
      setUser(updated)
      updateUser(updated)
    } catch (err) {
      setError(err?.message || 'Failed to update')
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <Spinner />
      </div>
    )
  }

  if (error && !user) {
    return (
      <div className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>
    )
  }

  const u = user || authUser
  if (!u) return null

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Profile</h1>

      <Card title="Account">
        <dl className="space-y-2 text-sm">
          <div>
            <dt className="text-gray-500">Email</dt>
            <dd className="font-medium">{u.email}</dd>
          </div>
          <div>
            <dt className="text-gray-500">Role</dt>
            <dd>{USER_ROLE_LABELS[u.role] ?? u.role}</dd>
          </div>
          <div>
            <dt className="text-gray-500">Joined</dt>
            <dd>{formatDateTime(u.date_joined)}</dd>
          </div>
        </dl>
      </Card>

      <Card title="Edit profile">
        <form onSubmit={handleSave} className="space-y-4">
          {error && (
            <div className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div>
          )}
          <Input
            label="First name"
            value={edit.first_name}
            onChange={(e) => setEdit((x) => ({ ...x, first_name: e.target.value }))}
          />
          <Input
            label="Last name"
            value={edit.last_name}
            onChange={(e) => setEdit((x) => ({ ...x, last_name: e.target.value }))}
          />
          <Button type="submit" loading={saving}>
            Save
          </Button>
        </form>
      </Card>
    </div>
  )
}
