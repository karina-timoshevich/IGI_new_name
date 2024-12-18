import React, { useRef } from "react";
import ProductAdmin from "../components/ProductsAdmin";

const AdminPage = () => {
    const productAdminRef = useRef(null);

    const containerStyles = {
        padding: "20px",
        color: "#333",
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
    };

    const headerStyles = {
        textAlign: "center",
        marginBottom: "20px",
        fontSize: "2rem",
    };

    const sectionsContainerStyles = {
        display: "flex",
        flexDirection: "column",
        gap: "20px",
        width: "100%",
        maxWidth: "1200px",
    };

    const sectionStyles = {
        padding: "20px",
        backgroundColor: "#fff",
        borderRadius: "10px",
        boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
    };

    const sectionHeaderStyles = {
        marginBottom: "10px",
        fontSize: "1.5rem",
        borderBottom: "2px solid #ccc",
        paddingBottom: "10px",
    };

    return (
        <div style={containerStyles}>
            <h1 style={headerStyles}>Admin Page</h1>
            <div style={sectionsContainerStyles}>
                <div style={sectionStyles}>
                    <ProductAdmin ref={productAdminRef} />
                </div>
            </div>
        </div>
    );
};

export default AdminPage;
