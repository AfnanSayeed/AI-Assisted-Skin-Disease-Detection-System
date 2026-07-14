import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { useLang } from "../utils/useLang";

function Chatbot() {
  const [msg, setMsg] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);

  const t = useLang();
  const chatRef = useRef(null);

  useEffect(() => {
    chatRef.current?.scrollTo(0, chatRef.current.scrollHeight);
  }, [chat]);

  const sendMessage = async () => {
    if (!msg.trim()) return;

    const lang = localStorage.getItem("lang") || "en";
    const userMsg = msg;

    setMsg("");

    setChat(prev => [
      ...prev,
      { user: userMsg, bot: "Thinking..." }
    ]);

    try {
      setLoading(true);

      const res = await axios.post("http://localhost:8000/chat", {
        msg: userMsg,
        language: lang
      });

      setChat(prev => {
        const updated = [...prev];
        updated[updated.length - 1].bot = res.data.response;
        return updated;
      });

    } catch {
      setChat(prev => {
        const updated = [...prev];
        updated[updated.length - 1].bot = "⚠ Error generating response";
        return updated;
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="card">

        <h2 className="title">🤖 {t.chatbot}</h2>
        <p className="subtitle">
          Ask about skin problems, symptoms, or treatments.
        </p>

        {/* CHAT */}
        <div
          ref={chatRef}
          style={{
            maxHeight: "350px",
            overflowY: "auto",
            padding: "10px",
            borderRadius: "10px",
            background: "rgba(255,255,255,0.05)",
            marginTop: "10px"
          }}
        >
          {chat.map((c, i) => (
            <div key={i} style={{ marginBottom: "12px" }}>

              {/* USER */}
              <div style={{
                background: "#3b82f6",
                padding: "10px",
                borderRadius: "10px",
                color: "#fff",
                marginBottom: "5px"
              }}>
                {c.user}
              </div>

              {/* BOT */}
              <div style={{
                background: "#1e293b",
                padding: "10px",
                borderRadius: "10px",
                whiteSpace: "pre-line",
                lineHeight: "1.6"
              }}>
                {c.bot}
              </div>

            </div>
          ))}
        </div>

        {/* INPUT */}
        <textarea
          className="input"
          value={msg}
          onChange={(e) => setMsg(e.target.value)}
          rows={3}
          placeholder={t.placeholderChat}
          style={{ marginTop: "10px", resize: "none" }}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              sendMessage();
            }
          }}
        />

        {/* BUTTON */}
        <button className="btn" onClick={sendMessage}>
          {loading ? "Thinking..." : t.send}
        </button>

        <p style={{
          marginTop: "15px",
          color: "#ff4d4d",
          fontSize: "13px"
        }}>
          ⚠ Informational only. Consult a doctor for real diagnosis.
        </p>

      </div>
    </div>
  );
}

export default Chatbot;