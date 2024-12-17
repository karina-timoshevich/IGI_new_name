import React, { createContext, useState, useEffect } from "react";
import api from "../utils/api";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem("token");
      if (token) {
        try {
          const response = await api.get("/auth/me", {
            headers: { "x-auth-token": token },
          });
          setUser(response.data);
        } catch (error) {
          console.error(error);
        }
      }
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
    setUser(response.data.user);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};