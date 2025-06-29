import { body } from 'express-validator';

export const CreateReviewValidation = [
    body('comment')
        .isString()
        .withMessage('Comment must be a valid string')
        .isLength({ min: 5 })
        .withMessage('Comment must be at least 5 characters long'),

    body('user_id')
        .isMongoId()
        .withMessage('User ID must be a valid ObjectId'),

    body('rating')
        .isInt({ min: 1, max: 5 })
        .withMessage('Rating must be an integer between 1 and 5'),
];
