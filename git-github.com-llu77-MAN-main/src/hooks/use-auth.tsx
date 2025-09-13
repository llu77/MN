"use client";

import React, { createContext, useContext } from 'react';

// This is a placeholder for a real authentication system.
// In a real app, this would be populated from an API call, JWT, or session.

type UserRole = 'admin' | 'supervisor' | 'employee' | 'partner';

interface User {
  id: string;
  name: string;
  role: UserRole;
  avatar: string;
}

interface AuthContextType {
  user: User;
}

// SIMULATE CURRENT LOGGED-IN USER
// Change the 'role' to 'admin', 'supervisor', 'employee', or 'partner' to test different access levels.
const mockUser: User = {
  id: 'sup1', // Corresponds to the ID in /lib/data.ts
  name: 'عبدالحي جلال',
  role: 'supervisor', // <-- CHANGE THIS TO TEST DIFFERENT ROLES
  avatar: '',
};


const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // In a real app, you might have logic here to fetch the user or check a session.
  const user = mockUser;

  return (
    <AuthContext.Provider value={{ user }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// A higher-order component to wrap pages/components that need auth
export const withAuth = <P extends object>(Component: React.ComponentType<P>) => {
  return function AuthenticatedComponent(props: P) {
    return (
      <AuthProvider>
        <Component {...props} />
      </AuthProvider>
    );
  };
};
