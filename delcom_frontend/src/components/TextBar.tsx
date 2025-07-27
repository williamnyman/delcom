{
  /* Text for users to put their requests into */
}
import React, {useRef, useEffect} from 'react';
import burgerImg from '../assets/burger.png';

function TextBar() {
  const textareaRef = React.useRef<HTMLTextAreaElement>(null);
  const maxHeight = 200; // Maximum height in pixels

  const handleInput = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"; // Reset height
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`; // Set to scroll height
    

      if (textareaRef.current.scrollHeight > maxHeight) {
          textareaRef.current.style.overflowY = "auto";
          textareaRef.current.style.height = `${maxHeight}px`;
      } 
      else {
          textareaRef.current.style.overflowY = "hidden";
      }
    }
  }

  React.useEffect(() => {
    handleInput(); // Adjust height on mount
  }, []);

  return (
    <form style={{ marginTop: "20px" }}>
      <div className="form-group">
        <textarea
          ref ={textareaRef}
          placeholder='Enter your cravings here...'
          onInput={handleInput}
          rows={1}
          className="form-control"
          
          style={{  borderRadius: "10px",
                    backgroundImage: `url(${burgerImg})`,
                    backgroundPosition: "8px 5px",
                    backgroundRepeat: "no-repeat",
                    backgroundSize: "25px 25px",
                    paddingLeft: "40px",
                    backgroundColor: "#c6cfd8ff",
                    width: "60%",
                    margin: "0 auto",
                    overflow: "hidden",
                    border: "2px solid black",
                    resize: "none", // Prevent resizing
                    maxHeight: "200px", // Limit height
                  }}
        />
      </div>
    </form>
  );
}

export default TextBar;