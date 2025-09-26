import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../../AuthContext";
import { useNavigate } from "react-router-dom";
import "./Challenges.css";

function Challenges() {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const [challenges, setChallenges] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/challenges")
      .then((res) => res.json())
      .then((data) => setChallenges(data))
      .catch((err) => console.error("Error fetching challenges:", err));
  }, []);

  const handleJoin = async (challengeId) => {
    if (!user) {
      alert("Please log in first");
      navigate("/login");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:5000/user_challenges", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: user.id,
          challenge_id: challengeId,
          join_date: new Date().toISOString().split("T")[0],
          status: "active",
        }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || "Failed to join challenge");
      }

      await res.json();
      navigate("/profile");
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className="challenges">
      <h1>Community Challenges</h1>
      <div className="challenge-list">
        {challenges.length > 0 ? (
          challenges.map((ch) => (
            <div key={ch.id} className="challenge-card">
              <h2>{ch.title}</h2>
              <p>{ch.description}</p>
              <button onClick={() => handleJoin(ch.id)}>Join</button>
            </div>
          ))
        ) : (
          <p>No challenges available.</p>
        )}
      </div>
    </div>
  );
}

export default Challenges;
