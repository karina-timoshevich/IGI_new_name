import React, { useState, useEffect, forwardRef, useImperativeHandle } from "react";
import api from "../utils/api";
import '../styles/ProductAdmin.css';
const ProductAdmin = forwardRef((props, ref) => {
    const [products, setProducts] = useState([]);
    const [manufacturers, setManufacturers] = useState([]);
    const [name, setName] = useState("");
    const [manufacturer_id, setManufacturer] = useState("");
    const [price, setPrice] = useState("");
    const [imageUrl, setPhotoUrl] = useState("");
    const [editMode, setEditMode] = useState(false);
    const [editProductId, setEditProductId] = useState(null);
    const [error, setError] = useState("");

    useEffect(() => {
        fetchProducts();
        fetchManufacturers();
    }, []);

    const fetchProducts = async () => {
        try {
            const response = await api.get("/products");
            setProducts(response.data);
        } catch (error) {
            console.error("Error fetching products:", error);
        }
    };

    const fetchManufacturers = async () => {
        try {
            const response = await api.get("/manufacturers/all");
            setManufacturers(response.data);
        } catch (error) {
            console.error("Error fetching manufacturers:", error);
        }
    };

    useImperativeHandle(ref, () => ({
        fetchManufacturers,
    }));

   const addProduct = async (e) => {
    e.preventDefault();
    if (!name || !manufacturer_id || !price) {
        setError("Please fill in all required fields.");
        return;
    }

    const productData = {
        name,
        manufacturer_id,
        price,
       imageUrl,
    };

    console.log("Product data to be sent:", productData);

    try {
        await api.post("/products/create", productData, {
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("token")}`,
                "Content-Type": "application/json",
            },
        });
        fetchProducts();
        resetForm();
    } catch (error) {
        console.error("Error adding product:", error);
        setError("Failed to add product.");
    }
};

    const resetForm = () => {
        setName("");
        setManufacturer("");
        setPrice("");
        setPhotoUrl("");
        setError("");
        setEditMode(false);
        setEditProductId(null);
    };

    const startEditProduct = (product) => {
        setEditMode(true);
        setEditProductId(product._id);
        setName(product.name);
        setManufacturer(product.manufacturer_id?._id || "");
        setPrice(product.price);
        setPhotoUrl(product.imageUrl || "");
    };

   const editProduct = async (e) => {
    e.preventDefault();
    if (!name || !manufacturer_id || !price) {
        setError("Please fill in all required fields.");
        return;
    }

    const productData = {
        name,
        manufacturer_id,
        price,
        imageUrl,
    };

    try {
        await api.put(`/products/update/${editProductId}`, productData, {
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("token")}`,
                "Content-Type": "application/json",
            },
        });
        fetchProducts();
        resetForm();
    } catch (error) {
        console.error("Error updating Product:", error);
        setError("Failed to update Product.");
    }
};

    const deleteProduct = async (id) => {
        try {
            await api.delete(`/products/delete/${id}`, {
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("token")}`,
                "Content-Type": "application/json",
            },
        });
            fetchProducts();
        } catch (error) {
            console.error("Error deleting Product:", error);
        }
    };
// onclick, onchange, onsubmit, onblur, ondoubleclick  то что ниже
 const handleManufacturerSelect = (selectedManufacturer, customParam) => {
        console.log("Selected Manufacturer:", selectedManufacturer);
        console.log("Custom Param:", customParam);
        setManufacturer(selectedManufacturer);
    };

  return (
        <div className="product-admin">
            <h2>Manage Products</h2>
            {error && <div className="error">{error}</div>}
            <form
                onSubmit={editMode ? editProduct : addProduct}
                className="product-form"
            >
                <input
                    type="text"
                    placeholder="Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="input-field"
                />
                <select
                    value={manufacturer_id}
                    onChange={(e) => handleManufacturerSelect(e.target.value, "customParam")}
                    className="input-field"
                >
                    <option value="">Select Manufacturer</option>
                    {manufacturers.map((m) => (
                        <option key={m._id} value={m._id}>
                            {m.name}
                        </option>
                    ))}
                </select>

                <input
                    type="number"
                    placeholder="Price"
                    value={price}
                    onChange={(e) => setPrice(e.target.value)}
                    className="input-field"
                />

                <input
                    type="text"
                    placeholder="Image URL"
                    value={imageUrl}
                    onChange={(e) => setPhotoUrl(e.target.value)}
                    className="input-field"
                />
                <button type="submit" className="submit-button">
                    {editMode ? "Update Product" : "Add Product"}
                </button>
                {editMode && (
                    <button type="button" onClick={resetForm} className="cancel-button">
                        Cancel
                    </button>
                )}
            </form>
            <div className="product-list">
                {products.map((product) => (
                    <div
                        key={product._id}
                        className="product-item"
                    >
                        <div>
                            <h4>{product.name}</h4>
                            <p>Price: ${product.price}</p>
                            <p>Manufacturer: {product.manufacturer_id?.name || "Unknown"}</p>
                        </div>
                        <div>
                            <button onClick={() => startEditProduct(product)} className="edit-button">Edit</button>
                            <button onClick={() => deleteProduct(product._id)} className="delete-button">Delete</button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
});

export default ProductAdmin;