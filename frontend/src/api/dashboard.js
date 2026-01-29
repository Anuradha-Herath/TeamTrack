import { apiClient } from './client'

function unwrap(res) {
  const data = res.data
  if (data && typeof data.success !== 'undefined' && !data.success) {
    throw { message: data.message, code: data.code, details: data.errors }
  }
  return data?.data ?? data
}

export async function getSummary() {
  return apiClient.get('/dashboard/summary/').then(unwrap)
}
