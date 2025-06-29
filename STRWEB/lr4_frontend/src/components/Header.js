import React, { useState, useEffect } from "react";
import Navbar from "./Navbar";
import AuthLinks from "./AuthLinks";
import axios from "axios";

const Header = () => {

    const headerStyles = {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "20px 0px",
        backgroundColor: "#f0f0f0",
        color: "#000",
        position: "fixed",
        top: 0,
        width: "100%",
        zIndex: 1000,
    };

    return (
        <header style={headerStyles}>
            <Navbar />
            <AuthLinks />

        </header>
    );
};

export default Header;
