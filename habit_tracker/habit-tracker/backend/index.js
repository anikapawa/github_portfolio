import express from "express";
import fs from "fs";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

const HABITS_FILE = "./habits.json";

function readHabits() {
  try {
    const data = fs.readFileSync(HABITS_FILE, "utf-8");
    return JSON.parse(data || "[]");
  } catch (err) {
    return [];
  }
}

function writeHabits(habits) {
  fs.writeFileSync(HABITS_FILE, JSON.stringify(habits, null, 2));
}

app.get("/habits", (req, res) => {
  const habits = readHabits();
  res.json(habits);
});

app.post("/habits", (req, res) => {
  const { name } = req.body;
  const habits = readHabits();
  const newHabit = { name, streak: 0, lastCompletedDate: null };
  habits.push(newHabit);
  writeHabits(habits);
  res.json(newHabit);
});

app.put("/habits/:index/toggle", (req, res) => {
  const index = parseInt(req.params.index);
  const habits = readHabits();
  if (!habits[index]) return res.status(404).send("Habit not found");

  const habit = habits[index];
  const today = new Date().toISOString().slice(0, 10);

  if (habit.lastCompletedDate === today) {
    habit.lastCompletedDate = null;
    habit.streak = Math.max(habit.streak - 1, 0);
  } else {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const yesterdayStr = yesterday.toISOString().slice(0, 10);

    if (habit.lastCompletedDate === yesterdayStr) {
      habit.streak += 1;
    } else {
      habit.streak = 1;
    }

    habit.lastCompletedDate = today;
  }

  habits[index] = habit;
  writeHabits(habits);
  res.json(habit);
});

app.listen(3000, () => console.log("Server running on http://localhost:3000"));