'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import Navbar from '@/components/Navbar'
import Hero from '@/components/Hero'
import Features from '@/components/Features'
import ResumeUploader from '@/components/ResumeUploader'
import AnalysisTabs from '@/components/AnalysisTabs'
import JobCard from '@/components/JobCard'
import Footer from '@/components/Footer'
import { MapPin, CheckCircle, Loader2, AlertCircle } from 'lucide-react'
import { analyzeResume, fetchJobs } from '@/lib/api'
import { Job } from '@/lib/types'

const locations = [
  { value: 'India', label: 'India' },
  { value: 'USA', label: 'United States' },
  { value: 'UK', label: 'United Kingdom' },
  { value: 'Remote', label: 'Remote' },
  { value: 'All', label: 'All Locations' },
]

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [selectedLocation, setSelectedLocation] = useState('India')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisComplete, setAnalysisComplete] = useState(false)
  const [isSearchingJobs, setIsSearchingJobs] = useState(false)
  
  // Analysis results
  const [analysisResult, setAnalysisResult] = useState({
    summary: '',
    skillGaps: '',
    roadmap: '',
    keywords: '',
  })
  
  const [jobs, setJobs] = useState<Job[]>([])
  const [error, setError] = useState<string | null>(null)

  const handleAnalyze = async () => {
    if (!selectedFile) return

    setIsAnalyzing(true)
    setAnalysisComplete(false)
    setError(null)

    try {
      const response = await analyzeResume(selectedFile, selectedLocation)
      
      setAnalysisResult({
        summary: response.data.summary,
        skillGaps: response.data.skillGaps,
        roadmap: response.data.roadmap,
        keywords: response.data.keywords,
      })

      setAnalysisComplete(true)

      setIsSearchingJobs(true)
      const jobsResponse = await fetchJobs(response.data.keywords, selectedLocation)
      setJobs(jobsResponse.data || [])
      setIsSearchingJobs(false)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Analysis failed. Please try again.'
      setError(message)
      console.error('Analysis failed:', err)
    } finally {
      setIsAnalyzing(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <Hero />
      
      {/* Upload Section */}
      <section id="upload" className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="section-title">
              Get Your Free{' '}
              <span className="gradient-text">Career Analysis</span>
            </h2>
            <p className="section-subtitle mx-auto">
              Upload your resume and discover personalized insights to accelerate your career growth
            </p>
          </motion.div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
            {/* Upload Card */}
            <div className="lg:col-span-2">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                className="card"
              >
                <h3 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2">
                  <span className="bg-gradient-to-br from-primary-600 to-primary-700 p-2 rounded-lg">
                    📄
                  </span>
                  Upload Your Resume
                </h3>
                <ResumeUploader
                  onFileSelect={setSelectedFile}
                  selectedFile={selectedFile}
                  isLoading={isAnalyzing}
                />
              </motion.div>
            </div>

            {/* Preferences Card */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="card"
            >
              <h3 className="text-xl font-bold text-slate-900 mb-6 flex items-center gap-2">
                <span className="bg-gradient-to-br from-secondary-600 to-secondary-700 p-2 rounded-lg">
                  ⚙️
                </span>
                Job Preferences
              </h3>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-3">
                    Preferred Location
                  </label>
                  <div className="relative">
                    <MapPin className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <select
                      value={selectedLocation}
                      onChange={(e) => setSelectedLocation(e.target.value)}
                      className="input-field pl-12 appearance-none bg-white"
                    >
                      {locations.map((loc) => (
                        <option key={loc.value} value={loc.value}>
                          {loc.label}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <button
                  onClick={handleAnalyze}
                  disabled={!selectedFile || isAnalyzing}
                  className="btn-primary w-full flex items-center justify-center gap-2"
                >
                  {isAnalyzing ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <CheckCircle className="w-5 h-5" />
                      Analyze Resume
                    </>
                  )}
                </button>

                {!selectedFile && (
                  <p className="text-sm text-slate-500 text-center">
                    Please upload your resume to begin
                  </p>
                )}

                {error && (
                  <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                    <AlertCircle className="w-4 h-4 flex-shrink-0" />
                    <span>{error}</span>
                  </div>
                )}
              </div>
            </motion.div>
          </div>

          {/* Analysis Results */}
          {analysisComplete && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-16"
            >
              {/* Analysis Tabs */}
              <AnalysisTabs
                summary={analysisResult.summary}
                skillGaps={analysisResult.skillGaps}
                roadmap={analysisResult.roadmap}
                keywords={analysisResult.keywords}
              />

              {/* Jobs Section */}
              <div className="mt-12">
                <div className="flex items-center justify-between mb-8">
                  <div>
                    <h3 className="text-3xl font-bold text-slate-900 mb-2">
                      Matching Job Opportunities
                    </h3>
                    <p className="text-slate-600">
                      Based on your profile, we found {jobs.length} relevant positions
                    </p>
                  </div>
                </div>

                {isSearchingJobs ? (
                  <div className="flex flex-col items-center justify-center py-16">
                    <Loader2 className="w-12 h-12 text-primary-600 animate-spin mb-4" />
                    <p className="text-slate-600 font-medium">Searching for matching jobs...</p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {jobs.map((job, index) => (
                      <JobCard key={job.id} job={job} index={index} />
                    ))}
                  </div>
                )}
              </div>

              {/* Success Message */}
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="mt-12 bg-gradient-to-r from-green-50 to-green-100 border border-green-200 rounded-2xl p-8 text-center"
              >
                <CheckCircle className="w-16 h-16 text-green-600 mx-auto mb-4" />
                <h3 className="text-2xl font-bold text-green-900 mb-2">
                  Analysis Complete!
                </h3>
                <p className="text-green-700">
                  Your personalized career roadmap is ready. Keep learning and growing!
                </p>
              </motion.div>
            </motion.div>
          )}
        </div>
      </section>

      <Features />
      <Footer />
    </div>
  )
}
