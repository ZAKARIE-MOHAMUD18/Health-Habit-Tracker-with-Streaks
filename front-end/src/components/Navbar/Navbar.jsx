import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <Link to="/">Habit Tracker</Link>
      </div>

      {/* Hamburger Icon */}
      <div className="hamburger" onClick={toggleMenu}>
        <div className={isOpen ? "bar open" : "bar"}></div>
        <div className={isOpen ? "bar open" : "bar"}></div>
        <div className={isOpen ? "bar open" : "bar"}></div>
      </div>

      {/* Nav Links */}
      <ul className={isOpen ? "navbar-links active" : "navbar-links"}>
        <li>
          <Link to="/dashboard" onClick={toggleMenu}>Dashboard</Link>
        </li>
        <li>
          <Link to="/habits" onClick={toggleMenu}>Habits</Link>
        </li>
        <li>
          <Link to="/challenges" onClick={toggleMenu}>Challenges</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
