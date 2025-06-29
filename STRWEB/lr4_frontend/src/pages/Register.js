import React, { useState } from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { useNavigate } from "react-router-dom";
import api from "../utils/api";

const Register = () => {
    const navigate = useNavigate();
    const [serverError, setServerError] = useState("");
    const today = new Date().toISOString().split("T")[0];


    const formik = useFormik({
        initialValues: {
            name: "",
            email: "",
            password: "",
            birthday: "",
            phone: "",
        },
        validationSchema: Yup.object({
            name: Yup.string()
                .required("Name is required"),
            email: Yup.string()
                .email("Invalid email address")
                .required("Email is required"),
            password: Yup.string()
                .min(6, "Password must be at least 6 characters")
                .required("Password is required"),
            birthday: Yup.date()
                .nullable()
                .max(new Date(), "Birthday cannot be in the future")
                .test(
                    "is-18",
                    "You must be at least 18 years old",
                    (value) => {
                        if (!value) return false;
                        const today = new Date();
                        const birthDate = new Date(value);
                        const age = today.getFullYear() - birthDate.getFullYear();
                        const monthDiff = today.getMonth() - birthDate.getMonth();
                        return (
                            age > 18 || (age === 18 && monthDiff >= 0 && today.getDate() >= birthDate.getDate())
                        );
                    }
                ),
            phone: Yup.string()
                .matches(
                    /^\+375(25|29|33|44|17)\d{7}$/,
                    "Please enter a valid phone number in the format +375XXXXXXXXX"
                ).nullable(),

        }),
        onSubmit: async (values) => {
            try {
                await api.post("/auth/register", values);
                navigate("/login");
            } catch (error) {
                setServerError(error.response?.data?.message || "Registration failed. Please try again.");
                console.error("Error during registration:", error);
            }
        },
    });


    const containerStyles = {
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
    };

    const formStyles = {
        display: "flex",
        flexDirection: "column",
        gap: "10px",
        padding: "20px",
        backgroundColor: "#fff",
        color: "#000",
        borderRadius: "5px",
        boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
        maxWidth: "400px",
        width: "100%",
    };

    const inputStyles = {
        padding: "10px",
        borderRadius: "5px",
        border: "1px solid #ccc",
        backgroundColor: "#fff",
        color: "#000",
    };

    const buttonStyles = {
        padding: "10px",
        borderRadius: "5px",
        border: "none",
        cursor: "pointer",
        backgroundColor: "#009688",
        color: "#fff",
        fontWeight: "bold",
    };

    const errorStyles = {
        color: "red",
        marginBottom: "10px",
    };

    return (
        <div style={containerStyles}>
            <form onSubmit={formik.handleSubmit} style={formStyles}>
                <h1>Register</h1>
                {serverError && <div style={errorStyles}>{serverError}</div>}

                {/* Поле Name */}
                <input
                    type="text"
                    placeholder="Name"
                    {...formik.getFieldProps("name")}
                    style={inputStyles}
                />
                {formik.touched.name && formik.errors.name ? (
                    <div style={errorStyles}>{formik.errors.name}</div>
                ) : null}

                <input
                    type="email"
                    placeholder="Email"
                    {...formik.getFieldProps("email")}
                    style={inputStyles}
                />
                {formik.touched.email && formik.errors.email ? (
                    <div style={errorStyles}>{formik.errors.email}</div>
                ) : null}

                <input
                    type="password"
                    placeholder="Password"
                    {...formik.getFieldProps("password")}
                    style={inputStyles}
                />
                {formik.touched.password && formik.errors.password ? (
                    <div style={errorStyles}>{formik.errors.password}</div>
                ) : null}

                <input
                    type="date"
                    max={today}
                    placeholder="Birthday"
                    {...formik.getFieldProps("birthday")}
                    style={inputStyles}
                />
                {formik.touched.birthday && formik.errors.birthday ? (
                    <div style={errorStyles}>{formik.errors.birthday}</div>
                ) : null}

                <input
                    type="text"
                    placeholder="Phone (+375XXXXXXXXX)"
                    {...formik.getFieldProps("phone")}
                    style={inputStyles}
                />
                {formik.touched.phone && formik.errors.phone ? (
                    <div style={errorStyles}>{formik.errors.phone}</div>
                ) : null}


                <button type="submit" style={buttonStyles}>
                    Register
                </button>
            </form>
        </div>
    );
};

export default Register;
