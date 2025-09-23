import React, { useEffect, useState } from "react";
import "./UserSelector.css";

function UserSelector({ onSelectUser }) {
  const [users, setUsers] = useState([]);
  const [selected, setSelected] = useState("");

  // Fetch users from backend
  useEffect(() => {
    fetch("http://127.0.0.1:5000/users")
      .then((res) => res.json())
      .then((data) => setUsers(data));
  }, []);

  const handleChange = (e) => {
    const userId = parseInt(e.target.value, 10);
    setSelected(userId);
    onSelectUser(userId);
  };

  return (
    <div className="user-selector">
      <label htmlFor="user-select">Select User:</label>
      <select id="user-select" value={selected} onChange={handleChange}>
        <option value="">-- Choose User --</option>
        {users.map((user) => (
          <option key={user.id} value={user.id}>
            {user.name}
          </option>
        ))}
      </select>
    </div>
  );
}

export default UserSelector;
