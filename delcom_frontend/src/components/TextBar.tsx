import React, { useState, useRef, useEffect } from "react";

function TextBar() {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const maxChars = 400; // maximum characters
  const [text, setText] = useState(""); // track textarea content

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    setText(value);

    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"; // reset height
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;

      if (textareaRef.current.scrollHeight > 200) {
        textareaRef.current.style.overflowY = "auto";
        textareaRef.current.style.height = `200px`;
      } else {
        textareaRef.current.style.overflowY = "hidden";
      }
    }
  };

  // adjust height on mount
  useEffect(() => {
    if (textareaRef.current) {
      handleInput({ target: textareaRef.current } as React.ChangeEvent<HTMLTextAreaElement>);
    }
  }, []);

  return (
    <div style={{ width: "60%", display: "flex", flexDirection: "column", alignItems: "center" }}>
      <textarea
        className="bar text"
        ref={textareaRef}
        placeholder="Enter your cravings..."
        value={text}
        onChange={handleInput}
        maxLength={maxChars}
        rows={1}
        style={{ maxHeight: 200, width: "100%" }}
        spellCheck={false}
      />

      <div style={{ fontSize: "12px", color: "#457B9D", marginTop: "4px", alignSelf: "flex-end", fontFamily: 'Poppins' }}>
        {text.length} / {maxChars}
      </div>
    </div>
  );
}

export default TextBar;
