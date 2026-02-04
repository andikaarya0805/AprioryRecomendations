'use client';

import { useState } from 'react';
import axios from 'axios';
import { Play, Settings2, ArrowRight, Loader2 } from 'lucide-react';

export default function AnalysisPage() {
    const [minSupport, setMinSupport] = useState(0.1);
    const [minConfidence, setMinConfidence] = useState(0.5);
    const [loading, setLoading] = useState(false);
    const [rules, setRules] = useState<any[]>([]);
    const [error, setError] = useState('');

    const runAnalysis = async () => {
        setLoading(true);
        setError('');
        setRules([]);
        try {
            const response = await axios.post('http://localhost:8000/analyze', {
                min_support: minSupport,
                min_confidence: minConfidence
            });
            setRules(response.data.rules || []);
        } catch (err) {
            setError('Analysis failed. Make sure you have uploaded data.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-6xl mx-auto p-8">
            <div className="flex justify-between items-start mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900">Analysis Process</h1>
                    <p className="text-slate-500 mt-2">Configure Apriori parameters to discover association rules.</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Controls Panel */}
                <div className="lg:col-span-1 space-y-6">
                    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
                        <div className="flex items-center gap-2 mb-6 text-slate-900 font-semibold">
                            <Settings2 size={20} className="text-blue-600" />
                            Parameters
                        </div>

                        <div className="space-y-6">
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-2">
                                    Min. Support ({minSupport})
                                </label>
                                <input
                                    type="range"
                                    min="0.01" max="1.0" step="0.01"
                                    value={minSupport}
                                    onChange={(e) => setMinSupport(parseFloat(e.target.value))}
                                    className="w-full accent-blue-600"
                                />
                                <p className="text-xs text-slate-400 mt-1">Minimum frequency of item occurrence.</p>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-2">
                                    Min. Confidence ({minConfidence})
                                </label>
                                <input
                                    type="range"
                                    min="0.01" max="1.0" step="0.01"
                                    value={minConfidence}
                                    onChange={(e) => setMinConfidence(parseFloat(e.target.value))}
                                    className="w-full accent-blue-600"
                                />
                                <p className="text-xs text-slate-400 mt-1">Likelihood of consequent given antecedent.</p>
                            </div>

                            <button
                                onClick={runAnalysis}
                                disabled={loading}
                                className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-medium flex items-center justify-center gap-2 transition-all shadow-lg shadow-blue-500/20 disabled:opacity-50"
                            >
                                {loading ? <Loader2 className="animate-spin" /> : <Play size={18} fill="currentColor" />}
                                {loading ? 'Processing...' : 'Start Mining'}
                            </button>
                            {error && <p className="text-sm text-red-500 text-center">{error}</p>}
                        </div>
                    </div>
                </div>

                {/* Results Panel */}
                <div className="lg:col-span-2">
                    {rules.length > 0 ? (
                        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 animate-in fade-in slide-in-from-bottom-4">
                            <h2 className="text-xl font-bold text-slate-900 mb-4">Generated Rules ({rules.length})</h2>
                            <div className="overflow-x-auto">
                                <table className="w-full text-sm text-left">
                                    <thead className="text-xs text-slate-500 uppercase bg-slate-50">
                                        <tr>
                                            <th className="px-4 py-3 rounded-l-lg">If (Antecedent)</th>
                                            <th className="px-4 py-3">Then (Consequent)</th>
                                            <th className="px-4 py-3">Confidence</th>
                                            <th className="px-4 py-3 rounded-r-lg">Lift</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-slate-100">
                                        {rules.map((rule, idx) => (
                                            <tr key={idx} className="hover:bg-slate-50/50 transition-colors">
                                                <td className="px-4 py-3 font-medium text-slate-800">
                                                    {rule.antecedents.join(', ')}
                                                </td>
                                                <td className="px-4 py-3 text-blue-600 font-medium">
                                                    <div className="flex items-center gap-2">
                                                        <ArrowRight size={14} className="text-slate-300" />
                                                        {rule.consequents.join(', ')}
                                                    </div>
                                                </td>
                                                <td className="px-4 py-3">
                                                    {(rule.confidence * 100).toFixed(1)}%
                                                </td>
                                                <td className="px-4 py-3">
                                                    {rule.lift.toFixed(2)}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    ) : (
                        <div className="h-full min-h-[400px] flex flex-col items-center justify-center text-slate-400 border-2 border-dashed border-slate-200 rounded-2xl">
                            <Settings2 size={48} className="mb-4 opacity-20" />
                            <p>Parameters ready. Start mining to see results.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
