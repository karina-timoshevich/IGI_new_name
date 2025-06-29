import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../utils/api";
import config from "../config";

const Catalog = () => {
    const [items, setItems] = useState([]);
    const [name, setSearch] = useState("");
    const [sort, setOrder] = useState("asc");


    useEffect(() => {
        fetchItems();
    }, [name, sort]);


    const fetchItems = () => {
        api
            .get("/products", { params: { name, sort} })
            .then((response) => setItems(response.data))
            .catch((error) => console.error("Error fetching items:", error));
    };


    const containerStyles = {
        padding: "20px",
        color: "#333",
        minHeight: "100vh",
    };

    const filterStyles = {
        display: "flex",
        gap: "10px",
        marginBottom: "20px",
        flexWrap: "wrap",
    };

    const selectStyles = {
        padding: "10px",
        borderRadius: "5px",
        border: "1px solid #ccc",
        backgroundColor: "#fff",
        color: "#333",
        flex: "1 1 200px",
    };

    const gridStyles = {
        display: "grid",
        gridTemplateColumns: "repeat(3, 1fr)",
        gap: "20px",
    };

    const cardStyles = {
        backgroundColor: "#fff",
        padding: "20px",
        borderRadius: "10px",
        boxShadow: "0 0 15px rgba(0, 0, 0, 0.1)",
        textAlign: "center",
        transition: "transform 0.3s",
    };

    const imageStyles = {
        width: "100%",
        height: "200px",
        objectFit: "cover",
        borderRadius: "10px",
        marginBottom: "10px",
    };

    const buttonStyles = {
        padding: "10px 20px",
        borderRadius: "5px",
        border: "none",
        cursor: "pointer",
        backgroundColor: "#009688",
        color: "#fff",
        textDecoration: "none",
        transition: "background-color 0.3s",
    };

    return (
        <div style={containerStyles}>
            <h1>Catalog</h1>
            <div style={filterStyles}>
                <input
                    type="text"
                    placeholder="Search by name of product"
                    value={name}
                    onChange={(e) => setSearch(e.target.value)}
                    style={selectStyles}
                />

                <select
                    value={sort}
                    onChange={(e) => setOrder(e.target.value)}
                    style={selectStyles}
                >
                    <option value="price_asc">Ascending</option>
                    <option value="price_desc">Descending</option>
                </select>

            </div>

            <div style={gridStyles}>
                {items.map((item) => (
                    <div
                        key={item._id}
                        style={cardStyles}
                        onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.05)")}
                        onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
                    >
                        {item.imageUrl && (
                            <img
                                src={`${item.imageUrl}`}
                                alt={item.name}
                                style={imageStyles}
                            />
                        )}
                        <h2>{item.name}</h2>
                        <p>{item.price} BYN</p>
                        <Link
                            to={`/item/${item._id}`}
                            state={{ item }}
                            style={buttonStyles}
                        >
                            More Details
                        </Link>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Catalog;
