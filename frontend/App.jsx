import React, { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext.jsx';
import AuthPage from './pages/AuthPage';
import FeedPage from './pages/FeedPage';
import TrendingPage from './pages/TrendingPage';
import NotificationsPage from './pages/NotificationsPage';
import ProfilePage from './pages/ProfilePage';
import Header from './components/Header';
import apiService from './services/api';

const AppContent = () => {
    const { isAuthenticated } = useAuth();
    const [currentView, setCurrentView] = useState('feed');
    const [unreadCount, setUnreadCount] = useState(0);

    useEffect(() => {
        if (isAuthenticated) {
            loadUnreadCount();
            // Refresh unread count every 30 seconds
            const interval = setInterval(loadUnreadCount, 30000);
            return () => clearInterval(interval);
        }
    }, [isAuthenticated]);

    const loadUnreadCount = async () => {
        try {
            const data = await apiService.getUnreadCount();
            setUnreadCount(data.unread_count || 0);
        } catch (error) {
            console.error('Failed to load unread count:', error);
        }
    };

    if (!isAuthenticated) {
        return <AuthPage onSuccess={() => setCurrentView('feed')} />;
    }

    return (
        <div className="min-h-screen bg-gray-100">
            <Header
                currentView={currentView}
                setCurrentView={setCurrentView}
                unreadCount={unreadCount}
            />

            <main className="max-w-2xl mx-auto px-4 py-6">
                {currentView === 'feed' && <FeedPage />}
                {currentView === 'trending' && <TrendingPage />}
                {currentView === 'notifications' && <NotificationsPage />}
                {currentView === 'profile' && <ProfilePage />}
            </main>
        </div>
    );
};

const App = () => {
    return (
        <AuthProvider>
            <AppContent />
        </AuthProvider>
    );
};

export default App;