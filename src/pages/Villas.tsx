import { motion } from "framer-motion";
import PageHero from "@/components/PageHero";
import villaRomantic from "@/assets/villa-romantic.jpg";
import villaFamily from "@/assets/villa-family.jpg";
import villaCultural from "@/assets/villa-cultural.jpg";
import { Heart, Users, Palette } from "lucide-react";

const villas = [
  {
    img: villaRomantic,
    icon: Heart,
    title: "Romantic Villas",
    desc: "Intimate spaces designed for couples. Private gardens, plunge pools, and candlelit terraces create the perfect romantic atmosphere.",
    features: ["Private plunge pool", "Garden terrace", "King-size bed", "Couples spa access"],
  },
  {
    img: villaFamily,
    icon: Users,
    title: "Family Villas",
    desc: "Spacious villas with separate living areas, child-friendly amenities, and room for the whole family to relax and explore.",
    features: ["Separate bedrooms", "Living area", "Kids' amenities", "Garden access"],
  },
  {
    img: villaCultural,
    icon: Palette,
    title: "Cultural Experience Villas",
    desc: "Immerse yourself in authentic African artistry. Each villa showcases unique regional craftsmanship and traditional Ethiopian design.",
    features: ["Authentic artifacts", "Handwoven textiles", "Carved wooden panels", "Cultural tours included"],
  },
];

const fadeUp = { initial: { opacity: 0, y: 30 }, whileInView: { opacity: 1, y: 0 }, viewport: { once: true } };

const Villas = () => (
  <div>
    <PageHero title="Our Villas" subtitle="54 uniquely crafted African-themed villas await you" image={villaRomantic} />

    <section className="section-padding bg-background">
      <div className="container-resort">
        <motion.div {...fadeUp} className="text-center mb-12">
          <p className="text-accent font-body text-sm uppercase tracking-[0.2em] mb-2">Accommodation</p>
          <h2 className="font-display text-3xl font-bold text-foreground">Choose Your African Experience</h2>
        </motion.div>

        <div className="space-y-16">
          {villas.map((v, i) => (
            <motion.div key={v.title} {...fadeUp} transition={{ delay: i * 0.1 }} className={`grid grid-cols-1 lg:grid-cols-2 gap-8 items-center ${i % 2 ? "lg:direction-rtl" : ""}`}>
              <div className={i % 2 ? "lg:order-2" : ""}>
                <div className="rounded-2xl overflow-hidden shadow-xl">
                  <img src={v.img} alt={v.title} loading="lazy" width={800} height={600} className="w-full h-full object-cover aspect-[4/3]" />
                </div>
              </div>
              <div className={i % 2 ? "lg:order-1" : ""}>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 rounded-lg gradient-gold flex items-center justify-center">
                    <v.icon className="w-5 h-5 text-primary-foreground" />
                  </div>
                  <h3 className="font-display text-2xl font-bold text-foreground">{v.title}</h3>
                </div>
                <p className="text-muted-foreground font-body leading-relaxed mb-6">{v.desc}</p>
                <div className="grid grid-cols-2 gap-3">
                  {v.features.map((f) => (
                    <div key={f} className="glass-card px-4 py-3 text-sm text-foreground font-body">✦ {f}</div>
                  ))}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  </div>
);

export default Villas;
