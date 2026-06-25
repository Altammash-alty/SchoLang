import { useState } from 'react'

export default function SearchBar({ onSearch, loading, initialValue = '' }) {
  const [query, setQuery] = useState(initialValue)

  function handleSubmit(e) {
    e.preventDefault()
    if (query.trim()) onSearch(query.trim())
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-3 w-full">
      <input
        type="text"
        className="input flex-1"
        placeholder="Type any research topic... e.g. AI for crop disease detection"
        value={query}
        onChange={e => setQuery(e.target.value)}
        disabled={loading}
      />
      <button
        type="submit"
        className="btn-primary whitespace-nowrap"
        disabled={loading || !query.trim()}
      >
        {loading ? (
          <span className="flex items-center gap-2">
            <span className="w-4 h-4 border-2 border-white border-t-transparent
                             rounded-full animate-spin" />
            Searching...
          </span>
        ) : 'Search'}
      </button>
    </form>
  )
}
