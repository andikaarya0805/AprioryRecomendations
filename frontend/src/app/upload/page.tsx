'use client';

import { useState } from 'react';
import { UploadCloud, FileSpreadsheet, CheckCircle, AlertCircle } from 'lucide-react';
import axios from 'axios';

export default function UploadPage() {
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');
    const [message, setMessage] = useState('');

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
            setStatus('idle');
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setUploading(true);
        setStatus('idle');
        const formData = new FormData();
        formData.append('file', file);

        try {
            // Assuming backend is on port 8000
            const response = await axios.post('http://localhost:8000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setStatus('success');
            setMessage(`Success! Uploaded ${response.data.rows} transactions.`);
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
                <h1 className="text-3xl font-bold text-slate-900">Upload Transactions</h1>
                <p className="text-slate-500 mt-2">Import your historical transaction data (CSV or Excel) to train the model.</p>
            </div>

            <div className="bg-white rounded-3xl p-10 shadow-sm border border-slate-100 text-center">
                <div className="border-2 border-dashed border-slate-200 rounded-2xl p-12 hover:border-blue-400 hover:bg-blue-50/30 transition-all cursor-pointer relative group">
                    <input
                        type="file"
                        accept=".csv, .xlsx, .xls"
                        onChange={handleFileChange}
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                    />
                    <div className="space-y-4">
                        <div className="w-20 h-20 bg-blue-50 text-blue-500 rounded-full flex items-center justify-center mx-auto group-hover:scale-110 transition-transform">
                            {file ? <FileSpreadsheet size={40} /> : <UploadCloud size={40} />}
                        </div>
                        {file ? (
                            <div>
                                <h3 className="text-xl font-bold text-slate-900">{file.name}</h3>
                                <p className="text-slate-500 text-sm">{(file.size / 1024).toFixed(2)} KB</p>
                            </div>
                        ) : (
                            <div>
                                <h3 className="text-xl font-bold text-slate-900">Click or Drag file here</h3>
                                <p className="text-slate-500 mt-1">Supports .csv, .xlsx</p>
                            </div>
                        )}
                    </div>
                </div>

                <div className="mt-8 flex justify-end">
                    <button
                        onClick={handleUpload}
                        disabled={!file || uploading}
                        className={`px-8 py-3 rounded-xl font-medium text-white transition-all flex items-center gap-2 ${!file || uploading ? 'bg-slate-300 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 shadow-lg shadow-blue-500/20'
                            }`}
                    >
                        {uploading ? 'Uploading...' : 'Upload Data'}
                    </button>
                </div>

                {status === 'success' && (
                    <div className="mt-6 p-4 bg-emerald-50 text-emerald-700 rounded-xl flex items-center gap-3 animate-in fade-in slide-in-from-bottom-2">
                        <CheckCircle size={20} />
                        {message}
                    </div>
                )}

                {status === 'error' && (
                    <div className="mt-6 p-4 bg-red-50 text-red-700 rounded-xl flex items-center gap-3 animate-in fade-in slide-in-from-bottom-2">
                        <AlertCircle size={20} />
                        {message}
                    </div>
                )}
            </div>
        </div>
    );
}
