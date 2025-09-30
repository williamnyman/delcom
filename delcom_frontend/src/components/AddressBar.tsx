  /* Text for users to put their adress into */

/*
function AddressBar() {
  return (
        <input 
          className='bar address'
          type="text"
          placeholder='Enter your address here...'
          maxLength={80}
          spellCheck={false}


    />
  );
}

export default AddressBar;
*/


import React from "react";

interface AddressBarProps {
  value: string; // parent state
  onChange: (val: string) => void; // updates parent state
  maxChars?: number; // optional, default 80
}

function AddressBar({ value, onChange, maxChars = 80 }: AddressBarProps) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value);
  };

  return (
    <input
      className="bar address"
      type="text"
      placeholder="Enter your address here..."
      value={value}
      onChange={handleChange}
      maxLength={maxChars}
      spellCheck={false}
      style={{ width: "60%" }}
    />
  );
}

export default AddressBar;
