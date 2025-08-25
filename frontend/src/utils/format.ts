export function formatInt(n: number): string {
  // 12 345 — тонкий пробел между тысячами
  return n.toLocaleString("ru-RU").replace(/\s/g, "\u202F");
}

export function formatDate(iso: string): string {
  const d = new Date(iso);
  // 24 авг 2025, 13:42
  return d.toLocaleString("ru-RU", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function wn8Color(value: number): string {
  // приблизительная палитра XVM
  if (value >= 3200) return "#8A2BE2"; // Super Unicum
  if (value >= 2450) return "#5B9BD5"; // Unicum
  if (value >= 1850) return "#66CC66"; // Very Good
  if (value >= 1450) return "#A0CF64"; // Good
  if (value >= 900)  return "#FFD966"; // Average
  if (value >= 650)  return "#F4B183"; // Below Avg
  if (value >= 450)  return "#E06666"; // Bad
  return "#C00000";                    // Very Bad
}

export function resultBadgeColor(result: string): string {
  switch (result) {
    case "Victory": return "#2e7d32";
    case "Defeat":  return "#c62828";
    case "Draw":    return "#6b7280";
    default:        return "#374151";
  }
}

export function className(...parts: Array<string | false | undefined | null>) {
  return parts.filter(Boolean).join(" ");
}

export function mapSlug(name: string): string {
  return name.toLowerCase()
    .replace(/[^a-zа-я0-9\s_-]/gi, "")
    .trim()
    .replace(/\s+/g, "_");
}
