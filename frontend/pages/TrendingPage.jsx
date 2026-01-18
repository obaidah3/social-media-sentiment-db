import React, { useState, useEffect } from 'react';
import { TrendingUp } from 'lucide-react';
import PostCard from '../components/PostCard';
import PostModal from '../components/PostModal';
import apiService from '../services/api';

const TrendingPage = () => {
    const [trendingPosts, setTrendingPosts] = useState([]);
    const [selectedPost, setSelectedPost] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadTrending();
    }, []);

    const loadTrending = async () => {
        setLoading(true);
        try {
            const data = await apiService.getTrendingPosts();
            setTrendingPosts(data.posts || []);
        } catch (error) {
            console.error('Failed to load trending posts:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleLike = async (postId) => {
        try {
            await apiService.toggleReaction(postId);
            await loadTrending();
        } catch (error) {
            console.error('Failed to like post:', error);
        }
    };

    const handleComment = (post) => {
        setSelectedPost(post);
    };

    const handleCloseModal = () => {
        setSelectedPost(null);
    };

    const handleModalUpdate = async () => {
        await loadTrending();
    };

    return (
        <>
            <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-3xl p-6 text-white mb-6">
                <h2 className="text-3xl font-black mb-2">🔥 Trending Now</h2>
                <p className="text-purple-100">See what everyone is talking about</p>
            </div>

            <div className="space-y-4">
                {loading && (
                    <div className="text-center py-8">
                        <p className="text-gray-500">Loading...</p>
                    </div>
                )}

                {!loading && trendingPosts.length === 0 && (
                    <div className="text-center py-16 bg-white rounded-3xl shadow-md">
                        <TrendingUp size={64} className="mx-auto text-gray-300 mb-4" />
                        <p className="text-gray-500 text-lg font-semibold">No trending posts</p>
                    </div>
                )}

                {!loading && trendingPosts.map((post) => (
                    <PostCard
                        key={post.id}
                        post={post}
                        onLike={handleLike}
                        onComment={handleComment}
                    />
                ))}
            </div>

            {selectedPost && (
                <PostModal
                    post={selectedPost}
                    onClose={handleCloseModal}
                    onUpdate={handleModalUpdate}
                />
            )}
        </>
    );
};

export default TrendingPage;