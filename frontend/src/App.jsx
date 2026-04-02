import { Routes, Route } from "react-router-dom";
import { Login } from "./pages/Login/login";
import { Home } from "./pages/Home/index";
import { MainLayout } from "./layouts/MainLayout";
import { Account } from "./pages/Account";

function App() {
  return (
    <Routes>
      <Route path="/" element={<MainLayout />}>
        {/* Các page con */}
        <Route index element={<Home />} />
        <Route path="/accounts" element={<Account />} />
      </Route>
      <Route path="/login" element={<Login />} />
    </Routes>
  );
}

export default App;
