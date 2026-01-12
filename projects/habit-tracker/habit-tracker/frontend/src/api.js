const API_URL = "http://localhost:3000";

export async function getHabits() {
  try {
    const res = await fetch(`${API_URL}/habits`);
    if (!res.ok) throw new Error("Failed to fetch habits");
    return res.json();
  } catch (err) {
    console.error(err);
    return [];
  }
}

export async function addHabitBackend(name) {
  try {
    const res = await fetch(`${API_URL}/habits`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });
    if (!res.ok) throw new Error("Failed to add habit");
    return res.json();
  } catch (err) {
    console.error(err);
    return null;
  }
}

export async function toggleHabitBackend(index) {
  try {
    const res = await fetch(`${API_URL}/habits/${index}/toggle`, {
      method: "PUT",
    });
    if (!res.ok) throw new Error("Failed to toggle habit");
    return res.json();
  } catch (err) {
    console.error(err);
    return null;
  }
}
