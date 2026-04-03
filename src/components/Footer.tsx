import { Link } from "react-router-dom";

const Footer = () => (
  <footer className="gradient-earth text-primary-foreground">
    <div className="container-resort section-padding">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        <div className="md:col-span-2">
          <h3 className="font-display text-2xl font-bold mb-3">
            <span className="text-gradient-gold">Kuriftu</span> Resort & Spa
          </h3>
          <p className="text-primary-foreground/70 font-body text-sm leading-relaxed max-w-md">
            Experience African luxury at Kuriftu African Village, Ethiopia. Built by Ethiopia. Shared with the world.
          </p>
        </div>
        <div>
          <h4 className="font-display font-semibold mb-3">Explore</h4>
          <div className="space-y-2 text-sm">
            {["/villas", "/experiences", "/events", "/about"].map((to) => (
              <Link key={to} to={to} className="block text-primary-foreground/70 hover:text-gold-light transition-colors">
                {to.slice(1).charAt(0).toUpperCase() + to.slice(2)}
              </Link>
            ))}
          </div>
        </div>
        <div>
          <h4 className="font-display font-semibold mb-3">AI Services</h4>
          <div className="space-y-2 text-sm">
            <Link to="/concierge" className="block text-primary-foreground/70 hover:text-gold-light transition-colors">AI Concierge</Link>
            <Link to="/smart-room" className="block text-primary-foreground/70 hover:text-gold-light transition-colors">Smart Room</Link>
            <Link to="/feedback" className="block text-primary-foreground/70 hover:text-gold-light transition-colors">Feedback</Link>
          </div>
        </div>
      </div>
      <div className="mt-12 pt-6 border-t border-primary-foreground/20 text-center text-xs text-primary-foreground/50">
        © {new Date().getFullYear()} Kuriftu Resort & Spa – African Village. All rights reserved.
      </div>
    </div>
  </footer>
);

export default Footer;
