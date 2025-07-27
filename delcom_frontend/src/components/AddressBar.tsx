{
  /* Text for users to put their adress into */
}

import pinImg from '../assets/pin.png';

function AddressBar() {
  return (
    <form style={{ marginTop: "20px" }}>
      <div className="form-group">
        <div contentEditable
          
          className="form-control"
          
          style={{  borderRadius: "20px",
                    backgroundImage: `url(${pinImg})`,
                    backgroundPosition: "8px 5px",
                    backgroundRepeat: "no-repeat",
                    backgroundSize: "25px 25px",
                    paddingLeft: "40px",
                    backgroundColor: "#c6cfd8ff",
                    width: "60%",
                    margin: "0 auto",
                    maxHeight: "200px",
                    overflow: "auto",
                    border: "2px solid black",
        
                  }}
        />
      </div>
    </form>
  );
}

export default AddressBar;
