# Habit Tracker

## Brief Summary
Habit Tracker is a simple web application that allows users to track daily habits and monitor streaks for consecutive days. Users can add habits, mark them as done for the day, undo today’s completion, and see streaks persist across sessions. The app uses a React frontend and a Node.js + Express backend with persistent storage.

## Features Included
- Add new habits
- Mark habits as **Done** for the day
- Undo today’s completion
- Tracks **streaks** for consecutive days
- Persistent storage in a backend JSON file
- Responsive frontend built with React and Vite
- Backend API built with Node.js and Express

## Time Spent
Approximately **5 hours** developing this project from scratch.

## Running the Project Locally

### Prerequisites
- Node.js installed
- npm (comes with Node.js)

### Steps
1. **Clone the repository and navigate into it:**  
git clone https://github.com/anikapawa/habit-tracker.git  
cd habit-tracker

2. **Start the backend server:**
cd backend  
npm install  
node index.js  
The backend runs on: `http://localhost:3000`

3. **Start the frontend server** (in a separate terminal):
cd frontend  
npm install  
npm run dev  
The frontend will provide a local URL (e.g., `http://localhost:5173`) — open this in your browser.

4. **Use the app:**
- Add habits in the input field and click `Add`  
- Click `Done` to mark a habit for today  
- Click `Undo` to undo today’s completion  
- Streaks update automatically for consecutive days  
- Data persists across refreshes via the backend
