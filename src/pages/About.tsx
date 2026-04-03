import { motion } from "framer-motion";
import PageHero from "@/components/PageHero";
import heroImg from "@/assets/hero-resort.jpg";
import { Users, Heart, Globe, Award } from "lucide-react";

const stats = [
  { icon: Users, value: "2,000+", label: "Jobs Created" },
  { icon: Heart, value: "Since 2002", label: "Serving Guests" },
  { icon: Globe, value: "54", label: "Luxury Villas" },
  { icon: Award, value: "#1", label: "African Resort" },
];

const fadeUp = { initial: { opacity: 0, y: 30 }, whileInView: { opacity: 1, y: 0 }, viewport: { once: true } };

const About = () => (
  <div>
    <PageHero title="About Kuriftu" subtitle="Built by Ethiopia. Shared with the world." image={heroImg} />

    <section className="section-padding bg-background">
      <div className="container-resort">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <motion.div {...fadeUp}>
            <p className="text-accent font-body text-sm uppercase tracking-[0.2em] mb-2">Our Story</p>
            <h2 className="font-display text-3xl font-bold text-foreground mb-6">A Legacy of African Craftsmanship</h2>
            <div className="space-y-4 text-muted-foreground font-body leading-relaxed">
              <p>Founded in 2002, Kuriftu Resort & Spa has grown to become Ethiopia's premier luxury hospitality destination. Our African Village concept celebrates the rich heritage and craftsmanship of the continent.</p>
              <p>Every villa is a masterpiece of African identity — handcrafted by local artisans using traditional techniques passed down through generations. From carved wooden panels to handwoven textiles, every detail tells a story.</p>
              <p>We believe luxury should be rooted in community. Our resort has created over 2,000 jobs, supporting local families and preserving cultural traditions for future generations.</p>
            </div>
          </motion.div>
          <motion.div {...fadeUp} transition={{ delay: 0.2 }}>
            <div className="grid grid-cols-2 gap-4">
              {stats.map((s) => (
                <div key={s.label} className="glass-card p-6 text-center">
                  <s.icon className="w-8 h-8 text-accent mx-auto mb-3" />
                  <div className="font-display text-2xl font-bold text-foreground">{s.value}</div>
                  <div className="text-muted-foreground text-sm">{s.label}</div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>

    <section className="section-padding bg-muted/50">
      <div className="container-resort text-center max-w-3xl mx-auto">
        <motion.div {...fadeUp}>
          <p className="text-accent font-body text-sm uppercase tracking-[0.2em] mb-2">Our Philosophy</p>
          <h2 className="font-display text-3xl font-bold text-foreground mb-6">"Built by Ethiopia. Shared with the world."</h2>
          <p className="text-muted-foreground font-body leading-relaxed text-lg">
            At Kuriftu, we don't just offer a stay — we offer a journey into the heart of Africa. Our commitment to authenticity, sustainability, and excellence defines every guest experience. From the moment you arrive, you become part of our story.
          </p>
        </motion.div>
      </div>
    </section>
  </div>
);

export default About;
