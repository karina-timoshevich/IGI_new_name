
import {request} from "express";

export const checkRole = (roles) => (req, res, next) => {
    if (!roles.includes(req.role)) {
        return res.status(403).json({ message: "Access denied" });
    }
    next();
};
