"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardTitle,
  CardDescription,
  CardFooter,
} from "@/components/ui/card";
import { Send, ShoppingBag } from "lucide-react";

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  image: string;
  category: string;
}

interface Message {
  role: "user" | "assistant";
  content: string;
  products?: Product[];
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.reply,
          products: data.products,
        },
      ]);
    } catch (error) {
      console.error("Error fetching chat:", error);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Sorry, I encountered an error connecting to the server. Please ensure the backend is running.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-background text-foreground">
      {/* Header */}
      <header className="flex items-center p-4 border-b sticky top-0 bg-background/95 backdrop-blur z-10">
        <ShoppingBag className="w-6 h-6 mr-2" />
        <h1 className="text-xl font-bold">Product Finder Agent</h1>
      </header>

      {/* Chat Area */}
      <main className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-muted-foreground space-y-4">
            <ShoppingBag className="w-12 h-12 opacity-20" />
            <p>
              Ask me about our products! Try &quot;Show me clothing under
              $50&quot;
            </p>
          </div>
        )}

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex flex-col ${
              msg.role === "user" ? "items-end" : "items-start"
            }`}
          >
            {/* Message Bubble */}
            <div
              className={`max-w-[80%] rounded-lg px-4 py-2 ${
                msg.role === "user"
                  ? "bg-primary text-primary-foreground"
                  : "bg-muted text-foreground"
              }`}
            >
              <p className="whitespace-pre-wrap">{msg.content}</p>
            </div>

            {/* Product Cards (only for assistant) */}
            {msg.role === "assistant" &&
              msg.products &&
              msg.products.length > 0 && (
                <div className="mt-4 flex flex-col gap-4 w-full max-w-xl">
                  {msg.products.map((product) => (
                    <Card
                      key={product.id}
                      className="flex flex-row overflow-hidden h-48"
                    >
                      <div className="w-48 shrink-0 relative bg-muted">
                        <img
                          src={product.image}
                          alt={product.name}
                          className="object-cover w-full h-full"
                          onError={(e) => {
                            (e.target as HTMLImageElement).src =
                              "https://placehold.co/400?text=No+Image";
                          }}
                        />
                      </div>
                      <div className="flex flex-col flex-1 p-6 justify-between">
                        <div>
                          <div className="flex justify-between items-start mb-2">
                            <div>
                              <CardTitle className="text-lg">
                                {product.name}
                              </CardTitle>
                              <CardDescription className="capitalize mt-1">
                                {product.category}
                              </CardDescription>
                            </div>
                            <span className="font-bold text-lg">
                              ${product.price.toFixed(2)}
                            </span>
                          </div>
                          <CardContent className="p-0">
                            <p className="text-sm text-muted-foreground line-clamp-3">
                              {product.description}
                            </p>
                          </CardContent>
                        </div>
                        <CardFooter className="p-0 justify-end mt-auto">
                          <Button size="sm" variant="outline">
                            View Details
                          </Button>
                        </CardFooter>
                      </div>
                    </Card>
                  ))}
                </div>
              )}
          </div>
        ))}

        {isLoading && (
          <div className="flex items-start">
            <div className="bg-muted rounded-lg px-4 py-2">
              <span className="animate-pulse">Thinking...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      {/* Input Area */}
      <footer className="p-4 border-t bg-background">
        <form onSubmit={handleSubmit} className="flex gap-2 max-w-4xl mx-auto">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about products..."
            disabled={isLoading}
            className="flex-1"
          />
          <Button type="submit" disabled={isLoading || !input.trim()}>
            <Send className="w-4 h-4" />
            <span className="sr-only">Send</span>
          </Button>
        </form>
      </footer>
    </div>
  );
}
