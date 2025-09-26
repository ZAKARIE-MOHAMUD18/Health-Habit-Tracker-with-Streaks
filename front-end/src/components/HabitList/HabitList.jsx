import React, { useEffect, useState } from "react";
import "./HabitList.css";

export default function HabitList({ userId }) {
  const [habits, setHabits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // For editing
  const [editingHabit, setEditingHabit] = useState(null);
  const [editTitle, setEditTitle] = useState("");
  const [editFrequency, setEditFrequency] = useState("");

  // For creating new habit
  const [newTitle, setNewTitle] = useState("");
  const [newFrequency, setNewFrequency] = useState("daily");

  // Fetch habits
  useEffect(() => {
    if (!userId) return;

    const fetchHabits = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`http://127.0.0.1:5000/habits?user_id=${userId}`);
        if (!res.ok) throw new Error("Failed to fetch habits");

        const data = await res.json();
        setHabits(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchHabits();
  }, [userId]);

  // Create habit
  const handleCreate = async () => {
    if (!newTitle) return alert("Title is required");

    try {
      const res = await fetch("http://127.0.0.1:5000/habits", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: userId,
          title: newTitle,
          frequency: newFrequency,
          start_date: new Date().toISOString().split("T")[0],
        }),
      });

      if (!res.ok) throw new Error("Failed to create habit");
      const habit = await res.json();
      setHabits([habit, ...habits]);
      setNewTitle("");
      setNewFrequency("daily");
    } catch (err) {
      alert(err.message);
    }
  };

  // Delete habit
  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this habit?")) return;

    try {
      const res = await fetch(`http://127.0.0.1:5000/habits/${id}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error("Failed to delete habit");
      setHabits(habits.filter((h) => h.id !== id));
    } catch (err) {
      alert(err.message);
    }
  };

  // Start editing
  const startEdit = (habit) => {
    setEditingHabit(habit.id);
    setEditTitle(habit.title);
    setEditFrequency(habit.frequency);
  };

  // Cancel editing
  const cancelEdit = () => {
    setEditingHabit(null);
    setEditTitle("");
    setEditFrequency("");
  };

  // Save edited habit
  const saveEdit = async (id) => {
    try {
      const res = await fetch(`http://127.0.0.1:5000/habits/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: editTitle, frequency: editFrequency }),
      });
      if (!res.ok) throw new Error("Failed to update habit");

      const updatedHabit = await res.json();
      setHabits(habits.map((h) => (h.id === id ? updatedHabit : h)));
      cancelEdit();
    } catch (err) {
      alert(err.message);
    }
  };

  if (loading) return <p>Loading habits...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div>
      {/* Create habit form */}
      <div className="create-habit">
        <input
          placeholder="New habit title"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
        />
        <select
          value={newFrequency}
          onChange={(e) => setNewFrequency(e.target.value)}
        >
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </select>
        <button onClick={handleCreate}>Add Habit</button>
      </div>

      {/* Habits list */}
      {habits.length === 0 ? (
        <p>No habits found.</p>
      ) : (
        <ul className="habit-list">
          {habits.map((habit) => (
            <li key={habit.id} className="habit-card">
              {editingHabit === habit.id ? (
                <div>
                  <input
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                  />
                  <select
                    value={editFrequency}
                    onChange={(e) => setEditFrequency(e.target.value)}
                  >
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="monthly">Monthly</option>
                  </select>
                  <button onClick={() => saveEdit(habit.id)}>Save</button>
                  <button onClick={cancelEdit}>Cancel</button>
                </div>
              ) : (
                <div>
                  <h3>{habit.title}</h3>
                  <p>Frequency: {habit.frequency}</p>
                  {habit.description && <p>{habit.description}</p>}
                  <button onClick={() => startEdit(habit)}>Edit</button>
                  <button onClick={() => handleDelete(habit.id)}>Delete</button>
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
