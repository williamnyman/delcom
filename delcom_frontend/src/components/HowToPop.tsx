import React, { useState } from "react";
import fakeAddressImg from "../assets/fakeAddress.png"; // your fake address image
import vagueCravingImg from "../assets/vagueCraving.png";
import somewhatSpecificImg from "../assets/somewhatSpecific.png";
import specificImg from "../assets/specific.png";
import verySpecificImg from "../assets/verySpecific.png";
import submit from "../assets/submit.png";

interface HowToPopProps {
    showHowTo: boolean;
    setShowHowTo: React.Dispatch<React.SetStateAction<boolean>>;
  }

function HowToPop({ showHowTo, setShowHowTo }: HowToPopProps) {
  const closeHowTo = () => setShowHowTo(false);

  // Styling to match your app's vibe
  const styles = {
    popup: {
      position: "fixed" as "fixed",
      top: 0,
      left: 0,
      width: "100%",
      height: "100%",
      backgroundColor: "rgba(29, 53, 87, 0.85)", // semi-transparent dark blue
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      zIndex: 1000,
      fontFamily: "'Poppins', sans-serif",
    },
    popupContent: {
      backgroundColor: "#1D3557", // light background for contrast
      padding: "30px",
      borderRadius: "12px",
      maxWidth: "600px",
      width: "90%",
      textAlign: "center" as "center",
      position: "relative" as "relative",
      overflowY: "auto" as "auto",
      maxHeight: "80%",
      boxShadow: "0 0 20px rgba(0,0,0,0.3)",
    },
    close: {
      position: "absolute" as "absolute",
      top: "10px",
      right: "15px",
      fontSize: "28px",
      fontWeight: "600" as "600",
      cursor: "pointer",
      color: "#E63946",
      transition: "color 0.2s ease",
    },
    closeHover: {
      color: "#F4A261",
    },
    heading: {
      color: "#ffffffff",
      margin: "10px 0",
    },
    subHeading: {
      color: "#ffffffff",
      margin: "10px 0 5px",
    },
    paragraph: {
      color: "#457B9D",
      margin: "10px 0",
    },
    instructionImg: {
      maxWidth: "100%",
      margin: "10px 0",
      borderRadius: "6px",
      border: "2px solid #457B9D",
    },
    cravingImages: {
      display: "flex",
      flexWrap: "wrap" as "wrap",
      gap: "10px",
      justifyContent: "center" as "center",
    },
  };

  return (
    <>
      {showHowTo && (
        <div style={styles.popup}>
          <div style={styles.popupContent}>
            <span
              style={styles.close}
              onClick={closeHowTo}
              onMouseOver={(e: any) => (e.currentTarget.style.color = "#F4A261")}
              onMouseOut={(e: any) => (e.currentTarget.style.color = "#E63946")}
            >
              &times;
            </span>
            <h2 style={styles.heading}>How to Use Delcom</h2>

            <section>
              <h3 style={styles.subHeading}>Step 1: Enter Your Address</h3>
              <p style={styles.paragraph}>Type your address in the search bar like this:</p>
              <img
                src={fakeAddressImg}
                alt="Example address input"
                style={styles.instructionImg}
              />
            </section>

            <section>
              <h3 style={styles.subHeading}>Step 2: Enter Your Craving</h3>
              <p style={styles.paragraph}>
                Your craving can be as vague or specific as you'd like. Here are some examples:
              </p>
              <div style={styles.cravingImages}>
                <img src={vagueCravingImg} alt="Vague craving" style={styles.instructionImg} />
                <img src={somewhatSpecificImg} alt="Somewhat specific craving" style={styles.instructionImg} />
                <img src={specificImg} alt="Specific craving" style={styles.instructionImg} />
                <img src={verySpecificImg} alt="Very specific craving" style={styles.instructionImg} />
              </div>
            
            </section>

            <section>
              <h3 style={styles.subHeading}>Step 3: Hit submit!</h3>
              <p style={styles.paragraph}>
                Hang tight for ~90 seconds while we find the best matches for you!
              </p>
              <div style={styles.cravingImages}>
            <img
                src={submit}
                alt="Vague craving"
                
            />
            </div>

            
            </section>
          </div>
        </div>
      )}
    </>
  );
}

export default HowToPop;