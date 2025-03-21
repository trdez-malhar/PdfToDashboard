// src/components/Sidebar.js
import React from "react";
import { Link } from "react-router-dom";
import { FaTimes } from "react-icons/fa";  // ✅ Correct close icon
const Sidebar = ({ isOpen, toggleSidebar }) => {
  return (
    <div style={{ ...styles.sidebar, width: isOpen ? "250px" : "0" }}>
      {/* Close Button */}
      <button onClick={toggleSidebar} style={styles.closeBtn}>
        <FaTimes />
      </button>

      {/* Sidebar Content (Only visible when open) */}
      {isOpen && (
        <ul style={styles.navList}>
          <li><Link to="/dashboard" style={styles.link}>Dashboard</Link></li>
          <li><Link to="/settings" style={styles.link}>Settings</Link></li>
        </ul>
      )}
    </div>
  );
};

const styles = {
  sidebar: {
    height: "100vh",
    backgroundColor: "#333",
    color: "white",
    position: "fixed",
    top: "0",
    left: "0",
    overflowX: "hidden",
    transition: "width 0.3s ease",
    paddingTop: "20px",
  },
  closeBtn: {
    position: "absolute",
    top: "10px",
    right: "10px",
    background: "transparent",
    border: "none",
    color: "white",
    fontSize: "24px",
    cursor: "pointer",
  },
  navList: {
    listStyleType: "none",
    padding: 0,
  },
  link: {
    color: "white",
    textDecoration: "none",
    display: "block",
    padding: "15px 20px",
  },
};

export default Sidebar;