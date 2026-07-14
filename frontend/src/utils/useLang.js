import translations from "./translations";
import { useState, useEffect } from "react";

export function useLang() {
  const [lang, setLang] = useState(localStorage.getItem("lang") || "en");

  useEffect(() => {
    const interval = setInterval(() => {
      const current = localStorage.getItem("lang") || "en";
      if (current !== lang) {
        setLang(current);
      }
    }, 200); // small refresh loop

    return () => clearInterval(interval);
  }, [lang]);

  return translations[lang];
}