// src/components/OfflinePopup.tsx
import React from "react";

const OfflinePopup: React.FC = () => {
  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: "rgba(0,0,0,0.5)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 1000,
      }}
    >
      <div
        style={{
          background: "white",
          padding: "24px",
          borderRadius: "12px",
          textAlign: "center",
          maxWidth: "320px",
          fontFamily: "Poppins, sans-serif",
          boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
        }}
      >
        <h2
          style={{ color: "#1D3557", marginBottom: "12px", fontSize: "22px" }}
        >
          Delcom is currently offline
        </h2>
        <p
          style={{
            color: "#457B9D",
            fontSize: "16px",
            marginBottom: "0",
            lineHeight: "1.4",
          }}
        >
          It will be live again by{" "}
          <span style={{ fontWeight: "bold" }}>12pm PST Nov. 22</span>.
        </p>
      </div>
    </div>
  );
};

export default OfflinePopup;
