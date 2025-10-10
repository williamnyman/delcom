import React from "react";
import { Mail, Linkedin } from "lucide-react";

interface ContactButtonProps {
  type: "email" | "linkedin";
}

const ContactButton: React.FC<ContactButtonProps> = ({ type }) => {
  const handleClick = () => {
    if (type === "email") {
      window.location.href = "mailto:yourname@email.com";
    } else if (type === "linkedin") {
      window.open("https://www.linkedin.com/in/yourlinkedinusername", "_blank");
    }
  };

  const iconColor =
    type === "email" ? "text-red-500" : "text-blue-600"; // mail = red, linkedin = blue

  return (
    <button
      onClick={handleClick}
      className="p-2 rounded-full hover:bg-gray-200 transition-colors shadow-md"
      aria-label={type === "email" ? "Send me an email" : "Visit my LinkedIn"}
    >
      {type === "email" ? (
        <Mail className={`w-6 h-6 ${iconColor}`} />
      ) : (
        <Linkedin className={`w-6 h-6 ${iconColor}`} />
      )}
    </button>
  );
};

export default ContactButton;
