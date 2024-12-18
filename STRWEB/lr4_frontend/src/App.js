import React, {useEffect, useState} from "react";
import {BrowserRouter as Router, Link, Route, Routes} from "react-router-dom";
// import Home from "./pages/Home";
import ItemDetails from "./pages/ItemDetails";
// import AdminPage from "./pages/AdminPage";
import Login from "./pages/Login";
import Reviews from "./pages/Reviews";
import { AuthProvider } from "./context/AuthContext";
import Register from "./pages/Register";
import Catalog from "./pages/Catalog";
// import { ThemeProvider } from "./context/ThemeContext";
// import ProtectedRoute from "./components/ProtectedRoute";
import Header from "./components/Header";
import AdminRoute from "./components/AdminRoute";
import AdminPage from "./pages/AdminPage";
import axios from "axios";
// import Footer from "./components/Footer";

function App() {
  const appStyles = {
    display: "flex",
    flexDirection: "column",
    minHeight: "100vh",
    overflowX: "hidden",
  };

  const mainStyles = {
    flex: 1,
    marginTop: "60px",
    display: "flex",
    justifyContent: "center",
  };

  const contentStyles = {
    width: "100%",
  };
 const [currentDate, setCurrentDate] = useState("");
    const [timeZone, setTimeZone] = useState("");
    const [utcDate, setUtcDate] = useState("");

    useEffect(() => {
        const fetchTimeZone = async () => {
            try {
                const response = await axios.get("http://ip-api.com/json");
                const timezone = response.data.timezone;
                if (timezone) {
                    setTimeZone(timezone);
                } else {
                    setTimeZone("UTC");
                }
            } catch (error) {
                console.error("Error fetching time zone:", error);
                setTimeZone("UTC");
            }
        };

        const updateDate = () => {
            const date = new Date();
            try {
                const formattedCurrentDate = date.toLocaleString("en-US", { timeZone: timeZone || "UTC" });
                setCurrentDate(formattedCurrentDate);
            } catch (error) {
                console.error("Error formatting date:", error);
                setCurrentDate(date.toLocaleString("en-US", { timeZone: "UTC" }));
            }

            setUtcDate(new Date().toLocaleString("en-US", { timeZone: "UTC" }));
        };

        fetchTimeZone();
        updateDate();
        const intervalId = setInterval(updateDate, 1000);

        return () => clearInterval(intervalId);
    }, [timeZone]);

    const timeZoneStyles = {
        fontSize: "0.8rem",
        marginTop: "5px",
        marginBottom: "5px",
    };


 return (
    <AuthProvider>

        <Router>
          <div style={appStyles}>
            <Header/>
            <main style={mainStyles}>
              <div style={contentStyles}>
                <Routes>
                  <Route path="/catalog" element={<Catalog/>}/>
                  <Route path="/item/:id" element={<ItemDetails/>}/>
                  <Route path="/reviews" element={<Reviews />} />
                  <Route path="/admin" element={ <AdminRoute element={<AdminPage/>} adminOnly/> } />
                  <Route path="/login" element={<Login/>}/>
                  <Route path="/register" element={<Register/>}/>
                </Routes>
              </div>
            </main>
            <footer style={{textAlign: "center", padding: "10px"}}>
               Hello from Karina Timoshevich :)
               <div>
                <p style={timeZoneStyles}>Current Date: {currentDate}  |  Time Zone: {timeZone}  |  UTC Time: {utcDate}</p>
            </div>
            </footer>
          </div>
        </Router>

    </AuthProvider>
 );
}

export default App;