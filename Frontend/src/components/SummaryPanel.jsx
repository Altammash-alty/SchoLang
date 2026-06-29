import { useState } from 'react'
import { summarisePaper } from '../services/api'
import { useLanguage } from '../context/LanguageContext'

export default function SummaryPanel({ doi, abstract }) {
  const { language }          = useLanguage()
  const [summary,  setSummary]  = useState(null)
  const [loading,  setLoading]  = useState(false)
  const [expanded, setExpanded] = useState(false)

  async function handleSummarise() {
    if (summary) { setExpanded(!expanded); return }
    setLoading(true)
    try {
      const result = await summarisePaper(doi, abstract, language)
      setSummary(result)
      setExpanded(true)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mt-3">
      <button
        onClick={handleSummarise}
        disabled={loading || !abstract}
        className="text-xs text-accent hover:underline disabled:opacity-40
                   disabled:cursor-not-allowed font-medium"
      >
        {loading ? 'Summarising...' : expanded ? 'Hide summary ▲' : 'AI Summary ▼'}
      </button>

      {expanded && summary && (
        <div className="mt-3 space-y-3 bg-blue-50 rounded-lg p-4 border border-blue-100">

          {/* Plain summary */}
          {summary.summary && (
            <p className="text-sm text-ink leading-relaxed">{summary.summary}</p>
          )}

          {/* Key findings */}
          {summary.findings?.length > 0 && (
            <div>
              <p className="text-xs font-medium text-muted mb-1.5 uppercase tracking-wide">
                Key Findings
              </p>
              <ul className="space-y-1">
                {summary.findings.map((f, i) => (
                  <li key={i} className="text-sm text-ink flex gap-2">
                    <span className="text-accent flex-shrink-0">·</span>
                    {f}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Methodology */}
          {summary.methodology && (
            <div>
              <p className="text-xs font-medium text-muted mb-1 uppercase tracking-wide">
                Methodology
              </p>
              <p className="text-sm text-ink">{summary.methodology}</p>
            </div>
          )}

          {/* Limitations */}
          {summary.limitations && (
            <div>
              <p className="text-xs font-medium text-muted mb-1 uppercase tracking-wide">
                Limitations
              </p>
              <p className="text-sm text-ink">{summary.limitations}</p>
            </div>
          )}

        </div>
      )}
    </div>
  )
}
