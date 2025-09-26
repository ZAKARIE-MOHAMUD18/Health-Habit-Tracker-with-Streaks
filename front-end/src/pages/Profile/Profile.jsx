// src/pages/Profile/Profile.jsx
import { useEffect, useState, useContext } from "react";
import { AuthContext } from "../../AuthContext";
import "./Profile.css";

export default function Profile() {
  const { user } = useContext(AuthContext); // logged-in user
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!user?.id) {
      setLoading(false);
      return;
    }

    fetch(`http://127.0.0.1:5000/profile/${user.id}`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch profile");
        return res.json();
      })
      .then((data) => {
        setProfileData(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [user]);

  if (loading) return <p>Loading profile...</p>;
  if (error) return <p className="error">{error}</p>;
  if (!profileData) return <p>No profile data found.</p>;

  return (
    <div className="profile-container">
      {/* User Info */}
      <div className="profile-header">
        <h2>{profileData.name}</h2>
        <p>Email: {profileData.email}</p>
      </div>

      {/* Habits Section */}
      <div className="profile-section">
        <h3>My Habits</h3>
        {profileData.habits && profileData.habits.length > 0 ? (
          <ul className="profile-list">
            {profileData.habits.map((habit) => (
              <li key={habit.id} className="profile-card">
                <strong>{habit.title}</strong>
                <p>Frequency: {habit.frequency}</p>
                {habit.description && <p>{habit.description}</p>}
              </li>
            ))}
          </ul>
        ) : (
          <p>No habits yet.</p>
        )}
      </div>

      {/* Challenges Section */}
      <div className="profile-section">
        <h3>My Challenges</h3>
        {profileData.challenges && profileData.challenges.length > 0 ? (
          <ul className="profile-list">
            {profileData.challenges.map((challenge) => (
              <li key={challenge.id} className="profile-card">
                <strong>{challenge.title}</strong>
                {challenge.description && <p>{challenge.description}</p>}
                {challenge.start_date && challenge.end_date && (
                  <p>
                    {challenge.start_date} → {challenge.end_date}
                  </p>
                )}
              </li>
            ))}
          </ul>
        ) : (
          <p>No challenges joined yet.</p>
        )}
      </div>
    </div>
  );
}
