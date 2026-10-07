const API_BASE = import.meta.env.VITE_HISTORY_API_BASE_URL || 'http://127.0.0.1:8000/api/history'
const TOKEN_URL = import.meta.env.VITE_AUTH_TOKEN_URL || 'http://127.0.0.1:8000/api/auth/token/'
const REGISTER_URL = import.meta.env.VITE_AUTH_REGISTER_URL || 'http://127.0.0.1:8000/api/auth/register/'
const AUTH_BASE = REGISTER_URL.replace(/register\/?$/, '')
const TOKEN_STORAGE_KEY = 'tarixchi_ai_token'

export function getToken() {
  return localStorage.getItem(TOKEN_STORAGE_KEY)
}

export function setToken(token) {
  localStorage.setItem(TOKEN_STORAGE_KEY, token)
}

export function clearToken() {
  localStorage.removeItem(TOKEN_STORAGE_KEY)
  navigator.serviceWorker?.controller?.postMessage('clear-content')
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

export async function register(username, password, firstName, email) {
  const res = await fetch(REGISTER_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password, first_name: firstName, email }),
  })
  const body = await res.json().catch(() => ({}))
  if (!res.ok) {
    const first = Object.values(body).flat()[0]
    throw new Error(typeof first === 'string' ? first : "Ro'yxatdan o'tib bo'lmadi")
  }
  setToken(body.token)
  return body.token
}

export function getReview(bookId) {
  return request(`/books/${bookId}/review/`)
}

export function answerReview(bookId, key, choice) {
  return request(`/books/${bookId}/review/answer/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ key, choice }),
  })
}

export function getMixedPractice(bookId) {
  return request(`/books/${bookId}/mixed/`)
}

export function answerMixedPractice(bookId, key, choice) {
  return request(`/books/${bookId}/mixed/answer/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ key, choice }),
  })
}

export function searchBook(bookId, q) {
  return request(`/books/${bookId}/search/?q=${encodeURIComponent(q)}`)
}

export function getProfile() {
  return request('/profile/')
}

/** Sahifa ochiq/faol paytda chaqiriladi — admin panelda kunlik faollik jadvali uchun. */
export function sendHeartbeat() {
  return request('/heartbeat/', { method: 'POST' })
}

async function authPost(path, payload) {
  const res = await fetch(`${AUTH_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...(getToken() ? { Authorization: `Token ${getToken()}` } : {}) },
    body: JSON.stringify(payload),
  })
  const body = await res.json().catch(() => ({}))
  if (!res.ok) {
    const first = body.detail || Object.values(body).flat()[0]
    throw new Error(typeof first === 'string' ? first : "So'rov bajarilmadi")
  }
  return body
}

export function requestPasswordReset(email) {
  return authPost('password-reset/', { email })
}

export function confirmPasswordReset(uid, token, password) {
  return authPost('password-reset/confirm/', { uid, token, password })
}

export async function changePassword(oldPassword, newPassword) {
  const data = await authPost('change-password/', { old_password: oldPassword, new_password: newPassword })
  setToken(data.token)
}

export function updateMe(payload) {
  return request('/me/', {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

export function listSubjects() {
  return request('/subjects/')
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

export function listBooks(subjectSlug) {
  return request(subjectSlug ? `/books/?subject=${encodeURIComponent(subjectSlug)}` : '/books/')
}

export function listTopics(bookId) {
  return request(`/books/${bookId}/topics/`)
}

export function createLesson(topicId, { regenerate = false } = {}) {
  const params = { topic: topicId }
  if (regenerate) params.regenerate = 'true'
  return request('/lessons/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams(params),
  })
}

export function getLesson(lessonId) {
  return request(`/lessons/${lessonId}/`)
}

/** Mavzu uchun mavjud lesson'ni oladi; hali yaratilmagan bo'lsa null qaytaradi (404 emas, xato emas). */
export async function getLessonByTopic(topicId) {
  try {
    return await request(`/topics/${topicId}/lesson/`)
  } catch (err) {
    if (err.status === 404) return null
    throw err
  }
}

export function createAsset(topicId, kind, { regenerate = false } = {}) {
  const params = { topic: topicId, kind }
  if (regenerate) params.regenerate = 'true'
  return request('/assets/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams(params),
  })
}

export function getAsset(assetId) {
  return request(`/assets/${assetId}/`)
}

/** Mavzu+kind uchun mavjud asset'ni oladi; hali yaratilmagan bo'lsa null qaytaradi. */
export async function getAssetByTopic(topicId, kind) {
  try {
    return await request(`/topics/${topicId}/assets/${kind}/`)
  } catch (err) {
    if (err.status === 404) return null
    throw err
  }
}

export function getMe() {
  return request('/me/')
}

export function getBookProgress(bookId) {
  return request(`/books/${bookId}/progress/`)
}

export function getTopicTestHint(topicId, index, level) {
  return request(`/topics/${topicId}/test/hint/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ index, level }),
  })
}

export function submitTopicTest(topicId, answers) {
  return request(`/topics/${topicId}/test/submit/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ answers }),
  })
}

/** Yakuniy imtihon; hali yaratilmagan bo'lsa null. */
export async function getBookExam(bookId) {
  try {
    return await request(`/books/${bookId}/exam/`)
  } catch (err) {
    if (err.status === 404) return null
    throw err
  }
}

export function createBookExam(bookId) {
  return request(`/books/${bookId}/exam/create/`, { method: 'POST' })
}

export function submitBookExam(bookId, answers) {
  return request(`/books/${bookId}/exam/submit/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ answers }),
  })
}

export async function downloadCertificate(bookId) {
  const res = await fetch(`${API_BASE}/books/${bookId}/certificate/`, {
    headers: { Authorization: `Token ${getToken()}` },
  })
  if (!res.ok) throw new Error('Sertifikatni yuklab bo\'lmadi')
  const url = URL.createObjectURL(await res.blob())
  const a = document.createElement('a')
  a.href = url
  a.download = 'sertifikat.pdf'
  a.click()
  URL.revokeObjectURL(url)
}

export function getSections(bookId) {
  return request(`/books/${bookId}/sections/`)
}

export async function getSectionExam(sectionId) {
  try {
    return await request(`/sections/${sectionId}/exam/`)
  } catch (err) {
    if (err.status === 404) return null
    throw err
  }
}

export function submitSectionExam(sectionId, answers) {
  return request(`/sections/${sectionId}/exam/submit/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ answers }),
  })
}

export function getLessonFeedback(topicId) {
  return request(`/topics/${topicId}/feedback/`)
}

export function sendLessonFeedback(topicId, rating) {
  return jsonRequest(`/topics/${topicId}/feedback/`, 'POST', { rating })
}

export function listPlacements() {
  return request('/placement/')
}

export function getPlacementTest(slug) {
  return request(`/placement/${slug}/`)
}

export function submitPlacement(slug, answers) {
  return request(`/placement/${slug}/`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ answers }),
  })
}

export function getDashboard() {
  return request('/dashboard/')
}

export function getLeaderboard() {
  return request('/leaderboard/')
}

export async function verifyCertificate(code) {
  const res = await fetch(`${API_BASE}/certificates/verify/${encodeURIComponent(code)}/`)
  const body = await res.json().catch(() => ({}))
  if (!res.ok) return { valid: false }
  return body
}

/* ───────── Boshqaruv paneli (faqat is_staff) ───────── */

function jsonRequest(path, method, payload) {
  return request(path, { method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
}

export function getAdminOverview(days = 30) {
  return request(`/admin/overview/?days=${days}`)
}

export function getAdminCourses() {
  return request('/admin/courses/')
}

export function getAdminCourse(bookId) {
  return request(`/admin/courses/${bookId}/`)
}

export function getAdminStats() {
  return request('/admin/stats/')
}

export function getAdminStudents(q = '') {
  return request(`/admin/students/${q ? `?q=${encodeURIComponent(q)}` : ''}`)
}

export function getAdminStudent(userId) {
  return request(`/admin/students/${userId}/`)
}

export function adminStudentAction(userId, action) {
  return jsonRequest(`/admin/students/${userId}/action/`, 'POST', { action })
}

export function listAdminSubjects() {
  return request('/admin/subjects/')
}

export function createAdminSubject(payload) {
  return jsonRequest('/admin/subjects/', 'POST', payload)
}

export function updateAdminSubject(id, payload) {
  return jsonRequest(`/admin/subjects/${id}/`, 'PATCH', payload)
}

export function deleteAdminSubject(id) {
  return request(`/admin/subjects/${id}/`, { method: 'DELETE' })
}

export function listAdminBooks() {
  return request('/admin/books/')
}

export function updateAdminBook(id, payload) {
  return jsonRequest(`/admin/books/${id}/`, 'PATCH', payload)
}

export function deleteAdminBook(id) {
  return request(`/admin/books/${id}/`, { method: 'DELETE' })
}

export function createAdminSection(bookId, payload) {
  return jsonRequest(`/admin/books/${bookId}/sections/`, 'POST', payload)
}

export function updateAdminSection(id, payload) {
  return jsonRequest(`/admin/sections/${id}/`, 'PATCH', payload)
}

export function deleteAdminSection(id) {
  return request(`/admin/sections/${id}/`, { method: 'DELETE' })
}

export function createAdminTopic(sectionId, payload) {
  return jsonRequest(`/admin/sections/${sectionId}/topics/`, 'POST', payload)
}

export function updateAdminTopic(id, payload) {
  return jsonRequest(`/admin/topics/${id}/`, 'PATCH', payload)
}

export function deleteAdminTopic(id) {
  return request(`/admin/topics/${id}/`, { method: 'DELETE' })
}

export function getAdminBookQuality(bookId) {
  return request(`/admin/books/${bookId}/quality/`)
}

export function getBookAnalytics(bookId) {
  return request(`/books/${bookId}/analytics/`)
}

export function getAdminTopicLesson(topicId) {
  return request(`/admin/topics/${topicId}/lesson/`)
}

export function saveAdminTopicLesson(topicId, lessonPlan) {
  return jsonRequest(`/admin/topics/${topicId}/lesson/`, 'PUT', { lesson_plan: lessonPlan })
}

export function getAdminTopicTest(topicId) {
  return request(`/admin/topics/${topicId}/test/`)
}

export function saveAdminTopicTest(topicId, questions) {
  return jsonRequest(`/admin/topics/${topicId}/test/`, 'PUT', { questions })
}
