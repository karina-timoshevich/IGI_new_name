import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import { useLocation } from "react-router-dom";

const ProductDetails = () => {
    const location = useLocation();
    const { item } = location.state || {};
    const [timeZone, setTimeZone] = useState("");

    useEffect(() => {
        // Получаем временную зону пользователя
        const fetchTimeZone = async () => {
            try {
                const response = await fetch("http://ip-api.com/json");
                const data = await response.json();
                const timezone = data.timezone;
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

            } catch (error) {
                console.error("Error formatting date:", error);
            }
        };

        fetchTimeZone();
        updateDate();
        const intervalId = setInterval(updateDate, 1000);

        return () => clearInterval(intervalId);
    }, [timeZone]);

    const formatDate = (date, timeZone) => {
        try {
            return new Date(date).toLocaleString("en-US", { timeZone });
        } catch (error) {
            console.error("Error formatting date:", error);
            return "Invalid Date";
        }
    };

    if (!item) return <div>Loading...</div>;

    const containerStyles = {
        padding: "20px",
        color: "#333",
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
    };

    const cardStyles = {
        backgroundColor: "#fff",
        borderRadius: "12px",
        boxShadow: "0 8px 20px rgba(0, 0, 0, 0.1)",
        overflow: "hidden",
        maxWidth: "600px",
        width: "100%",
    };

    const contentStyles = {
        padding: "20px",
        textAlign: "center",
    };

    const textStyles = {
        fontSize: "16px",
        marginBottom: "10px",
        color: "#555",
    };

    const highlightTextStyles = {
        fontWeight: "bold",
        color: "#000",
    };

    const dateStyles = {
        fontSize: "14px",
        marginTop: "10px",
        color: "#777",
    };

    const imageStyles = {
        width: "100%",
        height: "300px",
        objectFit: "cover",
    };

    return (
        <div style={containerStyles}>
            <div style={cardStyles}>
                {item.imageUrl && (
                    <img src={`${item.imageUrl}`} alt={item.name} style={imageStyles} />
                )}
                <div style={contentStyles}>
                    <h1>{item.name}</h1>
                    <p style={textStyles}>
                        Price: <span style={highlightTextStyles}>${item.price}</span>
                    </p>
                    {item.manufacturer_id && (
                        <p style={textStyles}>
                            Manufacturer:{" "}
                            <span style={highlightTextStyles}>{item.manufacturer_id.name}</span>
                        </p>
                    )}
                    {item.manufacturer_id && item.manufacturer_id.country && (
                        <p style={textStyles}>
                            Country:{" "}
                            <span style={highlightTextStyles}>{item.manufacturer_id.country}</span>
                        </p>
                    )}

                    {item.createdAt && (
                        <div style={dateStyles}>
                            <p>
                                Created At (Local):{" "}
                                <span style={highlightTextStyles}>
                                    {formatDate(item.createdAt, timeZone)}
                                </span>
                            </p>
                            <p>
                                Created At (UTC):{" "}
                                <span style={highlightTextStyles}>
                                    {formatDate(item.createdAt, "UTC")}
                                </span>
                            </p>
                        </div>
                    )}
                    {item.updatedAt && (
                        <div style={dateStyles}>
                            <p>
                                Updated At (Local):{" "}
                                <span style={highlightTextStyles}>
                                    {formatDate(item.updatedAt, timeZone)}
                                </span>
                            </p>
                            <p>
                                Updated At (UTC):{" "}
                                <span style={highlightTextStyles}>
                                    {formatDate(item.updatedAt, "UTC")}
                                </span>
                            </p>
                        </div>
                    )}


                </div>
            </div>
        </div>
    );
};

ProductDetails.propTypes = {
    item: PropTypes.shape({
        name: PropTypes.string.isRequired,
        price: PropTypes.number.isRequired,
        imageUrl: PropTypes.string,
        createdAt: PropTypes.string,
        updatedAt: PropTypes.string,
        manufacturer_id: PropTypes.shape({
            name: PropTypes.string,
            country: PropTypes.string,
        }),
    }),
};

ProductDetails.defaultProps = {
    item: {
        name: "Unknown Name",
        price: 0,
        imageUrl: "",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        manufacturer_id: {
            name: "Unknown Manufacturer",
            country: "Unknown",
        },
    },
};

export default ProductDetails;
