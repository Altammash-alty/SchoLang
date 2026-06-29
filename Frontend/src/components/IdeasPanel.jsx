import { useState } from 'react'
import { generateIdeas } from '../services/api'
import { useLanguage } from '../context/LanguageContext'

const DIFFICULTY_COLOR = {
  Beginner: 'tag-success',
  Intermediate: 'tag-accent',
  Advanced: 'bg-orange-50 text-orange-600 border-orange-100 text-xs font-mono px-2 py-0.5 rounded border',
}

export default function IdeasPanel({ doi, title, abstract }) {
  const { language } = useLanguage()
  const [ideas, setIdeas] = useState(null)
  const [loading, setLoading] = useState(false)
  const [expanded, setExpanded] = useState(false)

  async function handleGenerate() {
    if (ideas) { setExpanded(!expanded); return }
    setLoading(true)
    try {
      const result = await generateIdeas(doi, title, abstract, language)
      setIdeas(result)
      setExpanded(true)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mt-2">
      <button
        onClick={handleGenerate}
        disabled={loading || !abstract}
        className="text-xs text-success hover:underline disabled:opacity-40
                   disabled:cursor-not-allowed font-medium"
      >
        {loading ? 'Generating ideas...' : expanded ? 'Hide project ideas ▲' : '★ Generate Project Ideas ▼'}
      </button>

      {expanded && ideas && (
        <div className="mt-3 space-y-3">
          {ideas.map((idea, i) => (
            <div key={i}
              className="bg-green-50 border border-green-100 rounded-lg p-4 space-y-2"
            >
              {/* Header */}
              <div className="flex items-start justify-between gap-2">
                <p className="text-sm font-semibold text-ink">{idea.title}</p>
                <span className={DIFFICULTY_COLOR[idea.difficulty] || 'tag'}>
                  {idea.difficulty}
                </span>
              </div>

              {/* Description */}
              <p className="text-sm text-gray-600">{idea.description}</p>

              {/* Tech stack */}
              {idea.tech_stack?.length > 0 && (
                <div className="flex flex-wrap gap-1.5">
                  {idea.tech_stack.map((t, j) => (
                    <span key={j} className="tag">{t}</span>
                  ))}
                </div>
              )}

              {/* Meta row */}
              <div className="flex items-center gap-4 text-xs text-muted pt-1">
                <span>⏱ {idea.build_time}</span>
                {idea.competition_angle && (
                  <span className="text-success">★ {idea.competition_angle}</span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
