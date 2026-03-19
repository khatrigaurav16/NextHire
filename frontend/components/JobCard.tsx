'use client'

import { motion } from 'framer-motion'
import { MapPin, Briefcase, TrendingUp, ExternalLink } from 'lucide-react'
import { Job } from '@/lib/types'
import clsx from 'clsx'

interface JobCardProps {
  job: Job
  index: number
}

export default function JobCard({ job, index }: JobCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
      className="group card hover:scale-[1.02]"
    >
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-bold text-slate-900 mb-2 group-hover:text-primary-600 transition-colors">
            {job.title}
          </h3>
          <p className="text-primary-600 font-semibold flex items-center gap-2">
            <Briefcase className="w-4 h-4" />
            {job.companyName}
          </p>
        </div>
      </div>

      {/* Meta Information */}
      <div className="flex flex-wrap gap-3 mb-4">
        <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-100 rounded-lg text-sm text-slate-700">
          <MapPin className="w-4 h-4" />
          {job.location}
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-100 rounded-lg text-sm text-slate-700">
          <Briefcase className="w-4 h-4" />
          {job.type}
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-100 rounded-lg text-sm text-slate-700">
          <TrendingUp className="w-4 h-4" />
          {job.seniority}
        </div>
      </div>

      {/* Skills */}
      {job.skills && job.skills.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          {job.skills.slice(0, 5).map((skill, idx) => (
            <span
              key={idx}
              className="px-3 py-1 bg-gradient-to-r from-primary-50 to-primary-100 text-primary-700 rounded-full text-sm font-medium border border-primary-200"
            >
              {skill}
            </span>
          ))}
        </div>
      )}

      {/* Salary & Apply Button */}
      <div className="flex justify-between items-center pt-4 border-t border-slate-100">
        {job.salary && (
          <p className="text-sm text-slate-600">
            💰 {job.salary}
          </p>
        )}
        <a
          href={job.link}
          target="_blank"
          rel="noopener noreferrer"
          className="ml-auto flex items-center gap-2 bg-gradient-to-r from-primary-600 to-primary-700 text-white px-5 py-2.5 rounded-xl font-semibold hover:from-primary-700 hover:to-primary-800 transition-all shadow-md hover:shadow-lg"
        >
          Apply Now
          <ExternalLink className="w-4 h-4" />
        </a>
      </div>
    </motion.div>
  )
}
