import React from "react";
import PropTypes from "prop-types";
import { useLocation } from "react-router-dom";
import config from "../config";
import moment from "moment";

const ProductDetails = () => {
  const location = useLocation();
  const { item } = location.state || {};

  if (!item) return <div>Loading...</div>;

  const containerStyles = {
    padding: "20px",
    minHeight: "100vh",
  };

  const itemStyles = {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    textAlign: "center",
  };

  const imageStyles = {
    width: "300px",
    height: "400px",
    objectFit: "cover",
    borderRadius: "5px",
    marginBottom: "20px",
  };

  return (
    <div style={containerStyles}>
      <div style={itemStyles}>
        {item.imageUrl && (
          <img
            src={item.imageUrl}
            alt={item.name}
            style={imageStyles}
          />
        )}
        <h1>{item.name}</h1>
        <p>Price: ${item.price}</p>
        {item.manufacturer_id && (
          <p>Manufacturer: {item.manufacturer_id.name}</p>
        )}
        {item.manufacturer_id && item.manufacturer_id.country && (
          <p>Country: {item.manufacturer_id.country}</p>
        )}
         {item.createdAt && (
          <p>Created At: {moment(item.createdAt).format("YYYY-MM-DD HH:mm:ss")}</p>
        )}
        {item.updatedAt && (
          <p>Updated At: {moment(item.updatedAt).format("YYYY-MM-DD HH:mm:ss")}</p>
        )}
      </div>
    </div>
  );
};

ProductDetails.propTypes = {
  item: PropTypes.shape({
    name: PropTypes.string.isRequired,
    price: PropTypes.number.isRequired,
    imageUrl: PropTypes.string,
    createdAt: PropTypes.string,
    updatedAt: PropTypes.string,
    manufacturer_id: PropTypes.shape({
      name: PropTypes.string,
      country: PropTypes.string,
    }),
  }),
};

ProductDetails.defaultProps = {
  item: {
    name: "Unknown Name",
    price: 0,
    imageUrl: "",
    createdAt: moment().format("YYYY-MM-DD HH:mm:ss"),
    updatedAt: moment().format("YYYY-MM-DD HH:mm:ss"),
    manufacturer_id: {
      name: "Unknown Manufacturer",
      country: "Unknown",
    },
  },
};

export default ProductDetails;
