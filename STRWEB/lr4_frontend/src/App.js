import React from "react";
import {BrowserRouter as Router, Link, Route, Routes} from "react-router-dom";
// import Home from "./pages/Home";
// import Catalog from "./pages/Catalog";
// import ItemDetails from "./pages/ItemDetails";
// import AdminPage from "./pages/AdminPage";
import Login from "./pages/Login";
// import Register from "./pages/Register";
// import Reviews from "./pages/Reviews";
import { AuthProvider } from "./context/AuthContext";
import Register from "./pages/Register";
// import { ThemeProvider } from "./context/ThemeContext";
// import ProtectedRoute from "./components/ProtectedRoute";
// import Header from "./components/Header";
// import Footer from "./components/Footer";

/* Декларативная функция */
function App() {
  const appStyles = {
    display: "flex",
    flexDirection: "column",
    minHeight: "100vh",
    overflowX: "hidden",
  };

  const mainStyles = {
    flex: 1,
    marginTop: "60px",
    display: "flex",
    justifyContent: "center",
  };

  const contentStyles = {
    width: "100%",
  };

  return (
      <AuthProvider>
        <Router>
          <div style={appStyles}>
            <header style={{ textAlign: "center", padding: "10px" }}>
              <nav>
                <Link to="/login" style={{ margin: "10px" }}>Login</Link>
                <Link to={"/register"} style={{ margin: "10px" }}>Register</Link>
                {/* Добавьте другие ссылки для навигации при необходимости */}
              </nav>
            </header>

            <main style={mainStyles}>
              <div style={contentStyles}>
                <Routes>
                  <Route path="/login" element={<Login />} />
                  <Route path={"/register"} element={<Register />} />
                  {/* Добавьте другие маршруты при необходимости */}
                </Routes>
              </div>
            </main>

            <footer style={{ textAlign: "center", padding: "10px" }}>
              © {new Date().getFullYear()} Created by Karina
            </footer>
          </div>
        </Router>
      </AuthProvider>
  );
}


export default App;
