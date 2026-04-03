const OPENROUTER_API_KEY = "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";
const OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions";

export interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
}

export async function chatCompletion(messages: ChatMessage[], model = "google/gemini-2.5-flash"): Promise<string> {
  const response = await fetch(OPENROUTER_URL, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
      "Content-Type": "application/json",
      "HTTP-Referer": window.location.origin,
      "X-Title": "Kuriftu Resort AI Concierge",
    },
    body: JSON.stringify({ model, messages }),
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`OpenRouter error ${response.status}: ${err}`);
  }

  const data = await response.json();
  return data.choices?.[0]?.message?.content ?? "I'm sorry, I couldn't generate a response.";
}

export async function streamChatCompletion({
  messages,
  onDelta,
  onDone,
  model = "google/gemini-2.5-flash",
}: {
  messages: ChatMessage[];
  onDelta: (text: string) => void;
  onDone: () => void;
  model?: string;
}) {
  const response = await fetch(OPENROUTER_URL, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
      "Content-Type": "application/json",
      "HTTP-Referer": window.location.origin,
      "X-Title": "Kuriftu Resort AI Concierge",
    },
    body: JSON.stringify({ model, messages, stream: true }),
  });

  if (!response.ok || !response.body) {
    throw new Error(`OpenRouter error: ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    let newlineIdx: number;
    while ((newlineIdx = buffer.indexOf("\n")) !== -1) {
      let line = buffer.slice(0, newlineIdx);
      buffer = buffer.slice(newlineIdx + 1);
      if (line.endsWith("\r")) line = line.slice(0, -1);
      if (!line.startsWith("data: ")) continue;
      const jsonStr = line.slice(6).trim();
      if (jsonStr === "[DONE]") { onDone(); return; }
      try {
        const parsed = JSON.parse(jsonStr);
        const content = parsed.choices?.[0]?.delta?.content;
        if (content) onDelta(content);
      } catch { /* partial JSON, skip */ }
    }
  }
  onDone();
}

export async function analyzeSentimentAI(text: string): Promise<{
  sentiment: "positive" | "neutral" | "negative";
  confidence: number;
  suggestion: string;
}> {
  const messages: ChatMessage[] = [
    {
      role: "system",
      content: `You are a sentiment analysis AI for Kuriftu Resort & Spa. Analyze guest feedback and return ONLY valid JSON with this exact structure:
{"sentiment": "positive"|"neutral"|"negative", "confidence": 0.0-1.0, "suggestion": "personalized response message"}
For positive: thank the guest warmly. For negative: apologize and promise follow-up. For neutral: encourage more details. Be warm and professional.`,
    },
    { role: "user", content: `Analyze this guest feedback:\n\n"${text}"` },
  ];

  const response = await chatCompletion(messages);
  
  try {
    const cleaned = response.replace(/```json\n?/g, "").replace(/```\n?/g, "").trim();
    return JSON.parse(cleaned);
  } catch {
    // Fallback
    return {
      sentiment: "neutral",
      confidence: 0.5,
      suggestion: response,
    };
  }
}
