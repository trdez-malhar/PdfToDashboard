import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import Navbar from "./appbar";
import Sidebar from "./sidebar";
import { Outlet } from "react-router-dom";
import { FiMenu } from "react-icons/fi";

const Layout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const isUploadPage = location.pathname === "/";
  // Function to toggle sidebar
  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);
  return (
    <div style={{ display: "flex", width: "100%" }}>
      {/* Sidebar (Only show on dashboard) */}
      {!isUploadPage && <Sidebar isOpen={sidebarOpen} />}
      
      {/* Main Content Area */}
      <div
        style={{
          flex: 1,
          marginLeft: !isUploadPage && sidebarOpen ? "250px" : "0", // Shift content when sidebar is open
          transition: "margin-left 0.3s ease",
          width: "100%",
        }}
      >
       {/* Navbar with Menu Button - Only on Dashboard */}
       {!isUploadPage && <Navbar toggleSidebar={toggleSidebar} />}
        {/* Page Content */}
        <div style={{ marginTop: !isUploadPage ? "60px" : "0", padding: "20px" }}>
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default Layout;
