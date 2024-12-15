import ProductModel from '../models/product.js'
import mongoose from "mongoose";
import Product from "../models/product.js";
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

export const getAll = async (req, res) => {
  try {
    const products = await ProductModel.find().populate('manufacturer_id').exec();
    res.json(products);
  } catch (err) {
    console.error('Error fetching products:', err);
    res.status(500).json({
      message: 'Не удалось получить список продуктов',
    });
  }
};

export const getOne = async (req, res) => {
    try {
        const productId = req.params.id;
        if (!mongoose.Types.ObjectId.isValid(productId)) {
            return res.status(400).json({ message: "Invalid product ID" });
        }

        const product = await Product.findById(productId).populate('manufacturer_id').exec();

        if (!product) {
            return res.status(404).json({ message: "Product not found" });
        }

        res.json(product);
    } catch (err) {
        console.log(err);
        res.status(400).json({
            message: 'Could not get the products',
        });
    }
};

export const update = async (req, res) => {
  try {
    const productId = req.params.id;

    // Проверяем, существует ли продукт
    const product = await ProductModel.findById(productId);
    if (!product) {
      return res.status(404).json({
        message: 'Продукт не найден',
      });
    }

    // Обновляем продукт
    const updatedProduct = await ProductModel.findByIdAndUpdate(
      productId,
      {
        name: req.body.name || product.name,  // Если новое значение есть, то обновляем
        manufacturer_id: req.body.manufacturer_id || product.manufacturer_id,
        price: req.body.price || product.price,
        imageUrl: req.body.imageUrl || product.imageUrl,
      },
      { new: true }  // Возвращаем обновленный документ
    );

    res.json(updatedProduct);  // Возвращаем обновленный продукт
  } catch (err) {
    console.log(err);
    res.status(500).json({
      message: 'Не удалось обновить продукт',
    });
  }
};

export const remove = async (req, res) => {
    try {
        const productId = req.params.id;

        if (!mongoose.Types.ObjectId.isValid(productId)) {
            return res.status(400).json({
                message: 'Invalid product ID',
            });
        }

        const deletedProduct = await Product.findOneAndDelete({ _id: productId });

        if (!deletedProduct) {
            return res.status(404).json({
                message: 'Product not found',
            });
        }

        res.json({
            success: true,
            message: 'Product deleted successfully',
        });
    } catch (err) {
        console.error(err);
        res.status(500).json({
            message: 'Could not delete the product',
        });
    }
};
