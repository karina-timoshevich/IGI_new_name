import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const AuthLinks = () => {
  const { user, logout } = useContext(AuthContext);

  const authLinksStyles = {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    span: {
      marginRight: "10px",
      fontWeight: "bold",
    },
    button: {
      padding: "5px 10px",
      border: "none",
      cursor: "pointer",
      backgroundColor: "#000",
      color: "#fff",
      borderRadius: "5px",
    },
    link: {
      textDecoration: "none",
      color: "#000",
    },
  };

  return (
    <div style={authLinksStyles}>
      {user ? (
        <>
          <span style={authLinksStyles.span}>{user.name}</span>
          <button style={authLinksStyles.button} onClick={logout}>
            Logout
          </button>
        </>
      ) : (
        <>
          <Link to="/login" style={authLinksStyles.link}>
            Login
          </Link>
          <Link to="/register" style={authLinksStyles.link}>
            Register
          </Link>
        </>
      )}
    </div>
  );
};

export default AuthLinks;
