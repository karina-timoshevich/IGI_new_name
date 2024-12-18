import React, { useState, useEffect } from "react";
import Navbar from "./Navbar";
import AuthLinks from "./AuthLinks";
import axios from "axios";

const Header = () => {
    const [currentDate, setCurrentDate] = useState("");
    const [timeZone, setTimeZone] = useState("");
    const [utcDate, setUtcDate] = useState("");

    useEffect(() => {
        const fetchTimeZone = async () => {
            try {
                const response = await axios.get("http://ip-api.com/json");
                const timezone = response.data.timezone;
                if (timezone) {
                    setTimeZone(timezone);
                } else {
                    setTimeZone("UTC");
                }
            } catch (error) {
                console.error("Error fetching time zone:", error);
                setTimeZone("UTC");
            }
        };

        const updateDate = () => {
            const date = new Date();
            try {
                const formattedCurrentDate = date.toLocaleString("en-US", { timeZone: timeZone || "UTC" });
                setCurrentDate(formattedCurrentDate);
            } catch (error) {
                console.error("Error formatting date:", error);
                setCurrentDate(date.toLocaleString("en-US", { timeZone: "UTC" }));
            }

            setUtcDate(new Date().toLocaleString("en-US", { timeZone: "UTC" }));
        };

        fetchTimeZone();
        updateDate();
        const intervalId = setInterval(updateDate, 1000);

        return () => clearInterval(intervalId);
    }, [timeZone]);

    const headerStyles = {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "20px 20px",
        backgroundColor: "#f0f0f0",
        color: "#000",
        position: "fixed",
        top: 0,
        width: "100%",
        zIndex: 1000,
    };

    const timeZoneStyles = {
        fontSize: "0.6rem",
        marginTop: "5px",
        marginBottom: "5px",
    };

    return (
        <header style={headerStyles}>
            <Navbar />
            <AuthLinks />
            <div>
                <p style={timeZoneStyles}>Current Date: {currentDate}</p>
                <p style={timeZoneStyles}>Time Zone: {timeZone}</p>
                <p style={timeZoneStyles}>UTC Time: {utcDate}</p>
            </div>
        </header>
    );
};

export default Header;
