import React from "react";
import "./Home.css";

function Home() {
  return (
    <div className="home">
      {/* Hero Section */}
      <section className="hero">
        <h1>Welcome to Health & Habit Tracker</h1>
        <p>
          Track your daily habits, stay motivated with streaks, and push
          yourself with community challenges.
        </p>
      </section>

      {/* Features Section */}
      <section className="features">
        <div className="feature-card">
          <h2>📊 Dashboard</h2>
          <p>Visualize your progress with streaks and charts.</p>
        </div>
        <div className="feature-card">
          <h2>🔥 Streaks</h2>
          <p>Keep the momentum going — don’t break the chain!</p>
        </div>
        <div className="feature-card">
          <h2>🤝 Challenges</h2>
          <p>Join challenges with friends and stay accountable together.</p>
        </div>
      </section>
    </div>
  );
}

export default Home;
