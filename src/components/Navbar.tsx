import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Menu, X, MessageCircle } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const navLinks = [
  { to: "/", label: "Home" },
  { to: "/about", label: "About" },
  { to: "/villas", label: "Villas" },
  { to: "/experiences", label: "Experiences" },
  { to: "/events", label: "Events" },
  { to: "/concierge", label: "AI Concierge" },
  { to: "/smart-room", label: "Smart Room" },
  { to: "/feedback", label: "Feedback" },
];

const Navbar = () => {
  const [open, setOpen] = useState(false);
  const location = useLocation();

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-xl border-b border-border/50">
      <div className="container-resort flex items-center justify-between h-16 px-4 sm:px-6 lg:px-8">
        <Link to="/" className="font-display text-xl font-bold text-foreground tracking-wide">
          <span className="text-gradient-gold">Kuriftu</span>
        </Link>

        {/* Desktop */}
        <div className="hidden lg:flex items-center gap-1">
          {navLinks.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              className={`px-3 py-2 text-sm font-body rounded-lg transition-colors ${
                location.pathname === link.to
                  ? "text-accent font-bold bg-accent/10"
                  : "text-muted-foreground hover:text-foreground hover:bg-muted"
              }`}
            >
              {link.label}
            </Link>
          ))}
        </div>

        <Link
          to="/concierge"
          className="hidden lg:flex items-center gap-2 gradient-gold text-primary-foreground px-4 py-2 rounded-full text-sm font-semibold shadow-md hover:shadow-lg transition-shadow"
        >
          <MessageCircle className="w-4 h-4" />
          Talk to AI
        </Link>

        {/* Mobile toggle */}
        <button onClick={() => setOpen(!open)} className="lg:hidden text-foreground p-2">
          {open ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile menu */}
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="lg:hidden bg-background/95 backdrop-blur-xl border-b border-border overflow-hidden"
          >
            <div className="px-4 py-4 space-y-1">
              {navLinks.map((link) => (
                <Link
                  key={link.to}
                  to={link.to}
                  onClick={() => setOpen(false)}
                  className={`block px-4 py-3 rounded-lg text-sm font-body transition-colors ${
                    location.pathname === link.to
                      ? "text-accent font-bold bg-accent/10"
                      : "text-muted-foreground hover:text-foreground hover:bg-muted"
                  }`}
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};

export default Navbar;
