import React, { useEffect, useState } from "react";
import HabitForm from "../HabitForm/HabitForm";
import "./HabitList.css";

function HabitList({ userId }) {
  const [habits, setHabits] = useState([]);

  // Fetch habits for selected user
  useEffect(() => {
    if (!userId) return;
    fetch("http://127.0.0.1:5000/habits")
      .then((res) => res.json())
      .then((data) => {
        const userHabits = data.filter((h) => h.user_id === userId);
        setHabits(userHabits);
      });
  }, [userId]);

  // Add new habit
  const handleAddHabit = (habit) => {
    fetch("http://127.0.0.1:5000/habits", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        title: habit.title,
        description: habit.description || "",
        frequency: habit.frequency.toLowerCase(),
        start_date: new Date().toISOString().split("T")[0],
      }),
    })
      .then((res) => res.json())
      .then((newHabit) => setHabits([...habits, newHabit]));
  };

  // Mark habit as done (log it)
  const handleMarkDone = (habitId) => {
    fetch("http://127.0.0.1:5000/habitlogs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        habit_id: habitId,
        date: new Date().toISOString().split("T")[0],
        status: true,
        note: "Marked from frontend",
      }),
    })
      .then((res) => res.json())
      .then(() => {
        alert("Habit logged as done ✅");
      });
  };

  return (
    <div className="habit-list">
      <h2>Your Habits</h2>
      <HabitForm onAddHabit={handleAddHabit} />
      <ul>
        {habits.map((habit) => (
          <li key={habit.id} className="habit-item">
            <span>
              {habit.title} <small>({habit.frequency})</small>
            </span>
            <button onClick={() => handleMarkDone(habit.id)}>Mark Done</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default HabitList;
