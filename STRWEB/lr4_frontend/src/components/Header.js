import React, { useContext, useState, useEffect } from "react";
import Navbar from "./Navbar";
import AuthLinks from "./AuthLinks";

import axios from "axios";

const Header = () => {


    /*useEffect(() => {
        const fetchCatImage = async () => {
            try {
                const response = await axios.get(
                    "https://api.thecatapi.com/v1/images/search"
                );
                setCatImage(response.data[0].url);
            } catch (error) {
                console.error("Error fetching cat image:", error);
            }
        };

        fetchCatImage();
    }, []);*/

    const headerStyles = {
        display: "flex",
        justifyContent: "space-around",
        alignItems: "center",
        padding: "20px 20px",
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
