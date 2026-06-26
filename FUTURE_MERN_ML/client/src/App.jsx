import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Upload from './pages/Upload';
import History from './pages/History';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/history" element={<History />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
