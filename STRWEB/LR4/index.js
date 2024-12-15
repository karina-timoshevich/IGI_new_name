import express from "express";
import jwt from "jsonwebtoken"
import mongoose from "mongoose"
import bcrypt from 'bcrypt'
import {validationResult} from 'express-validator';
import {registerValidation} from './validations/auth.js'
import userModel from "./models/user.js"
mongoose.connect('mongodb://root:example@localhost:27017/onlinestore', {
    authSource: "admin"
})
.then(() => console.log('DB ok'))
.catch((err) => console.log('DB error', err));


const app = express();
app.use(express.json());


app.post('/auth/register',registerValidation, async (req, res)=>{
try {
    const errors = validationResult(req);
if (!errors.isEmpty()){
    return res.status(400).json(errors.array());
}

const password = req.body.password;
const salt = await bcrypt.genSalt(10);
const hash = await bcrypt.hash(password, salt)

const doc = new userModel({
    email: req.body.email,
    name: req.body.name,
    birthday: req.body.birthday,
    phone: req.body.phone,
    passwordHash: hash,
})

const user = await doc.save()
const token = jwt.sign({
    _id: user._id
}, 'secret123',
    {
    expiresIn: '1h',
    },
    )

const {passwordHash, ...userData} = user._doc
res.json({
    ... userData, token
})
}
catch(err){
    console.log(err);
   res.status(500).json({
       message: "Не удалось зарегистрироваться"
   })
}
})

app.listen(4444, (err)=>{
if(err){
    return console.log(err);
}
console.log("Server OK");
});