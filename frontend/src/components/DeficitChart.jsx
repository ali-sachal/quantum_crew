import React from 'react';

export default function DeficitChart({ data = [], selectedZip = '10451' }) {
  const maxScore = Math.max(...data.map(d => d.score), 10);
  const peakDay = data.reduce((prev, curr) => (curr.score > (prev?.score || 0) ? curr : prev), null);

  return (
    <div className="bg-white p-6 rounded-3xl border border-stone-200/90 shadow-sm">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 mb-6">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-base font-bold text-stone-900">Neighborhood Fresh Produce Deficit</h3>
            <span className="text-[10px] font-mono uppercase bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full border border-blue-200 font-bold">
              Snowflake CoCo
            </span>
          </div>
          <p className="text-xs text-stone-500 mt-0.5">
            Predictive deficit score for ZIP <span className="font-mono font-semibold text-stone-700">{selectedZip}</span> based on consumer spending & census data
          </p>
        </div>

        {peakDay && (
          <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-amber-50 border border-amber-200 rounded-xl text-xs font-bold text-amber-900">
            <span className="text-amber-600">⚡</span>
            <span>Peak Deficit: {peakDay.day} ({peakDay.score.toFixed(1)}/10)</span>
          </div>
        )}
      </div>

      <div className="flex items-end justify-between h-48 pt-8 gap-2 sm:gap-4 px-2">
        {data.map((item) => {
          const heightPct = Math.max((item.score / maxScore) * 100, 12);
          const isPeak = peakDay && item.day === peakDay.day;

          return (
            <div key={item.day} className="flex-1 flex flex-col items-center gap-2 h-full justify-end group">
              <span className={`text-xs font-bold transition-all duration-200 ${
                isPeak ? 'text-amber-700 font-black scale-110' : 'text-stone-500 group-hover:text-stone-800'
              }`}>
                {item.score.toFixed(1)}
              </span>

              <div className="w-full max-w-[48px] bg-stone-100 rounded-t-xl h-full flex items-end overflow-hidden p-0.5">
                <div
                  className={`w-full rounded-t-lg transition-all duration-700 ease-out ${
                    isPeak
                      ? 'bg-gradient-to-t from-amber-500 to-amber-400 shadow-sm shadow-amber-500/40'
                      : 'bg-gradient-to-t from-brand-600 to-brand-500 group-hover:from-brand-700 group-hover:to-brand-600'
                  }`}
                  style={{ height: `${heightPct}%` }}
                />
              </div>

              <span className={`text-xs font-semibold truncate ${
                isPeak ? 'text-amber-900 font-bold' : 'text-stone-600'
              }`}>
                {item.day.slice(0, 3)}
              </span>
            </div>
          );
        })}
      </div>

      <div className="mt-4 pt-3 border-t border-stone-100 flex items-center justify-between text-[11px] text-stone-500">
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded bg-brand-500 inline-block"></span> Standard Deficit
          <span className="w-2.5 h-2.5 rounded bg-amber-500 inline-block ml-3"></span> Critical Restock Window
        </span>
        <span>High deficit = maximum unmet customer demand for fresh food</span>
      </div>
    </div>
  );
}

