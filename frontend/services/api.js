// API Service - Handles all API communication
const API_BASE = 'http://localhost:8000/api/v1';  // Replace with your actual API URL

class ApiService {
    constructor() {
        this.token = null;
    }

    setToken(token) {
        this.token = token;
    }

    getToken() {
        return this.token;
    }

    clearToken() {
        this.token = null;
    }

    async call(endpoint, options = {}) {
        const headers = {
            'Content-Type': 'application/json',
            ...(this.token && { 'Authorization': `Bearer ${this.token}` })
        };

        try {
            const response = await fetch(`${API_BASE}${endpoint}`, {
                ...options,
                headers: { ...headers, ...options.headers }
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API call failed:', error);
            throw error;
        }
    }

    // Auth endpoints
    async signup(email, password, username, full_name) {
        return this.call('/auth/signup', {
            method: 'POST',
            body: JSON.stringify({ email, password, username, full_name })
        });
    }

    async login(email, password) {
        return this.call('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
    }

    // User endpoints
    async getCurrentUser() {
        return this.call('/users/me');
    }

    async updateCurrentUser(data) {
        return this.call('/users/me', {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async getUserById(userId) {
        return this.call(`/users/${userId}`);
    }

    // Post endpoints
    async createPost(content, media_url = null) {
        return this.call('/posts', {
            method: 'POST',
            body: JSON.stringify({ content, media_url })
        });
    }

    async getFeed() {
        return this.call('/posts/feed');
    }

    async getPost(postId) {
        return this.call(`/posts/${postId}`);
    }

    async updatePost(postId, content, media_url = null) {
        return this.call(`/posts/${postId}`, {
            method: 'PUT',
            body: JSON.stringify({ content, media_url })
        });
    }

    async toggleReaction(postId, reaction_type = 'like') {
        return this.call(`/posts/${postId}/react`, {
            method: 'POST',
            body: JSON.stringify({ reaction_type })
        });
    }

    async getTrendingPosts() {
        return this.call('/posts/trending');
    }

    async getPostsByUser(userId) {
        return this.call(`/posts/user/${userId}`);
    }

    // Profile endpoints
    async getProfileByUserId(userId) {
        return this.call(`/profiles/${userId}`);
    }

    async getMyProfile() {
        return this.call('/profiles/me');
    }

    async updateMyProfile(data) {
        return this.call('/profiles/me', {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    // Follow endpoints
    async followUser(userId) {
        return this.call(`/follows/follows/${userId}`, {
            method: 'POST'
        });
    }

    async unfollowUser(userId) {
        return this.call(`/follows/follows/${userId}`, {
            method: 'DELETE'
        });
    }

    async getFollowers(userId) {
        return this.call(`/follows/follows/${userId}/followers`);
    }

    async getFollowing(userId) {
        return this.call(`/follows/follows/${userId}/following`);
    }

    async getFollowStatus(userId) {
        return this.call(`/follows/follows/${userId}/status`);
    }

    // Comment endpoints
    async createComment(postId, content) {
        return this.call(`/comments/posts/${postId}`, {
            method: 'POST',
            body: JSON.stringify({ content })
        });
    }

    async listComments(postId) {
        return this.call(`/comments/posts/${postId}`);
    }

    async deleteComment(commentId) {
        return this.call(`/comments/${commentId}`, {
            method: 'DELETE'
        });
    }

    // Notification endpoints
    async listNotifications() {
        return this.call('/notifications/notifications');
    }

    async markNotificationRead(notificationId) {
        return this.call(`/notifications/notifications/${notificationId}/read`, {
            method: 'PATCH'
        });
    }

    async getUnreadCount() {
        return this.call('/notifications/notifications/unread-count');
    }

    // Health check
    async healthCheck() {
        return this.call('/health');
    }
}

export default new ApiService();