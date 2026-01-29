import { apiClient } from './client'

function unwrap(res) {
  const data = res.data
  if (data && typeof data.success !== 'undefined' && !data.success) {
    throw { message: data.message, code: data.code, details: data.errors }
  }
  return data?.data ?? data
}

export async function getProjects(params = {}) {
  const res = await apiClient.get('/projects/', { params })
  const data = res.data
  const payload = data?.data ?? data
  if (payload?.results != null) return payload
  if (Array.isArray(payload)) return { results: payload, pagination: null }
  return { results: [], pagination: null }
}

export async function getProject(id) {
  return apiClient.get(`/projects/${id}/`).then(unwrap)
}

export async function createProject(payload) {
  return apiClient.post('/projects/', payload).then(unwrap)
}

export async function updateProject(id, payload) {
  return apiClient.patch(`/projects/${id}/`, payload).then(unwrap)
}

export async function deleteProject(id) {
  return apiClient.delete(`/projects/${id}/`)
}

export async function getProjectMembers(projectId) {
  return apiClient.get(`/projects/${projectId}/members/`).then(unwrap)
}

export async function addProjectMember(projectId, payload) {
  return apiClient.post(`/projects/${projectId}/members/`, payload).then(unwrap)
}

export async function removeProjectMember(projectId, userId) {
  return apiClient.delete(`/projects/${projectId}/members/${userId}/`)
}
