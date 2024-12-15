import {body} from 'express-validator';
export const CreateProductValidation = [
     body('name').isString().withMessage('Please enter a valid name'),
     body('price').isFloat().withMessage('Price must be a number'),
     body('manufacturer_id').isString().withMessage('Manufacturer id must be a number'),
     body('imageUrl').isURL().optional().withMessage('Invalid image url'),
];