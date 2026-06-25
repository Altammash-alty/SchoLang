import { Link } from 'react-router-dom'
import LanguageSelector from './LanguageSelector'

export default function Navbar() {
  return (
    <nav className="border-b border-gray-100 bg-white sticky top-0 z-50">
      <div className="max-w-5xl mx-auto px-6 h-14 flex items-center justify-between">

        {/* Brand */}
        <Link to="/" className="text-xl font-semibold tracking-tight">
          <span className="text-ink">Scho</span>
          <span className="text-accent">Lang</span>
        </Link>

        {/* Right side */}
        <div className="flex items-center gap-4">
          <LanguageSelector />
          <Link to="/search" className="btn-primary text-sm">
            Search Papers
          </Link>
        </div>

      </div>
    </nav>
  )
}
