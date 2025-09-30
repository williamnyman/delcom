import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LoadingPage from "./pages/LoadingPage";
import ResultsPage from "./pages/ResultsPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/loading" element={<LoadingPage />} />
      <Route path="/results" element={<ResultsPage />} />
    </Routes>
  );
}

export default App;
