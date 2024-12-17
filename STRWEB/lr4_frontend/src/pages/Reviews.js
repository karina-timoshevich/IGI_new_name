import React, { useState, useEffect, useContext, useRef } from "react";
import { AuthContext } from "../context/AuthContext";
import api from "../utils/api";
import moment from "moment";

const Reviews = () => {
    const { user } = useContext(AuthContext);
    const [reviews, setReviews] = useState([]);
    const [rating, setRating] = useState(1);
    const [comment, setComment] = useState("");
    const formRef = useRef(null);

    useEffect(() => {
        fetchReviews();
    }, []);

    const fetchReviews = async () => {
        try {
            const response = await api.get("/reviews");
            setReviews(response.data);
        } catch (error) {
            console.error("Error fetching reviews:", error);
        }
    };

    const addReview = async (e) => {
        e.preventDefault();
        try {
            const newReview = { rating, comment };
            await api.post("/reviews/create", newReview, {
                headers: { authorization: localStorage.getItem("token") },
            });
            fetchReviews();
            setRating(1);
            setComment("");
        } catch (error) {
            console.error("Error adding review:", error);
        }
    };

    const containerStyles = {
        padding: "20px",
        backgroundColor: "#f9f9f9",
        minHeight: "100vh",
    };

    const formStyles = {
        display: "flex",
        flexDirection: "column",
        gap: "10px",
        marginBottom: "20px",
        maxWidth: "600px",
        margin: "0 auto",
        backgroundColor: "#fff",
        padding: "20px",
        borderRadius: "10px",
        boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
    };

    const inputStyles = {
        padding: "10px",
        borderRadius: "5px",
        border: "1px solid #ccc",
        fontSize: "16px",
    };

    const buttonStyles = {
        padding: "10px 20px",
        borderRadius: "5px",
        backgroundColor: "#009688",
        color: "#fff",
        border: "none",
        cursor: "pointer",
        fontSize: "16px",
        transition: "background-color 0.3s",
    };

    const reviewListStyles = {
        marginTop: "20px",
        display: "flex",
        flexDirection: "column",
        gap: "20px",
    };

    const reviewCardStyles = {
        backgroundColor: "#fff",
        padding: "20px",
        borderRadius: "10px",
        boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
    };

    const serviceTitleStyles = {
        fontSize: "14px",
        fontWeight: "bold",
        marginBottom: "10px",
        color: "#777",
    };

    const commentStyles = {
        fontSize: "16px",
        marginBottom: "10px",
        color: "#555",
    };

    const userStyles = {
        fontSize: "14px",
        color: "#777",
    };

    const renderStars = (rating) => {
        return Array.from({ length: 5 }, (_, index) => (
            <span
                key={index}
                style={{
                    color: index < rating ? "#ffd700" : "#ddd",
                    fontSize: "18px",
                }}
            >
                ★
            </span>
        ));
    };


    return (
        <div style={containerStyles}>
            <h1 style={{ textAlign: "center", marginBottom: "20px" }}>Reviews</h1>
            {user && (
                <form onSubmit={addReview} style={formStyles} ref={formRef}>
                    <h2 style={{ marginBottom: "10px", fontSize: "20px" }}>Add a Review</h2>
                    <input
                        type="number"
                        min="1"
                        max="5"
                        value={rating}
                        onChange={(e) => setRating(e.target.value)}
                        required
                        placeholder="Rating (1 to 5)"
                        style={inputStyles}
                    />
                    <textarea
                        placeholder="Write your comment"
                        value={comment}
                        onChange={(e) => setComment(e.target.value)}
                        style={inputStyles}
                    />
                    <button type="submit" style={buttonStyles}>
                        Submit Review
                    </button>
                </form>
            )}
            <div style={reviewListStyles}>
                {reviews.map((review) => (
                    <div key={review._id} style={reviewCardStyles}>
                        <p style={serviceTitleStyles}>
                            {moment(review.created_at).format("MMMM Do YYYY, h:mm:ss a")}
                        </p>
                        <div>{renderStars(review.rating)}</div>
                        <p style={commentStyles}>{review.comment}</p>
                        <p style={userStyles}>By: {review.user_id.email}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Reviews;
