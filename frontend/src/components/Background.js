import React from "react";

function Background() {
  const text = "AI ASSISTED SKIN DISEASE DETECTION SYSTEM • ";

  return (
    <div className="bg-animated-text">
      {[...Array(8)].map((_, i) => (
        <div
          key={i}
          className="bg-line"
          style={{
            top: `${i * 12}%`,
            animationDuration: `${15 + i * 2}s`
          }}
        >
          {text.repeat(10)}
        </div>
      ))}
    </div>
  );
}

export default Background;