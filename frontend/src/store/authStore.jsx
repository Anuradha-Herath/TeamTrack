/**
 * Auth context: user, loading, login, register, logout.
 * Persists user/tokens via storage; syncs from storage on mount.
 */

import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import * as authApi from '../api/auth'
import { getUser, setUser, getAccessToken, setAuth, clearAuth } from '../utils/storage'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUserState] = useState(null)
  const [loading, setLoading] = useState(true)

  const loadFromStorage = useCallback(() => {
    const token = getAccessToken()
    const stored = getUser()
    if (token && stored) {
      setUserState(stored)
    } else {
      setUserState(null)
    }
    setLoading(false)
  }, [])

  useEffect(() => {
    loadFromStorage()
  }, [loadFromStorage])

  const login = useCallback(async (email, password) => {
    const data = await authApi.login(email, password)
    setUserState(data.user)
    return data
  }, [])

  const register = useCallback(async (payload) => {
    const data = await authApi.register(payload)
    setUserState(data.user)
    return data
  }, [])

  const logout = useCallback(async () => {
    await authApi.logout()
    setUserState(null)
  }, [])

  const updateUser = useCallback((updated) => {
    setUser(updated)
    setUserState(updated)
  }, [])

  const value = {
    user,
    loading,
    isAuthenticated: !!user,
    isAdmin: user?.role === 'ADMIN',
    login,
    register,
    logout,
    updateUser,
    loadFromStorage,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
