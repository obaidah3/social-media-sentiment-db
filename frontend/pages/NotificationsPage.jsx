import React, { useState, useEffect } from 'react';
import { Bell } from 'lucide-react';
import apiService from '../services/api';

const NotificationsPage = () => {
    const [notifications, setNotifications] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadNotifications();
    }, []);

    const loadNotifications = async () => {
        setLoading(true);
        try {
            const data = await apiService.listNotifications();
            setNotifications(data.notifications || []);
        } catch (error) {
            console.error('Failed to load notifications:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleMarkRead = async (notificationId) => {
        try {
            await apiService.markNotificationRead(notificationId);
            await loadNotifications();
        } catch (error) {
            console.error('Failed to mark notification as read:', error);
        }
    };

    return (
        <div className="bg-white rounded-3xl shadow-md p-6 border border-gray-200">
            <h2 className="text-3xl font-black text-gray-800 mb-6">Notifications</h2>

            {loading && (
                <div className="text-center py-8">
                    <p className="text-gray-500">Loading...</p>
                </div>
            )}

            {!loading && notifications.length === 0 && (
                <div className="text-center py-16">
                    <Bell size={64} className="mx-auto text-gray-300 mb-4" />
                    <p className="text-gray-500 text-lg font-semibold">No notifications yet</p>
                </div>
            )}

            {!loading && notifications.length > 0 && (
                <div className="space-y-3">
                    {notifications.map((notif) => (
                        <div
                            key={notif.id}
                            onClick={() => !notif.is_read && handleMarkRead(notif.id)}
                            className={`p-4 rounded-2xl transition cursor-pointer ${notif.is_read
                                ? 'bg-gray-50'
                                : 'bg-gradient-to-r from-purple-50 to-pink-50 hover:from-purple-100 hover:to-pink-100'
                                }`}
                        >
                            <div className="flex items-start gap-3">
                                <div className="w-10 h-10 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full flex items-center justify-center flex-shrink-0">
                                    <Bell size={18} className="text-white" />
                                </div>
                                <div className="flex-1">
                                    <p className="font-bold">{notif.type}</p>
                                    <p className="text-sm text-gray-600 mt-1">{notif.content}</p>
                                    <p className="text-xs text-gray-500 mt-2">
                                        {new Date(notif.created_at).toLocaleString()}
                                    </p>
                                </div>
                                {!notif.is_read && (
                                    <div className="w-3 h-3 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full"></div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default NotificationsPage;