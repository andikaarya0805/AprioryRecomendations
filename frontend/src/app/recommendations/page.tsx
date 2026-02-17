'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, Sparkles, AlertCircle, ArrowUpLeft } from 'lucide-react';

interface Recommendation {
    item: string;
    confidence: string;
}

export default function RecommendationsPage() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<Recommendation[]>([]);
    const [items, setItems] = useState<string[]>([]);
    const [filteredItems, setFilteredItems] = useState<string[]>([]);
    const [showDropdown, setShowDropdown] = useState(false);
    const [loading, setLoading] = useState(false);
    const [searched, setSearched] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const backendUrl = typeof window !== 'undefined'
                    ? `http://${window.location.hostname}:8000`
                    : 'http://localhost:8000';

                const [statusRes, itemsRes] = await Promise.all([
                    axios.get(`${backendUrl}/status`),
                    axios.get(`${backendUrl}/items`)
                ]);

                setDataStatus(statusRes.data);
                setItems(itemsRes.data.items || []);
            } catch (err) {
                console.error("Failed to fetch data", err);
            }
        };
        fetchData();
    }, []);

    const [selectedDetails, setSelectedDetails] = useState<any>(null);

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!query.trim()) return;

        setLoading(true);
        setSearched(true);
        setShowDropdown(false);
        setSelectedDetails(null); // Reset details

        try {
            const backendUrl = typeof window !== 'undefined'
                ? `http://${window.location.hostname}:8000/recommendations?service=${encodeURIComponent(query)}`
                : `http://localhost:8000/recommendations?service=${encodeURIComponent(query)}`;

            const response = await axios.get(backendUrl);
            setResults(response.data.recommendations || []);
            if (response.data.service_details) {
                setSelectedDetails(response.data.service_details);
            }
        } catch (error) {
            console.error(error);
            setError('Gagal mengambil rekomendasi. Pastikan backend berjalan.');
        } finally {
            setLoading(false);
        }
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const val = e.target.value;
        setQuery(val);
        setError('');

        if (val.trim()) {
            const filtered = items.filter(item =>
                item.toLowerCase().includes(val.toLowerCase())
            );
            setFilteredItems(filtered);
            setShowDropdown(true);
        } else {
            setShowDropdown(false);
        }
    };

    const selectItem = (item: string) => {
        setQuery(item);
        setShowDropdown(false);
        // Optional: Auto-search when item is selected
        // handleSearch({ preventDefault: () => {} } as any); 
    };

    const [error, setError] = useState('');
    const [dataStatus, setDataStatus] = useState<{ rules_count: number } | null>(null);

    // Helper to format currency
    const formatPrice = (price: string) => {
        if (!price) return '';
        const num = parseFloat(price.replace(/[^0-9.-]+/g, ""));
        if (isNaN(num)) return price;
        return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(num);
    };

    return (
        <div className="max-w-6xl mx-auto p-8 relative min-h-screen" onClick={() => setShowDropdown(false)}>
            <div className="text-center mb-12">
                <h1 className="text-4xl font-bold text-slate-900 tracking-tight mb-4">Sistem Rekomendasi Paket</h1>
                <p className="text-slate-500 text-lg">Cari paket utama untuk melihat pasangan paket yang paling sering dipesan.</p>
            </div>

            {dataStatus && dataStatus.rules_count === 0 && (
                <div className="max-w-xl mx-auto mb-8 p-4 bg-amber-50 border border-amber-200 rounded-xl flex items-start gap-3 text-amber-800 animate-in fade-in slide-in-from-top-4">
                    <AlertCircle className="shrink-0 mt-0.5" />
                    <div>
                        <h3 className="font-semibold">Belum Ada Data Analisis</h3>
                        <p className="text-sm mt-1 opacity-90">
                            Sistem belum memiliki pola rekomendasi. Silakan pergi ke menu <a href="/analysis" className="underline font-medium hover:text-amber-900">Analysis</a> dan jalankan "Start Mining" terlebih dahulu.
                        </p>
                    </div>
                </div>
            )}

            <div className={`max-w-xl mx-auto mb-12 relative z-10 transition-opacity duration-300 ${dataStatus?.rules_count === 0 ? 'opacity-50 pointer-events-none grayscale' : ''}`}>
                <form onSubmit={handleSearch} className="relative" onClick={(e) => e.stopPropagation()}>
                    <input
                        type="text"
                        placeholder="Contoh: Engagement Platinum, Wedding Gold..."
                        value={query}
                        onChange={handleInputChange}
                        onFocus={() => {
                            if (query.trim()) setShowDropdown(true);
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

                    {/* Autocomplete Dropdown */}
                    {showDropdown && filteredItems.length > 0 && (
                        <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-2xl shadow-xl border border-slate-100 max-h-[300px] overflow-y-auto z-50 animate-in fade-in slide-in-from-top-2">
                            {filteredItems.map((item, idx) => (
                                <button
                                    key={idx}
                                    type="button"
                                    onClick={() => selectItem(item)}
                                    className="w-full text-left px-6 py-3 hover:bg-slate-50 transition-colors text-slate-700 font-medium flex items-center justify-between group"
                                >
                                    <span>{item}</span>
                                    <ArrowUpLeft size={16} className="text-slate-300 group-hover:text-blue-500 transition-colors" />
                                </button>
                            ))}
                        </div>
                    )}
                </form>
                {error && <p className="text-center text-red-500 mt-4 text-sm">{error}</p>}
            </div>

            {searched && (
                <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 space-y-8">

                    {/* Selected Package Details */}
                    {selectedDetails && (
                        <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm flex flex-col md:flex-row gap-8 items-center md:items-start">
                            <div className="w-full md:w-1/3 aspect-video bg-slate-100 rounded-2xl overflow-hidden relative">
                                {selectedDetails.image ? (
                                    <img src={selectedDetails.image} alt={selectedDetails.name} className="w-full h-full object-cover" />
                                ) : (
                                    <div className="w-full h-full flex items-center justify-center text-slate-300">
                                        <Sparkles size={48} />
                                    </div>
                                )}
                            </div>
                            <div className="flex-1 text-center md:text-left">
                                <span className="bg-blue-50 text-blue-600 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider mb-2 inline-block">Paket Terpilih</span>
                                <h2 className="text-3xl font-bold text-slate-900 mb-2">{selectedDetails.name}</h2>
                                <h3 className="text-xl font-semibold text-slate-700 mb-4">{formatPrice(selectedDetails.price)}</h3>
                                <p className="text-slate-500 leading-relaxed">{selectedDetails.description || "Tidak ada deskripsi tersedia."}</p>
                            </div>
                        </div>
                    )}

                    {results.length > 0 ? (
                        <>
                            <h3 className="text-2xl font-bold text-slate-900 mb-6">Rekomendasi Paket Pendukung</h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                {results.map((rec: any, idx) => (
                                    <div key={idx} className="bg-white border border-slate-100 shadow-sm hover:shadow-md transition-shadow p-6 rounded-2xl relative overflow-hidden flex flex-col h-full group">

                                        {/* Image Section */}
                                        <div className="w-full h-40 bg-slate-50 rounded-xl mb-4 overflow-hidden relative">
                                            {rec.details?.image ? (
                                                <img src={rec.details.image} alt={rec.item} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                                            ) : (
                                                <div className="w-full h-full flex items-center justify-center text-slate-300">
                                                    <Sparkles size={32} />
                                                </div>
                                            )}
                                            <div className="absolute top-2 right-2 bg-emerald-500 text-white text-xs font-bold px-2 py-1 rounded-lg shadow-sm">
                                                {rec.confidence} Cocok
                                            </div>
                                        </div>

                                        <div className="flex-1">
                                            <h4 className="text-lg font-bold text-slate-900 mb-1 leading-tight">{rec.details?.name || rec.item}</h4>
                                            {rec.details?.price && (
                                                <p className="text-emerald-600 font-semibold text-sm mb-2">{formatPrice(rec.details.price)}</p>
                                            )}
                                            <p className="text-slate-500 text-sm line-clamp-2">
                                                {rec.details?.description || `Paket ini sering diambil bersamaan dengan "${query}".`}
                                            </p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </>
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
