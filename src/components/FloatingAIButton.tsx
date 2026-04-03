import { MessageCircle } from "lucide-react";
import { Link, useLocation } from "react-router-dom";

const FloatingAIButton = () => {
  const location = useLocation();
  if (location.pathname === "/concierge") return null;

  return (
    <Link
      to="/concierge"
      className="fixed bottom-6 right-6 z-50 gradient-gold text-primary-foreground w-14 h-14 rounded-full flex items-center justify-center shadow-xl animate-pulse-gold hover:scale-110 transition-transform"
      aria-label="Talk to AI Concierge"
    >
      <MessageCircle className="w-6 h-6" />
    </Link>
  );
};

export default FloatingAIButton;
