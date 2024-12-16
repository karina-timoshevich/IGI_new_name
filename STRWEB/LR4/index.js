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
import passport from "passport";
import session from 'express-session';
import './config/passport.js';
import * as ReviewController from './controllers/reviewController.js';
import {CreateReviewValidation} from "./validations/review.js";


const app = express();
app.use(express.json());
app.use(session({ secret: process.env.SESSION_SECRET, resave: false, saveUninitialized: false }));
app.use(passport.initialize());
app.use(passport.session());

mongoose.connect('mongodb://root:example@localhost:27017/onlinestore', {
    authSource: "admin"
})
.then(() => console.log('DB ok'))
.catch((err) => console.log('DB error', err));

app.use(express.json());
app.post('/auth/register',registerValidation, UserController.register);
app.post('/auth/login',loginValidation,  UserController.login);
app.get('/auth/me', checkAuth, UserController.getMe);
app.get('/api/users/google', passport.authenticate('google', { scope: ['profile', 'email'] }));
app.get(
    '/api/users/google/callback',
    passport.authenticate('google', { failureRedirect: '/auth/login' }),
    (req, res) => {
        res.json({
            message: 'Google authentication successful!',
            token: req.user.jwtToken,
            user: req.user,
        });
    }
);


app.post('/products/create',checkAuth, checkRole(['admin']),CreateProductValidation, ProductController.create);
app.get('/products', ProductController.getAll);
app.get('/products/:id', ProductController.getOne);
app.put('/products/update/:id',checkAuth, checkRole(['admin']),CreateProductValidation, ProductController.update);
app.delete('/products/delete/:id',checkAuth, checkRole(['admin']),CreateProductValidation, ProductController.remove);

app.post('/reviews/create', checkAuth, checkRole(['client', 'admin']), CreateReviewValidation, ReviewController.create);
app.get('/reviews', ReviewController.getAll);


app.listen(7300, (err)=>{
if(err){
    return console.log(err);
}
console.log("Server OK");
});