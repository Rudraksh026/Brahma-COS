import { Badge } from "@/components/ui/badge";
import type { RiskLevel } from "@/lib/types";

const riskVariants: Record<
  RiskLevel,
  "success" | "warning" | "danger" | "secondary"
> = {
  low: "success",
  medium: "warning",
  high: "danger",
  critical: "danger"
};

export function RiskBadge({ level }: { level: RiskLevel }) {
  return (
    <Badge
      variant={riskVariants[level]}
      className={level === "critical" ? "border-red-300 bg-red-100" : ""}
    >
      {level}
    </Badge>
  );
}
