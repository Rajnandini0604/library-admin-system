import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";

import Dashboard from "./pages/Dashboard";
import Books from "./pages/Books";
import Authors from "./pages/Authors";
import AuthorDetails from "./pages/AuthorDetails";
import Stats from "./pages/Stats";

function App() {

  return (

    <BrowserRouter>

      <Navbar />

      <Routes>

        <Route path="/" element={<Dashboard />} />

        <Route path="/books" element={<Books />} />

        <Route path="/authors" element={<Authors />} />

        <Route path="/authors/:id" element={<AuthorDetails />} />

        <Route path="/stats" element={<Stats />} />

      </Routes>

    </BrowserRouter>

  );

}

export default App;