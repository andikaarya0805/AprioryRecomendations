'use client';

import { useState } from 'react';
import { UploadCloud, FileSpreadsheet, CheckCircle, AlertCircle } from 'lucide-react';
import axios from 'axios';

export default function UploadPage() {
    const [uploading, setUploading] = useState(false);
    const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');
    const [message, setMessage] = useState('');
    const [activeType, setActiveType] = useState<'transaction' | 'catalog' | null>(null);

    const handleUpload = async (file: File, type: 'transaction' | 'catalog') => {
        setUploading(true);
        setStatus('idle');
        setActiveType(type);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const backendUrl = typeof window !== 'undefined'
                ? `http://${window.location.hostname}:8000`
                : 'http://localhost:8000';

            const endpoint = type === 'catalog' ? '/upload-catalog' : '/upload';

            const response = await axios.post(`${backendUrl}${endpoint}`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setStatus('success');
            setMessage(response.data.message);
        } catch (error) {
            console.error(error);
            setStatus('error');
            setMessage('Failed to upload file. Ensure backend is running.');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto p-8">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-slate-900">Upload Data</h1>
                <p className="text-slate-500 mt-2">Manage your data sources for analysis and recommendations.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Transaction Data Upload */}
                <div className="bg-white rounded-3xl p-8 shadow-sm border border-slate-100 text-center flex flex-col">
                    <div className="mb-6">
                        <h2 className="text-xl font-bold text-slate-900">1. Transaction History</h2>
                        <p className="text-slate-400 text-sm mt-1">Upload client order history for Analysis.</p>
                    </div>

                    <div className="border-2 border-dashed border-slate-200 rounded-2xl p-8 hover:border-blue-400 hover:bg-blue-50/30 transition-all cursor-pointer relative group flex-1 flex flex-col items-center justify-center">
                        <input
                            type="file"
                            accept=".csv, .xlsx, .xls"
                            onChange={(e) => {
                                if (e.target.files?.[0]) {
                                    handleUpload(e.target.files[0], 'transaction');
                                }
                            }}
                            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                        />
                        <div className="space-y-4 pointer-events-none">
                            <div className="w-16 h-16 bg-blue-50 text-blue-500 rounded-full flex items-center justify-center mx-auto group-hover:scale-110 transition-transform">
                                {uploading && activeType === 'transaction' ? <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div> : <UploadCloud size={32} />}
                            </div>
                            <div>
                                <h3 className="font-bold text-slate-700">Upload Transactions</h3>
                                <p className="text-slate-400 text-xs mt-1">Supports .csv, .xlsx</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Product Catalog Upload */}
                <div className="bg-white rounded-3xl p-8 shadow-sm border border-slate-100 text-center flex flex-col">
                    <div className="mb-6">
                        <h2 className="text-xl font-bold text-slate-900">2. Product Catalog</h2>
                        <p className="text-slate-400 text-sm mt-1">Upload package details (Price, Image, etc).</p>
                    </div>

                    <div className="border-2 border-dashed border-slate-200 rounded-2xl p-8 hover:border-emerald-400 hover:bg-emerald-50/30 transition-all cursor-pointer relative group flex-1 flex flex-col items-center justify-center">
                        <input
                            type="file"
                            accept=".xlsx, .xls, .sql"
                            onChange={(e) => {
                                if (e.target.files?.[0]) {
                                    handleUpload(e.target.files[0], 'catalog');
                                }
                            }}
                            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                        />
                        <div className="space-y-4 pointer-events-none">
                            <div className="w-16 h-16 bg-emerald-50 text-emerald-500 rounded-full flex items-center justify-center mx-auto group-hover:scale-110 transition-transform">
                                {uploading && activeType === 'catalog' ? <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500"></div> : <FileSpreadsheet size={32} />}
                            </div>
                            <div>
                                <h3 className="font-bold text-slate-700">Upload Catalog</h3>
                                <p className="text-slate-400 text-xs mt-1">Supports .xlsx, .sql</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Status Messages for Transaction Upload */}
            {activeType === 'transaction' && (
                <>
                    {status === 'success' && (
                        <div className="mt-6 p-4 bg-blue-50 text-blue-700 rounded-xl flex items-center gap-3 animate-in fade-in slide-in-from-bottom-2 border border-blue-100">
                            <CheckCircle size={20} />
                            <div>
                                <p className="font-medium">Transaction Data Uploaded!</p>
                                <p className="text-sm opacity-80">{message}</p>
                            </div>
                        </div>
                    )}
                    {status === 'error' && (
                        <div className="mt-6 p-4 bg-red-50 text-red-700 rounded-xl flex items-center gap-3 animate-in fade-in slide-in-from-bottom-2 border border-red-100">
                            <AlertCircle size={20} />
                            <div>
                                <p className="font-medium">Upload Failed</p>
                                <p className="text-sm opacity-80">{message}</p>
                            </div>
                        </div>
                    )}
                </>
            )}

            {/* Status Messages for Catalog Upload */}
            {activeType === 'catalog' && (
                <>
                    {status === 'success' && (
                        <div className="mt-6 p-4 bg-emerald-50 text-emerald-700 rounded-xl flex items-center gap-3 animate-in fade-in slide-in-from-bottom-2 border border-emerald-100">
                            <CheckCircle size={20} />
                            <div>
                                <p className="font-medium">Product Catalog Uploaded!</p>
                                <p className="text-sm opacity-80">{message}</p>
                            </div>
                        </div>
                    )}
                    {status === 'error' && (
                        <div className="mt-6 p-4 bg-red-50 text-red-700 rounded-xl flex items-center gap-3 animate-in fade-in slide-in-from-bottom-2 border border-red-100">
                            <AlertCircle size={20} />
                            <div>
                                <p className="font-medium">Catalog Upload Failed</p>
                                <p className="text-sm opacity-80">{message}</p>
                            </div>
                        </div>
                    )}
                </>
            )}

        </div>
    );
}
