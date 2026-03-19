import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'NextHire - AI-Powered Job Recommendation System',
  description: 'Transform your career with AI-powered resume analysis and personalized job recommendations',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
