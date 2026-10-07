"use client";

import { useEffect, useState } from "react";
import { Shell, Pill } from "./ui";
import { getCareers, getMarket, getOpportunities, type Career, type Opportunity } from "../lib/api";

type ViewProps = { title: string; description: string; eyebrow?: string };

export function CompatibilityView({ title, description, eyebrow = "PRISM" }: ViewProps) {
  const [careers, setCareers] = useState<Career[]>([]);
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [market, setMarket] = useState<any>();
  useEffect(() => {
    getCareers().then(setCareers);
    getOpportunities().then(setOpportunities);
    getMarket().then(setMarket);
  }, []);
  return <Shell>
    <Pill>{eyebrow}</Pill>
    <h1 className="mt-4 text-4xl font-black">{title}</h1>
    <p className="mt-2 text-slate-500">{description}</p>
    <div className="mt-8 grid gap-5 md:grid-cols-3">
      {careers.slice(0, 3).map((career) => <section key={career.id} className="rounded-3xl bg-white p-6 shadow-soft">
        <Pill>{career.fit}% fit</Pill>
        <h2 className="mt-4 text-xl font-black">{career.title}</h2>
        <p className="mt-1 text-sm text-slate-500">{career.category}</p>
        <p className="mt-4 text-sm leading-6 text-slate-600">{career.why}</p>
      </section>)}
    </div>
    {market && <section className="mt-8 rounded-3xl bg-ink p-6 text-white">
      <p className="text-xs font-black uppercase tracking-widest text-mint">Current signals</p>
      <div className="mt-4 grid gap-3 sm:grid-cols-3">{market.sectors.map((sector: { name: string; growth: number; signal: string }) =>
        <div key={sector.name} className="rounded-2xl bg-white/10 p-4"><p className="font-bold">{sector.name}</p><p className="mt-2 text-2xl font-black">+{sector.growth}%</p><p className="mt-1 text-xs text-slate-300">{sector.signal}</p></div>
      )}</div>
    </section>}
    {opportunities.length > 0 && <section className="mt-8 rounded-3xl bg-white p-6 shadow-soft">
      <h2 className="text-2xl font-black">Next experiments</h2>
      <div className="mt-4 grid gap-3 md:grid-cols-3">{opportunities.slice(0, 3).map((opportunity) =>
        <div key={opportunity.id} className="rounded-2xl border border-black/5 p-4"><Pill tone="coral">{opportunity.type}</Pill><h3 className="mt-3 font-black">{opportunity.title}</h3><p className="mt-1 text-sm text-slate-500">{opportunity.org} · {opportunity.deadline}</p></div>
      )}</div>
    </section>}
  </Shell>;
}

export function TrackerView() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [tracked, setTracked] = useState<string[]>([]);
  useEffect(() => { getOpportunities().then(setOpportunities); }, []);
  return <Shell><Pill>OPPORTUNITY TRACKER</Pill><h1 className="mt-4 text-4xl font-black">Keep momentum visible.</h1><p className="mt-2 text-slate-500">Save a few low-risk experiments and choose one next step.</p>
    <div className="mt-8 grid gap-3 md:grid-cols-2">{opportunities.map((opportunity) => {
      const isTracked = tracked.includes(opportunity.id);
      return <button key={opportunity.id} onClick={() => setTracked((items) => isTracked ? items.filter((id) => id !== opportunity.id) : [...items, opportunity.id])} className={`rounded-3xl p-5 text-left shadow-soft ${isTracked ? "bg-mint" : "bg-white"}`}>
        <div className="flex items-center justify-between"><Pill tone={isTracked ? "dark" : "coral"}>{isTracked ? "TRACKING" : opportunity.type}</Pill><span className="text-xs font-bold text-slate-400">{opportunity.deadline}</span></div>
        <h2 className="mt-4 font-black">{opportunity.title}</h2><p className="mt-1 text-sm text-slate-500">{opportunity.org} · {opportunity.location}</p>
      </button>;
    })}</div>
  </Shell>;
}
