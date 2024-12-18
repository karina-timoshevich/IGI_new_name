import React, { Component } from "react";
import axios from "axios";

class ApiClass extends Component {
    constructor(props) {
        super(props);
        this.state = {
            dogImage: null,
            catImage: null,
            error: "",
        };

        this.fetchDogImage = this.fetchDogImage.bind(this);
        this.fetchCatImage = this.fetchCatImage.bind(this);
    }

    async fetchDogImage() {
        try {
            const response = await axios.get("https://dog.ceo/api/breeds/image/random");
            this.setState({ dogImage: response.data.message, error: "" });
        } catch (error) {
            this.setState({ error: "Failed to fetch dog image." });
        }
    }

    async fetchCatImage() {
        try {
            const response = await axios.get("https://api.thecatapi.com/v1/images/search");
            this.setState({ catImage: response.data[0].url, error: "" });
        } catch (error) {
            this.setState({ error: "Failed to fetch cat image." });
        }
    }

    render() {
        const { dogImage, catImage, error } = this.state;

        return (
            <div style={{ padding: "20px", fontFamily: "Arial, sans-serif", textAlign: "center" }}>
                <h1 style={{ marginBottom: "20px" }}>Animal Images</h1>

                <div style={{ display: "flex", justifyContent: "center", gap: "20px" }}>

                    <div
                        style={{
                            width: "250px",
                            border: "1px solid #ddd",
                            borderRadius: "8px",
                            padding: "10px",
                            textAlign: "center",
                        }}
                        onDoubleClick={this.fetchDogImage}
                    >
                        <h3 style={{ fontSize: "18px", marginBottom: "10px" }}>Random Dog</h3>
                        {dogImage && (
                            <img
                                src={dogImage}
                                alt="Random Dog"
                                style={{
                                    width: "100%",
                                    height: "200px",
                                    objectFit: "cover",
                                    borderRadius: "4px",
                                }}
                            />
                        )}
                        {!dogImage && (
                            <button
                                onClick={this.fetchDogImage}
                                style={{
                                    padding: "8px 12px",
                                    fontSize: "14px",
                                    border: "none",
                                    borderRadius: "4px",
                                    backgroundColor: "#4CAF50",
                                    color: "white",
                                    cursor: "pointer",
                                    marginTop: "10px",
                                }}
                            >
                                Fetch Dog Image
                            </button>
                        )}
                    </div>

                    <div
                        style={{
                            width: "250px",
                            border: "1px solid #ddd",
                            borderRadius: "8px",
                            padding: "10px",
                            textAlign: "center",
                        }}
                        onDoubleClick={this.fetchCatImage}
                    >
                        <h3 style={{ fontSize: "18px", marginBottom: "10px" }}>Random Cat</h3>
                        {catImage && (
                            <img
                                src={catImage}
                                alt="Random Cat"
                                style={{
                                    width: "100%",
                                    height: "200px",
                                    objectFit: "cover",
                                    borderRadius: "4px",
                                }}
                            />
                        )}
                        {!catImage && (
                            <button
                                onClick={this.fetchCatImage}
                                style={{
                                    padding: "8px 12px",
                                    fontSize: "14px",
                                    border: "none",
                                    borderRadius: "4px",
                                    backgroundColor: "#4CAF50",
                                    color: "white",
                                    cursor: "pointer",
                                    marginTop: "10px",
                                }}
                            >
                                Fetch Cat Image
                            </button>
                        )}
                    </div>
                </div>

                {error && <p style={{ color: "red", marginTop: "20px" }}>{error}</p>}
            </div>
        );
    }
}

export default ApiClass;
