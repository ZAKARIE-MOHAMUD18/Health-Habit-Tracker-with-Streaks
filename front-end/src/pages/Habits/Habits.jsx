import { useEffect, useState } from "react";
import "./Habits.css";

export default function Habits() {
  const [habits, setHabits] = useState([]);
  const [newHabit, setNewHabit] = useState({
    title: "",
    description: "",
    frequency: "daily",
    start_date: "",
    user_id: 1, // temporary hardcoded user (adjust later)
  });

  // Fetch all habits
  useEffect(() => {
    fetch("http://127.0.0.1:5000/habits")
      .then((res) => res.json())
      .then((data) => setHabits(data))
      .catch((err) => console.error("Error fetching habits:", err));
  }, []);

  // CREATE habit
  function handleAddHabit(e) {
    e.preventDefault();
    fetch("http://127.0.0.1:5000/habits", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newHabit),
    })
      .then((res) => res.json())
      .then((data) => {
        setHabits([...habits, data]);
        setNewHabit({
          title: "",
          description: "",
          frequency: "daily",
          start_date: "",
          user_id: 1,
        });
      })
      .catch((err) => console.error("Error adding habit:", err));
  }

  // UPDATE habit (quick demo: just change title)
  function handleUpdateHabit(id) {
    const updatedTitle = prompt("Enter new title:");
    if (!updatedTitle) return;

    fetch(`http://127.0.0.1:5000/habits/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: updatedTitle }),
    })
      .then((res) => res.json())
      .then((updated) => {
        setHabits(habits.map((h) => (h.id === id ? updated : h)));
      })
      .catch((err) => console.error("Error updating habit:", err));
  }

  // DELETE habit
  function handleDeleteHabit(id) {
    fetch(`http://127.0.0.1:5000/habits/${id}`, {
      method: "DELETE",
    })
      .then(() => {
        setHabits(habits.filter((h) => h.id !== id));
      })
      .catch((err) => console.error("Error deleting habit:", err));
  }

  return (
    <div className="habits-container">
      <h1>My Habits</h1>

      {/* Add Habit Form */}
      <form className="habit-form" onSubmit={handleAddHabit}>
        <input
          type="text"
          placeholder="Title"
          value={newHabit.title}
          onChange={(e) => setNewHabit({ ...newHabit, title: e.target.value })}
        />
        <input
          type="text"
          placeholder="Description"
          value={newHabit.description}
          onChange={(e) =>
            setNewHabit({ ...newHabit, description: e.target.value })
          }
        />
        <select
          value={newHabit.frequency}
          onChange={(e) =>
            setNewHabit({ ...newHabit, frequency: e.target.value })
          }
        >
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </select>
        <input
          type="date"
          value={newHabit.start_date}
          onChange={(e) =>
            setNewHabit({ ...newHabit, start_date: e.target.value })
          }
        />
        <button type="submit">Add Habit</button>
      </form>

      {/* Habits List */}
      {habits.length === 0 ? (
        <p className="no-habits">No habits found.</p>
      ) : (
        <ul className="habit-list">
          {habits.map((habit) => (
            <li key={habit.id} className="habit-card">
              <div>
                <strong>{habit.title}</strong>
                <span>({habit.frequency})</span>
              </div>
              <div>
                <button onClick={() => handleUpdateHabit(habit.id)}>Edit</button>
                <button onClick={() => handleDeleteHabit(habit.id)}>Delete</button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
