/**
 * Token and auth storage. Single place for keys and get/set/remove.
 */

const ACCESS_KEY = 'teamtrack_access'
const REFRESH_KEY = 'teamtrack_refresh'
const USER_KEY = 'teamtrack_user'

export function getAccessToken() {
  return localStorage.getItem(ACCESS_KEY)
}

export function setAccessToken(token) {
  if (token) localStorage.setItem(ACCESS_KEY, token)
  else localStorage.removeItem(ACCESS_KEY)
}

export function getRefreshToken() {
  return localStorage.getItem(REFRESH_KEY)
}

export function setRefreshToken(token) {
  if (token) localStorage.setItem(REFRESH_KEY, token)
  else localStorage.removeItem(REFRESH_KEY)
}

export function getUser() {
  try {
    const raw = localStorage.getItem(USER_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export function setUser(user) {
  if (user) localStorage.setItem(USER_KEY, JSON.stringify(user))
  else localStorage.removeItem(USER_KEY)
}

export function clearAuth() {
  localStorage.removeItem(ACCESS_KEY)
  localStorage.removeItem(REFRESH_KEY)
  localStorage.removeItem(USER_KEY)
}

export function setAuth({ user, access, refresh }) {
  setUser(user)
  setAccessToken(access)
  setRefreshToken(refresh)
}
