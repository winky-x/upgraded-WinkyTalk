// File: app/search/page.tsx
import SuperSearchDashboard from '@/components/SuperSearchDashboard';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';

export default function SearchPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <header className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between px-4">
          <Link 
            href="/" 
            className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-100"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Assistant
          </Link>
          
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
              <span className="text-sm font-medium">AI Search Active</span>
            </div>
          </div>
        </div>
      </header>
      
      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold gradient-text mb-2">
            🚀 Winky Super Search
          </h1>
          <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Advanced AI-powered web navigation system. Tell Winky what to find, and watch it browse, analyze, and deliver results.
          </p>
        </div>
        
        {/* Dashboard */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
          <SuperSearchDashboard />
        </div>
        
        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          <div className="p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
            <div className="text-2xl mb-2">🌐</div>
            <h3 className="font-bold mb-2">Multi-Platform Search</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Searches Google, Facebook Marketplace, Amazon, and more simultaneously
            </p>
          </div>
          
          <div className="p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
            <div className="text-2xl mb-2">🤖</div>
            <h3 className="font-bold mb-2">AI Analysis</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Analyzes results with GPT-4, provides recommendations and insights
            </p>
          </div>
          
          <div className="p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
            <div className="text-2xl mb-2">⚡</div>
            <h3 className="font-bold mb-2">Real-Time Updates</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Watch Winky navigate websites live with real-time progress updates
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}