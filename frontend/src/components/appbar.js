// src/components/Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';
import { FaSearch, FaBell, FaCog, FaBars } from 'react-icons/fa';

const Navbar = ({ toggleSidebar }) => {
  return (
    <div style={styles.navbar}>
      {/* Hamburger Menu Icon */}
      <FaBars style={styles.icon} onClick={toggleSidebar} />

      {/* Search Bar */}
      <div style={styles.searchContainer}>
        <FaSearch style={styles.searchIcon} />
        <input type="text" placeholder="Search" style={styles.searchInput} />
      </div>

      {/* Right-side Icons */}
      <div style={styles.iconContainer}>
        <FaBell style={styles.icon} />
        <Link to="/settings"><FaCog style={styles.icon} /></Link>
        <div style={styles.profileIcon}></div>
      </div>
    </div>
  );
};


const styles = {
  navbar: {
    width: "100%",
    height: "60px",
    backgroundColor: "white",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 20px",
    boxShadow: "0px 2px 10px rgba(0, 0, 0, 0.1)",
    position: "fixed",
    top: "0",
    left: "0",
    zIndex: "1000",
  },
  searchContainer: {
    display: "flex",
    alignItems: "center",
    backgroundColor: "#f5f5f5",
    borderRadius: "20px",
    padding: "5px 10px",
    width: "250px",
  },
  searchIcon: {
    color: "#888",
    marginRight: "8px",
  },
  searchInput: {
    border: "none",
    background: "none",
    outline: "none",
    width: "100%",
  },
  iconContainer: {
    display: "flex",
    alignItems: "center",
    gap: "15px",
  },
  icon: {
    color: "#555",
    fontSize: "20px",
    cursor: "pointer",
    marginBottom: "10px"
  },
  profileIcon: {
    width: "35px",
    height: "35px",
    borderRadius: "50%",
    backgroundColor: "#ccc",
    // marginBottom: "10px"
  },
};

export default Navbar;