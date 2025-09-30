import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function LoadingPage() {
  const [progress, setProgress] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/progress");
        const data = await res.json();
        setProgress(data.value);

        if (data.done) {
          clearInterval(interval);

          // fetch final result
          const resultRes = await fetch("http://127.0.0.1:8000/result");
          const resultData = await resultRes.json();

          // navigate to results page with data
          navigate("/results", { state: { result: resultData } });
        }
      } catch (err) {
        console.error("Error polling progress:", err);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [navigate]);

  return (
    <div className="main-content">
      <h2>Loading your cravings... 🍔🍕🥡</h2>

      <div style={{ width: "100%", background: "#eee", borderRadius: "8px", marginTop: "1rem" }}>
        <div
          style={{
            width: `${progress}%`,
            background: "green",
            height: "20px",
            borderRadius: "8px",
            transition: "width 0.5s ease",
          }}
        />
      </div>

      <p>{progress}%</p>
    </div>
  );
}

export default LoadingPage;
