import React, { useState } from "react";
import axios from "axios";
import { useLang } from "../utils/useLang";

function Detect() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const t = useLang();

  const handleFile = (f) => {
    if (!f) return;
    setFile(f);
    setPreview(URL.createObjectURL(f));
    setResult(null);
  };

  const sendImage = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const lang = localStorage.getItem("lang") || "en";

    try {
      setLoading(true);

      const res = await axios.post(
        `http://localhost:8000/predict/image?language=${lang}`,
        formData
      );

      setResult(res.data);
    } catch {
      alert("Server error");
    } finally {
      setLoading(false);
    }
  };

  // 🔥 DOWNLOAD PDF
  const downloadReport = async () => {
    if (!result) return;

    const data = {
      disease: result.predictions?.[0]?.disease,
      confidence: result.predictions?.[0]?.confidence,
      risk: result.risk,
      treatment: result.treatment,
      advice: result.advice
    };

    const res = await axios.post(
      "http://localhost:8000/generate-report",
      data,
      { responseType: "blob" }
    );

    const url = window.URL.createObjectURL(new Blob([res.data]));
    const a = document.createElement("a");
    a.href = url;
    a.download = "skin-report.pdf";
    a.click();
  };

  return (
    <div className="container">
      <div className="card">

        <h2 className="title">📸 {t.detect}</h2>

        <div
          onClick={() => document.getElementById("fileInput").click()}
          style={{
            border: "2px dashed #3b82f6",
            padding: "20px",
            borderRadius: "12px",
            textAlign: "center",
            cursor: "pointer"
          }}
        >
          {preview ? "Change Image" : "Upload Image"}
        </div>

        <input
          id="fileInput"
          type="file"
          hidden
          onChange={(e) => handleFile(e.target.files[0])}
        />

        {preview && (
          <img src={preview} alt="" style={{ width: "100%", marginTop: 10 }} />
        )}

        <button className="btn" onClick={sendImage}>
          {loading ? "Analyzing..." : t.predict}
        </button>

        {result && (
          <div className="result">

            <h3>Top Predictions</h3>

            {result.predictions.map((p, i) => (
              <p key={i}>
                {p.disease} — {p.confidence}%
              </p>
            ))}

            <p><b>Risk:</b> {result.risk}</p>
            <p><b>Treatment:</b> {result.treatment}</p>
            <p><b>Advice:</b> {result.advice}</p>

            {/* 🔥 DOWNLOAD BUTTON */}
            <button className="btn" onClick={downloadReport}>
              Download Report
            </button>

          </div>
        )}

      </div>
    </div>
  );
}

export default Detect;