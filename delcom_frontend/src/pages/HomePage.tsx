import React from "react";
import { useNavigate } from "react-router-dom";
import AddressBar from "../components/AddressBar";
import Subtitle from "../components/Subtitle";
import Title from "../components/Title";
import TextBar from "../components/TextBar";
import SubmitButton from "../components/SubmitButton";
import HowToPop from "../components/HowToPop"; // import the popup component
import mail from "../assets/file.svg";
import linkedin2 from "../assets/linkedin2.png";
import mark from "../assets/question-sign.png";

function HomePage() {
  const [address, setAddress] = React.useState("");
  const [craving, setCraving] = React.useState("");
  const [showHowTo, setShowHowTo] = React.useState(true);
  const navigate = useNavigate();

  const handleSubmit = async () => {
    try {
      const res = await fetch("https://api.delcomapi.work/api/craving", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ address, craving }),
      });

      const data = await res.json();
      const sessionId = data.session_id;

      navigate("/loading", { state: { sessionId } }); // go to loading page first
    } catch (error) {
      console.error("Error submitting craving:", error);
    }
  };

  //import OfflinePopup from "../components/OfflinePopup";
  //return <OfflinePopup />;

  return (
    <div className="page-container">
      <div className="top-section">
        <HowToPop showHowTo={showHowTo} setShowHowTo={setShowHowTo} />{" "}
        {/* popup will show on page load */}
        <Title />
        <Subtitle />
        <AddressBar value={address} onChange={setAddress} />
        <TextBar value={craving} onChange={setCraving} />
        <SubmitButton onClick={handleSubmit} />
      </div>

      <div className="bottom-section">
        <p className="created-by">Created by William Nyman</p>
        <div className="divforthreebuttons">
          <button
            className="threebutton"
            onClick={() => window.open("mailto:williamhnyman@gmail.com")}
          >
            <img src={mail} alt="icon" className="button-icon" />
          </button>
          <button
            className="threebutton"
            onClick={() =>
              window.open("https://www.linkedin.com/in/william-nyman/")
            }
          >
            <img src={linkedin2} alt="icon" className="button-icon" />
          </button>
          <button className="threebutton" onClick={() => setShowHowTo(true)}>
            <img src={mark} alt="icon" className="button-icon" />
          </button>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
