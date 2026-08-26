"use client";
import { LucideIcon } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
interface StatCardProps { label:string; value:string|number; detail:string; icon:LucideIcon; tone?:"neutral"|"success"|"warning"|"danger"; changed?:boolean; }
const tones={neutral:"border-border",success:"border-emerald-200 bg-emerald-50/50 dark:border-emerald-900 dark:bg-emerald-950/20",warning:"border-amber-200 bg-amber-50/60 dark:border-amber-900 dark:bg-amber-950/20",danger:"border-red-200 bg-red-50/60 dark:border-red-900 dark:bg-red-950/20"};
const iconTones={neutral:"bg-muted text-muted-foreground",success:"bg-emerald-100 text-emerald-700",warning:"bg-amber-100 text-amber-700",danger:"bg-red-100 text-red-700"};
export function StatCard({label,value,detail,icon:Icon,tone="neutral",changed=false}:StatCardProps){return <Card className={cn("relative overflow-hidden transition-all duration-500",tones[tone],changed&&"animate-value-pop ring-2 ring-primary/20 shadow-lg")}><div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-primary/40 to-transparent"/><CardContent className="flex items-start justify-between gap-4 p-5"><div><p className="text-sm font-medium text-muted-foreground">{label}</p><p className="mt-2 text-3xl font-semibold tracking-tight tabular-nums">{value}</p><p className="mt-1 text-xs text-muted-foreground">{detail}</p></div><div className={cn("rounded-xl p-2.5",iconTones[tone])}><Icon className="h-5 w-5"/></div></CardContent></Card>}
