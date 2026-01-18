import React from 'react';
import { User } from 'lucide-react';
import { useAuth } from '../context/AuthContext.jsx';

const ProfilePage = () => {
    const { currentUser } = useAuth();

    if (!currentUser) return null;

    return (
        <div className="bg-white rounded-3xl shadow-md border border-gray-200 overflow-hidden">
            <div className="h-32 bg-gradient-to-r from-purple-600 via-pink-500 to-red-500"></div>

            <div className="px-6 pb-6">
                <div className="flex items-end -mt-16 mb-4">
                    <div className="w-32 h-32 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full flex items-center justify-center border-4 border-white">
                        <User size={64} className="text-white" />
                    </div>
                </div>

                <h2 className="text-3xl font-black text-gray-800">{currentUser.full_name}</h2>
                <p className="text-gray-600 text-lg">@{currentUser.username}</p>
                <p className="text-gray-500 mt-2">{currentUser.email}</p>

                <div className="flex gap-6 mt-6 py-6 border-y">
                    <div className="text-center">
                        <p className="text-3xl font-black bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                            0
                        </p>
                        <p className="text-sm text-gray-600 font-semibold">Posts</p>
                    </div>
                    <div className="text-center">
                        <p className="text-3xl font-black bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                            0
                        </p>
                        <p className="text-sm text-gray-600 font-semibold">Followers</p>
                    </div>
                    <div className="text-center">
                        <p className="text-3xl font-black bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                            0
                        </p>
                        <p className="text-sm text-gray-600 font-semibold">Following</p>
                    </div>
                </div>

                <div className="mt-6">
                    <p className="text-gray-600">
                        <span className="font-semibold">Member since:</span>{' '}
                        {new Date(currentUser.created_at).toLocaleDateString()}
                    </p>
                </div>

                <div className="mt-6 pt-6 border-t">
                    <h3 className="font-bold text-xl mb-4">About</h3>
                    <p className="text-gray-600">
                        Welcome to my profile! I'm excited to connect with friends and share stories on ConnectSphere.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default ProfilePage;