import { useState, useEffect } from "react";
import { getHabits, addHabitBackend, toggleHabitBackend } from "./api";
import "./App.css";

function App() {
  const [habits, setHabits] = useState([]);
  const [newHabit, setNewHabit] = useState("");

  // Utility function to check if a habit is completed today
  const isCompletedToday = (habit) => {
    const todayStr = new Date().toISOString().slice(0, 10);
    return habit.lastCompletedDate === todayStr;
  };

  useEffect(() => {
    async function fetchHabits() {
      const data = await getHabits();
      const updated = data.map((h) => ({
        ...h,
        completedToday: isCompletedToday(h),
      }));
      setHabits(updated);
    }
    fetchHabits();
  }, []);

  const addHabit = async () => {
    if (!newHabit.trim()) return;
    const habit = await addHabitBackend(newHabit.trim());
    if (!habit) return;
    habit.completedToday = false;
    setHabits([...habits, habit]);
    setNewHabit("");
  };

  const toggleHabit = async (index) => {
    const updatedHabit = await toggleHabitBackend(index);
    if (!updatedHabit) return;
    updatedHabit.completedToday = isCompletedToday(updatedHabit);
    const updatedHabits = [...habits];
    updatedHabits[index] = updatedHabit;
    setHabits(updatedHabits);
  };

  return (
    <div className="container">
      <h1>Habit Tracker</h1>

      <div className="input-group">
        <input
          type="text"
          value={newHabit}
          onChange={(e) => setNewHabit(e.target.value)}
          placeholder="New habit..."
        />
        <button onClick={addHabit}>Add</button>
      </div>

      {habits.length === 0 && (
        <p className="no-habits">No habits yet. Add one above!</p>
      )}

      <ul>
        {habits.map((habit, index) => (
          <li
            key={index}
            className={`habit-item ${habit.completedToday ? "done" : ""}`}
          >
            <span className="habit-name">{habit.name}</span>
            <div className="habit-controls">
              <span
                className={`streak ${habit.streak >= 7 ? "high-streak" : ""}`}
              >
                🔥 {habit.streak}
              </span>
              <button
                onClick={() => toggleHabit(index)}
                className={habit.completedToday ? "undo" : ""}
              >
                {habit.completedToday ? "Undo" : "Done"}
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
