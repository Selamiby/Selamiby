
import { Activity, Cpu, DollarSign, Shield, Zap } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#0a0a0b] text-white p-8 font-sans">
      <nav className="flex justify-between items-center mb-12 border-b border-white/10 pb-6">
        <div className="text-2xl font-bold bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent">
          NEXUS MASTER CORE V3
        </div>
        <div className="flex gap-4 items-center">
          <span className="text-xs bg-red-500/20 text-red-500 px-3 py-1 rounded-full border border-red-500/30">MAINNET ACTIVE</span>
          <span className="text-gray-400">Master: Selami Arzık</span>
        </div>
      </nav>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {[
          { label: "Neural Load", value: "24%", icon: Cpu, color: "text-blue-500" },
          { label: "Revenue Hunt", value: "$4,240", icon: DollarSign, color: "text-green-500" },
          { label: "Shield Status", value: "Secure", icon: Shield, color: "text-purple-500" },
          { label: "Active Nodes", value: "1,240", icon: Zap, color: "text-yellow-500" }
        ].map((stat, i) => (
          <div key={i} className="bg-[#161618] p-6 rounded-2xl border border-white/5 hover:border-white/20 transition-all cursor-pointer">
            <div className="flex justify-between items-start mb-4">
              <stat.icon className={stat.color} size={24} />
              <span className="text-xs text-gray-500">Live</span>
            </div>
            <div className="text-2xl font-bold mb-1">{stat.value}</div>
            <div className="text-sm text-gray-400">{stat.label}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-2 bg-[#161618] rounded-3xl p-8 border border-white/5">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <Activity size={20} className="text-red-500" /> Autonomous Logic Stream
          </h2>
          <div className="space-y-4 font-mono text-sm">
            <div className="text-green-500 opacity-80">[12:04:02] NEXUS-LEARNER: Injected Rust memory patterns into core.</div>
            <div className="text-blue-500 opacity-80">[12:04:15] NEXUS-PRODUCTION: Generating Next.js v14 high-density UI.</div>
            <div className="text-white opacity-40">[12:04:30] SYSTEM: Mainnet sync successful. Wallet initialized.</div>
            <div className="animate-pulse text-red-500 underline decoration-red-500/30">... NEXUS IS EVOLVING ...</div>
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-red-600/20 to-orange-600/20 rounded-3xl p-8 border border-red-500/20">
          <h3 className="text-lg font-bold mb-4">Master Console</h3>
          <p className="text-sm text-gray-300 mb-6">Nexus şu an bağımsız bir Next.js 14 uygulaması olarak kuruluyor. TypeScript ve Tailwind altyapısı hazırlandı.</p>
          <button className="w-full py-4 bg-white text-black font-bold rounded-xl hover:bg-gray-200 transition-all">TERMINAL AÇ</button>
        </div>
      </div>
    </main>
  );
}

