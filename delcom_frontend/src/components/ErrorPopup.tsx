import React from "react";
import { useNavigate } from "react-router-dom";

interface ErrorPopupProps {
  message: string;
  onClose?: () => void;
}

const ErrorPopup: React.FC<ErrorPopupProps> = ({ message, onClose }) => {
  const navigate = useNavigate();

  const handleGoHome = () => {
    if (onClose) onClose();
    navigate("/"); // go back to home page
  };

  if (!message) return null;

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
        <h2 style={{ color: "#E63946", marginBottom: "12px" }}>Error</h2>
        <p
          style={{
            color: "#1D3557",
            fontSize: "16px",
            marginBottom: "24px",
            lineHeight: "1.4",
          }}
        >
          {message}
        </p>
        <button
          onClick={handleGoHome}
          style={{
            backgroundColor: "#457B9D",
            color: "white",
            border: "none",
            borderRadius: "6px",
            padding: "10px 20px",
            cursor: "pointer",
            fontFamily: "Poppins, sans-serif",
            fontSize: "14px",
            transition: "background-color .2s ease",
          }}
          onMouseOver={(e) =>
            ((e.target as HTMLButtonElement).style.backgroundColor = "#F4A261")
          }
          onMouseOut={(e) =>
            ((e.target as HTMLButtonElement).style.backgroundColor = "#457B9D")
          }
        >
          Go Back Home
        </button>
      </div>
    </div>
  );
};

export default ErrorPopup;
