'use client'

import { useCallback, useState } from 'react'
import { motion } from 'framer-motion'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react'
import clsx from 'clsx'

interface ResumeUploaderProps {
  onFileSelect: (file: File) => void
  selectedFile: File | null
  isLoading: boolean
}

export default function ResumeUploader({ onFileSelect, selectedFile, isLoading }: ResumeUploaderProps) {
  const [dragActive, setDragActive] = useState(false)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles[0]) {
      onFileSelect(acceptedFiles[0])
    }
  }, [onFileSelect])

  const { getRootProps, getInputProps, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
    },
    maxFiles: 1,
    disabled: isLoading,
    onDragEnter: () => setDragActive(true),
    onDragLeave: () => setDragActive(false),
  })

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full"
    >
      <div
        {...getRootProps()}
          className={clsx(
            'relative border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300 cursor-pointer',
            dragActive && !isDragReject && 'border-primary-500 bg-primary-50',
            isDragReject && 'border-red-500 bg-red-50',
            !dragActive && !selectedFile && 'border-slate-300 hover:border-primary-400 hover:bg-slate-50',
            selectedFile && !dragActive && 'border-green-500 bg-green-50',
            isLoading && 'opacity-50 cursor-not-allowed'
          )}
      >
        <input {...getInputProps()} />
        
        {selectedFile ? (
          <motion.div
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            className="flex flex-col items-center"
          >
            <CheckCircle className="w-16 h-16 text-green-500 mb-4" />
            <FileText className="w-12 h-12 text-primary-600 mb-4" />
            <p className="text-lg font-semibold text-slate-900 mb-2">
              {selectedFile.name}
            </p>
            <p className="text-sm text-slate-600">
              {(selectedFile.size / 1024 / 1024).toFixed(2)} MB • PDF
            </p>
            {!isLoading && (
              <p className="text-sm text-primary-600 mt-4 font-medium">
                Click or drag to replace
              </p>
            )}
          </motion.div>
        ) : isDragReject ? (
          <motion.div
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            className="flex flex-col items-center"
          >
            <AlertCircle className="w-16 h-16 text-red-500 mb-4" />
            <p className="text-lg font-semibold text-red-600">
              Invalid file type
            </p>
            <p className="text-sm text-slate-600 mt-2">
              Please upload a PDF file
            </p>
          </motion.div>
        ) : (
          <motion.div
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            className="flex flex-col items-center"
          >
            <Upload className={clsx(
              'w-16 h-16 mb-4 transition-colors',
              dragActive ? 'text-primary-600' : 'text-slate-400'
            )} />
            <p className="text-lg font-semibold text-slate-900 mb-2">
              {dragActive ? 'Drop your resume here' : 'Drag & drop your resume'}
            </p>
            <p className="text-sm text-slate-600 mb-4">
              or click to browse your files
            </p>
            <p className="text-xs text-slate-500">
              Supported format: PDF (Max 10MB)
            </p>
          </motion.div>
        )}
      </div>

      {isLoading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-4 flex items-center justify-center gap-3"
        >
          <div className="animate-spin rounded-full h-5 w-5 border-2 border-primary-600 border-t-transparent" />
          <span className="text-slate-600 font-medium">Processing your resume...</span>
        </motion.div>
      )}
    </motion.div>
  )
}
