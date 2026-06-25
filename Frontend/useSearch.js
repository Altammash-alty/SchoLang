import { useState } from 'react'
import { searchPapers } from '../services/api'

export function useSearch() {
  const [papers,  setPapers]  = useState([])
  const [loading, setLoading] = useState(false)
  const [error,   setError]   = useState(null)
  const [query,   setQuery]   = useState('')

  async function search(q, language) {
    if (!q.trim()) return
    setLoading(true)
    setError(null)
    setQuery(q)
    try {
      const results = await searchPapers(q, language)
      setPapers(results)
    } catch (err) {
      setError('Search failed. Please try again.')
      setPapers([])
    } finally {
      setLoading(false)
    }
  }

  function clear() {
    setPapers([])
    setQuery('')
    setError(null)
  }

  return { papers, loading, error, query, search, clear }
}
