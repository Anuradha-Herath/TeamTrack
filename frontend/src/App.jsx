import { AuthProvider } from './store/authStore'
import { AppRoutes } from './routes'

export default function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  )
}
