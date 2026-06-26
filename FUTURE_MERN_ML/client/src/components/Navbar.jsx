import { TrendingUp, BarChart3, History, Upload } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

export default function Navbar() {
  const location = useLocation();
  
  const navItems = [
    { path: '/', icon: TrendingUp, label: 'Dashboard' },
    { path: '/upload', icon: Upload, label: 'Upload Data' },
    { path: '/history', icon: History, label: 'History' },
  ];

  return (
    <nav className="bg-gray-900 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-2">
            <BarChart3 className="w-8 h-8 text-blue-400" />
            <span className="text-xl font-bold">SalesForecast AI</span>
          </div>
          <div className="flex space-x-4">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition ${
                  location.pathname === item.path
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-300 hover:bg-gray-800'
                }`}
              >
                <item.icon className="w-5 h-5" />
                <span>{item.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
}
