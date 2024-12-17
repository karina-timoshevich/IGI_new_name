import React, { Component } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

class Navbar extends Component {
    static contextType = AuthContext;

    render() {
       // const { user } = this.context;

        const navStyles = {
            ul: {
                listStyle: "none",
                display: "flex",
                gap: "40px",
            },
            li: {
                display: "inline",
            },
            a: {
                textDecoration: "none",
                color: "inherit",
            },
        };

        return (
            <nav>
                <ul style={navStyles.ul}>
                    <li style={navStyles.li}>
                        <Link to="/catalog" style={navStyles.a}>
                            Catalog
                        </Link>
                    </li>
                    <li style={navStyles.li}>
                        <Link to="/reviews" style={navStyles.a}>
                            Reviews
                        </Link>
                    </li>
                    {/* {user && user.isAdmin && (
                        <li style={navStyles.li}>
                            <Link to="/admin" style={navStyles.a}>
                                Admin
                            </Link>
                        </li>
                    )}*/}
                </ul>
            </nav>
        );
    }
}

export default Navbar;
