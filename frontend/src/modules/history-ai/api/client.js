const API_BASE = import.meta.env.VITE_HISTORY_API_BASE_URL || 'http://127.0.0.1:8000/api/history'
const TOKEN_URL = import.meta.env.VITE_AUTH_TOKEN_URL || 'http://127.0.0.1:8000/api/auth/token/'
const TOKEN_STORAGE_KEY = 'tarixchi_ai_token'

export function getToken() {
  return localStorage.getItem(TOKEN_STORAGE_KEY)
}

export function setToken(token) {
  localStorage.setItem(TOKEN_STORAGE_KEY, token)
}

export function clearToken() {
  localStorage.removeItem(TOKEN_STORAGE_KEY)
}

export async function login(username, password) {
  const res = await fetch(TOKEN_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ username, password }),
  })
  if (!res.ok) {
    throw new Error("Login yoki parol noto'g'ri")
  }
  const data = await res.json()
  setToken(data.token)
  return data.token
}

async function request(path, options = {}) {
  const token = getToken()
  const headers = { ...(options.headers || {}) }
  if (token) headers.Authorization = `Token ${token}`

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers })

  if (!res.ok) {
    let detail = `So'rov xatosi (${res.status})`
    try {
      const body = await res.json()
      detail = body.error || body.detail || JSON.stringify(body)
    } catch {
      // javob JSON emas, standart xabar qoladi
    }
    const error = new Error(detail)
    error.status = res.status
    throw error
  }

  if (res.status === 204) return null
  return res.json()
}

export function uploadBook(file, title) {
  const formData = new FormData()
  formData.append('file', file)
  if (title) formData.append('title', title)
  return request('/books/', { method: 'POST', body: formData })
}

export function listTopics(bookId) {
  return request(`/books/${bookId}/topics/`)
}

export function createLesson(topicId) {
  return request('/lessons/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ topic: topicId }),
  })
}

export function getLesson(lessonId) {
  return request(`/lessons/${lessonId}/`)
}

export function createAsset(topicId, kind) {
  return request('/assets/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ topic: topicId, kind }),
  })
}

export function getAsset(assetId) {
  return request(`/assets/${assetId}/`)
}
