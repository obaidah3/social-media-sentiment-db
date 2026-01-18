import React, { useState, useEffect } from 'react';
import { Users } from 'lucide-react';
import PostCreator from '../components/PostCreator';
import PostCard from '../components/PostCard';
import PostModal from '../components/PostModal';
import apiService from '../services/api';

const FeedPage = () => {
    const [feed, setFeed] = useState([]);
    const [selectedPost, setSelectedPost] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadFeed();
    }, []);

    const loadFeed = async () => {
        setLoading(true);
        try {
            const data = await apiService.getFeed();
            setFeed(data.posts || []);
        } catch (error) {
            console.error('Failed to load feed:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleLike = async (postId) => {
        try {
            await apiService.toggleReaction(postId);
            await loadFeed();
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
        await loadFeed();
    };

    return (
        <>
            <PostCreator onPostCreated={loadFeed} />

            <div className="space-y-4">
                {loading && (
                    <div className="text-center py-8">
                        <p className="text-gray-500">Loading...</p>
                    </div>
                )}

                {!loading && feed.length === 0 && (
                    <div className="text-center py-16 bg-white rounded-3xl shadow-md">
                        <Users size={64} className="mx-auto text-gray-300 mb-4" />
                        <p className="text-gray-500 text-lg font-semibold">No posts yet</p>
                        <p className="text-gray-400">Create your first post to get started!</p>
                    </div>
                )}

                {!loading && feed.map((post) => (
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

export default FeedPage;