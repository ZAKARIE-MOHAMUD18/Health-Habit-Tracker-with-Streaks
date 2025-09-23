import React from "react";
import "./Dashboard.css";

function Dashboard() {
  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <div className="dashboard-cards">
        <div className="card">
          <h2>Streaks 🔥</h2>
          <p>Keep going strong!</p>
        </div>
        <div className="card">
          <h2>Progress 📊</h2>
          <p>Your habits overview.</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
