import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { MessageCircle, Sparkles, Building, Star } from "lucide-react";
import heroImg from "@/assets/hero-resort.jpg";
import villaImg from "@/assets/villa-romantic.jpg";
import wellnessImg from "@/assets/wellness.jpg";
import diningImg from "@/assets/dining.jpg";

const features = [
  { icon: MessageCircle, title: "AI Concierge", desc: "24/7 personalized assistance powered by AI", link: "/concierge" },
  { icon: Sparkles, title: "Smart Room", desc: "Control your room with intelligent automation", link: "/smart-room" },
  { icon: Building, title: "54 Luxury Villas", desc: "African-themed villas with cultural design", link: "/villas" },
  { icon: Star, title: "Wellness & Spa", desc: "Rejuvenate with world-class treatments", link: "/experiences" },
];

const highlights = [
  { img: villaImg, title: "Luxury Villas", desc: "54 uniquely designed African-themed villas", link: "/villas" },
  { img: diningImg, title: "Fine Dining", desc: "Local Ethiopian & international cuisine", link: "/experiences" },
  { img: wellnessImg, title: "Wellness Retreat", desc: "Yoga, meditation, and spa experiences", link: "/experiences" },
];

const fadeUp = {
  initial: { opacity: 0, y: 30 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true },
  transition: { duration: 0.6 },
};

const Index = () => (
  <div>
    {/* Hero */}
    <section className="relative h-screen min-h-[600px] flex items-center overflow-hidden">
      <img src={heroImg} alt="Kuriftu Resort aerial view" className="absolute inset-0 w-full h-full object-cover" width={1920} height={1080} />
      <div className="absolute inset-0 hero-overlay" />
      <div className="relative container-resort px-4 sm:px-6 lg:px-8">
        <motion.div initial={{ opacity: 0, y: 40 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }} className="max-w-2xl">
          <p className="text-gold-light font-body text-sm uppercase tracking-[0.3em] mb-4">Kuriftu Resort & Spa</p>
          <h1 className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold text-primary-foreground leading-tight mb-6">
            Experience African Luxury at <span className="text-gradient-gold">Kuriftu African Village</span>
          </h1>
          <p className="text-primary-foreground/80 font-body text-lg mb-8 leading-relaxed">
            Discover 54 handcrafted villas nestled in Ethiopia's breathtaking landscape. Where African heritage meets modern luxury.
          </p>
          <div className="flex flex-wrap gap-4">
            <Link to="/villas" className="gradient-gold text-primary-foreground px-8 py-3 rounded-full font-semibold shadow-lg hover:shadow-xl transition-shadow">
              Explore Villas
            </Link>
            <Link to="/concierge" className="glass-card px-8 py-3 rounded-full font-semibold text-primary-foreground border-primary-foreground/20 hover:bg-primary-foreground/10 transition-colors flex items-center gap-2">
              <MessageCircle className="w-4 h-4" /> Talk to AI Concierge
            </Link>
          </div>
        </motion.div>
      </div>
    </section>

    {/* Features */}
    <section className="section-padding bg-background">
      <div className="container-resort">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((f, i) => (
            <motion.div key={f.title} {...fadeUp} transition={{ delay: i * 0.1 }}>
              <Link to={f.link} className="glass-card p-6 block hover:shadow-xl transition-all hover:-translate-y-1 group">
                <div className="w-12 h-12 rounded-xl gradient-gold flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                  <f.icon className="w-6 h-6 text-primary-foreground" />
                </div>
                <h3 className="font-display text-lg font-semibold mb-2 text-foreground">{f.title}</h3>
                <p className="text-muted-foreground text-sm">{f.desc}</p>
              </Link>
            </motion.div>
          ))}
        </div>
      </div>
    </section>

    {/* Highlights */}
    <section className="section-padding bg-muted/50">
      <div className="container-resort">
        <motion.div {...fadeUp} className="text-center mb-12">
          <p className="text-accent font-body text-sm uppercase tracking-[0.2em] mb-2">Discover</p>
          <h2 className="font-display text-3xl sm:text-4xl font-bold text-foreground">Unforgettable Experiences</h2>
        </motion.div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {highlights.map((h, i) => (
            <motion.div key={h.title} {...fadeUp} transition={{ delay: i * 0.15 }}>
              <Link to={h.link} className="group block rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-shadow">
                <div className="aspect-[4/3] overflow-hidden">
                  <img src={h.img} alt={h.title} loading="lazy" width={800} height={600} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                </div>
                <div className="p-6 bg-card">
                  <h3 className="font-display text-xl font-semibold text-foreground mb-1">{h.title}</h3>
                  <p className="text-muted-foreground text-sm">{h.desc}</p>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      </div>
    </section>

    {/* CTA */}
    <section className="relative py-24 overflow-hidden">
      <div className="absolute inset-0 gradient-earth" />
      <div className="relative container-resort px-4 sm:px-6 lg:px-8 text-center">
        <motion.div {...fadeUp}>
          <h2 className="font-display text-3xl sm:text-4xl font-bold text-primary-foreground mb-4">Ready to Experience African Luxury?</h2>
          <p className="text-primary-foreground/70 font-body max-w-lg mx-auto mb-8">
            Let our AI concierge help you plan the perfect stay at Kuriftu African Village.
          </p>
          <Link to="/concierge" className="inline-flex items-center gap-2 gradient-gold text-primary-foreground px-8 py-3 rounded-full font-semibold shadow-lg hover:shadow-xl transition-shadow">
            <MessageCircle className="w-5 h-5" /> Start Planning
          </Link>
        </motion.div>
      </div>
    </section>
  </div>
);

export default Index;
