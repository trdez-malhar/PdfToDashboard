// src/components/Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <div style={styles.navbar}>
      <h3 style={styles.title}>My Dashboard</h3>
      <div style={styles.navLinks}>
        <Link to="/" style={styles.link}>Upload</Link>
        {/* <Link to="/dashboard" style={styles.link}>Dashboard</Link> */}
      </div>
    </div>
  );
};

const styles = {
  navbar: {
    width: '100%',
    height: '60px',
    backgroundColor: 'darkorange',
    color: 'white',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '0 20px',
    position: 'fixed',
    top: '0',
    left: '0',
    zIndex: '1000',
  },
  title: {
    margin: 0,
  },
  navLinks: {
    display: 'flex',
    gap: '15px',
  },
  link: {
    color: 'white',
    textDecoration: 'none',
    fontSize: '16px',
  },
};

export default Navbar;
