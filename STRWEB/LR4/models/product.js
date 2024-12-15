import mongoose from "mongoose";
const productSchema = new mongoose.Schema({
        name: {
            type: String,
            required: true,
        },
        manufacturer_id: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'Manufacturer',
            required: true,
        },
        price:{
            type: Number,
            required: true,
        },
        imageUrl: String,
    },
    {
        timestamps: true,
    })

export default mongoose.model('product', productSchema);