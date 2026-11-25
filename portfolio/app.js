/**
 * Aryan Arora (FROSTY-MUG) Portfolio Application
 * Loads dynamic telemetry from data/github-data.json with offline fallback.
 */

document.addEventListener('DOMContentLoaded', () => {
  loadTelemetry();
});

const FALLBACK_TELEMETRY = {
  metadata: {
    public_repos_count: 9,
    total_stars: 5,
    harvested_at: new Date().toISOString(),
    location: "Uttarakhand, India"
  },
  languages: [
    { language: "TypeScript", percentage: 46.2 },
    { language: "Python", percentage: 21.8 },
    { language: "C++", percentage: 13.5 },
    { language: "Rust", percentage: 9.1 },
    { language: "JavaScript", percentage: 6.8 },
    { language: "Swift", percentage: 1.8 }
  ],
  pinned_repositories: [
    { name: "Ghost-Tag", pushed_at: "2026-11-25T10:07:54Z", stars: 4, description: "Zero-knowledge, offline-first encrypted vaults for NFC tags — AES-256-GCM, Argon2id." },
    { name: "Genome_Firewall", pushed_at: "2026-11-22T19:00:00Z", stars: 1, description: "High-throughput C++ antimicrobial-resistance screening and decision-support engine." },
    { name: "CareSentry", pushed_at: "2026-10-10T10:04:48Z", stars: 0, description: "Deterministic attention-anchored context sentry and defense guard for medical models." },
    { name: "FPA", pushed_at: "2026-04-08T11:49:52Z", stars: 0, description: "Financial Planning & Analysis Studio: real-time forecasting dashboard powered by Groq." }
  ]
};

async function loadTelemetry() {
  const statsEl = document.getElementById('telemetry-stats');
  const langsEl = document.getElementById('telemetry-languages');
  const footerUpdatedEl = document.getElementById('footer-updated');

  let data = FALLBACK_TELEMETRY;

  try {
    const res = await fetch('data/github-data.json');
    if (res.ok) {
      data = await res.json();
    }
  } catch (err) {
    console.info('Using pre-bundled telemetry snapshot:', err);
  }

  // Render Stats for the 4 Pinned Repositories
  if (statsEl) {
    const meta = data.metadata || {};
    const repos = (data.pinned_repositories && data.pinned_repositories.length > 0) 
      ? data.pinned_repositories 
      : FALLBACK_TELEMETRY.pinned_repositories;
    
    let recentRows = repos.map(r => `
      <tr>
        <td><code>${r.name}</code></td>
        <td>${r.stars || 0} ⭐</td>
        <td><code>${(r.pushed_at || '').substring(0, 10)}</code></td>
      </tr>
    `).join('');

    statsEl.innerHTML = `
      <table class="telemetry-table">
        <thead>
          <tr>
            <th>Pinned System</th>
            <th>Stars</th>
            <th>Last Push</th>
          </tr>
        </thead>
        <tbody>
          ${recentRows}
        </tbody>
      </table>
      <div style="margin-top: 16px; font-size: 0.82rem; color: var(--text-muted); font-family: var(--font-mono);">
        Public Repositories: <strong>${meta.public_repos_count || 9}</strong> &bull; Total Stars: <strong>${meta.total_stars || 5}</strong>
      </div>
    `;
  }

  // Render Languages
  if (langsEl) {
    const langs = data.languages || [];
    let langRows = langs.slice(0, 5).map(l => `
      <div style="margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 4px;">
          <span><code>${l.language}</code></span>
          <span style="color: var(--text-muted); font-family: var(--font-mono);">${l.percentage}%</span>
        </div>
        <div class="progress-bar-bg">
          <div class="progress-bar-fill" style="width: ${l.percentage}%;"></div>
        </div>
      </div>
    `).join('');

    langsEl.innerHTML = langRows || '<p>Telemetry loaded.</p>';
  }

  // Render Footer Date
  if (footerUpdatedEl) {
    const rawDate = (data.metadata && data.metadata.harvested_at) ? data.metadata.harvested_at.substring(0, 10) : '2026-11-25';
    footerUpdatedEl.textContent = `Auto-refreshed via GitHub Actions on ${rawDate}`;
  }
}
