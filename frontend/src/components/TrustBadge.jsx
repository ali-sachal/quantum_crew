import React from 'react';

export default function TrustBadge({ solanaAddress, txSignature, reputation = 4.8, compact = false }) {
  const shortAddress = solanaAddress
    ? `${solanaAddress.slice(0, 4)}...${solanaAddress.slice(-4)}`
    : 'Solana Devnet';

  const shortTx = txSignature
    ? `${txSignature.slice(0, 6)}...${txSignature.slice(-4)}`
    : null;

  const explorerUrl = txSignature
    ? `https://explorer.solana.com/tx/${txSignature}?cluster=devnet`
    : (solanaAddress ? `https://explorer.solana.com/address/${solanaAddress}?cluster=devnet` : null);

  if (compact) {
    return (
      <div className="inline-flex items-center gap-1.5 bg-brand-50 border border-brand-200 px-2 py-0.5 rounded-full text-[11px] text-brand-800">
        <span className="w-1.5 h-1.5 rounded-full bg-brand-600 animate-pulse"></span>
        <span className="font-semibold">Solana Verified</span>
        <span className="font-bold text-stone-700">★{reputation}</span>
      </div>
    );
  }

  return (
    <div className="inline-flex flex-wrap items-center gap-2 bg-brand-50/80 border border-brand-200/90 px-3 py-1.5 rounded-2xl text-xs text-brand-900 shadow-sm">
      <span className="flex h-2 w-2 relative">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-400 opacity-75"></span>
        <span className="relative inline-flex rounded-full h-2 w-2 bg-brand-600"></span>
      </span>

      <span className="font-bold tracking-tight">Verified on Solana</span>
      <span className="text-stone-300">|</span>

      <span className="font-mono text-stone-600 bg-white/80 px-1.5 py-0.5 rounded border border-brand-100" title={solanaAddress}>
        {shortAddress}
      </span>

      <span className="font-black text-amber-700 bg-amber-50 border border-amber-200 px-1.5 py-0.5 rounded flex items-center gap-0.5">
        ★ {reputation}
      </span>

      {explorerUrl && (
        <>
          <span className="text-stone-300">|</span>
          <a
            href={explorerUrl}
            target="_blank"
            rel="noreferrer"
            className="font-medium text-brand-700 hover:text-brand-900 hover:underline flex items-center gap-1 font-mono"
            title="Inspect on official Solana Devnet Explorer"
          >
            <span>{shortTx || 'Explorer'}</span>
            <span className="text-[10px]">↗</span>
          </a>
        </>
      )}
    </div>
  );
}
