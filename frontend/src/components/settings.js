import React, { useState } from "react";
import "./SettingsPage.css"; // Import the CSS file

export default function SettingsPage() {
  const [darkMode, setDarkMode] = useState(false);
  const [emailNotifications, setEmailNotifications] = useState(true);
  const [username, setUsername] = useState("JohnDoe");

  return (
    <div className="settings-container">
      <h1>Settings</h1>

      {/* Account Section */}
      <div className="settings-card">
        <h2>Account</h2>
        <label>Username:</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <button>Save</button>
      </div>

      {/* Dark Mode Toggle */}
      <div className="settings-card">
        <h2>Dark Mode</h2>
        <p>Enable dark theme</p>
        <label className="switch">
          <input
            type="checkbox"
            checked={darkMode}
            onChange={() => setDarkMode(!darkMode)}
          />
          <span className="slider"></span>
        </label>
      </div>

      {/* Email Notifications Toggle */}
      <div className="settings-card">
        <h2>Email Notifications</h2>
        <p>Receive updates via email</p>
        <label className="switch">
          <input
            type="checkbox"
            checked={emailNotifications}
            onChange={() => setEmailNotifications(!emailNotifications)}
          />
          <span className="slider"></span>
        </label>
      </div>
    </div>
  );
}
