import React from "react";
import HabitList from "../../components/HabitList/HabitList";
import "./Habits.css";

function Habits({ userId }) {
  if (!userId) {
    return (
      <div className="habits-page">
        <h2>Please select a user first 👤</h2>
      </div>
    );
  }

  return (
    <div className="habits-page">
      <h1>Habits</h1>
      <HabitList userId={userId} />
    </div>
  );
}

export default Habits;
