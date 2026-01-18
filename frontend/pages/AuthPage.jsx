import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext.jsx';

const AuthPage = ({ onSuccess }) => {
    const [currentView, setCurrentView] = useState('login');
    const { signup, login, loading } = useAuth();

    const [authForm, setAuthForm] = useState({
        email: '',
        password: '',
        username: '',
        full_name: ''
    });

    const handleKeyPress = (e, callback) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            callback();
        }
    };

    const handleSignup = async () => {
        if (!authForm.username || !authForm.full_name || !authForm.email || !authForm.password) {
            alert('Please fill in all fields');
            return;
        }

        const result = await signup(
            authForm.email,
            authForm.password,
            authForm.username,
            authForm.full_name
        );

        if (result.success) {
            onSuccess();
        } else {
            alert('Signup failed. Please try again.');
        }
    };

    const handleLogin = async () => {
        if (!authForm.email || !authForm.password) {
            alert('Please fill in all fields');
            return;
        }

        const result = await login(authForm.email, authForm.password);

        if (result.success) {
            onSuccess();
        } else {
            alert('Login failed. Please check your credentials.');
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-600 via-pink-500 to-red-500 flex items-center justify-center p-4">
            <div className="bg-white rounded-3xl shadow-2xl w-full max-w-md overflow-hidden">
                <div className="bg-gradient-to-r from-purple-600 to-pink-600 p-8 text-white text-center">
                    <h1 className="text-5xl font-black mb-2">ConnectSphere</h1>
                    <p className="text-purple-100 text-lg">Where Friends Connect & Stories Unite</p>
                </div>

                <div className="p-8">
                    <div className="flex gap-2 mb-6">
                        <button
                            onClick={() => setCurrentView('login')}
                            className={`flex-1 py-3 rounded-xl font-bold transition-all ${currentView === 'login'
                                ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                                }`}
                        >
                            Login
                        </button>
                        <button
                            onClick={() => setCurrentView('signup')}
                            className={`flex-1 py-3 rounded-xl font-bold transition-all ${currentView === 'signup'
                                ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                                }`}
                        >
                            Sign Up
                        </button>
                    </div>

                    <div className="space-y-4">
                        {currentView === 'signup' && (
                            <>
                                <input
                                    type="text"
                                    placeholder="Username"
                                    value={authForm.username}
                                    onChange={(e) => setAuthForm({ ...authForm, username: e.target.value })}
                                    onKeyPress={(e) => handleKeyPress(e, handleSignup)}
                                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition"
                                />
                                <input
                                    type="text"
                                    placeholder="Full Name"
                                    value={authForm.full_name}
                                    onChange={(e) => setAuthForm({ ...authForm, full_name: e.target.value })}
                                    onKeyPress={(e) => handleKeyPress(e, handleSignup)}
                                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition"
                                />
                            </>
                        )}
                        <input
                            type="email"
                            placeholder="Email"
                            value={authForm.email}
                            onChange={(e) => setAuthForm({ ...authForm, email: e.target.value })}
                            onKeyPress={(e) => handleKeyPress(e, currentView === 'login' ? handleLogin : handleSignup)}
                            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition"
                        />
                        <input
                            type="password"
                            placeholder="Password"
                            value={authForm.password}
                            onChange={(e) => setAuthForm({ ...authForm, password: e.target.value })}
                            onKeyPress={(e) => handleKeyPress(e, currentView === 'login' ? handleLogin : handleSignup)}
                            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:outline-none transition"
                        />
                        <button
                            onClick={currentView === 'login' ? handleLogin : handleSignup}
                            disabled={loading}
                            className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 rounded-xl font-bold hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {loading ? 'Please wait...' : currentView === 'login' ? 'Login' : 'Create Account'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AuthPage;