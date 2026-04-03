import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";

import Layout from "./components/Layout";
import Index from "./pages/Index";
import About from "./pages/About";
import Villas from "./pages/Villas";
import Experiences from "./pages/Experiences";
import Events from "./pages/Events";
import SmartRoom from "./pages/SmartRoom";
import Feedback from "./pages/Feedback";
import NotFound from "./pages/NotFound";

// ✅ USE THIS ONE (AI CHAT PAGE)
import ConciergePage from "./pages/ConciergePage";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />

      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>

            {/* MAIN PAGES */}
            <Route path="/" element={<Index />} />
            <Route path="/about" element={<About />} />
            <Route path="/villas" element={<Villas />} />
            <Route path="/experiences" element={<Experiences />} />
            <Route path="/events" element={<Events />} />
            <Route path="/smart-room" element={<SmartRoom />} />
            <Route path="/feedback" element={<Feedback />} />

            {/* ✅ AI CONCIERGE PAGE */}
            <Route path="/concierge" element={<ConciergePage />} />

          </Route>

          {/* 404 PAGE */}
          <Route path="*" element={<NotFound />} />

        </Routes>
      </BrowserRouter>

    </TooltipProvider>
  </QueryClientProvider>
);

export default App;