import { useState } from 'react'
import { useLanguage } from '../context/LanguageContext'

export default function LanguageSelector() {
  const { language, setLanguage, LANGUAGES } = useLanguage()
  const [open, setOpen] = useState(false)

  const current = LANGUAGES.find(l => l.code === language)

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 text-sm text-muted hover:text-ink
                   border border-gray-200 rounded-lg px-3 py-1.5 transition-colors"
      >
        <span>{current.flag}</span>
        <span>{current.label}</span>
        <span className="text-xs opacity-50">▾</span>
      </button>

      {open && (
        <div className="absolute right-0 top-10 bg-white border border-gray-100
                        rounded-xl shadow-lg z-50 w-44 py-1 overflow-hidden">
          {LANGUAGES.map(lang => (
            <button
              key={lang.code}
              onClick={() => { setLanguage(lang.code); setOpen(false) }}
              className={`w-full flex items-center gap-3 px-4 py-2.5 text-sm
                          hover:bg-surface transition-colors text-left
                          ${language === lang.code ? 'text-accent font-medium' : 'text-ink'}`}
            >
              <span>{lang.flag}</span>
              <span>{lang.label}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
