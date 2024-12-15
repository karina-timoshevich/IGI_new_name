import express from "express";
import jwt from "jsonwebtoken"
import mongoose from "mongoose"
import bcrypt from 'bcrypt'
import {validationResult} from 'express-validator';
import {loginValidation, registerValidation} from './validations/auth.js'
import userModel from "./models/user.js"
import checkAuth from "./utils/checkAuth.js"
import * as UserController from "./controllers/userController.js"
import User from "./models/user.js";
import * as ProductController from "./controllers/productController.js"
import {CreateProductValidation} from "./validations/product.js";
import {checkRole} from "./utils/checkRole.js";
mongoose.connect('mongodb://root:example@localhost:27017/onlinestore', {
    authSource: "admin"
})
.then(() => console.log('DB ok'))
.catch((err) => console.log('DB error', err));

const app = express();
app.use(express.json());
app.post('/auth/register',registerValidation, UserController.register);
app.post('/auth/login',loginValidation,  UserController.login);
app.get('/auth/me', checkAuth, UserController.getMe);

app.post('/products/create',checkAuth, checkRole(['admin']),CreateProductValidation, ProductController.create);

app.listen(4444, (err)=>{
if(err){
    return console.log(err);
}
console.log("Server OK");
});