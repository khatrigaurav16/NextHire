'use client'

import { motion } from 'framer-motion'
import { FileSearch, Target, Briefcase, Sparkles, Shield, Map } from 'lucide-react'
import { LucideIcon } from 'lucide-react'

const features: Array<{
  icon: LucideIcon
  title: string
  description: string
  color: string
}> = [
  {
    icon: FileSearch,
    title: 'Smart Resume Analysis',
    description: 'AI-powered extraction of key skills, experiences, and qualifications from your resume',
    color: 'from-blue-500 to-blue-600',
  },
  {
    icon: Target,
    title: 'Skill Gap Detection',
    description: 'Identify missing skills and get actionable recommendations for career growth',
    color: 'from-red-500 to-red-600',
  },
  {
    icon: Briefcase,
    title: 'Personalized Job Matching',
    description: 'Get job recommendations tailored to your unique profile and preferences',
    color: 'from-green-500 to-green-600',
  },
  {
    icon: Map,
    title: 'Learning Roadmap',
    description: 'Customized learning path to bridge your skill gaps and advance your career',
    color: 'from-purple-500 to-purple-600',
  },
  {
    icon: Sparkles,
    title: 'AI-Powered Insights',
    description: 'Leverage advanced AI to get personalized career advice and recommendations',
    color: 'from-yellow-500 to-orange-500',
  },
  {
    icon: Shield,
    title: 'Privacy First',
    description: 'Your data is secure. We never share your personal information with third parties',
    color: 'from-indigo-500 to-indigo-600',
  },
]

export default function Features() {
  return (
    <section id="features" className="py-24 bg-slate-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="section-title">
            Powerful Features for{' '}
            <span className="gradient-text">Career Success</span>
          </h2>
          <p className="section-subtitle mx-auto">
            Everything you need to transform your career and land your dream job
          </p>
        </motion.div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="group card hover:scale-105"
            >
              <div className={`inline-flex p-4 rounded-2xl bg-gradient-to-br ${feature.color} mb-6 shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                {(() => {
                  const Icon = feature.icon
                  return <Icon className="w-8 h-8 text-white" />
                })()}
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">
                {feature.title}
              </h3>
              <p className="text-slate-600 leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
