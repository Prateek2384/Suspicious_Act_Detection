import React, { useState } from "react";
import "./App.css";
import { FaCamera, FaUpload } from "react-icons/fa";

const App = () => {
  const [image, setImage] = useState(null);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="landing-page">
      <nav className="navbar">
        <div className="logo">
          <span className="dot"></span> Suspicious Activity Detector
        </div>
        <ul className="nav-links">
          <li>Home</li>
          <li>About</li>
          <li>Services</li>
        </ul>
      </nav>
      <header className="hero-section">
        <h1>Suspicious Activity Detector</h1>
        <p>
          Detect suspicious human activities in real-time to enhance security
          and safety. Utilize advanced AI to monitor and analyze behavior
          automatically.
        </p>
        <div className="button-container">
          <button className="btn camera-btn">
            <FaCamera /> Camera
          </button>
          <label className="btn upload-btn">
            <FaUpload /> Upload
            <input
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
              hidden
            />
          </label>
        </div>
      </header>
      <section className="features-section">
        <h2>Features</h2>
        <div className="features">
          <div className="feature">
            <h3>Real-Time Monitoring</h3>
            <p>
              Continuously monitor activity through live video feeds to quickly
              identify potential threats.
            </p>
          </div>
          <div className="feature">
            <h3>AI-Driven Analysis</h3>
            <p>
              Leverage the power of artificial intelligence to detect abnormal
              and suspicious behaviors.
            </p>
          </div>
          <div className="feature">
            <h3>Enhanced Security</h3>
            <p>
              Improve the safety of public and private spaces with automated
              behavior detection.
            </p>
          </div>
        </div>
      </section>
      <footer className="footer">
        <p>© 2024 Suspicious Activity Detector, All rights reserved.</p>
        <div className="footer-links">
          <span>Privacy Policy</span>
          <span>Terms of Service</span>
        </div>
      </footer>
    </div>
  );
};

export default App;
