import React, { useState } from 'react';
import { User, Image, Video, Smile } from 'lucide-react';
import { useAuth } from '../context/AuthContext.jsx';
import apiService from '../services/api';

const PostCreator = ({ onPostCreated }) => {
    const { currentUser } = useAuth();
    const [newPost, setNewPost] = useState({ content: '', media_url: '' });
    const [loading, setLoading] = useState(false);

    const handleCreatePost = async () => {
        if (!newPost.content.trim()) return;

        setLoading(true);
        try {
            await apiService.createPost(newPost.content, newPost.media_url || null);
            setNewPost({ content: '', media_url: '' });
            if (onPostCreated) onPostCreated();
        } catch (error) {
            alert('Failed to create post');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-white rounded-3xl shadow-md p-6 mb-6 border border-gray-200">
            <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full flex items-center justify-center">
                    <User className="text-white" size={20} />
                </div>
                <textarea
                    value={newPost.content}
                    onChange={(e) => setNewPost({ ...newPost, content: e.target.value })}
                    placeholder={`What's on your mind, ${currentUser?.username}?`}
                    className="flex-1 px-4 py-3 bg-gray-100 rounded-3xl resize-none focus:outline-none focus:bg-gray-50 transition"
                    rows="2"
                />
            </div>

            <div className="border-t pt-4 mt-4">
                <input
                    type="url"
                    value={newPost.media_url}
                    onChange={(e) => setNewPost({ ...newPost, media_url: e.target.value })}
                    placeholder="Add image URL (optional)"
                    className="w-full px-4 py-2 bg-gray-100 rounded-full mb-3 focus:outline-none focus:bg-gray-50 transition"
                />

                <div className="flex items-center justify-between">
                    <div className="flex gap-2">
                        <button className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-xl transition">
                            <Image size={20} className="text-green-600" />
                            <span className="text-sm font-semibold hidden sm:inline">Photo</span>
                        </button>
                        <button className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-xl transition">
                            <Video size={20} className="text-red-600" />
                            <span className="text-sm font-semibold hidden sm:inline">Video</span>
                        </button>
                        <button className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-xl transition">
                            <Smile size={20} className="text-yellow-600" />
                            <span className="text-sm font-semibold hidden sm:inline">Feeling</span>
                        </button>
                    </div>
                    <button
                        onClick={handleCreatePost}
                        disabled={loading || !newPost.content.trim()}
                        className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-2 rounded-xl font-bold hover:shadow-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        Post
                    </button>
                </div>
            </div>
        </div>
    );
};

export default PostCreator;