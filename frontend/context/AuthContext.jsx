import React, { createContext, useState, useContext, useEffect } from 'react';
import apiService from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(null);
    const [currentUser, setCurrentUser] = useState(null);
    const [loading, setLoading] = useState(false);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        if (token) {
            apiService.setToken(token);
            loadCurrentUser();
        } else {
            apiService.clearToken();
            setCurrentUser(null);
            setIsAuthenticated(false);
        }
    }, [token]);

    const loadCurrentUser = async () => {
        try {
            const user = await apiService.getCurrentUser();
            setCurrentUser(user);
            setIsAuthenticated(true);
        } catch (error) {
            console.error('Failed to load user:', error);
            logout();
        }
    };

    const signup = async (email, password, username, full_name) => {
        setLoading(true);
        try {
            const response = await apiService.signup(email, password, username, full_name);
            setToken(response.access_token);
            return { success: true };
        } catch (error) {
            return { success: false, error: error.message };
        } finally {
            setLoading(false);
        }
    };

    const login = async (email, password) => {
        setLoading(true);
        try {
            const response = await apiService.login(email, password);
            setToken(response.access_token);
            return { success: true };
        } catch (error) {
            return { success: false, error: error.message };
        } finally {
            setLoading(false);
        }
    };

    const logout = () => {
        setToken(null);
        setCurrentUser(null);
        setIsAuthenticated(false);
        apiService.clearToken();
    };

    const value = {
        token,
        currentUser,
        loading,
        isAuthenticated,
        signup,
        login,
        logout,
        refreshUser: loadCurrentUser
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
};