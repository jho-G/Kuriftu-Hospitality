import { motion } from "framer-motion";
import PageHero from "@/components/PageHero";
import eventsImg from "@/assets/events-hall.jpg";
import { Wifi, Monitor, Speaker, Users } from "lucide-react";

const halls = [
  { name: "Pan-African Hall", capacity: "500+ guests", desc: "Grand ballroom for large-scale events, conferences, and celebrations." },
  { name: "Haile Selassie Hall", capacity: "200 guests", desc: "An elegant space named after the last Ethiopian emperor, ideal for corporate events." },
  { name: "Kwame Nkrumah Hall", capacity: "150 guests", desc: "Honoring the Ghanaian leader, perfect for mid-size gatherings and workshops." },
];

const facilities = [
  { icon: Wifi, label: "High-Speed WiFi" },
  { icon: Monitor, label: "HD Projectors" },
  { icon: Speaker, label: "Sound Systems" },
  { icon: Users, label: "Event Planning" },
];

const fadeUp = { initial: { opacity: 0, y: 30 }, whileInView: { opacity: 1, y: 0 }, viewport: { once: true } };

const Events = () => (
  <div>
    <PageHero title="Events & Meetings" subtitle="World-class venues for conferences, weddings, and celebrations" image={eventsImg} />

    <section className="section-padding bg-background">
      <div className="container-resort">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
          <div>
            <motion.div {...fadeUp}>
              <p className="text-accent font-body text-sm uppercase tracking-[0.2em] mb-2">Venues</p>
              <h2 className="font-display text-3xl font-bold text-foreground mb-8">Our Event Spaces</h2>
            </motion.div>
            <div className="space-y-4">
              {halls.map((h, i) => (
                <motion.div key={h.name} {...fadeUp} transition={{ delay: i * 0.1 }} className="glass-card p-6">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-display text-lg font-semibold text-foreground">{h.name}</h3>
                    <span className="text-xs font-body bg-accent/10 text-accent px-3 py-1 rounded-full">{h.capacity}</span>
                  </div>
                  <p className="text-muted-foreground text-sm">{h.desc}</p>
                </motion.div>
              ))}
            </div>
          </div>
          <motion.div {...fadeUp} transition={{ delay: 0.2 }}>
            <div className="rounded-2xl overflow-hidden shadow-xl mb-8">
              <img src={eventsImg} alt="Pan-African Hall" loading="lazy" width={800} height={600} className="w-full aspect-[4/3] object-cover" />
            </div>
            <div className="glass-card p-6">
              <h3 className="font-display text-lg font-semibold text-foreground mb-4">Facilities</h3>
              <div className="grid grid-cols-2 gap-4">
                {facilities.map((f) => (
                  <div key={f.label} className="flex items-center gap-3">
                    <f.icon className="w-5 h-5 text-accent" />
                    <span className="text-sm text-foreground">{f.label}</span>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  </div>
);

export default Events;
