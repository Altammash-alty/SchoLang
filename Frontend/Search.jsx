import { useEffect }    from 'react'
import { useSearchParams } from 'react-router-dom'
import { useLanguage }   from '../context/LanguageContext'
import { useSearch }     from '../hooks/useSearch'
import SearchBar         from '../components/SearchBar'
import PaperCard         from '../components/PaperCard'

export default function Search() {
  const [params]              = useSearchParams()
  const { language }          = useLanguage()
  const { papers, loading, error, query, search } = useSearch()

  // Auto-search from URL params on load
  useEffect(() => {
    const q    = params.get('q')
    const lang = params.get('lang') || language
    if (q) search(q, lang)
  }, [])

  function handleSearch(q) {
    search(q, language)
    window.history.replaceState({}, '', `/search?q=${encodeURIComponent(q)}&lang=${language}`)
  }

  return (
    <main className="max-w-3xl mx-auto px-6 py-10">

      {/* Search bar */}
      <div className="mb-8">
        <SearchBar onSearch={handleSearch} loading={loading} initialValue={params.get('q') || ''} />
      </div>

      {/* Loading */}
      {loading && (
        <div className="space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="card animate-pulse">
              <div className="h-4 bg-gray-100 rounded w-3/4 mb-3" />
              <div className="h-3 bg-gray-100 rounded w-1/2 mb-4" />
              <div className="h-3 bg-gray-100 rounded w-full mb-2" />
              <div className="h-3 bg-gray-100 rounded w-5/6" />
            </div>
          ))}
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="text-center py-16 text-red-500 text-sm">{error}</div>
      )}

      {/* Results header */}
      {!loading && papers.length > 0 && (
        <div className="flex items-center justify-between mb-5">
          <p className="text-sm text-muted">
            <span className="font-medium text-ink">{papers.length} papers</span>
            {query && <> for <span className="font-medium text-ink">"{query}"</span></>}
          </p>
          <span className="tag">Sorted by relevance</span>
        </div>
      )}

      {/* Paper list */}
      {!loading && (
        <div className="space-y-4">
          {papers.map((paper, i) => (
            <PaperCard key={paper.doi || i} paper={paper} index={i} />
          ))}
        </div>
      )}

      {/* Empty state */}
      {!loading && !error && papers.length === 0 && query && (
        <div className="text-center py-20">
          <p className="text-4xl mb-4">🔍</p>
          <p className="text-ink font-medium mb-2">No papers found</p>
          <p className="text-sm text-muted">Try a different topic or broader keywords</p>
        </div>
      )}

    </main>
  )
}
