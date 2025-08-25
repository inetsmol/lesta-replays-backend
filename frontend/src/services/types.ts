export interface Replay {
  id: string;
  player_name: string;
  vehicle: string;
  vehicle_tier: number;
  map_name: string;
  battle_type: string;
  battle_time: string; // ISO
  region: string;
  server: string | null;
  result: "Victory" | "Defeat" | "Draw" | "Unknown";
  damage: number;
  frags: number;
  spotted: number;
  defense_points: number;
  blocked: number;
  credits: number;
  xp: number;
  bonds: number;
  wn8: number;
}
