import React from "react";
import type { Replay } from "../services/types";
import { formatDate, formatInt, wn8Color, resultBadgeColor, mapSlug } from "../utils/format";
import StatChip from "./StatChip";

type Props = {
  item: Replay;
  onClick?: (id: string) => void;
};

export default function ReplayCard({ item, onClick }: Props) {
  const mapImg = `/static/maps/${mapSlug(item.map_name)}.jpg`;
  const tankImg = `/static/tanks/${item.vehicle}.png`;
  const mapFallback = "/static/images/map_placeholder.jpg";
  const tankFallback = "/static/images/tank_placeholder.png";

  const [mapSrc, setMapSrc] = React.useState(mapImg);
  const [tankSrc, setTankSrc] = React.useState(tankImg);

  return (
    <article className="replay-card" onClick={() => onClick?.(item.id)}>
      <div className="replay-card__media">
        <img
          src={mapSrc}
          onError={() => setMapSrc(mapFallback)}
          alt={item.map_name}
          className="replay-card__bg"
          loading="lazy"
        />
        <div className="replay-card__overlay" />
        <div className="replay-card__topbar">
          <span className="badge" style={{ backgroundColor: resultBadgeColor(item.result) }}>
            {item.result}
          </span>
          <span className="badge badge--dark">{item.battle_type}</span>
          <span className="badge badge--dark">{item.region}{item.server ? ` • ${item.server}` : ""}</span>
          <span className="badge badge--dark">{formatDate(item.battle_time)}</span>
        </div>

        <div className="replay-card__bottom">
          <div className="replay-card__tank">
            <img
              src={tankSrc}
              onError={() => setTankSrc(tankFallback)}
              alt={item.vehicle}
              className="replay-card__tank-img"
              loading="lazy"
            />
            <div className="replay-card__tank-info">
              <div className="replay-card__vehicle">
                {item.vehicle} <span className="tier">Т{item.vehicle_tier}</span>
              </div>
              <div className="replay-card__player">
                {item.player_name} • {item.map_name}
              </div>
            </div>
          </div>

          <div className="replay-card__stats">
            <StatChip label="Урон" value={formatInt(item.damage)} />
            <StatChip label="Фраги" value={item.frags} />
            <StatChip label="Засвет" value={item.spotted} />
            <StatChip label="Блок" value={formatInt(item.blocked)} />
            <StatChip label="Опыта" value={formatInt(item.xp)} />
            <div className="stat-chip" title="WN8">
              <span className="stat-chip__label">WN8</span>
              <span className="stat-chip__value" style={{ color: wn8Color(item.wn8), fontWeight: 700 }}>
                {formatInt(Math.round(item.wn8))}
              </span>
            </div>
          </div>
        </div>
      </div>
    </article>
  );
}
