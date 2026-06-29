import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home   from './pages/Home'
import Search from './pages/Search'
import Paper  from './pages/Paper'

export default function App() {
  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      <Routes>
        <Route path="/"              element={<Home />}   />
        <Route path="/search"        element={<Search />} />
        <Route path="/paper/:doi"    element={<Paper />}  />
      </Routes>
    </div>
  )
}
