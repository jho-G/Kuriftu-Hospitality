import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Smile, Meh, Frown, Sparkles, Star } from "lucide-react";
import { analyzeSentimentAI } from "@/lib/openrouter";
import { toast } from "sonner";

interface SentimentResult {
  sentiment: "positive" | "neutral" | "negative";
  confidence: number;
  suggestion: string;
}

const sentimentConfig = {
  positive: { icon: Smile, label: "Positive", color: "text-forest", bg: "bg-forest/10", border: "border-forest/30" },
  neutral: { icon: Meh, label: "Neutral", color: "text-accent", bg: "bg-accent/10", border: "border-accent/30" },
  negative: { icon: Frown, label: "Negative", color: "text-destructive", bg: "bg-destructive/10", border: "border-destructive/30" },
};

const Feedback = () => {
  const [text, setText] = useState("");
  const [rating, setRating] = useState(0);
  const [result, setResult] = useState<SentimentResult | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [category, setCategory] = useState("overall");

  const handleSubmit = async () => {
    if (!text.trim()) return;
    setIsAnalyzing(true);
    setResult(null);
    try {
      const feedbackText = `Category: ${category}. Rating: ${rating}/5. Feedback: ${text}`;
      const res = await analyzeSentimentAI(feedbackText);
      setResult(res);
    } catch {
      toast.error("Failed to analyze feedback. Please try again.");
    }
    setIsAnalyzing(false);
  };

  const config = result ? sentimentConfig[result.sentiment] : null;

  return (
    <div className="min-h-screen bg-background">
      <div className="gradient-earth px-4 py-10 sm:px-6">
        <div className="container-resort">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <p className="text-gold-light font-body text-sm uppercase tracking-[0.2em] mb-2">Feedback</p>
            <h1 className="font-display text-3xl sm:text-4xl font-bold text-primary-foreground">Share Your Experience</h1>
            <p className="text-primary-foreground/60 text-sm mt-2">AI-powered sentiment analysis of your feedback</p>
          </motion.div>
        </div>
      </div>

      <div className="container-resort section-padding max-w-2xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="glass-card p-6 sm:p-8">
          <h2 className="font-display text-xl font-semibold text-foreground mb-4">How was your stay?</h2>

          {/* Category */}
          <div className="mb-4">
            <label className="text-sm font-body text-muted-foreground mb-2 block">Category</label>
            <div className="flex flex-wrap gap-2">
              {["overall", "villa", "dining", "spa", "activities", "staff"].map((c) => (
                <button key={c} onClick={() => setCategory(c)} className={`px-4 py-2 rounded-full text-xs font-semibold capitalize transition-all ${category === c ? "gradient-gold text-primary-foreground" : "bg-secondary text-secondary-foreground hover:bg-muted"}`}>
                  {c}
                </button>
              ))}
            </div>
          </div>

          {/* Star Rating */}
          <div className="mb-4">
            <label className="text-sm font-body text-muted-foreground mb-2 block">Rating</label>
            <div className="flex gap-1">
              {[1, 2, 3, 4, 5].map((s) => (
                <button key={s} onClick={() => setRating(s)} className="p-1 transition-transform hover:scale-110">
                  <Star className={`w-7 h-7 ${s <= rating ? "text-accent fill-accent" : "text-muted-foreground"}`} />
                </button>
              ))}
            </div>
          </div>

          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Tell us about your experience at Kuriftu African Village..."
            rows={5}
            className="w-full bg-background border border-border rounded-xl px-4 py-3 text-sm font-body text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring resize-none"
          />
          <button
            onClick={handleSubmit}
            disabled={!text.trim() || isAnalyzing}
            className="mt-4 w-full gradient-gold text-primary-foreground py-3 rounded-xl font-semibold text-sm flex items-center justify-center gap-2 disabled:opacity-50 hover:shadow-lg transition-shadow"
          >
            {isAnalyzing ? (
              <><Sparkles className="w-4 h-4 animate-spin" /> Analyzing with AI...</>
            ) : (
              <><Send className="w-4 h-4" /> Submit Feedback</>
            )}
          </button>
        </motion.div>

        <AnimatePresence>
          {result && config && (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className={`glass-card p-6 sm:p-8 mt-6 border ${config.border}`}>
              <div className="flex items-center gap-4 mb-4">
                <div className={`w-14 h-14 rounded-2xl ${config.bg} flex items-center justify-center`}>
                  <config.icon className={`w-8 h-8 ${config.color}`} />
                </div>
                <div>
                  <h3 className={`font-display text-xl font-bold ${config.color}`}>{config.label}</h3>
                  <p className="text-muted-foreground text-sm">Confidence: {(result.confidence * 100).toFixed(0)}%</p>
                </div>
              </div>
              <div className="w-full bg-secondary rounded-full h-2 mb-6">
                <motion.div initial={{ width: 0 }} animate={{ width: `${result.confidence * 100}%` }} transition={{ duration: 0.8 }}
                  className={`h-2 rounded-full ${result.sentiment === "positive" ? "bg-forest" : result.sentiment === "negative" ? "bg-destructive" : "bg-accent"}`}
                />
              </div>
              <div className={`${config.bg} rounded-xl p-4`}>
                <p className="text-sm font-body text-foreground leading-relaxed">{result.suggestion}</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default Feedback;
