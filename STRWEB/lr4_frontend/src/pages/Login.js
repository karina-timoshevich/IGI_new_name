import React, { useContext } from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { useNavigate } from "react-router-dom";
import api from "../utils/api";
import { AuthContext } from "../context/AuthContext";

const Login = () => {
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const formik = useFormik({
    initialValues: {
      email: "",
      password: "",
    },
    validationSchema: Yup.object({
      email: Yup.string().required("Username or Email is required"),
      password: Yup.string().required("Password is required"),
    }),
    onSubmit: async (values) => {
      try {
         console.log("Submitting form with values:", values);
        await login(values.email, values.password);
        navigate("/catalog");
      } catch (error) {

        console.error(error);
      }
    },
  });

  const handleGoogleLogin = (e) => {
    e.preventDefault();
    window.location.href = "http://localhost:7300/api/users/google";
  };

  const containerStyles = {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    backgroundColor: "#f0f0f0", // Removed theme dependency
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
    backgroundColor: "#007bff",
    color: "#fff",
  };

  return (
    <div style={containerStyles}>
      <form onSubmit={formik.handleSubmit} style={formStyles}>
        <h1>Login</h1>
        <input
          type="text"
          placeholder="Username or Email"
          {...formik.getFieldProps("email")}
          style={inputStyles}
        />
        {formik.touched.identifier && formik.errors.identifier ? (
          <div>{formik.errors.identifier}</div>
        ) : null}
        <input
          type="password"
          placeholder="Password"
          {...formik.getFieldProps("password")}
          style={inputStyles}
        />
        {formik.touched.password && formik.errors.password ? (
          <div>{formik.errors.password}</div>
        ) : null}
        <button type="submit" style={buttonStyles}>
          Login
        </button>
        <button onClick={handleGoogleLogin} style={buttonStyles}>
          Login with Google
        </button>
      </form>
    </div>
  );
};
export default Login;