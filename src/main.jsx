// React
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

// Components
import App from "./App.jsx";

// ------------------------------------------------------------------------

const container = document.getElementById("root");
const root = createRoot(container);

root.render(
  <StrictMode>
    <App />
  </StrictMode>
);
