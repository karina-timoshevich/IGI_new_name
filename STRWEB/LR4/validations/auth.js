import {body} from 'express-validator';
export const registerValidation = [
     body('email').isEmail().withMessage('Please enter a valid email address'),
     body('password').isLength({min: 6}).withMessage('Password must be at least 6 characters long'),
     body('name').isLength({min: 3}).withMessage('Name must be at least 2 characters long'),
     body('birthday').isDate().withMessage('Please enter a valid date'),
     body('phone').optional()
                        .matches(/^\+375(25|29|33|44|17)\d{7}$/)
                        .withMessage('Please enter a valid phone number in the format +375XXXXXXXXX'),
];