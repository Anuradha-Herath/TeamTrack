import { apiClient } from './client'

function unwrap(res) {
  const data = res.data
  if (data && typeof data.success !== 'undefined' && !data.success) {
    throw { message: data.message, code: data.code, details: data.errors }
  }
  return data?.data ?? data
}

export async function getMe() {
  return apiClient.get('/users/me/').then(unwrap)
}

export async function updateMe(payload) {
  return apiClient.patch('/users/me/', payload).then(unwrap)
}

export async function getUsers(params = {}) {
  const res = await apiClient.get('/users/', { params })
  const data = res.data
  const payload = data?.data ?? data
  if (payload?.results != null) return payload
  if (Array.isArray(payload)) return { results: payload, pagination: null }
  return { results: [], pagination: null }
}

export async function getUser(id) {
  return apiClient.get(`/users/${id}/`).then(unwrap)
}

export async function updateUser(id, payload) {
  return apiClient.patch(`/users/${id}/`, payload).then(unwrap)
}
