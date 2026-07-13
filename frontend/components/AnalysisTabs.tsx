'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { FileText, Target, Map, Briefcase } from 'lucide-react'
import clsx from 'clsx'

interface AnalysisTabsProps {
  summary: string
  skillGaps: string
  roadmap: string
  keywords: string
}

export default function AnalysisTabs({ summary, skillGaps, roadmap, keywords }: AnalysisTabsProps) {
  const [activeTab, setActiveTab] = useState(0)

  const tabs = [
    { id: 0, name: 'Resume Summary', icon: FileText, color: 'primary' },
    { id: 1, name: 'Skill Gaps', icon: Target, color: 'red' },
    { id: 2, name: 'Learning Roadmap', icon: Map, color: 'green' },
    { id: 3, name: 'Keywords', icon: Briefcase, color: 'purple' },
  ]

  const contents = [
    { content: summary, type: 'summary' },
    { content: skillGaps, type: 'list' },
    { content: roadmap, type: 'roadmap' },
    { content: '', type: 'jobs' },
  ]

  return (
    <div className="w-full">
      {/* Tab Navigation */}
      <div className="flex flex-wrap gap-2 mb-6 bg-white p-2 rounded-xl shadow-md border border-slate-200/50">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={clsx(
              'flex items-center gap-2 px-5 py-3 rounded-lg font-semibold transition-all duration-300',
              activeTab === tab.id
                ? 'bg-gradient-to-r from-primary-600 to-primary-700 text-white shadow-md'
                : 'text-slate-600 hover:bg-slate-100'
            )}
          >
            <tab.icon className="w-5 h-5" />
            <span className="hidden sm:inline">{tab.name}</span>
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <motion.div
        key={activeTab}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="bg-white rounded-2xl shadow-lg border border-slate-200/50 p-8"
      >
        {activeTab === 0 && (
          <div>
            <h3 className="text-2xl font-bold text-slate-900 mb-4 flex items-center gap-3">
              <FileText className="w-7 h-7 text-primary-600" />
              Professional Summary
            </h3>
            <div className="prose prose-slate max-w-none">
              <p className="text-slate-700 leading-relaxed text-lg whitespace-pre-wrap">
                {summary}
              </p>
            </div>
          </div>
        )}

        {activeTab === 1 && (
          <div>
            <h3 className="text-2xl font-bold text-slate-900 mb-4 flex items-center gap-3">
              <Target className="w-7 h-7 text-red-600" />
              Identified Skill Gaps
            </h3>
            <div className="prose prose-slate max-w-none">
              <p className="text-slate-700 leading-relaxed text-lg whitespace-pre-wrap">
                {skillGaps}
              </p>
            </div>
          </div>
        )}

        {activeTab === 2 && (
          <div>
            <h3 className="text-2xl font-bold text-slate-900 mb-4 flex items-center gap-3">
              <Map className="w-7 h-7 text-green-600" />
              Your Learning Journey
            </h3>
            <div className="prose prose-slate max-w-none">
              <p className="text-slate-700 leading-relaxed text-lg whitespace-pre-wrap">
                {roadmap}
              </p>
            </div>
          </div>
        )}

        {activeTab === 3 && (
          <div>
            <h3 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-3">
              <Briefcase className="w-7 h-7 text-purple-600" />
              Recommended Keywords
            </h3>
            <div className="flex flex-wrap gap-3 mb-6">
              {keywords.split(',').map((keyword, idx) => (
                <span
                  key={idx}
                  className="px-5 py-2 bg-gradient-to-r from-primary-600 to-primary-700 text-white rounded-full font-semibold shadow-md"
                >
                  🔍 {keyword.trim()}
                </span>
              ))}
            </div>
          </div>
        )}
      </motion.div>
    </div>
  )
}
