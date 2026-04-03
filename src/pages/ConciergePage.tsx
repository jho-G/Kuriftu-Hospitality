import { useState } from "react";
import { sendMessage } from "@/services/aiService";

const ConciergePage = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<
    { role: "user" | "assistant"; content: string }[]
  >([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { role: "user" as const, content: input };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const reply = await sendMessage(input);

      const aiMessage = {
        role: "assistant" as const,
        content: reply,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "⚠️ AI failed. Please try again.",
        },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen p-4 bg-gray-100 flex flex-col">
      <h1 className="text-2xl font-bold mb-4 text-center">
        AI Concierge
      </h1>

      {/* CHAT BOX */}
      <div className="flex-1 bg-white p-4 rounded shadow overflow-y-auto mb-4">
        {messages.length === 0 && (
          <p className="text-gray-400 text-center">
            Ask me anything about Kuriftu Resort ✨
          </p>
        )}

        {messages.map((msg, index) => (
          <div
            key={index}
            className={
              msg.role === "user" ? "text-right" : "text-left"
            }
          >
            <p
              className={`inline-block p-3 rounded m-1 max-w-[80%] ${
                msg.role === "user"
                  ? "bg-indigo-600 text-white"
                  : "bg-gray-200"
              }`}
            >
              {msg.content}
            </p>
          </div>
        ))}

        {loading && (
          <p className="text-gray-400 text-sm mt-2">
            AI is typing...
          </p>
        )}
      </div>

      {/* INPUT */}
      <div className="flex">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          className="flex-1 p-2 border rounded-l"
          placeholder="Ask about villas, spa, dining..."
        />

        <button
          onClick={handleSend}
          disabled={loading}
          className="bg-indigo-600 text-white px-4 rounded-r disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ConciergePage;