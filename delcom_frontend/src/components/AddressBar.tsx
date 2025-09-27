  /* Text for users to put their adress into */


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
