import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";
import Footer from "./Footer";
import FloatingAIButton from "./FloatingAIButton";

const Layout = () => (
  <div className="min-h-screen flex flex-col">
    <Navbar />
    <main className="flex-1 pt-16">
      <Outlet />
    </main>
    <Footer />
    <FloatingAIButton />
  </div>
);

export default Layout;
