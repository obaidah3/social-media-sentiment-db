import React from 'react';
import { Home, TrendingUp, Bell, User, LogOut, Search } from 'lucide-react';
import { useAuth } from '../context/AuthContext.jsx';

const Header = ({ currentView, setCurrentView, unreadCount }) => {
    const { logout, currentUser } = useAuth();

    return (
        <header className="bg-white shadow-md sticky top-0 z-40 border-b-2 border-gray-200">
            <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
                <h1 className="text-3xl font-black bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                    ConnectSphere
                </h1>

                <div className="hidden md:flex items-center flex-1 max-w-md mx-8">
                    <div className="relative w-full">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                        <input
                            type="text"
                            placeholder="Search..."
                            className="w-full pl-10 pr-4 py-2 bg-gray-100 rounded-full focus:outline-none focus:bg-white focus:ring-2 focus:ring-purple-500 transition"
                        />
                    </div>
                </div>

                <nav className="flex items-center gap-4">
                    <button
                        onClick={() => setCurrentView('feed')}
                        className={`p-3 rounded-xl transition ${currentView === 'feed'
                            ? 'bg-gradient-to-r from-purple-100 to-pink-100 text-purple-600'
                            : 'text-gray-600 hover:bg-gray-100'
                            }`}
                    >
                        <Home size={24} />
                    </button>
                    <button
                        onClick={() => setCurrentView('trending')}
                        className={`p-3 rounded-xl transition ${currentView === 'trending'
                            ? 'bg-gradient-to-r from-purple-100 to-pink-100 text-purple-600'
                            : 'text-gray-600 hover:bg-gray-100'
                            }`}
                    >
                        <TrendingUp size={24} />
                    </button>
                    <button
                        onClick={() => setCurrentView('notifications')}
                        className={`p-3 rounded-xl relative transition ${currentView === 'notifications'
                            ? 'bg-gradient-to-r from-purple-100 to-pink-100 text-purple-600'
                            : 'text-gray-600 hover:bg-gray-100'
                            }`}
                    >
                        <Bell size={24} />
                        {unreadCount > 0 && (
                            <span className="absolute -top-1 -right-1 bg-gradient-to-r from-red-500 to-pink-500 text-white text-xs rounded-full w-6 h-6 flex items-center justify-center font-bold">
                                {unreadCount}
                            </span>
                        )}
                    </button>
                    <button
                        onClick={() => setCurrentView('profile')}
                        className={`p-3 rounded-xl transition ${currentView === 'profile'
                            ? 'bg-gradient-to-r from-purple-100 to-pink-100 text-purple-600'
                            : 'text-gray-600 hover:bg-gray-100'
                            }`}
                    >
                        <User size={24} />
                    </button>
                    <button
                        onClick={logout}
                        className="p-3 text-gray-600 hover:bg-red-50 hover:text-red-600 rounded-xl transition"
                    >
                        <LogOut size={24} />
                    </button>
                </nav>
            </div>
        </header>
    );
};

export default Header;