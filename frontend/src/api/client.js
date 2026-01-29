/**
 * Central Axios instance: base URL, Authorization header, 401 refresh, error shape.
 * Backend success: { success: true, data?, message? }; error: { success: false, message, code?, errors? }.
 */

import axios from 'axios'
import { getAccessToken, getRefreshToken, setAuth, clearAuth } from '../utils/storage'

const baseURL = import.meta.env.VITE_API_BASE_URL || '/api/v1'

export const apiClient = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
})

// Attach access token to every request
apiClient.interceptors.request.use((config) => {
  const token = getAccessToken()
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// On 401: try refresh, retry original request; on refresh failure clear auth (caller can redirect to login)
let refreshing = false
let failedQueue = []

function processQueue(err, token = null) {
  failedQueue.forEach((prom) => (err ? prom.reject(err) : prom.resolve(token)))
  failedQueue = []
}

apiClient.interceptors.response.use(
  (response) => {
    // Backend wraps in { success, data?, message? }; expose .data from our API modules as the payload
    return response
  },
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(normalizeError(error))
    }

    if (refreshing) {
      return new Promise((resolve, reject) => {
        failedQueue.push({ resolve, reject })
      })
        .then((token) => {
          originalRequest.headers.Authorization = `Bearer ${token}`
          return apiClient(originalRequest)
        })
        .catch((err) => Promise.reject(normalizeError(err)))
    }

    originalRequest._retry = true
    refreshing = true
    const refresh = getRefreshToken()

    if (!refresh) {
      clearAuth()
      processQueue(new Error('No refresh token'), null)
      refreshing = false
      return Promise.reject(normalizeError(error))
    }

    try {
      const refreshTokenValue = getRefreshToken()
      const { data } = await axios.post(`${baseURL}/auth/refresh/`, { refresh: refreshTokenValue })
      const payload = data?.data || data
      const access = payload?.access
      const newRefresh = payload?.refresh
      if (access) {
        const user = JSON.parse(localStorage.getItem('teamtrack_user') || 'null')
        setAuth({ user, access, refresh: newRefresh || refresh })
        processQueue(null, access)
        originalRequest.headers.Authorization = `Bearer ${access}`
        return apiClient(originalRequest)
      }
    } catch (refreshError) {
      clearAuth()
      processQueue(refreshError, null)
      return Promise.reject(normalizeError(refreshError))
    } finally {
      refreshing = false
    }

    return Promise.reject(normalizeError(error))
  }
)

function normalizeError(error) {
  const res = error.response
  const data = res?.data
  const message = data?.message || res?.statusText || error.message || 'Request failed'
  const code = data?.code
  const details = data?.errors
  return { message, code, details, status: res?.status, original: error }
}
