import React from "react";
import { className } from "../utils/format";

type Props = {
  label: string;
  value: string | number;
  title?: string;
};

export default function StatChip({ label, value, title }: Props) {
  return (
    <div
      className={className(
        "stat-chip"
      )}
      title={title}
    >
      <span className="stat-chip__label">{label}</span>
      <span className="stat-chip__value">{value}</span>
    </div>
  );
}
