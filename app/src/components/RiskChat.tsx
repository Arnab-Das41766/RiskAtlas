import { useState, useRef, useEffect, useCallback } from 'react';
import { Bot, X, Send, Loader2, MessageSquare, Trash2 } from 'lucide-react';
import { sendChatMessage } from '@/services/api';

interface Message {
    id: number;
    role: 'user' | 'assistant';
    content: string;
}

interface RiskChatProps {
    selectedCountryId?: string;
}

const WELCOME: Message = {
    id: 0,
    role: 'assistant',
    content:
        'Hi! I\'m **RiskAtlas AI**, powered by your local Qwen model. I have full access to all country risk scores, policy alerts, and supply chain data.\n\nTry asking:\n• *"Which countries have critical trade risk?"*\n• *"What are the latest sanctions on Russia?"*\n• *"Best alternatives to sourcing from China?"*\n• *"Tell me about the selected country"*',
};

// Very lightweight markdown renderer: bold, italic, bullets
function renderMd(text: string) {
    const lines = text.split('\n');
    return lines.map((line, i) => {
        // Bullet
        if (line.match(/^[•*-] /)) {
            const content = line.replace(/^[•*-] /, '');
            return (
                <li key={i} className="ml-4 list-disc text-slate-300 my-0.5">
                    {inlineFormat(content)}
                </li>
            );
        }
        if (line.trim() === '') return <br key={i} />;
        return <p key={i} className="my-0.5">{inlineFormat(line)}</p>;
    });
}

function inlineFormat(text: string) {
    // Bold **text**
    const parts = text.split(/(\*\*[^*]+\*\*|\*[^*]+\*)/g);
    return parts.map((part, i) => {
        if (part.startsWith('**') && part.endsWith('**'))
            return <strong key={i} className="text-white font-semibold">{part.slice(2, -2)}</strong>;
        if (part.startsWith('*') && part.endsWith('*'))
            return <em key={i} className="text-slate-200">{part.slice(1, -1)}</em>;
        return <span key={i}>{part}</span>;
    });
}

export function RiskChat({ selectedCountryId }: RiskChatProps) {
    const [open, setOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([WELCOME]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const bottomRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLTextAreaElement>(null);
    const nextId = useRef(1);

    // Auto-scroll to latest message
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Focus input when chat opens
    useEffect(() => {
        if (open) setTimeout(() => inputRef.current?.focus(), 100);
    }, [open]);

    const send = useCallback(async () => {
        const text = input.trim();
        if (!text || loading) return;

        const userMsg: Message = { id: nextId.current++, role: 'user', content: text };
        setMessages((prev) => [...prev, userMsg]);
        setInput('');
        setLoading(true);

        // Build history for context (exclude welcome message)
        const history = messages
            .filter((m) => m.id !== 0)
            .map((m) => ({ role: m.role, content: m.content }));

        try {
            const data = await sendChatMessage(text, selectedCountryId, history);
            const aiMsg: Message = { id: nextId.current++, role: 'assistant', content: data.reply };
            setMessages((prev) => [...prev, aiMsg]);
        } catch (err) {
            const msg = err instanceof Error ? err.message : String(err);
            setMessages((prev) => [
                ...prev,
                {
                    id: nextId.current++,
                    role: 'assistant',
                    content: `⚠️ **${msg}**\n\nMake sure:\n• Backend is running → \`cd riskatlas/backend && python main.py\`\n• Ollama is running → \`ollama serve\``,
                },
            ]);
        } finally {
            setLoading(false);
        }
    }, [input, loading, messages, selectedCountryId]);

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            send();
        }
    };

    const clearChat = () => setMessages([WELCOME]);

    return (
        <>
            {/* ── Floating toggle button ───────────────────────────── */}
            <button
                onClick={() => setOpen((o) => !o)}
                className="fixed bottom-6 right-6 z-50 flex items-center justify-center w-14 h-14 rounded-full
                   bg-gradient-to-br from-blue-600 to-indigo-700 shadow-2xl
                   hover:scale-110 active:scale-95 transition-transform"
                title="RiskAtlas AI"
            >
                {open ? (
                    <X className="w-6 h-6 text-white" />
                ) : (
                    <>
                        <MessageSquare className="w-6 h-6 text-white" />
                        {/* pulse badge */}
                        <span className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-slate-950 animate-pulse" />
                    </>
                )}
            </button>

            {/* ── Chat panel ──────────────────────────────────────── */}
            {open && (
                <div
                    className="fixed bottom-24 right-6 z-50 flex flex-col
                     w-[360px] h-[520px] rounded-2xl overflow-hidden
                     bg-slate-900/95 border border-slate-700 shadow-2xl backdrop-blur-md"
                    style={{ animation: 'slideUpChat 0.22s ease-out' }}
                >
                    {/* Header */}
                    <div className="flex items-center gap-2.5 px-4 py-3 bg-gradient-to-r from-blue-900/60 to-indigo-900/60 border-b border-slate-700">
                        <div className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-600">
                            <Bot className="w-4 h-4 text-white" />
                        </div>
                        <div className="flex-1 min-w-0">
                            <p className="text-sm font-semibold text-white leading-tight">RiskAtlas AI</p>
                            <p className="text-[10px] text-slate-400 truncate">
                                qwen2.5-coder:7b · local{selectedCountryId ? ` · ctx: ${selectedCountryId}` : ''}
                            </p>
                        </div>
                        <button
                            onClick={clearChat}
                            title="Clear chat"
                            className="p-1.5 rounded-md text-slate-500 hover:text-red-400 hover:bg-red-500/10 transition-colors"
                        >
                            <Trash2 className="w-4 h-4" />
                        </button>
                    </div>

                    {/* Messages */}
                    <div className="flex-1 overflow-y-auto px-3 py-3 space-y-3 scroll-smooth">
                        {messages.map((msg) => (
                            <div
                                key={msg.id}
                                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                {msg.role === 'assistant' && (
                                    <div className="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-700 flex items-center justify-center mr-2 mt-0.5">
                                        <Bot className="w-3.5 h-3.5 text-white" />
                                    </div>
                                )}
                                <div
                                    className={`max-w-[82%] rounded-2xl px-3 py-2 text-sm leading-relaxed
                    ${msg.role === 'user'
                                            ? 'bg-blue-600 text-white rounded-tr-sm'
                                            : 'bg-slate-800 text-slate-200 rounded-tl-sm border border-slate-700'
                                        }`}
                                >
                                    <div className="space-y-0.5">{renderMd(msg.content)}</div>
                                </div>
                            </div>
                        ))}

                        {/* Typing indicator */}
                        {loading && (
                            <div className="flex items-start gap-2">
                                <div className="w-6 h-6 rounded-full bg-indigo-700 flex items-center justify-center flex-shrink-0">
                                    <Bot className="w-3.5 h-3.5 text-white" />
                                </div>
                                <div className="bg-slate-800 border border-slate-700 rounded-2xl rounded-tl-sm px-4 py-3">
                                    <div className="flex gap-1 items-center">
                                        <span className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                        <span className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                        <span className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                                    </div>
                                </div>
                            </div>
                        )}
                        <div ref={bottomRef} />
                    </div>

                    {/* Input */}
                    <div className="px-3 py-3 border-t border-slate-700 bg-slate-900/80">
                        <div className="flex items-end gap-2 bg-slate-800 rounded-xl border border-slate-600 px-3 py-2
                            focus-within:border-blue-500 transition-colors">
                            <textarea
                                ref={inputRef}
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={handleKeyDown}
                                placeholder="Ask about trade risks, alerts, suppliers…"
                                rows={1}
                                disabled={loading}
                                className="flex-1 resize-none bg-transparent text-sm text-slate-200 placeholder-slate-500
                           outline-none max-h-28 overflow-y-auto leading-relaxed disabled:opacity-50"
                                style={{ scrollbarWidth: 'none' }}
                            />
                            <button
                                onClick={send}
                                disabled={!input.trim() || loading}
                                className="flex-shrink-0 w-8 h-8 rounded-lg bg-blue-600 hover:bg-blue-500
                           disabled:opacity-40 disabled:cursor-not-allowed
                           flex items-center justify-center transition-colors"
                            >
                                {loading ? (
                                    <Loader2 className="w-4 h-4 text-white animate-spin" />
                                ) : (
                                    <Send className="w-4 h-4 text-white" />
                                )}
                            </button>
                        </div>
                        <p className="text-[10px] text-slate-600 mt-1.5 text-center">
                            Enter to send · Shift+Enter for newline
                        </p>
                    </div>
                </div>
            )}
        </>
    );
}
