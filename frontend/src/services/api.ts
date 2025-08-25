import type { Replay } from "./types";

const API_BASE = import.meta?.env?.VITE_API_BASE ?? "http://127.0.0.1:8000/api/v1";

export async function fetchReplays(limit = 24, offset = 0, publicOnly = true): Promise<Replay[]> {
  const url = new URL(`${API_BASE}/replays`);
  url.searchParams.set("limit", String(limit));
  url.searchParams.set("offset", String(offset));
  url.searchParams.set("public_only", String(publicOnly));
  const res = await fetch(url.toString());
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to fetch replays: ${res.status} ${text}`);
  }
  return res.json();
}
