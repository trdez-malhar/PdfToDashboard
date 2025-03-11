// src/components/Sidebar.js
import React from "react";
import { Link } from "react-router-dom";

const Sidebar = () => {
  return (
    <div style={styles.sidebar}>
      <h2>Menu</h2>
      <ul style={styles.navList}>
        {/* <li><Link to="/" style={styles.link}>Upload</Link></li> */}
        {/* <li><Link to="/dashboard" style={styles.link}>Dashboard</Link></li> */}
      </ul>
    </div>
  );
};

const styles = {
  sidebar: {
    width: "250px",
    height: "100vh",
    backgroundColor: "black",
    color: "white",
    padding: "20px",
    position: "fixed",
  },
  navList: {
    listStyleType: "none",
    padding: 0,
  },
  link: {
    color: "white",
    textDecoration: "none",
    display: "block",
    padding: "10px 0",
  },
};

export default Sidebar;
