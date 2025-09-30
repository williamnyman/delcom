import React from "react";

interface SubmitButtonProps {
  onClick: () => void; // function passed from parent
}

function SubmitButton({ onClick }: SubmitButtonProps) {
  return (
    <button className="submit-button" onClick={onClick}>
      Submit
    </button>
  );
}

export default SubmitButton;
