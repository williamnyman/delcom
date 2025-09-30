import React from "react";
import { useLocation } from "react-router-dom";

interface LocationState {
  result: any; // can refine later
}

function ResultsPage() {
  const location = useLocation();
  const { result } = location.state || { result: null };


  return (
    <div style={{ padding: "40px", textAlign: "center", fontFamily: "Poppins" }}>
      <h1>Results</h1>
      {result ? (
        <pre
          style={{
            textAlign: "left",
            backgroundColor: "#f8f9fa",
            padding: "20px",
            borderRadius: "10px",
            overflowX: "auto",
          }}
        >
          {JSON.stringify(result, null, 2)}
        </pre>
      ) : (
        <p>No results found.</p>
      )}
    </div>
  );
}

export default ResultsPage;
