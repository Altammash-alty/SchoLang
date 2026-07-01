import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Home   from './pages/Home'
import Search from './pages/Search'
import Paper  from './pages/Paper'

export default function App() {
  return (
    <div className="flex flex-col min-h-screen bg-white">
      <Navbar />
      <div className="flex-grow">
        <Routes>
          <Route path="/"              element={<Home />}   />
          <Route path="/search"        element={<Search />} />
          <Route path="/paper/:doi"    element={<Paper />}  />
        </Routes>
      </div>
      <Footer />
    </div>
  )
}

