import { useState } from "react";
import { useLocation } from "react-router-dom";
import BasicCard from "../components/Card";
import beach from "../assets/food.jpg";
import ErrorPopup from "../components/ErrorPopup";
import { useNavigate } from "react-router-dom";
import home from "../assets/home.png";

interface LocationState {
  //the questions marks here are for things that are optional
  // e.g. every item will have a name and a restaurant but desc, customizations, could be empty
  // not sure why meta has a ? because those will always exist too
  result: {
    data: Array<{
      item_name: string;
      restaurant_name: string;
      item_desc?: string;
      customizations?: string;
      restaurant_tags?: string[];
      image_url?: string;
      meta?: {
        rating?: number;
        eta?: number;
        price?: number;
      };
      url_info: {
        image_url: string;
        action_url: string;
        store_uuid: string;
        section_uuid: string;
        subsection_uuid: string;
        item_uuid: string;
      };
    }>;
  };
}

function ResultsPage() {
  const location = useLocation();
  const { result } = (location.state as LocationState) || { result: null };
  const [selectedItem, setSelectedItem] = useState<null | any>(null);
  const navigate = useNavigate();

  // thhe closePopup sets the selceted item to null which then makes the
  // popup de-render (or more so render as nothing)
  const closePopup = () => setSelectedItem(null);

  // inline styles eventually going to want to move this to App.css using
  // class names but not going to do so quite yet
  const styles = {
    popup: {
      position: "fixed" as "fixed",
      top: 0,
      left: 0,
      width: "100%",
      height: "100%",
      backgroundColor: "rgba(29,53,87,0.85)",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      zIndex: 1000,
      fontFamily: "'Poppins', sans-serif",
    },
    popupContent: {
      backgroundColor: "white",
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
    heading: { color: "#1D3557", margin: "10px 0" },
    subHeading: { color: "#457B9D", margin: "10px 0 5px" },
    paragraph: { color: "#1D3557", margin: "10px 0" },
    instructionImg: {
      maxWidth: "100%",
      borderRadius: "6px",
      margin: "10px 0",
      border: "2px solid #457B9D",
    },
    uberButton: {
      backgroundColor: "#457B9D",
      color: "white",
      border: "none",
      borderRadius: "6px",
      padding: "12px 24px",
      fontFamily: "'Poppins', sans-serif",
      fontSize: "16px",
      cursor: "pointer",
      marginTop: "15px",
    },
  };

  console.log(result);

  if (
    result &&
    (result as any).data.error ===
      "please enter a valid address and a sensible craving"
  ) {
    console.log("error!");
    // bring up pop up with button that says go to home page
    return <ErrorPopup message={(result as any).data.error} />;
  }

  return (
    <div
      style={{
        padding: "40px",
        textAlign: "center",
        fontFamily: "Poppins",
        alignItems: "center",
      }}
    >
      <h1 style={{ color: "white" }}>Results</h1>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
          gap: "20px",
          marginTop: "20px",
          marginLeft: "auto",
          marginRight: "auto",
          justifyContent: "center", // center the whole grid inside its container
          justifyItems: "center", // center items inside their grid cells
          maxWidth: "1400px", // optional: constrain grid width so auto margins work
        }}
      >
        {/*within result is an array of 4 top results so this is a loop that is puts 
            each result on a different card by looping through result.
            also, the onInfoClick at the bottom sets the selcted item to whatever item we are looking at
            this then lets the popup render becuase it makes the selectedItem not None or Null*/}
        {result?.data?.slice(0, 6).map((item, index) => (
          <BasicCard
            key={index}
            image={item.url_info.image_url || beach}
            food={item.item_name || "Food Name"}
            restaurant={item.restaurant_name || "Restaurant"}
            meta_price={`Price: $${item.meta?.price ?? "N/A"}`}
            meta_eta={`ETA: ${item.meta?.eta ?? "N/A"} mins`}
            meta_rating={`Rating: \n ${item.meta?.rating ?? "N/A"}/5`}
            buttonText="View on UberEats"
            onButtonClick={() =>
              window.open(
                `https://www.ubereats.com${item.url_info.action_url}?diningMode=DELIVERY&mod=quickView&modctx=%257B%2522storeUuid%2522%253A%2522${item.url_info.store_uuid}%2522%252C%2522sectionUuid%2522%253A%2522${item.url_info.section_uuid}%2522%252C%2522subsectionUuid%2522%253A%2522${item.url_info.subsection_uuid}%2522%252C%2522itemUuid%2522%253A%2522${item.url_info.item_uuid}%2522%252C%2522showSeeDetailsCTA%2522%253Atrue%257D&ps=1&surfaceName=`,
                "_blank"
              )
            }
            onInfoClick={() => setSelectedItem(item)} // open popup
          />
        ))}
      </div>

      <div className="divforonebutton">
        <button className="threebutton" onClick={() => navigate("/")}>
          <img src={home} alt="icon" className="button-icon" />
        </button>
      </div>

      {/*------------*/}
      {selectedItem && (
        <div style={styles.popup}>
          <div
            style={{
              ...styles.popupContent,
              display: "flex",
              gap: "20px",
              alignItems: "flex-start",
            }}
          >
            <span
              style={styles.close}
              onClick={closePopup}
              onMouseOver={(e: any) =>
                (e.currentTarget.style.color = "#F4A261")
              }
              onMouseOut={(e: any) => (e.currentTarget.style.color = "#E63946")}
            >
              &times;
            </span>
            {/* Left side: Image */}
            {selectedItem.url_info.image_url && (
              <img
                src={selectedItem.url_info.image_url}
                alt={selectedItem.item_name}
                style={{
                  width: "200px",
                  height: "200px",
                  objectFit: "cover",
                  borderRadius: "8px",
                }}
              />
            )}

            {/* Right side: Details */}
            <div
              style={{
                flex: 1,
                display: "flex",
                flexDirection: "column",
                gap: "8px",
              }}
            >
              <h2 style={styles.heading}>{selectedItem.item_name}</h2>
              <h3 style={styles.subHeading}>{selectedItem.restaurant_name}</h3>
              {selectedItem.item_desc && (
                <p style={styles.paragraph}>{selectedItem.item_desc}</p>
              )}
              {selectedItem.customizations && (
                <p style={styles.paragraph}>
                  <strong>Customizations:</strong>
                  <br />
                  {selectedItem.customizations
                    .split(";")
                    .map((group: string, index: number) => {
                      const [title, options] = group
                        .split(":")
                        .map((s: string) => s.trim());
                      return (
                        <span key={index}>
                          <strong>{title}:</strong> {options}
                          {index <
                            selectedItem.customizations.split(";").length -
                              1 && <br />}
                        </span>
                      );
                    })}
                </p>
              )}

              {selectedItem.meta && (
                <p style={styles.paragraph}>
                  Price: ${selectedItem.meta.price ?? "N/A"} | ETA:{" "}
                  {selectedItem.meta.eta ?? "N/A"} mins | Rating:{" "}
                  {selectedItem.meta.rating ?? "N/A"}/5
                </p>
              )}
              <button
                style={styles.uberButton}
                onClick={() => {
                  if (selectedItem.url_info) {
                    let url = `https://www.ubereats.com${selectedItem.url_info.action_url}?diningMode=DELIVERY&mod=quickView&modctx=%257B%2522storeUuid%2522%253A%2522${selectedItem.url_info.store_uuid}%2522%252C%2522sectionUuid%2522%253A%2522${selectedItem.url_info.section_uuid}%2522%252C%2522subsectionUuid%2522%253A%2522${selectedItem.url_info.subsection_uuid}%2522%252C%2522itemUuid%2522%253A%2522${selectedItem.url_info.item_uuid}%2522%252C%2522showSeeDetailsCTA%2522%253Atrue%257D&ps=1&surfaceName=`;
                    window.open(url, "_blank");
                  } else {
                    alert("No Uber Eats link available.");
                  }
                }}
              >
                View in Uber Eats
              </button>
            </div>
          </div>
        </div>
      )}
      {/*------------*/}
    </div>
  );
}

export default ResultsPage;
