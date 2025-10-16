//import React from "react";

type BasicCardProps = {
  image: string;
  food: string;
  restaurant: string;
  meta_price: string;
  meta_eta: string;
  meta_rating: string;
  buttonText: string;
  onButtonClick?: () => void;
  onInfoClick?: () => void; // new
};

export default function BasicCard({
  image,
  food,
  restaurant,
  meta_price,
  meta_eta,
  meta_rating,
  buttonText,
  onButtonClick,
  onInfoClick,
}: BasicCardProps) {
  return (
    <div className="card">
      <div className="image-wrapper">
        <img src={image} alt={food} className="card-image" />
        <button className="info-button" onClick={onInfoClick} title="More info">
          i
        </button>
      </div>

      <div className="card-content">
        <h3 className="card-title">{food}</h3>
        <h4 className="card-restaurant">{restaurant}</h4>
        <div className="meta-wrapper">
          <p className="card-meta">{meta_price}</p>
          <p className="card-meta">{meta_eta}</p>
          <p className="card-meta">{meta_rating}</p>
        </div>
      </div>

      <div className="card-footer">
        <button className="card-button" onClick={onButtonClick}>
          {buttonText}
        </button>
      </div>

      <style>{`
        .card {
          width: 240px;
          display: flex;
          flex-direction: column;
          background: #fff;
          border: 2px solid #457B9D;
          border-radius: 10px;
          overflow: hidden;
          font-family: sans-serif;
          transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .card:hover {
          transform: scale(1.03);
          box-shadow: 0 4px 20px rgba(244,162,97,0.7);
        }

        .image-wrapper {
          position: relative;
        }

        .card-image {
          width: 100%;
          height: 160px;
          object-fit: cover;
          display: block;
        }

        .info-button {
          position: absolute;
          top: 8px;
          right: 8px;
          background-color: #fff;
          color: #457B9D;
          border: 2px solid #457B9D;
          border-radius: 50%;
          width: 28px;
          height: 28px;
          font-size: 14px;
          font-weight: bold;
          font-family: 'Poppins', sans-serif;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: color 0.3s ease, border-color 0.3s ease, background-color 0.3s ease;
        }

        .info-button:hover {
          color: #F4A261;
          border-color: #F4A261;
        }

        .card-content {
          padding: 8px 10px;
          flex: 1;
        }

        .card-title {
          font-size: 18px;
          font-weight: 600;
          font-family: 'Poppins', sans-serif;
          margin: 0 0 8px;
          color: #1D3557;
        }

        .card-restaurant {
          font-size: 14px;
          color: #1D3557;
          margin: 2px 0;
        }
        
        .meta-wrapper {
          display: flex;
          justify-content: space-between;
          margin-top: 8px;
        }

        .card-meta {
          font-size: 12px;
          color: #457B9D;
          margin: 2px 0;
          font-family: 'Poppins', sans-serif;
        }

        .card-footer {
          padding: 8px 10px;
          border-top: 1px solid #eee;
          text-align: center;
        }

        .card-button {
          background-color: #457B9D;
          font-family: 'Poppins', sans-serif;
          color: white;
          border: none;
          padding: 8px 16px;
          border-radius: 6px;
          font-size: 14px;
          cursor: pointer;
          transition: background 0.3s ease;
        }

        .card-button:hover {
          background-color: #F4A261;
        }
      `}</style>
    </div>
  );
}
