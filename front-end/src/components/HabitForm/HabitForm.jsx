import React, { useState } from "react";
import "./HabitForm.css";

function HabitForm({ onAddHabit }) {
  const [title, setTitle] = useState("");
  const [frequency, setFrequency] = useState("Daily");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title) return;

    const newHabit = {
      id: Date.now(),
      title,
      frequency,
    };

    onAddHabit(newHabit);
    setTitle("");
    setFrequency("Daily");
  };

  return (
    <form className="habit-form" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Enter habit..."
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <select value={frequency} onChange={(e) => setFrequency(e.target.value)}>
        <option value="Daily">Daily</option>
        <option value="Weekly">Weekly</option>
      </select>
      <button type="submit">Add Habit</button>
    </form>
  );
}

export default HabitForm;
