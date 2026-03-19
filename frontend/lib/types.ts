export interface Job {
  id: string
  title: string
  companyName: string
  location: string
  type: string
  seniority: string
  skills: string[]
  link: string
  salary?: string
  posted?: string
}

export interface AnalysisResult {
  summary: string
  skillGaps: string
  roadmap: string
  keywords: string
}

export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}
