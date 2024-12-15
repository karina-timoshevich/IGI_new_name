import ProductModel from '../models/product.js'
import mongoose from "mongoose";
export const create = async (req, res) => {
    console.log('--- Request received ---');
    console.log('Request body:', req.body);
    try {
        const doc = new ProductModel({
            name: req.body.name,
            manufacturer_id: req.body.manufacturer_id,
            price: req.body.price,
            imageUrl: req.body.imageUrl,
        });
        console.log('Document to save:', doc);
        const product = await doc.save();
        console.log('Saved product:', product);
        res.json(product);
    } catch (err) {
        console.error('Error creating product:', err);
        res.status(500).json({ message: "Error occurred when creating product" });
    }
};

