import React, { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const AdminRoute = ({ element, adminOnly }) => {
  const { user } = useContext(AuthContext);

  if (!user) {
    return <Navigate to="/login" />;
  }

if (adminOnly && !['admin'].includes(user.role)) {
  return <Navigate to="/catalog" />;
}

  return element;
};

export default AdminRoute;