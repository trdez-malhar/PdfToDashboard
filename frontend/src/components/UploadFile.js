import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import axios from "axios";
import Typed from "typed.js";
import "bootstrap/dist/css/bootstrap.min.css";

const UploadFile = () => {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0);
  const navigate = useNavigate(); // Initialize navigation
  useEffect(() => {
    // Initialize Typed.js effect
    const typed = new Typed("#typed", {
      strings: ["Welcome to Wealth Management Journey"],
      typeSpeed: 50,
      backSpeed: 25,
      showCursor: false,
      loop: false,
    });

    return () => {
      typed.destroy(); // Clean up effect on unmount
    };
  }, []);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setStatus(""); // Reset status on new file selection
  };

  const handleUpload = async (event) => {
    event.preventDefault();
    if (!file) {
      setStatus("Please select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    
    setStatus(""); 
    setLoading(true);
    let startTime = Date.now();

    const interval = setInterval(() => {
      setElapsedTime(((Date.now() - startTime) / 1000).toFixed(1));
    }, 100);

    try {
      const response = await axios.post("http://127.0.0.1:5000/api/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        withCredentials: true, // Ensure cookies (session) are sent
      });

      clearInterval(interval);
      setLoading(false);

      if (response.data.status === "error") {
        setStatus(response.data.message);
      }  
      else if (response.data.status === "success") {
        const userId = response.data.session_id; // Get user_id from response
  
        // ✅ Save user ID in localStorage
        localStorage.setItem("session_id", userId);
  
        console.log("User ID saved:", userId);
        setStatus("Upload successful! Redirecting...");
        setTimeout(() => {
            navigate("/dashboard"); // Use React Router navigation
        }, 1000);
      }
    } catch (error) {
      clearInterval(interval);
      setLoading(false);
      setStatus(error.response?.data?.message || "An error occurred.");
    }
  };

  return (
    <div className="d-flex flex-column align-items-center justify-content-center vh-100 text-center">
      <h2 className="typed-text text-primary mb-3">
        <span id="typed"></span>
      </h2>

      <div className="upload-container bg-white p-4 rounded shadow-lg" style={{ width: "400px" }}>
        <h3 className="mb-3">Upload a PDF File</h3>
        <form onSubmit={handleUpload}>
          <input type="file" onChange={handleFileChange} accept="application/pdf" className="form-control mb-2" />
          <button type="submit" className="btn btn-primary w-100" disabled={loading}>
            {loading ? `Uploading... ${elapsedTime} sec` : "Upload"}
          </button>
        </form>
        {status && <p className="mt-2 text-danger">{status}</p>}
      </div>
    </div>
  );
};

export default UploadFile;
