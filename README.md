# NextHire - AI-Powered Job Recommendation System

<div align="center">

![NextHire Logo](https://img.shields.io/badge/NextHire-AI%20Powered-2563EB?style=for-the-badge&logo=target)
![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)

*Transform your career with AI-powered insights and personalized recommendations*

</div>

## Features

- **Smart Resume Upload** - Drag & drop interface with PDF validation and 10MB size limit
- **AI-Powered Analysis** - Gemini-powered resume analysis, skill gap identification, and learning roadmap generation
- **Personalized Roadmaps** - Custom learning paths based on your profile
- **Job Matching** - AI-suggested keywords for targeted job hunting
- **Job Source Integration** - JoinRise job API for matching opportunities
- **Beautiful UI** - Modern, responsive design with smooth Framer Motion animations
- **Fully Responsive** - Works on mobile, tablet, and desktop

## Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **UI**: React 18 + TypeScript
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Icons**: Lucide React

### Backend
- **Framework**: FastAPI (Python)
- **AI**: Google Gemini API
- **PDF Processing**: PyMuPDF
- **Job API**: JoinRise

## Project Structure

```
NextHire/
├── frontend/                 # Next.js 14 React application
│   ├── app/
│   │   ├── page.tsx         # Main landing page
│   │   ├── layout.tsx       # Root layout
│   │   └── globals.css      # Global styles
│   ├── components/
│   │   ├── Navbar.tsx       # Navigation bar
│   │   ├── Hero.tsx         # Hero section
│   │   ├── Features.tsx     # Features section
│   │   ├── ResumeUploader.tsx # Resume upload component
│   │   ├── AnalysisTabs.tsx # Analysis results tabs
│   │   ├── JobCard.tsx      # Individual job card
│   │   └── Footer.tsx       # Footer component
│   ├── lib/
│   │   ├── types.ts         # TypeScript interfaces
│   │   └── api.ts           # API client
│   ├── package.json
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── backend/                  # FastAPI backend
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
│
├── src/                      # Legacy Streamlit code (deprecated)
│   ├── helper.py
│   ├── job_api.py
│   └── __init__.py
│
├── main.py                   # Legacy Streamlit app (deprecated)
├── .gitignore
├── README.md
└── LICENSE
```

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Gemini API key (get one at [Google AI Studio](https://makersuite.google.com/app/apikey))

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local

# Edit .env.local and add your API URL:
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000)

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env and add your API keys:
# GEMINI_API_KEY=your_gemini_api_key
# JSEARCH_API_KEY=your_jsearch_api_key (optional)

# Start server
uvicorn main:app --reload --port 8000
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for API documentation

## Environment Variables

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
JSEARCH_API_KEY=your_jsearch_api_key_here
ALLOWED_ORIGINS=http://localhost:3000
```

## API Endpoints

### POST `/api/analyze`
Upload resume and get AI analysis.

**Request:**
- `file`: PDF file (max 10MB)
- `location`: Preferred job location (India, USA, UK, Remote, All)

**Response:**
```json
{
  "success": true,
  "data": {
    "summary": "Professional summary...",
    "skillGaps": "Skill gaps analysis...",
    "roadmap": "Learning roadmap...",
    "keywords": "keyword1, keyword2, keyword3"
  }
}
```

### GET `/api/jobs`
Fetch matching job opportunities from JoinRise.

**Query Parameters:**
- `keywords`: Job search keywords
- `location`: Preferred location

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "1",
      "title": "Job Title",
      "companyName": "Company",
      "location": "Location",
      "type": "Full-time",
      "seniority": "Senior",
      "skills": ["Python", "React"],
      "link": "https://..."
    }
  ]
}
```

### POST `/api/keywords`
Generate job search keywords from summary.

**Request:**
```json
{
  "summary": "Resume summary text..."
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "keywords": "keyword1, keyword2, keyword3"
  }
}
```

### GET `/health`
Health check endpoint.

## Deployment

### Deploy Backend to Railway

1. Create account at [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Set environment variables:
   - `GEMINI_API_KEY`
   - `ALLOWED_ORIGINS` (your Vercel frontend URL)
4. Railway will auto-detect FastAPI and install dependencies
5. Deploy!

### Deploy Frontend to Vercel

1. Create account at [vercel.com](https://vercel.com)
2. Import your frontend repository
3. Set environment variable:
   - `NEXT_PUBLIC_API_URL` = your-railway-backend-url
4. Vercel will auto-detect Next.js and build
5. Deploy!

## Design Highlights

- **Gradient backgrounds** with animated floating elements
- **Glass morphism** effects for modern aesthetic
- **Smooth animations** using Framer Motion
- **Professional color scheme** with Tailwind CSS
- **Responsive grid layouts** that adapt to all screen sizes
- **Interactive components** with hover effects and transitions
- **Clean typography** using Inter font family

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Google Gemini API](https://ai.google.dev/) for AI capabilities
- [Vercel](https://vercel.com) for hosting the frontend
- [Railway](https://railway.app) for hosting the backend
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [Framer Motion](https://www.framer.com/motion/) for animations
