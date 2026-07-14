import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Detect from "./pages/Detect";
import Symptoms from "./pages/Symptoms";
import Chatbot from "./pages/chatbot";
import Navbar from "./components/Navbar";

function App() {
  return (
    <Router>

      <Navbar />

      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/detect" element={<Detect />} />
          <Route path="/symptoms" element={<Symptoms />} />
          <Route path="/chatbot" element={<Chatbot />} />
        </Routes>
      </div>

    </Router>
  );
}

export default App;