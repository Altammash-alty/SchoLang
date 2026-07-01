import SummaryPanel from '../../components/SummaryPanel'
import IdeasPanel from './IdeasPanel'

const SOURCE_COLORS = {
  'Semantic Scholar': 'bg-blue-50   text-blue-600   border-blue-100',
  'OpenAlex': 'bg-purple-50 text-purple-600 border-purple-100',
  'arXiv': 'bg-red-50    text-red-600    border-red-100',
  'PubMed': 'bg-green-50  text-green-600  border-green-100',
}

export default function PaperCard({ paper, index }) {
  const authors = paper.authors?.slice(0, 3).join(', ')
  const hasMore = paper.authors?.length > 3
  const sourceTag = SOURCE_COLORS[paper.source] || 'bg-gray-50 text-gray-500 border-gray-100'

  return (
    <div className="card group">

      {/* Top row — index + source + year */}
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-mono text-muted">#{String(index + 1).padStart(2, '0')}</span>
        <div className="flex items-center gap-2">
          <span className={`tag text-xs border ${sourceTag}`}>{paper.source}</span>
          {paper.year && <span className="tag">{paper.year}</span>}
        </div>
      </div>

      {/* Title */}
      <h3 className="text-base font-semibold text-ink leading-snug mb-2 group-hover:text-accent
                     transition-colors">
        {paper.url ? (
          <a href={paper.url} target="_blank" rel="noreferrer">{paper.title}</a>
        ) : paper.title}
      </h3>

      {/* Authors */}
      {authors && (
        <p className="text-xs text-muted mb-3">
          {authors}{hasMore && ' et al.'}
        </p>
      )}

      {/* Abstract preview */}
      {paper.abstract && (
        <p className="text-sm text-gray-500 leading-relaxed line-clamp-3 mb-1">
          {paper.abstract}
        </p>
      )}

      {/* DOI */}
      {paper.doi && (
        <p className="text-xs text-muted mt-2">
          DOI:&nbsp;
          <a
            href={`https://doi.org/${paper.doi}`}
            target="_blank"
            rel="noreferrer"
            className="text-accent hover:underline"
          >
            {paper.doi}
          </a>
        </p>
      )}

      {/* AI panels */}
      <div className="mt-3 pt-3 border-t border-gray-50 space-y-1">
        <SummaryPanel doi={paper.doi} abstract={paper.abstract} />
        <IdeasPanel doi={paper.doi} title={paper.title} abstract={paper.abstract} />
      </div>

    </div>
  )
}
