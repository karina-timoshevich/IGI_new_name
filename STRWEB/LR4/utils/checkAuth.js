import jwt from 'jsonwebtoken';
import {request} from "express";


export default (request, response, next) => {
    const authHeader = request.headers['authorization'];
    if (!authHeader){
        return response.status(401).json({message: "No token provided"});
    }
    const token = (authHeader).replace(/Bearer\s?/, '');
    if (!token){
        return response.status(403).json({message: "No access"});
    }
    try {
        const decoded = jwt.verify(token, 'secret123');
        request.user_id = decoded._id;
        request.role = decoded.role;
        next();
    }
    catch (error){
        console.error(error.message);
        return response.status(401).json({message: "Unauthorized"});
    }
}
