import { motion } from "framer-motion";

interface PageHeroProps {
  title: string;
  subtitle: string;
  image?: string;
}

const PageHero = ({ title, subtitle, image }: PageHeroProps) => (
  <section className="relative h-[50vh] min-h-[350px] flex items-end overflow-hidden">
    {image && (
      <img src={image} alt={title} className="absolute inset-0 w-full h-full object-cover" />
    )}
    <div className="absolute inset-0 hero-overlay" />
    <div className="relative container-resort px-4 sm:px-6 lg:px-8 pb-12">
      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="font-display text-4xl sm:text-5xl font-bold text-primary-foreground mb-3"
      >
        {title}
      </motion.h1>
      <motion.p
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.15 }}
        className="text-primary-foreground/80 font-body text-lg max-w-xl"
      >
        {subtitle}
      </motion.p>
    </div>
  </section>
);

export default PageHero;
