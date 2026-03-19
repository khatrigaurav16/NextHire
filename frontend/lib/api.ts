import axios from 'axios'
import { Job, AnalysisResult } from './types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,
})

export const analyzeResume = async (file: File, location: string) => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('location', location)

  const response = await api.post('/api/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export const fetchJobs = async (keywords: string, location: string) => {
  const response = await api.get('/api/jobs', {
    params: { keywords, location },
  })
  return response.data
}

export const generateKeywords = async (summary: string) => {
  const response = await api.post('/api/keywords', { summary })
  return response.data
}

export default api
