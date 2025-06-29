import mongoose from "mongoose";
import Manufacturer from "../models/manufacturer.js";

export const getAll = async (req, res) => {
    try {
        const manufacturers = await Manufacturer.find();

        res.status(200).json(manufacturers);
    } catch (error) {
        console.error("Error fetching manufacturers:", error);
        res.status(500).json({
            message: "Error occurred while fetching manufacturers",
            error: error.message,
        });
    }
};
