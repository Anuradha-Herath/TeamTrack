import { apiClient } from './client'

function unwrap(res) {
  const data = res.data
  if (data && typeof data.success !== 'undefined' && !data.success) {
    throw { message: data.message, code: data.code, details: data.errors }
  }
  return data?.data ?? data
}

export async function getTasks(projectId, params = {}) {
  const res = await apiClient.get(`/projects/${projectId}/tasks/`, { params })
  const data = res.data
  const payload = data?.data ?? data
  if (payload?.results != null) return payload
  if (Array.isArray(payload)) return { results: payload, pagination: null }
  return { results: [], pagination: null }
}

export async function getTask(projectId, taskId) {
  return apiClient.get(`/projects/${projectId}/tasks/${taskId}/`).then(unwrap)
}

export async function createTask(projectId, payload) {
  return apiClient.post(`/projects/${projectId}/tasks/`, payload).then(unwrap)
}

export async function updateTask(projectId, taskId, payload) {
  return apiClient.patch(`/projects/${projectId}/tasks/${taskId}/`, payload).then(unwrap)
}

export async function deleteTask(projectId, taskId) {
  return apiClient.delete(`/projects/${projectId}/tasks/${taskId}/`)
}
