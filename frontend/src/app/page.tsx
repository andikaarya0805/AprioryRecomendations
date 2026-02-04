import Link from "next/link";
import { ArrowRight, Database, FileSpreadsheet, Sparkles } from "lucide-react";

export default function Home() {
  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      {/* Header Section */}
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-bold text-slate-900 tracking-tight">Welcome back, Admin 👋</h1>
          <p className="text-slate-500 mt-2 text-lg">Here's what's happening with your recommendations today.</p>
        </div>
        <div className="text-sm px-4 py-2 bg-blue-50 text-blue-700 rounded-full font-medium border border-blue-100">
          System Status: Active
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 bg-white rounded-2xl shadow-sm border border-slate-100 hover:shadow-lg hover:-translate-y-1 transition-all duration-300 ease-out group cursor-pointer">
          <div className="flex justify-between items-start mb-4">
            <div className="p-3 bg-purple-50 text-purple-600 rounded-xl group-hover:bg-purple-600 group-hover:text-white transition-colors">
              <FileSpreadsheet size={24} />
            </div>
            <span className="text-xs font-semibold text-slate-400 bg-slate-50 px-2 py-1 rounded-lg">Last 24h</span>
          </div>
          <h3 className="text-3xl font-bold text-slate-900">1,204</h3>
          <p className="text-slate-500 font-medium">Transactions Analyzed</p>
        </div>

        <div className="p-6 bg-white rounded-2xl shadow-sm border border-slate-100 hover:shadow-lg hover:-translate-y-1 transition-all duration-300 ease-out group cursor-pointer">
          <div className="flex justify-between items-start mb-4">
            <div className="p-3 bg-blue-50 text-blue-600 rounded-xl group-hover:bg-blue-600 group-hover:text-white transition-colors">
              <Sparkles size={24} />
            </div>
          </div>
          <h3 className="text-3xl font-bold text-slate-900">85</h3>
          <p className="text-slate-500 font-medium">Active Rules</p>
        </div>

        <div className="p-6 bg-white rounded-2xl shadow-sm border border-slate-100 hover:shadow-lg hover:-translate-y-1 transition-all duration-300 ease-out group cursor-pointer">
          <div className="flex justify-between items-start mb-4">
            <div className="p-3 bg-emerald-50 text-emerald-600 rounded-xl group-hover:bg-emerald-600 group-hover:text-white transition-colors">
              <Database size={24} />
            </div>
          </div>
          <h3 className="text-3xl font-bold text-slate-900">12</h3>
          <p className="text-slate-500 font-medium">Service Categories</p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white/80 backdrop-blur-md border border-slate-200/50 shadow-sm p-8 rounded-3xl relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:scale-110 transition-transform duration-500">
            <FileSpreadsheet size={120} />
          </div>
          <h2 className="text-2xl font-bold text-slate-900 mb-2 relative z-10">Upload New Data</h2>
          <p className="text-slate-500 mb-6 max-w-md relative z-10">Import latest transaction data from CSV or Excel to update the recommendation engine.</p>
          <Link href="/upload">
            <button className="flex items-center gap-2 px-6 py-3 bg-slate-900 text-white rounded-xl font-medium hover:bg-slate-800 transition-colors relative z-10">
              Go to Upload <ArrowRight size={18} />
            </button>
          </Link>
        </div>

        <div className="bg-white/80 backdrop-blur-md border border-slate-200/50 shadow-sm p-8 rounded-3xl relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:scale-110 transition-transform duration-500">
            <Sparkles size={120} />
          </div>
          <h2 className="text-2xl font-bold text-slate-900 mb-2 relative z-10">Run Analysis</h2>
          <p className="text-slate-500 mb-6 max-w-md relative z-10">Generate new association rules (Apriori) based on current data parameters (Support/Confidence).</p>
          <Link href="/analysis">
            <button className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 transition-colors relative z-10">
              Start Mining <ArrowRight size={18} />
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}
