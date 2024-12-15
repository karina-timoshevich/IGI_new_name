import express from "express";
import jwt from "jsonwebtoken"
import mongoose from "mongoose"
import bcrypt from 'bcrypt'
import {validationResult} from 'express-validator';
import {registerValidation} from './validations/auth.js'
import userModel from "./models/user.js"
import checkAuth from "./utils/checkAuth.js"
mongoose.connect('mongodb://root:example@localhost:27017/onlinestore', {
    authSource: "admin"
})
.then(() => console.log('DB ok'))
.catch((err) => console.log('DB error', err));


const app = express();
app.use(express.json());

app.post('/auth/register',registerValidation, async(req, res)=>{
    const errors = validationResult(req);
    if (!errors.isEmpty()){
        return res.status(400).json(errors.array());
    }
    try {
        const password = req.body.password;
        const salt = await bcrypt.genSalt(10);
        const passwordHash = await bcrypt.hash(password, salt);

        const doc = new userModel({
            name: req.body.name,
            email: req.body.email,
            passwordHash: passwordHash,
            birthday: req.body.birthday,
            phone: req.body.phone,
        });

        const user = await doc.save();
        const {passwordHash: _, ...userWithoutPassword} = user._doc;
        const token = jwt.sign({_id: user._id}, 'secret123', {expiresIn: '1h'});
        res.json({...userWithoutPassword, token});

    }
    catch (error){
        console.error(error.message);
        return res.status(500).json({message: "Error occurred when registering user"});
    }
});

app.post('/auth/login', async(req, res)=>{
    try {
        const user = await userModel.findOne({email: req.body.email});
        if (!user){
            return res.status(400).json({message: "Wrong email or password"});
        }
        const validPassword = await bcrypt.compare(req.body.password, user._doc.passwordHash);
        if (!validPassword){
            return res.status(400).json({message: "Wrong email or password"});
        }
        const {passwordHash: _, ...userWithoutPassword} = user._doc;
        const token = jwt.sign({_id: user._id}, 'secret123', {expiresIn: '1h'});
        res.json({...userWithoutPassword, token});
    }
    catch (error){
        console.error(error.message);
        return res.status(500).json({message: "Error occurred when logging in"});
    }
});

app.get('/auth/me', checkAuth, async(req, res)=> {
    try {
        const user = await userModel.findById(req.user_id);
        if (!user){
            return res.status(404).json({message: "User not found"});
        }
        const {passwordHash: _, ...userWithoutPassword} = user._doc;
        res.json(userWithoutPassword);

    } catch (error) {
        console.error(error.message);
        return res.status(400).json({message: "Error occurred when getting user info"});
    }
});

app.listen(4444, (err)=>{
if(err){
    return console.log(err);
}
console.log("Server OK");
});