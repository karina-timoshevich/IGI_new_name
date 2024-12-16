import ReviewModel from '../models/review.js';
import mongoose from 'mongoose';
import {request} from "express";

export const create = async (req, res) => {
    console.log('--- Request received ---');
    console.log('Request body:', req.body);
    try {
        const doc = new ReviewModel({
            comment: req.body.comment,
            user_id: req.user_id,
            rating: req.body.rating,
        });
        console.log('Document to save:', doc);

        const review = await doc.save();
        console.log('Saved review:', review);

        res.json(review);
    } catch (err) {
        console.error('Error creating review:', err);
        res.status(500).json({ message: "Error occurred when creating review" });
    }
};

export const getAll = async (req, res) => {
    try {
        const { sort, user_id } = req.query;

        const filter = user_id
            ? { user_id: mongoose.Types.ObjectId(user_id) }
            : {};

        const sortOptions = sort === 'rating_asc' ? { rating: 1 } : sort === 'rating_desc' ? { rating: -1 } : {};

        const reviews = await ReviewModel.find(filter)
            .populate('user_id')
            .sort(sortOptions)
            .exec();

        res.json(reviews);
    } catch (err) {
        console.error('Error fetching reviews:', err);
        res.status(500).json({
            message: 'Не удалось получить список отзывов',
        });
    }
};
