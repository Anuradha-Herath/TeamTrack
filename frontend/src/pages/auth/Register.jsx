import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../store/authStore'
import { Button } from '../../components/common/Button'
import { Input } from '../../components/common/Input'
import { Card } from '../../components/common/Card'
import { ROUTES } from '../../utils/constants'

export default function Register() {
  const { register } = useAuth()
  const navigate = useNavigate()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [first_name, setFirstName] = useState('')
  const [last_name, setLastName] = useState('')
  const [error, setError] = useState('')
  const [fieldErrors, setFieldErrors] = useState({})
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setFieldErrors({})
    setLoading(true)
    try {
      await register({
        email: email.trim(),
        password,
        first_name: first_name.trim(),
        last_name: last_name.trim(),
      })
      navigate(ROUTES.DASHBOARD, { replace: true })
    } catch (err) {
      setError(err?.message || 'Registration failed')
      if (err?.details && typeof err.details === 'object') {
        setFieldErrors(err.details)
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card>
      <h1 className="mb-6 text-xl font-semibold text-gray-900">Create your account</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{error}</div>
        )}
        <Input
          label="Email"
          type="email"
          name="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@example.com"
          error={fieldErrors.email?.[0]}
          required
          autoComplete="email"
        />
        <Input
          label="Password"
          type="password"
          name="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          error={fieldErrors.password?.[0]}
          required
          minLength={8}
          autoComplete="new-password"
        />
        <Input
          label="First name"
          name="first_name"
          value={first_name}
          onChange={(e) => setFirstName(e.target.value)}
          placeholder="John"
        />
        <Input
          label="Last name"
          name="last_name"
          value={last_name}
          onChange={(e) => setLastName(e.target.value)}
          placeholder="Doe"
        />
        <Button type="submit" loading={loading} className="w-full">
          Sign up
        </Button>
      </form>
      <p className="mt-4 text-center text-sm text-gray-600">
        Already have an account?{' '}
        <Link to={ROUTES.LOGIN} className="font-medium text-primary-600 hover:text-primary-700">
          Sign in
        </Link>
      </p>
    </Card>
  )
}
