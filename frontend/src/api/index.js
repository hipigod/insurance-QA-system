import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000
})

api.interceptors.request.use(
  config => config,
  error => Promise.reject(error)
)

api.interceptors.response.use(
  response => {
    const payload = response.data
    if (payload && payload.success) {
      return payload.data
    }
    const message = payload?.message || 'Request failed'
    return Promise.reject(new Error(message))
  },
  error => {
    console.error('API error:', error)
    return Promise.reject(error)
  }
)

export default api
