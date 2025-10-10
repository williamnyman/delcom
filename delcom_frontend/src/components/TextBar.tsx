import React, { useRef, useEffect } from "react";

interface TextBarProps {
  value: string; // value from parent state
  onChange: (val: string) => void; // updates parent state
  maxChars?: number; // optional max length, default 400
}

function TextBar({ value, onChange, maxChars = 400 }: TextBarProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const maxHeight = 200; // maximum height in px

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const val = e.target.value;
    onChange(val); // update parent state

    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"; // reset height
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;

      if (textareaRef.current.scrollHeight > maxHeight) {
        textareaRef.current.style.overflowY = "auto";
        textareaRef.current.style.height = `${maxHeight}px`;
      } else {
        textareaRef.current.style.overflowY = "hidden";
      }
    }
  };

  // adjust height on mount and when value changes
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [value]);

  return (
    <div style={{ width: "60%", display: "flex", flexDirection: "column", alignItems: "center" }}>
      <textarea
        className="bar text"
        ref={textareaRef}
        placeholder="Enter your cravings..."
        value={value}
        onChange={handleInput}
        maxLength={maxChars}
        rows={1}
        style={{ maxHeight, width: "100%" }}
        spellCheck={false}
      />

      <div
        style={{
          fontSize: "12px",
          color: "#457B9D",
          marginTop: "4px",
          alignSelf: "flex-end",
          fontFamily: "Poppins",
        }}
      >
        {value.length} / {maxChars}
      </div>
    </div>
  );
}

export default TextBar;

