import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { 
  Home, 
  Pill, 
  Bell, 
  BookHeart, 
  SmilePlus, 
  Brain, 
  User, 
  Menu, 
  X, 
  LogOut 
} from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import Logo from './Logo';

const Layout = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
  };

  const navItems = [
    { name: 'Dashboard', to: '/dashboard', icon: <Home size={20} /> },
    { name: 'Medications', to: '/medications', icon: <Pill size={20} /> },
    { name: 'Reminders', to: '/reminders', icon: <Bell size={20} /> },
    { name: 'Mood Tracker', to: '/mood', icon: <SmilePlus size={20} /> },
    { name: 'Journal', to: '/journal', icon: <BookHeart size={20} /> },
    { name: 'AI Support', to: '/ai-chat', icon: <Brain size={20} /> },
  ];

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar for desktop */}
      <aside className="hidden md:flex flex-col w-64 bg-white border-r border-gray-200">
        <div className="p-4 border-b border-gray-200">
          <Logo className="h-8 w-auto" />
        </div>
        
        <nav className="flex-1 overflow-y-auto py-4">
          <ul className="space-y-1 px-2">
            {navItems.map((item) => (
              <li key={item.name}>
                <NavLink
                  to={item.to}
                  className={({ isActive }) =>
                    `flex items-center px-4 py-2 text-sm font-medium rounded-md transition-colors ${
                      isActive
                        ? 'bg-primary-50 text-primary-700'
                        : 'text-gray-700 hover:text-primary-700 hover:bg-gray-50'
                    }`
                  }
                >
                  <span className="mr-3">{item.icon}</span>
                  {item.name}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
        
        <div className="border-t border-gray-200 p-4">
          <div className="flex items-center">
            <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center text-primary-700">
              <User size={18} />
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-700">{user?.name}</p>
              <p className="text-xs text-gray-500">{user?.email}</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="mt-3 flex items-center px-4 py-2 text-sm font-medium text-red-600 rounded-md hover:bg-red-50 w-full"
          >
            <LogOut size={18} className="mr-2" />
            Logout
          </button>
        </div>
      </aside>

      {/* Mobile menu */}
      <div className="md:hidden fixed inset-0 bg-gray-800 bg-opacity-50 z-20 transition-opacity duration-300 ease-in-out"
        style={{ display: isMobileMenuOpen ? 'block' : 'none' }}
        onClick={closeMobileMenu}
      ></div>
      
      <div className={`md:hidden fixed top-0 left-0 bottom-0 w-64 bg-white z-30 transform transition-transform duration-300 ease-in-out ${
        isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <div className="p-4 border-b border-gray-200 flex items-center justify-between">
          <Logo className="h-8 w-auto" />
          <button onClick={closeMobileMenu}>
            <X size={24} className="text-gray-500" />
          </button>
        </div>
        
        <nav className="flex-1 overflow-y-auto py-4">
          <ul className="space-y-1 px-2">
            {navItems.map((item) => (
              <li key={item.name}>
                <NavLink
                  to={item.to}
                  onClick={closeMobileMenu}
                  className={({ isActive }) =>
                    `flex items-center px-4 py-2 text-sm font-medium rounded-md transition-colors ${
                      isActive
                        ? 'bg-primary-50 text-primary-700'
                        : 'text-gray-700 hover:text-primary-700 hover:bg-gray-50'
                    }`
                  }
                >
                  <span className="mr-3">{item.icon}</span>
                  {item.name}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
        
        <div className="border-t border-gray-200 p-4">
          <div className="flex items-center">
            <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center text-primary-700">
              <User size={18} />
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-700">{user?.name}</p>
              <p className="text-xs text-gray-500">{user?.email}</p>
            </div>
          </div>
          <button
            onClick={() => {
              handleLogout();
              closeMobileMenu();
            }}
            className="mt-3 flex items-center px-4 py-2 text-sm font-medium text-red-600 rounded-md hover:bg-red-50 w-full"
          >
            <LogOut size={18} className="mr-2" />
            Logout
          </button>
        </div>
      </div>

      {/* Main content */}
      <div className="flex flex-col flex-1 overflow-hidden">
        {/* Top navbar for mobile */}
        <header className="bg-white shadow-sm border-b border-gray-200 md:hidden">
          <div className="px-4 h-16 flex items-center justify-between">
            <div className="flex items-center">
              <button
                onClick={() => setIsMobileMenuOpen(true)}
                className="text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
              >
                <Menu size={24} />
              </button>
              <Logo className="h-8 w-auto ml-3" />
            </div>
          </div>
        </header>
        
        {/* Page content */}
        <main className="flex-1 overflow-y-auto bg-gray-50 p-4 md:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;