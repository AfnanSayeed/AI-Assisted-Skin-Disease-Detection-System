import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";

function Navbar() {
  const [lang, setLang] = useState(localStorage.getItem("lang") || "en");
  const location = useLocation();

  useEffect(() => {
    localStorage.setItem("lang", lang);
  }, [lang]);

  // 🔥 Dynamic link style (active highlight)
  const linkStyle = (path) => ({
    color: location.pathname === path ? "#3b82f6" : "#cbd5f5",
    textDecoration: "none",
    fontWeight: location.pathname === path ? "600" : "400",
    transition: "0.2s"
  });

  // 🔥 Hover handlers
  const handleHover = (e) => {
    e.target.style.color = "#3b82f6";
  };

  const handleLeave = (e, path) => {
    e.target.style.color =
      location.pathname === path ? "#3b82f6" : "#cbd5f5";
  };

  return (
    <div
      style={{
        position: "sticky",
        top: 0,
        zIndex: 1000,
        padding: "15px 30px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        background: "rgba(15, 23, 42, 0.85)",
        backdropFilter: "blur(12px)",
        borderBottom: "1px solid rgba(255,255,255,0.1)"
      }}
    >
      {/* 🧠 LOGO */}
      <h3
        style={{
          color: "#fff",
          fontWeight: "600",
          letterSpacing: "0.5px"
        }}
      >
        🧠 Skin AI
      </h3>

      {/* 🔗 NAV LINKS */}
      <div
        style={{
          display: "flex",
          gap: "20px",
          alignItems: "center"
        }}
      >
        <Link
          to="/"
          style={linkStyle("/")}
          onMouseEnter={handleHover}
          onMouseLeave={(e) => handleLeave(e, "/")}
        >
          Home
        </Link>

        <Link
          to="/detect"
          style={linkStyle("/detect")}
          onMouseEnter={handleHover}
          onMouseLeave={(e) => handleLeave(e, "/detect")}
        >
          Detect
        </Link>

        <Link
          to="/symptoms"
          style={linkStyle("/symptoms")}
          onMouseEnter={handleHover}
          onMouseLeave={(e) => handleLeave(e, "/symptoms")}
        >
          Symptoms
        </Link>

        <Link
          to="/chatbot"
          style={linkStyle("/chatbot")}
          onMouseEnter={handleHover}
          onMouseLeave={(e) => handleLeave(e, "/chatbot")}
        >
          Chatbot
        </Link>

        {/* 🌐 LANGUAGE SWITCH */}
        <select
          value={lang}
          onChange={(e) => setLang(e.target.value)}
          style={{
            background: "rgba(255,255,255,0.08)",
            border: "none",
            borderRadius: "8px",
            padding: "6px 10px",
            color: "#fff",
            cursor: "pointer",
            outline: "none"
          }}
        >
          <option value="en">EN</option>
          <option value="hi">हिन्दी</option>
          <option value="kn">ಕನ್ನಡ</option>
        </select>
      </div>
    </div>
  );
}

export default Navbar;