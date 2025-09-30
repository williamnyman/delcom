/* Main app component */
/*
import AddressBar from '../components/AddressBar'
import Subtitle from '../components/Subtitle'
import Title from '../components/Title'
import Textbar from '../components/TextBar'
import SubmitButton from '../components/SubmitButton'


function HomePage() {
    const [craving, setCraving] = React.useState('');

    const handleSubmit = async () => {
    const response = await fetch("http://localhost:8000/api/craving", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ address, craving }),
    });


    return(
      <div className='main-content'>
        <Title />
        <Subtitle />
        <AddressBar />
        <Textbar />
        <SubmitButton />
      </div>


    )
}

export default HomePage
*/

import React from "react";
import { useNavigate } from "react-router-dom";

import AddressBar from '../components/AddressBar'
import Subtitle from '../components/Subtitle'
import Title from '../components/Title'
import TextBar from '../components/TextBar'
import SubmitButton from '../components/SubmitButton'

function HomePage() {
  const [address, setAddress] = React.useState("");
  const [craving, setCraving] = React.useState("");
  const navigate = useNavigate();

const handleSubmit = async () => {
  try {
    await fetch("http://127.0.0.1:8000/api/craving", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ address, craving }),
    });

    navigate("/loading"); // go to loading page first
  } catch (error) {
    console.error("Error submitting craving:", error);
  }
};

  return (
    <div className="main-content">
      <Title />
      <Subtitle />
      <AddressBar value={address} onChange={setAddress} />
      <TextBar value={craving} onChange={setCraving} />
      <SubmitButton onClick={handleSubmit} />
    </div>
  );
}

export default HomePage;
