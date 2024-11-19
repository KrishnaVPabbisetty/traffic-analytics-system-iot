import React from "react";
import Dashboard from "./components/Dashboard";
import "./App.css";

function App() {
  return (
    <div className="app-container">
      <nav className="bg-blue-600 text-white p-4">
        <div className="container mx-auto">
          <h1 className="text-2xl font-bold">Traffic Analytics System</h1>
        </div>
      </nav>
      <main className="container mx-auto p-4">
        <Dashboard />
      </main>
      <footer className="bg-gray-100 p-4 mt-8">
        <div className="container mx-auto text-center text-gray-600">
          <p>Traffic Analytics System © 2024</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
