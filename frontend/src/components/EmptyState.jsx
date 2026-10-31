import React from 'react';

export default function EmptyState({ icon = '🌱', title = 'No data available', description = 'Try adjusting your filters or check back later.' }) {
  return (
    <div className="bg-white rounded-3xl border border-dashed border-stone-300 p-12 text-center max-w-md mx-auto space-y-3">
      <div className="text-4xl">{icon}</div>
      <h3 className="text-base font-bold text-stone-800">{title}</h3>
      <p className="text-xs text-stone-500 leading-relaxed">{description}</p>
    </div>
  );
}
