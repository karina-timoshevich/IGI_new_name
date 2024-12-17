import React, { useContext, useState } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const AuthLinks = () => {
  const { user, logout } = useContext(AuthContext);
  console.log("User object in AuthLinks:", user);
  const [dropdownVisible, setDropdownVisible] = useState(false);

  const authLinksStyles = {
    display: "flex",
    gap: "10px",
    position: "relative",
    span: {
      marginRight: "10px",
      cursor: "pointer",
    },
    button: {
      padding: "5px 10px",
      border: "none",
      cursor: "pointer",
      backgroundColor: "#000",
      color: "#fff",
    },
    link: {
      textDecoration: "none",
      color: "#000",
    },
    dropdown: {
      position: "absolute",
      top: "100%",
      right: 0,
      backgroundColor: "#fff",
      color: "#000",
      border: "1px solid #ccc",
      borderRadius: "5px",
      boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
      display: dropdownVisible ? "block" : "none",
      zIndex: 1000,
    },
    dropdownItem: {
      padding: "10px",
      cursor: "pointer",
    },
  };

  const toggleDropdown = () => {
    setDropdownVisible(!dropdownVisible);
  };

  return (
    <div style={authLinksStyles}>
      {user ? (
        <>
          <span style={authLinksStyles.span} onClick={toggleDropdown}>
            {user.name}
          </span>
          <div style={authLinksStyles.dropdown}>
            <Link to="/settings" style={authLinksStyles.link}>
              <div style={authLinksStyles.dropdownItem}>Settings</div>
            </Link>
            <div style={authLinksStyles.dropdownItem} onClick={logout}>
              Logout
            </div>
          </div>
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
