import { useParams, Link } from 'react-router-dom'

// Single paper page — placeholder for Phase 3 expansion
export default function Paper() {
  const { doi } = useParams()

  return (
    <main className="max-w-3xl mx-auto px-6 py-10">
      <Link to="/search" className="text-sm text-muted hover:text-ink mb-6 inline-block">
        ← Back to search
      </Link>
      <div className="card">
        <p className="text-xs font-mono text-muted mb-3">DOI</p>
        <p className="text-sm text-ink font-medium break-all">{doi}</p>
        <p className="text-sm text-muted mt-4">
          Full paper detail page — coming in Phase 3.
        </p>
      </div>
    </main>
  )
}
