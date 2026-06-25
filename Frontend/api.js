import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

// Search papers across all 4 databases
export async function searchPapers(query, language = 'en', limit = 10) {
  const res = await api.post('/search', { query, language, limit })
  return res.data
}

// Summarise a single paper
export async function summarisePaper(doi, abstract, language = 'en') {
  const res = await api.post('/summarise', { doi, abstract, language })
  return res.data.summary
}

// Generate project ideas from a paper
export async function generateIdeas(doi, title, abstract, language = 'en') {
  const res = await api.post('/ideas', { doi, title, abstract, language })
  return res.data.ideas
}
