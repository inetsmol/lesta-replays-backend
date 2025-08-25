import React from "react";
import { fetchReplays } from "../services/api";
import type { Replay } from "../services/types";
import ReplayCard from "../components/ReplayCard";
import "./ReplaysPage.css";

export default function ReplaysPage() {
  const [items, setItems] = React.useState<Replay[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        setLoading(true);
        const data = await fetchReplays(24, 0, true);
        if (!cancelled) setItems(data);
      } catch (e: any) {
        if (!cancelled) setError(e?.message ?? "Ошибка загрузки");
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, []);

  return (
    <main className="replays-page">
      <header className="replays-page__header">
        <h1>Свежие реплеи</h1>
        <p className="muted">Список последних загруженных боёв (без фильтров).</p>
      </header>

      {loading && <div className="skeleton-grid">
        {Array.from({ length: 8 }).map((_, i) => <div className="skeleton-card" key={i} />)}
      </div>}

      {error && <div className="error">{error}</div>}

      {!loading && !error && (
        <section className="replays-grid">
          {items.map((it) => (
            <ReplayCard
              key={it.id}
              item={it}
              onClick={(id) => {
                // позже откроем страницу карточки боя
                // например: navigate(`/replays/${id}`)
                console.debug("Open replay", id);
              }}
            />
          ))}
          {items.length === 0 && <div className="empty">Пока нет реплеев.</div>}
        </section>
      )}
    </main>
  );
}
