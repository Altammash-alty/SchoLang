import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="bg-surface border-t border-gray-100 mt-auto">
      <div className="max-w-5xl mx-auto px-6 py-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          
          {/* Brand & Description */}
          <div className="md:col-span-2">
            <Link to="/" className="text-lg font-semibold tracking-tight">
              <span className="text-ink">Scho</span>
              <span className="text-accent">Lang</span>
            </Link>
            <p className="mt-2 text-sm text-muted max-w-sm leading-relaxed">
              Empowering global research by translating, summarizing, and turning academic papers into buildable project ideas.
            </p>
          </div>

          {/* Features Column */}
          <div>
            <h3 className="text-xs font-semibold text-ink uppercase tracking-wider">Features</h3>
            <ul className="mt-2 space-y-1.5">
              <li>
                <Link to="/search" className="text-sm text-muted hover:text-accent transition-colors">
                  Semantic Search
                </Link>
              </li>
              <li>
                <span className="text-sm text-muted">
                  Multi-language RAG
                </span>
              </li>
              <li>
                <span className="text-sm text-muted">
                  Project Generator
                </span>
              </li>
            </ul>
          </div>

          {/* Contact & Support Column */}
          <div>
            <h3 className="text-xs font-semibold text-ink uppercase tracking-wider">Contact & Support</h3>
            <ul className="mt-2 space-y-1.5">
              <li>
                <a 
                  href="mailto:support@scholang.org" 
                  className="text-sm text-muted hover:text-accent transition-colors"
                >
                  Contact Us
                </a>
              </li>
              <li>
                <a 
                  href="https://github.com" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="text-sm text-muted hover:text-accent transition-colors"
                >
                  GitHub Repository
                </a>
              </li>
              <li>
                <span className="text-sm text-muted">Documentation</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-6 pt-3 border-t border-gray-200/50 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-muted">
            &copy; {new Date().getFullYear()} SchoLang. All rights reserved.
          </p>
          <div className="flex gap-4">
            <span className="text-xs text-muted hover:text-ink cursor-pointer">Privacy Policy</span>
            <span className="text-xs text-muted hover:text-ink cursor-pointer">Terms of Service</span>
          </div>
        </div>
      </div>

    </footer>

  )
}
