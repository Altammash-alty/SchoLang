import { useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { useLanguage } from '../context/LanguageContext'

const EXAMPLES = [
  'AI for crop disease detection',
  'Quantum computing drug discovery',
  'Transformer models low resource languages',
  'Solar energy storage innovations',
]

export default function Home() {
  const navigate = useNavigate()
  const { language } = useLanguage()
  const [query, setQuery] = useState('')

  function handleSearch(e) {
    e.preventDefault()
    if (query.trim()) navigate(`/search?q=${encodeURIComponent(query)}&lang=${language}`)
  }

  return (
    <main className="max-w-3xl mx-auto px-6 pt-24 pb-20 text-center">

      {/* Hero */}
      <div className="mb-10">
        <span className="text-xs font-mono text-accent bg-blue-50 border border-blue-100
                         px-3 py-1 rounded-full">
          Research Intelligence Platform
        </span>
        <h1 className="mt-6 text-5xl font-semibold text-ink leading-tight tracking-tight">
          Find research.<br />
          <span className="text-accent">Understand it.</span><br />
          Build with it.
        </h1>
        <p className="mt-5 text-lg text-muted max-w-xl mx-auto leading-relaxed">
          Type any topic. Get real papers, plain-language summaries, and
          buildable project ideas — in your language.
        </p>
      </div>

      {/* Search */}
      <form onSubmit={handleSearch} className="flex gap-3 mb-6">
        <input
          type="text"
          className="input flex-1 text-base"
          placeholder="Type a research topic..."
          value={query}
          onChange={e => setQuery(e.target.value)}
        />
        <button type="submit" className="btn-primary px-8">
          Search
        </button>
      </form>

      {/* Examples */}
      <div className="flex flex-wrap justify-center gap-2 mb-16">
        {EXAMPLES.map(ex => (
          <button
            key={ex}
            onClick={() => navigate(`/search?q=${encodeURIComponent(ex)}&lang=${language}`)}
            className="tag hover:border-accent hover:text-accent transition-colors cursor-pointer"
          >
            {ex}
          </button>
        ))}
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 border-t border-gray-100 pt-10">
        {[
          ['300M+', 'Papers indexed'],
          ['8', 'Languages'],
          ['4', 'Databases'],
        ].map(([num, label]) => (
          <div key={label}>
            <p className="text-3xl font-semibold text-accent">{num}</p>
            <p className="text-sm text-muted mt-1">{label}</p>
          </div>
        ))}
      </div>

    </main>
  )
}
