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
            const backendUrl = typeof window !== 'undefined'
                ? `http://${window.location.hostname}:8000/recommendations?service=${encodeURIComponent(query)}`
                : `http://localhost:8000/recommendations?service=${encodeURIComponent(query)}`;

            const response = await axios.get(backendUrl);
            setResults(response.data.recommendations || []);
        } catch (error) {
            console.error(error);
            setError('Gagal mengambil rekomendasi. Pastikan backend berjalan.');
        } finally {
            setLoading(false);
        }
    };

    const [error, setError] = useState('');

    return (
        <div className="max-w-4xl mx-auto p-8">
            <div className="text-center mb-12">
                <h1 className="text-4xl font-bold text-slate-900 tracking-tight mb-4">Sistem Rekomendasi Paket</h1>
                <p className="text-slate-500 text-lg">Cari paket utama untuk melihat pasangan paket yang paling sering dipesan.</p>
            </div>

            <div className="max-w-xl mx-auto mb-12 relative z-10">
                <form onSubmit={handleSearch} className="relative">
                    <input
                        type="text"
                        placeholder="Contoh: photo, wedding, engagement..."
                        value={query}
                        onChange={(e) => {
                            setQuery(e.target.value);
                            setError('');
                        }}
                        className="w-full px-6 py-4 pl-14 text-lg rounded-full border-2 border-slate-100 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition-all shadow-lg shadow-slate-200/50"
                    />
                    <Search className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-400" size={24} />
                    <button
                        type="submit"
                        disabled={loading}
                        className="absolute right-2 top-2 bottom-2 bg-slate-900 text-white px-6 rounded-full font-medium hover:bg-slate-800 transition-colors"
                    >
                        {loading ? 'Mencari...' : 'Cari'}
                    </button>
                </form>
                {error && <p className="text-center text-red-500 mt-4 text-sm">{error}</p>}
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
                                            <p className="text-xs font-bold text-blue-600 uppercase tracking-wider mb-1">Paket Rekomendasi</p>
                                            <h3 className="text-xl font-bold text-slate-900 leading-tight">{rec.item}</h3>
                                        </div>
                                        <div className="bg-emerald-50 text-emerald-700 text-sm font-bold px-3 py-1 rounded-full border border-emerald-100">
                                            {rec.confidence} Cocok
                                        </div>
                                    </div>
                                    <p className="text-slate-500 text-sm mt-4 relative z-10">
                                        Paket ini sering diambil bersamaan dengan <span className="font-semibold text-slate-700">"{query}"</span> berdasarkan data transaksi Anda.
                                    </p>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-12 bg-white rounded-3xl border border-slate-100">
                            <AlertCircle size={48} className="mx-auto text-slate-300 mb-4" />
                            <h3 className="text-xl font-bold text-slate-900">Rekomendasi tidak ditemukan</h3>
                            <p className="text-slate-500">Coba cari paket lain atau sesuaikan parameter di menu Analysis.</p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
