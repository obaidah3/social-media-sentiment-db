import React, { useState, useEffect } from 'react';
import { User, Heart, MessageCircle, Send } from 'lucide-react';
import apiService from '../services/api';

const PostModal = ({ post, onClose, onUpdate }) => {
    const [comments, setComments] = useState([]);
    const [newComment, setNewComment] = useState('');

    useEffect(() => {
        if (post) {
            loadComments();
        }
    }, [post]);

    const loadComments = async () => {
        try {
            const data = await apiService.listComments(post.id);
            setComments(data.comments || []);
        } catch (error) {
            console.error('Failed to load comments:', error);
        }
    };

    const handleCreateComment = async () => {
        if (!newComment.trim()) return;

        try {
            await apiService.createComment(post.id, newComment);
            setNewComment('');
            await loadComments();
            if (onUpdate) onUpdate();
        } catch (error) {
            alert('Failed to create comment');
        }
    };

    const handleReaction = async () => {
        try {
            await apiService.toggleReaction(post.id);
            if (onUpdate) onUpdate();
        } catch (error) {
            console.error('Failed to react:', error);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleCreateComment();
        }
    };

    if (!post) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
                <div className="p-6">
                    <div className="flex justify-between items-start mb-4">
                        <div className="flex items-center gap-3">
                            <div className="w-14 h-14 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full flex items-center justify-center">
                                <User className="text-white" size={24} />
                            </div>
                            <div>
                                <p className="font-bold text-lg">{post.author?.username}</p>
                                <p className="text-sm text-gray-500">
                                    {new Date(post.created_at).toLocaleDateString()}
                                </p>
                            </div>
                        </div>
                        <button
                            onClick={onClose}
                            className="text-gray-400 hover:text-gray-600 text-3xl font-light transition"
                        >
                            ×
                        </button>
                    </div>

                    <p className="text-lg mb-4 leading-relaxed">{post.content}</p>

                    {post.media_url && (
                        <img
                            src={post.media_url}
                            alt="Post media"
                            className="w-full rounded-2xl mb-4"
                        />
                    )}

                    {post.sentiment_analysis && (
                        <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-2xl p-4 mb-4">
                            <p className="text-sm">
                                <span className="font-bold">Sentiment: </span>
                                <span className={`capitalize font-semibold ${post.sentiment_analysis.label === 'positive' ? 'text-green-600' :
                                    post.sentiment_analysis.label === 'negative' ? 'text-red-600' :
                                        'text-gray-600'
                                    }`}>
                                    {post.sentiment_analysis.label}
                                </span>
                                <span className="text-gray-500 ml-2">
                                    ({(post.sentiment_analysis.confidence * 100).toFixed(1)}% confidence)
                                </span>
                            </p>
                        </div>
                    )}

                    <div className="flex gap-8 mb-6 pb-6 border-b-2">
                        <button
                            onClick={handleReaction}
                            className="flex items-center gap-2 text-gray-600 hover:text-pink-600 transition font-semibold"
                        >
                            <Heart
                                className={post.user_reaction ? 'fill-pink-600 text-pink-600' : ''}
                                size={24}
                            />
                            <span>{post.reaction_count || 0}</span>
                        </button>
                        <div className="flex items-center gap-2 text-gray-600 font-semibold">
                            <MessageCircle size={24} />
                            <span>{post.comment_count || 0}</span>
                        </div>
                    </div>

                    <div className="mb-4">
                        <h3 className="font-bold text-xl mb-4">Comments</h3>
                        <div className="flex gap-2 mb-6">
                            <input
                                type="text"
                                value={newComment}
                                onChange={(e) => setNewComment(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Write a comment..."
                                className="flex-1 px-4 py-3 border-2 border-gray-200 rounded-full focus:border-purple-500 focus:outline-none transition"
                            />
                            <button
                                onClick={handleCreateComment}
                                className="bg-gradient-to-r from-purple-600 to-pink-600 text-white p-3 rounded-full hover:shadow-lg transition"
                            >
                                <Send size={20} />
                            </button>
                        </div>

                        <div className="space-y-4">
                            {comments.map((comment) => (
                                <div key={comment.id} className="flex gap-3 bg-gray-50 p-4 rounded-2xl">
                                    <div className="w-10 h-10 bg-gradient-to-br from-purple-300 to-pink-300 rounded-full flex items-center justify-center flex-shrink-0">
                                        <User size={18} className="text-white" />
                                    </div>
                                    <div className="flex-1">
                                        <p className="font-bold text-sm">{comment.author?.username}</p>
                                        <p className="text-gray-800 mt-1">{comment.content}</p>
                                        <p className="text-xs text-gray-500 mt-2">
                                            {new Date(comment.created_at).toLocaleDateString()}
                                        </p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PostModal;