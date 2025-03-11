import React, { useState } from "react";
import { useLocation } from "react-router-dom"; // Import useLocation
// import Navbar from "./appbar";
import { Outlet } from "react-router-dom";
import { FiMenu } from "react-icons/fi";

const Layout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation(); // Get current route

  return (
    <div style={{ display: "flex", width: "100%" }}>
      {/* Sidebar */}
      {location.pathname !== "/" && ( // Hide sidebar on "/"
        <div
          style={{
            width: sidebarOpen ? "250px" : "0",
            background: "linear-gradient(to right, #ff4500, #ef9e39)",
            position: "fixed",
            top: "0",
            left: "0",
            bottom: "0",
            transition: "width 0.3s ease",
            height: "100%",
            overflowX: "hidden",
          }}
        />
      )}

      {/* Main Content Area */}
      <div
        style={{
          flex: 1,
          marginLeft: location.pathname !== "/" && sidebarOpen ? "250px" : "0", // Push content only if not "/"
          transition: "margin-left 0.3s ease",
          width: "100%",
        }}
      >
        {/* Navbar with Hamburger */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            background: "linear-gradient(to right, #ff4500, #ef9e39)",
            color: "white",
            padding: "15px",
            position: "fixed",
            top: "0",
            left: "0",
            width: "100%",
            zIndex: "1000",
          }}
        >
          {location.pathname !== "/" && ( // Hide Hamburger on "/"
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              style={{
                background: "transparent",
                border: "none",
                color: "white",
                fontSize: "24px",
                cursor: "pointer",
                marginRight: "20px",
              }}
            >
              <FiMenu />
            </button>
          )}
          <h2>Portfolio Dashboard</h2>
        </div>

        {/* Page Content */}
        <div style={{ marginTop: "60px", padding: "20px" }}>
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default Layout;
