import React from "react";
import "./Challenges.css";

function Challenges() {
  const challenges = [
    { id: 1, title: "30-Day Water Challenge", description: "Drink 2L water daily" },
    { id: 2, title: "Meditation Streak", description: "Meditate for 10 min daily" },
  ];

  return (
    <div className="challenges">
      <h1>Community Challenges</h1>
      <div className="challenge-list">
        {challenges.map((ch) => (
          <div key={ch.id} className="challenge-card">
            <h2>{ch.title}</h2>
            <p>{ch.description}</p>
            <button>Join</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Challenges;
