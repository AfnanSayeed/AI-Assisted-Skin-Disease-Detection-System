import React from "react";
import { useNavigate } from "react-router-dom";
import { useLang } from "../utils/useLang";

function Home() {
  const navigate = useNavigate();
  const t = useLang(); // ✅ language hook

  return (
    <div>

      <h1 className="title">
        {t.homeTitle}
      </h1>

      <p className="subtitle">
        {t.homeSubtitle}
      </p>

      <div className="grid">

        <div className="card">
          <h3>{t.detect}</h3>
          <p>{t.detectDesc}</p>
          <button className="btn" onClick={()=>navigate("/detect")}>
            {t.start}
          </button>
        </div>

        <div className="card">
          <h3>{t.symptoms}</h3>
          <p>{t.symptomsDesc}</p>
          <button className="btn" onClick={()=>navigate("/symptoms")}>
            {t.start}
          </button>
        </div>

        <div className="card">
          <h3>{t.chatbot}</h3>
          <p>{t.chatbotDesc}</p>
          <button className="btn" onClick={()=>navigate("/chatbot")}>
            {t.start}
          </button>
        </div>

      </div>

    </div>
  );
}

export default Home;