import { useState } from 'react'
import './App.css'

function App() {
  const [mode, setMode] = useState('url')
  const [resume, setResume] = useState(null)
  const [jobUrl, setJobUrl] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [urlError, setUrlError] = useState(false)
  const handleAnalyze = async () => {
    console.log('Analyze button clicked')

    setLoading(true)
    setUrlError(false)
    setResults(null)
    const formData = new FormData()

    formData.append('file', resume)

    if (mode === 'url') {
      formData.append('url', jobUrl)
    } else {
      formData.append('job_description', jobDescription)
    }

    const endpoint =
      mode === 'url'
        ? 'http://127.0.0.1:8000/analyze-url'
        : 'http://127.0.0.1:8000/analyze-job-desc'

    const response = await fetch(endpoint, {
      method: 'POST',
      body: formData
    })

    const data = await response.json()

    console.log(data)

    if (data.job_description_found === false) {
      setLoading(false)
      setUrlError(true)
      setMode('paste')
      return
    }

    setResults(data)
    setLoading(false)
  }

  return (

    <div className="app">
      <h1>
        Resume<span>Pilot</span>
      </h1>

      <p>
        AI-powered resume & job matching
      </p>

      <div className="section">
        <h2>Resume</h2>

        <label className={`resume-upload ${resume ? 'uploaded' : ''}`}>
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setResume(e.target.files[0])}
          />

          {resume ? (
            <div className="upload-success">
              <span className="checkmark"></span>

              <div>
                <strong>{resume.name}</strong>
                <span>Resume attached successfully</span>
              </div>
            </div>
          ) : (
            <div className="upload-empty">
              <strong>Upload your resume</strong>
              <span>PDF files only</span>
            </div>
          )}
        </label>
      </div>

      <div className="section job-posting-section">
        <h2>Job Posting</h2>

        <div className="options">
          <button
            type="button"
            className={mode === 'url' ? 'active' : ''}
            onClick={() => {
              setMode('url')
              setUrlError(false)
            }}
          >
            Job URL
          </button>

          <button
            type="button"
            className={mode === 'paste' ? 'active' : ''}
            onClick={() => {
              setMode('paste')
              setUrlError(false)
            }}
          >
            Job Description
          </button>
        </div>

        {mode === 'url' && (
          <input
            type="text"
            placeholder="Paste job posting URL"
            value={jobUrl}
            onChange={(e) => {
              setJobUrl(e.target.value)
              setUrlError(false)
            }}
          />
        )}

        {mode === 'paste' && (
          <>
            {urlError && (
              <div className="url-error">
                No job description found at this URL. Please paste the job
                description below.
              </div>
            )}

            <textarea
              placeholder="Paste the job description here"
              rows="10"
              value={jobDescription}
              onChange={(e) => {
                setJobDescription(e.target.value)
                setUrlError(false)
              }}
            />
          </>
        )}

        {resume &&
          ((mode === 'url' && jobUrl.trim()) ||
            (mode === 'paste' && jobDescription.trim())) && (
            <button
              className={`analyze-button ${loading ? 'loading' : ''}`}
              onClick={handleAnalyze}
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Analyzing...
                </>
              ) : (
                'Analyze Resume'
              )}
            </button>
          )}

        {results && results.analysis && (
          <div className="results-section">
            <h2>Resume Analysis</h2>

            <div className="score-card">
              <span>Match Score</span>
              <strong>{results.analysis.match_score}%</strong>
            </div>

            <div className="results-card">
              <h3>Strengths</h3>

              <div className="tag-list">
                {results.analysis.strengths.map((strength, index) => (
                  <span key={index} className="tag">
                    {strength}
                  </span>
                ))}
              </div>
            </div>

            <div className="results-card">
              <h3>Skill Gaps</h3>

              <div className="tag-list">
                {results.analysis.skill_gaps.map((gap, index) => (
                  <span key={index} className="tag">
                    {gap}
                  </span>
                ))}
              </div>
            </div>

            <div className="results-card">
              <h3>Relevant Experience</h3>

              <ul>
                {results.analysis.relevant_experience.map(
                  (experience, index) => (
                    <li key={index}>{experience}</li>
                  )
                )}
              </ul>
            </div>

            <div className="results-card">
              <h3>Recommendations</h3>

              <ul>
                {results.analysis.recommendations.map(
                  (recommendation, index) => (
                    <li key={index}>{recommendation}</li>
                  )
                )}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>

  )
}

export default App