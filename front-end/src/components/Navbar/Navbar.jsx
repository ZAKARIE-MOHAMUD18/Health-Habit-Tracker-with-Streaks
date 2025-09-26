// src/components/Navbar/Navbar.jsx
import { useContext, useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { AuthContext } from "../../AuthContext";
import "./Navbar.css";

export default function Navbar() {
  const { user, logout } = useContext(AuthContext);
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          HabitTracker
        </Link>

        {/* ✅ Mobile toggle */}
        <button
          className="menu-toggle"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          ☰
        </button>

        {/* ✅ Navbar links */}
        <ul className={`navbar-links ${menuOpen ? "active" : ""}`}>
          {/* Home */}
          <li>
            <NavLink
              to="/"
              className={({ isActive }) =>
                isActive ? "active-link" : undefined
              }
            >
              Home
            </NavLink>
          </li>

          {user ? (
            <>
              

              {/* Habits */}
              <li>
                <NavLink
                  to="/habits"
                  className={({ isActive }) =>
                    isActive ? "active-link" : undefined
                  }
                >
                  Habits
                </NavLink>
              </li>

              {/* Challenges */}
              <li>
                <NavLink
                  to="/challenges"
                  className={({ isActive }) =>
                    isActive ? "active-link" : undefined
                  }
                >
                  Challenges
                </NavLink>
              </li>

               {/* Profile
              <li>
                <NavLink
                  to="/profile"
                  className={({ isActive }) =>
                    isActive ? "active-link" : undefined
                  }
                >
                  Profile
                </NavLink>
              </li> */}

              {/* Logout */}
              <li>
                <button className="logout-btn" onClick={logout}>
                  Logout
                </button>
              </li>
            </>
          ) : (
            <>
              {/* Login */}
              <li>
                <NavLink
                  to="/login"
                  className={({ isActive }) =>
                    isActive ? "active-link" : undefined
                  }
                >
                  Login
                </NavLink>
              </li>

              {/* Signup */}
              <li>
                <NavLink
                  to="/signup"
                  className={({ isActive }) =>
                    isActive ? "active-link" : undefined
                  }
                >
                  Signup
                </NavLink>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
}
