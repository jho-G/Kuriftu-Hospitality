import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Mic, MicOff, Bot, User } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { streamChatCompletion, type ChatMessage } from "@/lib/openrouter";
import { toast } from "sonner";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

const SYSTEM_PROMPT = `You are a luxury resort concierge for Kuriftu African Village in Ethiopia. You help guests with:
- Information about 54 African-themed villas (Romantic, Family, Cultural)
- Dining options (Ethiopian & international cuisine)
- Wellness services (spa, yoga, meditation)
- Activities (water park, kayaking, cinema, forest adventure)
- Events & meetings (Pan-African Hall, Haile Selassie Hall, Kwame Nkrumah Hall)
- Personalized recommendations for romantic stays, family trips, and wellness retreats
Be warm, professional, and knowledgeable. Keep responses concise but helpful. Use emojis sparingly for warmth.`;

const quickSuggestions = [
  "What are the best activities?",
  "Tell me about the villas",
  "Spa services available?",
  "Plan a romantic getaway",
  "Family-friendly options?",
  "Dining recommendations",
];

const Concierge = () => {
  const [messages, setMessages] = useState<Message[]>([
    { id: "1", role: "assistant", content: "Welcome to Kuriftu African Village! ✨\n\nI'm your AI concierge. How can I make your stay extraordinary today? Ask me about our villas, dining, wellness, or activities!" },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const sendMessage = async (text: string) => {
    if (!text.trim() || isTyping) return;
    const userMsg: Message = { id: Date.now().toString(), role: "user", content: text.trim() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    const history: ChatMessage[] = [
      { role: "system", content: SYSTEM_PROMPT },
      ...messages.map((m) => ({ role: m.role as "user" | "assistant", content: m.content })),
      { role: "user" as const, content: text.trim() },
    ];

    let assistantContent = "";
    const assistantId = (Date.now() + 1).toString();

    try {
      await streamChatCompletion({
        messages: history,
        onDelta: (chunk) => {
          assistantContent += chunk;
          setMessages((prev) => {
            const last = prev[prev.length - 1];
            if (last?.id === assistantId) {
              return prev.map((m) => m.id === assistantId ? { ...m, content: assistantContent } : m);
            }
            return [...prev, { id: assistantId, role: "assistant", content: assistantContent }];
          });
        },
        onDone: () => setIsTyping(false),
      });
    } catch (e) {
      toast.error("Failed to get AI response. Please try again.");
      setIsTyping(false);
    }
  };

  const toggleVoice = () => {
    if (!("webkitSpeechRecognition" in window) && !("SpeechRecognition" in window)) {
      toast.error("Speech recognition is not supported in your browser.");
      return;
    }
    if (isListening) {
      recognitionRef.current?.stop();
      setIsListening(false);
      return;
    }
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.onresult = (e: any) => {
      setInput(e.results[0][0].transcript);
      setIsListening(false);
    };
    recognition.onerror = () => setIsListening(false);
    recognition.onend = () => setIsListening(false);
    recognitionRef.current = recognition;
    recognition.start();
    setIsListening(true);
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <div className="gradient-earth px-4 py-6 sm:px-6">
        <div className="container-resort flex items-center gap-3">
          <div className="w-12 h-12 rounded-full gradient-gold flex items-center justify-center">
            <Bot className="w-6 h-6 text-primary-foreground" />
          </div>
          <div>
            <h1 className="font-display text-xl font-bold text-primary-foreground">AI Concierge</h1>
            <p className="text-primary-foreground/60 text-sm">Powered by AI • Your personal resort assistant</p>
          </div>
          <div className="ml-auto flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-forest animate-pulse" />
            <span className="text-primary-foreground/60 text-xs">Online</span>
          </div>
        </div>
      </div>

      {/* Quick suggestions */}
      <div className="bg-muted/50 border-b border-border px-4 py-3 overflow-x-auto">
        <div className="container-resort flex gap-2 min-w-max">
          {quickSuggestions.map((s) => (
            <button key={s} onClick={() => sendMessage(s)} className="px-4 py-2 text-xs font-body rounded-full bg-card border border-border text-foreground hover:bg-accent/10 hover:border-accent/30 transition-colors whitespace-nowrap">
              {s}
            </button>
          ))}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="container-resort max-w-3xl mx-auto space-y-4">
          <AnimatePresence>
            {messages.map((msg) => (
              <motion.div key={msg.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className={`flex gap-3 ${msg.role === "user" ? "justify-end" : ""}`}>
                {msg.role === "assistant" && (
                  <div className="w-8 h-8 rounded-full gradient-gold flex items-center justify-center flex-shrink-0 mt-1">
                    <Bot className="w-4 h-4 text-primary-foreground" />
                  </div>
                )}
                <div className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm font-body leading-relaxed ${
                  msg.role === "user"
                    ? "gradient-gold text-primary-foreground rounded-br-md"
                    : "glass-card text-foreground rounded-bl-md"
                }`}>
                  {msg.role === "assistant" ? (
                    <div className="prose prose-sm dark:prose-invert max-w-none [&>p]:mb-2 [&>ul]:mb-2 [&>ol]:mb-2">
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    </div>
                  ) : msg.content}
                </div>
                {msg.role === "user" && (
                  <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center flex-shrink-0 mt-1">
                    <User className="w-4 h-4 text-secondary-foreground" />
                  </div>
                )}
              </motion.div>
            ))}
          </AnimatePresence>

          {isTyping && messages[messages.length - 1]?.role !== "assistant" && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-3">
              <div className="w-8 h-8 rounded-full gradient-gold flex items-center justify-center flex-shrink-0">
                <Bot className="w-4 h-4 text-primary-foreground" />
              </div>
              <div className="glass-card rounded-2xl rounded-bl-md px-4 py-3 flex items-center gap-1">
                {[0, 1, 2].map((i) => (
                  <motion.div key={i} className="w-2 h-2 rounded-full bg-accent" animate={{ y: [0, -6, 0] }} transition={{ repeat: Infinity, duration: 0.6, delay: i * 0.15 }} />
                ))}
              </div>
            </motion.div>
          )}
          <div ref={bottomRef} />
        </div>
      </div>

      {/* Input */}
      <div className="border-t border-border bg-background px-4 py-4">
        <div className="container-resort max-w-3xl mx-auto flex gap-2">
          <button onClick={toggleVoice} className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center transition-colors ${isListening ? "gradient-gold text-primary-foreground animate-pulse-gold" : "bg-secondary text-secondary-foreground hover:bg-muted"}`}>
            {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
          </button>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage(input)}
            placeholder="Ask about villas, dining, spa, activities..."
            className="flex-1 bg-card border border-border rounded-full px-4 py-2 text-sm font-body text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          />
          <button onClick={() => sendMessage(input)} disabled={!input.trim() || isTyping} className="flex-shrink-0 w-10 h-10 rounded-full gradient-gold flex items-center justify-center text-primary-foreground disabled:opacity-50 hover:shadow-lg transition-shadow">
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Concierge;
