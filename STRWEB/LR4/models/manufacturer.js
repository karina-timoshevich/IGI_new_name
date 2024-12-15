import mongoose from "mongoose";
const manufacturerSchema = new mongoose.Schema({
        name: {
            type: String,
            required: true,
        },
        country: {
            type: String,
            required: true,
        },
    },
    {
        timestamps: true,
    })

export default mongoose.model('Manufacturer', manufacturerSchema);