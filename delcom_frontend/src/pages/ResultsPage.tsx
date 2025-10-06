import React from "react";
import { useLocation } from "react-router-dom";
import BasicCard from "../components/Card";
import beach from "../assets/beach.jpg";

interface LocationState {
  result: any; // can refine later
}

function ResultsPage() {
  const location = useLocation();
  const { result } = location.state || { result: null };
  console.log("ResultsPage received result:", result);
  let data = result.data;

  return (
    <div
      style={{ padding: "40px", textAlign: "center", fontFamily: "Poppins" }}
    >
      <h1>Results</h1>
      <BasicCard
        image={
          /* going to pull this from backend - this is just some random photo of some menu item*/
          data.image_url}
        food={data.item_name || "Food Name"}
        restaurant={data.restaurant_name || "Food Name"}
        meta_price={`Price: $${data.meta?.price || "Price"} `}
        meta_eta={`ETA: ${data.meta?.eta || "ETA"} mins.`}
        meta_rating={`Rating: ${data.meta?.rating || "Rating"}/5`}
        buttonText="Add to Cart"
        onButtonClick={() => alert("Button clicked!")}
      />

      {result ? (
        <pre
          style={{
            textAlign: "left",
            backgroundColor: "#f8f9fa",
            padding: "20px",
            borderRadius: "10px",
            overflowX: "auto",
          }}
        >
          {JSON.stringify(result, null, 2)}
        </pre>
      ) : (
        <p>No results found.</p>
      )}
    </div>
  );
}

export default ResultsPage;
