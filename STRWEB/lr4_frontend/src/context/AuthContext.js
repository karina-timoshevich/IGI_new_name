import React, { createContext, useState, useEffect } from "react";
import api from "../utils/api";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

   useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem("token");
      if (token) {
        try {
          const response = await api.get("/auth/me", {
            headers: { "authorization": token },
          });
          setUser(response.data);
        } catch (error) {
          console.error(error);
          localStorage.removeItem("token");
        }
      }
      setLoading(false); // Done fetching user
    };

    const checkGoogleLogin = () => {
      const urlParams = new URLSearchParams(window.location.search);
      const token = urlParams.get("token");
      if (token) {
        localStorage.setItem("token", token);
        fetchUser();
        window.history.replaceState({}, document.title, "/");
      }
    };

    fetchUser();
    checkGoogleLogin();
  }, []);

  const login = async (email, password) => {
    console.log("Attempting login with:", email, password);
    const response = await api.post("/auth/login", {
      email,
      password,
    });
    localStorage.setItem("token", response.data.token);
    setUser(response.data);
    console.log("User set in AuthProvider:", response.data);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };
if (loading) {
    return <div>Loading...</div>; // Optionally add a loading state
  }
  return (
    <AuthContext.Provider value={{ user, setUser, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};