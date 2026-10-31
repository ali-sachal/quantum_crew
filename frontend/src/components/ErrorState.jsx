import React from 'react';

export default function ErrorState({ error = 'Something went wrong', onRetry }) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-2xl p-6 text-center max-w-lg mx-auto space-y-3">
      <div className="text-3xl text-red-500">⚠️</div>
      <h3 className="text-sm font-bold text-red-900">An Error Occurred</h3>
      <p className="text-xs text-red-700 font-mono bg-white/60 p-2 rounded-lg border border-red-100">{error}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-xs font-bold rounded-xl shadow-sm transition"
        >
          Try Again
        </button>
      )}
    </div>
  );
}

