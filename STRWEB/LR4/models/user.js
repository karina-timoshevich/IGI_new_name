import mongoose from "mongoose";
const userSchema = new mongoose.Schema({
        name: {
            type: String,
            required: true,
        },
        googleId: {
            type: String
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
        },
        passwordHash:{
            type: String,
        },
        phone: String,
    },
    {
        timestamps: true,
    })

export default mongoose.model('user', userSchema);