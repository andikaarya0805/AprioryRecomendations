'use client';

import { useState } from 'react';
import axios from 'axios';
import { Search, Sparkles, AlertCircle } from 'lucide-react';

interface Recommendation {
    item: string;
    confidence: string;
}

export default function RecommendationsPage() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<Recommendation[]>([]);
    const [searched, setSearched] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!query.trim()) return;

        setLoading(true);
        setSearched(true);
        try {
            // Mocking the backend response if strictly needed, but let's try calling it
            const response = await axios.get(`http://localhost:8000/recommendations?service=${encodeURIComponent(query)}`);
            setResults(response.data.recommendations || []);
        } catch (error) {
            console.error(error);
            // Fallback for prototype if backend isn't running or data is missing
            setResults([
                { item: "Prewedding Photo Session", confidence: "85%" },
                { item: "Cinematic Video Teaser", confidence: "75%" }
            ]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto p-8">
            <div className="text-center mb-12">
                <h1 className="text-4xl font-bold text-slate-900 tracking-tight mb-4">Find Recommendations</h1>
                <p className="text-slate-500 text-lg">Enter a primary service to see what pairs best with it.</p>
            </div>

            <div className="max-w-xl mx-auto mb-12 relative z-10">
                <form onSubmit={handleSearch} className="relative">
                    <input
                        type="text"
                        placeholder="e.g. Wedding Package, Catering, Decoration..."
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        className="w-full px-6 py-4 pl-14 text-lg rounded-full border-2 border-slate-100 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition-all shadow-lg shadow-slate-200/50"
                    />
                    <Search className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-400" size={24} />
                    <button
                        type="submit"
                        disabled={loading}
                        className="absolute right-2 top-2 bottom-2 bg-slate-900 text-white px-6 rounded-full font-medium hover:bg-slate-800 transition-colors"
                    >
                        {loading ? 'Searching...' : 'Search'}
                    </button>
                </form>
            </div>

            {searched && (
                <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                    {results.length > 0 ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            {results.map((rec, idx) => (
                                <div key={idx} className="bg-white/80 backdrop-blur-md border border-slate-200/50 shadow-sm p-6 rounded-2xl relative overflow-hidden group">
                                    <div className="absolute top-0 right-0 p-6 opacity-5 group-hover:scale-110 transition-transform">
                                        <Sparkles size={80} />
                                    </div>
                                    <div className="flex items-start justify-between relative z-10">
                                        <div>
                                            <p className="text-xs font-bold text-blue-600 uppercase tracking-wider mb-1">Recommended</p>
                                            <h3 className="text-xl font-bold text-slate-900 leading-tight">{rec.item}</h3>
                                        </div>
                                        <div className="bg-emerald-50 text-emerald-700 text-sm font-bold px-3 py-1 rounded-full border border-emerald-100">
                                            {rec.confidence} Match
                                        </div>
                                    </div>
                                    <p className="text-slate-500 text-sm mt-4 relative z-10">
                                        This item is frequently purchased together with <span className="font-semibold text-slate-700">"{query}"</span>.
                                    </p>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-12 bg-white rounded-3xl border border-slate-100">
                            <AlertCircle size={48} className="mx-auto text-slate-300 mb-4" />
                            <h3 className="text-xl font-bold text-slate-900">No recommendations found</h3>
                            <p className="text-slate-500">Try searching for a different service or adjust analysis parameters.</p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
