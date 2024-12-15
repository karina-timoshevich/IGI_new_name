import mongoose from "mongoose";
const userSchema = new mongoose.Schema({
        name: {
            type: String,
            required: true,
        },
        role:{
             type: String,
            enum: ['admin', 'client'],
            default: 'client',
            required: true,
        },
        email: {
            type: String,
            required: true,
            unique: true
        },
        birthday:{
            type: Date,
            required: true,
        },
        passwordHash:{
            type: String,
            required: true,
        },
        phone: String,
    },
    {
        timestamps: true,
    })

export default mongoose.model('user', userSchema);