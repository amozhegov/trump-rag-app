import { useState } from 'react'
import './App.css'

const API_URL = 'http://127.0.0.1:8000'

function App() {
  const [keyword, setKeyword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)

  async function handleAnalyze(e) {
    e.preventDefault()
    const q = keyword.trim()
    if (!q) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const res = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ keyword: q }),
      })

      if (!res.ok) {
        const text = await res.text()
        throw new Error(text || `HTTP ${res.status}`)
      }

      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err.message || 'Request failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page">
      <header className="header">
        <h1>Trump RAG</h1>
        <p>Keyword → transcript → sentiment → Trump-style summary</p>
  </header>

      <form className="search-box" onSubmit={handleAnalyze}>
        <input
          type="text"
          placeholder="Enter a keyword (e.g. Italy)"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          disabled={loading}
        />
        <button type="submit" disabled={loading || !keyword.trim()}>
          {loading ? 'Analyzing…' : 'Analyze'}
        </button>
      </form>

      {loading && (
        <div className="card status">
          Searching and generating summary. This may take 5–30 seconds…
        </div>
      )}

      {error && (
        <div className="card error">
          {error}
        </div>
      )}

      {result && !result.found && (
        <div className="card status">
          {result.message || 'Nothing found for this keyword.'}
        </div>
      )}

      {result && result.found && (
        <div className="results">
          <div className="card">
            <div className="card-title">Sentiment</div>
            <span className={`badge ${result.sentiment}`}>
              {(result.sentiment || 'unknown').toUpperCase()}
            </span>
          </div>

          <div className="card">
            <div className="card-title">Transcript excerpt</div>
            <p className="body-text">{result.transcript_excerpt}</p>
          </div>

          <div className="card">
            <div className="card-title">Trump-style summary</div>
            <p className="summary-text">{result.summary}</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default App