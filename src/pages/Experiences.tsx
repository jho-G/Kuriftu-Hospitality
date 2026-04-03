import { motion } from "framer-motion";
import PageHero from "@/components/PageHero";
import diningImg from "@/assets/dining.jpg";
import wellnessImg from "@/assets/wellness.jpg";
import { UtensilsCrossed, Leaf, Waves, Film, TreePine, Sparkles } from "lucide-react";

const experiences = [
  { icon: UtensilsCrossed, title: "Fine Dining", desc: "Savor authentic Ethiopian cuisine alongside international dishes, prepared by world-class chefs using locally sourced ingredients.", category: "Dining" },
  { icon: Leaf, title: "Yoga & Meditation", desc: "Find inner peace with guided sessions in our tranquil garden pavilions overlooking the lake.", category: "Wellness" },
  { icon: Sparkles, title: "Spa & Treatments", desc: "Rejuvenate with traditional African treatments, aromatherapy, and luxury spa rituals.", category: "Wellness" },
  { icon: Waves, title: "Water Park & Kayaking", desc: "Enjoy thrilling water activities, from kayaking on the lake to our family water park.", category: "Activities" },
  { icon: Film, title: "Outdoor Cinema", desc: "Watch films under the African stars in our open-air cinema nestled in the gardens.", category: "Activities" },
  { icon: TreePine, title: "Forest Adventure", desc: "Explore guided nature walks, zip-lining, and eco-tours through Ethiopia's lush landscapes.", category: "Activities" },
];

const fadeUp = { initial: { opacity: 0, y: 30 }, whileInView: { opacity: 1, y: 0 }, viewport: { once: true } };

const Experiences = () => (
  <div>
    <PageHero title="Experiences" subtitle="Dining, wellness, and adventures await at every corner" image={wellnessImg} />

    {/* Images */}
    <section className="section-padding bg-background">
      <div className="container-resort">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
          {[{ img: diningImg, title: "World-Class Dining", sub: "Ethiopian & International Cuisine" }, { img: wellnessImg, title: "Wellness Retreat", sub: "Spa, Yoga & Meditation" }].map((item, i) => (
            <motion.div key={item.title} {...fadeUp} transition={{ delay: i * 0.15 }} className="rounded-2xl overflow-hidden shadow-xl relative group">
              <img src={item.img} alt={item.title} loading="lazy" width={800} height={600} className="w-full aspect-[16/10] object-cover group-hover:scale-105 transition-transform duration-500" />
              <div className="absolute inset-0 bg-gradient-to-t from-foreground/70 to-transparent" />
              <div className="absolute bottom-6 left-6">
                <h3 className="font-display text-2xl font-bold text-primary-foreground">{item.title}</h3>
                <p className="text-primary-foreground/80 text-sm">{item.sub}</p>
              </div>
            </motion.div>
          ))}
        </div>

        <motion.div {...fadeUp} className="text-center mb-12">
          <p className="text-accent font-body text-sm uppercase tracking-[0.2em] mb-2">What Awaits</p>
          <h2 className="font-display text-3xl font-bold text-foreground">Curated Experiences</h2>
        </motion.div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {experiences.map((e, i) => (
            <motion.div key={e.title} {...fadeUp} transition={{ delay: i * 0.08 }} className="glass-card p-6 hover:shadow-xl transition-all hover:-translate-y-1">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-10 h-10 rounded-lg gradient-gold flex items-center justify-center">
                  <e.icon className="w-5 h-5 text-primary-foreground" />
                </div>
                <span className="text-xs font-body uppercase tracking-wider text-accent">{e.category}</span>
              </div>
              <h3 className="font-display text-lg font-semibold text-foreground mb-2">{e.title}</h3>
              <p className="text-muted-foreground text-sm leading-relaxed">{e.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  </div>
);

export default Experiences;
