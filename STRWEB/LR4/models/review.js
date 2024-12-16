import mongoose from "mongoose";
const reviewSchema = new mongoose.Schema({
        comment: {
            type: String,
            required: true,
        },
        user_id: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'user',
            required: true,
        },
        rating:{
            type: Number,
            required: true,
        }
    },
    {
        timestamps: true,
    })

export default mongoose.model('review', reviewSchema);