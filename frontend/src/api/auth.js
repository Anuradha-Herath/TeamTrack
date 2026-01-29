/**
 * Auth API: login, register, refresh, logout.
 * Backend returns { success, data: { user, access, refresh? } } or error shape.
 */

import { apiClient } from './client'
import { setAuth, clearAuth } from '../utils/storage'

function unwrap(res) {
  const data = res.data
  if (data && typeof data.success !== 'undefined' && !data.success) {
    throw { message: data.message, code: data.code, details: data.errors }
  }
  return data?.data ?? data
}

export async function login(email, password) {
  const data = await apiClient.post('/auth/login/', { email, password }).then(unwrap)
  setAuth({ user: data.user, access: data.access, refresh: data.refresh })
  return data
}

export async function register(payload) {
  const data = await apiClient.post('/auth/register/', payload).then(unwrap)
  setAuth({ user: data.user, access: data.access, refresh: data.refresh })
  return data
}

export async function refreshToken() {
  const data = await apiClient.post('/auth/refresh/', {
    refresh: localStorage.getItem('teamtrack_refresh'),
  }).then(unwrap)
  return data
}

export async function logout() {
  try {
    const refresh = localStorage.getItem('teamtrack_refresh')
    if (refresh) await apiClient.post('/auth/logout/', { refresh })
  } finally {
    clearAuth()
  }
}
