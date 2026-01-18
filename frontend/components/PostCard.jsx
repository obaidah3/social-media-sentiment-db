import React from 'react';
import { User, Heart, MessageCircle } from 'lucide-react';

const PostCard = ({ post, onLike, onComment }) => {
    return (
        <div className="bg-white rounded-3xl shadow-md hover:shadow-lg transition border border-gray-200">
            <div className="p-6">
                <div className="flex items-center gap-3 mb-4">
                    <div className="w-12 h-12 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full flex items-center justify-center">
                        <User className="text-white" size={20} />
                    </div>
                    <div className="flex-1">
                        <p className="font-bold text-lg">{post.author?.username}</p>
                        <p className="text-sm text-gray-500">
                            {new Date(post.created_at).toLocaleDateString()}
                        </p>
                    </div>
                </div>

                <p className="text-gray-800 mb-4 leading-relaxed">{post.content}</p>

                {post.media_url && (
                    <img
                        src={post.media_url}
                        alt="Post media"
                        className="w-full rounded-2xl mb-4"
                    />
                )}

                {post.sentiment_analysis && (
                    <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl p-3 mb-4 text-sm">
                        <span className="font-bold">Sentiment: </span>
                        <span className={`capitalize font-semibold ${post.sentiment_analysis.label === 'positive' ? 'text-green-600' :
                            post.sentiment_analysis.label === 'negative' ? 'text-red-600' :
                                'text-gray-600'
                            }`}>
                            {post.sentiment_analysis.label}
                        </span>
                    </div>
                )}
            </div>

            <div className="flex gap-1 px-6 pb-6 border-t pt-2">
                <button
                    onClick={() => onLike(post.id)}
                    className={`flex-1 flex items-center justify-center gap-2 py-2 rounded-xl font-semibold transition ${post.user_reaction
                        ? 'text-pink-600 bg-pink-50'
                        : 'text-gray-600 hover:bg-gray-100'
                        }`}
                >
                    <Heart className={post.user_reaction ? 'fill-pink-600' : ''} size={20} />
                    <span>Like</span>
                    <span className="text-sm">({post.reaction_count || 0})</span>
                </button>
                <button
                    onClick={() => onComment(post)}
                    className="flex-1 flex items-center justify-center gap-2 py-2 text-gray-600 hover:bg-gray-100 rounded-xl font-semibold transition"
                >
                    <MessageCircle size={20} />
                    <span>Comment</span>
                    <span className="text-sm">({post.comment_count || 0})</span>
                </button>
            </div>
        </div>
    );
};

export default PostCard;