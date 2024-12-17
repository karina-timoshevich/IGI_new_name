import React, { useState, useEffect, useContext, useRef } from "react";
import { AuthContext } from "../context/AuthContext";
import api from "../utils/api";

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
      headers: { "authorization": localStorage.getItem("token") },
    });
    fetchReviews();
    setRating(1);
    setComment("");
  } catch (error) {
    console.error("Error adding review:", error);
  }
};


  return (
    <div style={{ padding: "20px" }}>
      <h1>Reviews</h1>
      {user && (
        <form
          onSubmit={addReview}
          style={{ display: "flex", flexDirection: "column", gap: "10px", marginBottom: "20px", maxWidth: "600px", margin: "0 auto" }}
          ref={formRef}
        >
          <input
            type="number"
            min="1"
            max="5"
            value={rating}
            onChange={(e) => setRating(e.target.value)}
            required
            style={{ padding: "10px", borderRadius: "5px" }}
          />
          <textarea
            placeholder="Comment"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            style={{ padding: "10px", borderRadius: "5px" }}
          />
          <button type="submit" style={{ padding: "10px 20px", borderRadius: "5px", backgroundColor: "#009688", color: "#fff" }}>
            Add Review
          </button>
        </form>
      )}
      <div style={{ marginTop: "20px", display: "flex", flexDirection: "column", gap: "20px" }}>
        {reviews.map((review) => (
          <div key={review._id} style={{ backgroundColor: "#fff", padding: "20px", borderRadius: "5px" }}>
            <div>
              <h3>{review.service?.title || "No Service"}</h3>
              <div>{Array.from({ length: 5 }, (_, index) => (index < review.rating ? "★" : "☆")).join("")}</div>
              <p>{review.comment}</p>
              <p>By: {review.user_id.name}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Reviews;
