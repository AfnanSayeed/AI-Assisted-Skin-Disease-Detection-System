import React, { useState } from "react";
import axios from "axios";
import { useLang } from "../utils/useLang";

function Symptoms() {
  const [symptom1, setSymptom1] = useState("");
  const [symptom2, setSymptom2] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const t = useLang();

  const detectSymptoms = async () => {
    if (!symptom1.trim() && !symptom2.trim()) return;

    const lang = localStorage.getItem("lang") || "en";

    try {
      setLoading(true);

      const res = await axios.post(
        "http://localhost:8000/predict/symptoms",
        {
          symptom1,
          symptom2,
          language: lang
        }
      );

      setResult(res.data);
    } catch {
      alert("Server error");
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setSymptom1("");
    setSymptom2("");
    setResult(null);
  };

  // 🔥 DOWNLOAD PDF
  const downloadReport = async () => {
    if (!result) return;

    try {
      const res = await axios.post(
        "http://localhost:8000/generate-report",
        result,
        { responseType: "blob" }
      );

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = "symptoms-report.pdf";
      a.click();
    } catch {
      alert("Download failed");
    }
  };

  const suggestions = ["itching", "rash", "pimple", "red patches", "dry skin"];

  return (
    <div className="container">
      <div className="card">

        <h2 className="title">🩺 {t.symptoms}</h2>
        <p className="subtitle">{t.symptomsDesc}</p>

        <input
          className="input"
          placeholder={t.enterSymptom}
          value={symptom1}
          onChange={(e) => setSymptom1(e.target.value)}
        />

        <input
          className="input"
          placeholder="Additional symptom (optional)"
          value={symptom2}
          onChange={(e) => setSymptom2(e.target.value)}
          style={{ marginTop: "10px" }}
        />

        {/* Suggestions */}
        <div style={{
          marginTop: "10px",
          display: "flex",
          flexWrap: "wrap",
          gap: "6px"
        }}>
          {suggestions.map((s, i) => (
            <span
              key={i}
              onClick={() => setSymptom1(s)}
              style={{
                padding: "6px 10px",
                borderRadius: "15px",
                background: "rgba(59,130,246,0.15)",
                cursor: "pointer",
                fontSize: "12px"
              }}
            >
              {s}
            </span>
          ))}
        </div>

        <div style={{ display: "flex", gap: "10px", marginTop: "15px" }}>
          <button className="btn" onClick={detectSymptoms}>
            {loading ? "🔍 Analyzing..." : t.analyze}
          </button>

          {(symptom1 || symptom2) && (
            <button
              className="btn"
              onClick={reset}
              style={{ background: "#ef4444" }}
            >
              Reset
            </button>
          )}
        </div>

        {result && (
          <div className="result" style={{ marginTop: "20px" }}>

            <h3>🧠 Analysis</h3>

            <p><b>{t.disease}:</b> {result.disease}</p>

            {/* Confidence */}
            {result.confidence && (
              <>
                <div style={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginTop: "10px"
                }}>
                  <span><b>{t.confidence}</b></span>
                  <span>{result.confidence}%</span>
                </div>

                <div style={{
                  height: "8px",
                  background: "#1e293b",
                  borderRadius: "6px",
                  overflow: "hidden",
                  marginTop: "4px"
                }}>
                  <div style={{
                    width: `${result.confidence}%`,
                    height: "100%",
                    background: "linear-gradient(90deg, #3b82f6, #60a5fa)"
                  }} />
                </div>
              </>
            )}

            <div style={{ marginTop: "15px", lineHeight: "1.6" }}>
              <p><b>{t.risk}:</b> {result.risk}</p>
              <p><b>{t.treatment}:</b> {result.treatment}</p>
              <p><b>{t.advice}:</b> {result.advice}</p>
            </div>

            {/* 🔥 DOWNLOAD */}
            <button className="btn" onClick={downloadReport}>
              Download Report
            </button>

            <p style={{
              marginTop: "15px",
              color: "#f87171",
              fontSize: "13px"
            }}>
              ⚠ AI suggestion only. Not a medical diagnosis.
            </p>

          </div>
        )}

      </div>
    </div>
  );
}

export default Symptoms;