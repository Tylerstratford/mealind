<template>
  <div class="b-root">

    <!-- Nav -->
    <nav class="b-nav">
      <div class="b-nav-inner">
        <div class="b-logo">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>
          </svg>
          MealMind
        </div>

        <div class="b-nav-links">
          <a v-for="link in navLinks" :key="link.label" href="#"
            :class="['b-nav-link', link.active ? 'active' : '']"
            @click.prevent="setActive(link)">
            {{ link.label }}
          </a>
        </div>

        <div class="b-nav-actions">
          <button class="b-btn b-btn-ghost b-btn-sm">Log in</button>
          <button class="b-btn b-btn-primary b-btn-sm">Add Recipe</button>
        </div>
      </div>
    </nav>

    <!-- Page -->
    <div class="b-page">

      <!-- Header -->
      <div class="b-header">
        <div class="b-header-left">
          <span class="b-eyebrow">Week of Mar 17 – 23</span>
          <h1 class="b-title">Meal Planner</h1>
          <p class="b-subtitle">Lock meals you love, regenerate the rest. Build your shopping list when ready.</p>
        </div>
        <div class="b-header-actions">
          <button class="b-btn b-btn-ghost" @click="showSaved = !showSaved">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v14a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
            Saved Plans
            <span class="b-count">3</span>
          </button>
          <button class="b-btn b-btn-secondary">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="4" y1="4" x2="9" y2="9"/></svg>
            Generate Plan
          </button>
          <button class="b-btn b-btn-primary">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
            Build Shopping List
          </button>
        </div>
      </div>

      <!-- Divider + filters row -->
      <div class="b-toolbar">
        <div class="b-filters">
          <span class="b-filters-label">Filter by source</span>
          <button v-for="src in sources" :key="src.name"
            :class="['b-chip', src.active ? 'active' : '']"
            @click="toggleSource(src)">
            {{ src.name }}
          </button>
        </div>
        <div class="b-view-meta">
          <span class="b-meta-text">{{ days.filter(d => d.recipe).length }} of 7 meals planned</span>
          <div class="b-progress-bar">
            <div class="b-progress-fill" :style="{ width: (days.filter(d => d.recipe).length / 7 * 100) + '%' }"></div>
          </div>
        </div>
      </div>

      <!-- Grid -->
      <div class="b-grid">
        <div v-for="day in days" :key="day.label" :class="['b-card', day.locked ? 'locked' : '', !day.recipe ? 'empty' : '']">

          <!-- Image area -->
          <div class="b-card-img-wrap">
            <img v-if="day.recipe?.image" :src="day.recipe.image" :alt="day.recipe?.name" class="b-card-img" />
            <div v-else class="b-card-img-empty">
              <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><rect x="3" y="3" width="18" height="18" rx="1"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
              <span>No meal selected</span>
              <button class="b-pick-btn">Choose recipe</button>
            </div>

            <!-- Overlays -->
            <div class="b-card-overlays">
              <div class="b-day-badge">{{ day.label.slice(0,3).toUpperCase() }}</div>
              <div class="b-card-controls">
                <button :class="['b-ctrl-btn', day.locked ? 'active' : '']"
                  @click="day.locked = !day.locked"
                  :title="day.locked ? 'Unlock' : 'Lock'">
                  <svg v-if="day.locked" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                  <svg v-else width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg>
                </button>
                <button class="b-ctrl-btn" :disabled="day.locked" title="Swap">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>
                </button>
              </div>
            </div>

            <div v-if="day.locked && day.recipe" class="b-locked-tag">
              <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              Locked
            </div>
          </div>

          <!-- Card body -->
          <div v-if="day.recipe" class="b-card-body">
            <div class="b-card-meta-row">
              <span class="b-day-date">{{ day.date }}</span>
              <span :class="['b-source-tag', 'src-' + day.recipe.source]">{{ day.recipe.source }}</span>
            </div>
            <h3 class="b-recipe-name">{{ day.recipe.name }}</h3>
            <div class="b-recipe-stats">
              <span v-if="day.recipe.time" class="b-stat">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                {{ day.recipe.time }}
              </span>
              <span v-if="day.recipe.servings" class="b-stat">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>
                {{ day.recipe.servings }} servings
              </span>
            </div>
            <a href="#" class="b-view-link" @click.prevent>
              View recipe
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
            </a>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const navLinks = ref([
  { label: 'Meal Planner', active: true },
  { label: 'Shopping List', active: false },
  { label: 'Recipes', active: false },
  { label: 'My Recipes', active: false },
])

function setActive(link) {
  navLinks.value.forEach(l => l.active = false)
  link.active = true
}

const showSaved = ref(false)

const sources = ref([
  { name: 'All', active: true },
  { name: 'ICA', active: false },
  { name: 'Coop', active: false },
  { name: 'Mathem', active: false },
  { name: 'Arla', active: false },
  { name: 'Koket', active: false },
])

function toggleSource(src) {
  sources.value.forEach(s => s.active = false)
  src.active = true
}

const days = ref([
  {
    label: 'Monday', date: 'Mar 17',
    locked: true,
    recipe: { name: 'Pasta Carbonara with Crispy Pancetta', source: 'ica', time: '25 min', servings: '4', image: 'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=600&q=80' }
  },
  {
    label: 'Tuesday', date: 'Mar 18',
    locked: false,
    recipe: { name: 'Thai Green Curry with Jasmine Rice', source: 'mathem', time: '35 min', servings: '4', image: 'https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?w=600&q=80' }
  },
  {
    label: 'Wednesday', date: 'Mar 19',
    locked: false,
    recipe: null
  },
  {
    label: 'Thursday', date: 'Mar 20',
    locked: false,
    recipe: { name: 'Salmon with Roasted Vegetables', source: 'coop', time: '40 min', servings: '2', image: 'https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=600&q=80' }
  },
  {
    label: 'Friday', date: 'Mar 21',
    locked: true,
    recipe: { name: 'Homemade Beef Tacos with Fresh Salsa', source: 'koket', time: '30 min', servings: '4', image: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=600&q=80' }
  },
  {
    label: 'Saturday', date: 'Mar 22',
    locked: false,
    recipe: { name: 'Margherita Pizza', source: 'ica', time: '45 min', servings: '2', image: 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=600&q=80' }
  },
  {
    label: 'Sunday', date: 'Mar 23',
    locked: false,
    recipe: { name: 'Swedish Meatballs with Lingonberry', source: 'arla', time: '50 min', servings: '6', image: 'https://images.unsplash.com/photo-1529042410759-befb1204b468?w=600&q=80' }
  },
])
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Root ──────────────────────────────────────────── */
.b-root {
  font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
  background: #f9f9f9;
  color: #191919;
  min-height: 100vh;
}

/* ── Nav ───────────────────────────────────────────── */
.b-nav {
  background: #ffffff;
  border-bottom: 1px solid #e8e8e8;
  position: sticky;
  top: 0;
  z-index: 50;
}

.b-nav-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
  height: 56px;
  display: flex;
  align-items: center;
  gap: 48px;
}

.b-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 700;
  color: #191919;
  letter-spacing: -0.01em;
  white-space: nowrap;
}

.b-nav-links {
  display: flex;
  align-items: center;
  gap: 0;
  flex: 1;
}

.b-nav-link {
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  color: #909090;
  text-decoration: none;
  transition: color 0.1s;
  border-bottom: 2px solid transparent;
  height: 56px;
  display: flex;
  align-items: center;
  cursor: pointer;
}

.b-nav-link:hover {
  color: #191919;
}

.b-nav-link.active {
  color: #0057ff;
  border-bottom-color: #0057ff;
  font-weight: 600;
}

.b-nav-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ── Buttons ───────────────────────────────────────── */
.b-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 0 16px;
  height: 36px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.1s, color 0.1s, border-color 0.1s;
  border: 1px solid transparent;
  white-space: nowrap;
  font-family: inherit;
  letter-spacing: 0;
}

.b-btn-sm {
  height: 32px;
  padding: 0 14px;
  font-size: 12.5px;
}

.b-btn-primary {
  background: #0057ff;
  color: #ffffff;
  border-color: #0057ff;
}

.b-btn-primary:hover {
  background: #003ecb;
  border-color: #003ecb;
}

.b-btn-secondary {
  background: #191919;
  color: #ffffff;
  border-color: #191919;
}

.b-btn-secondary:hover {
  background: #2d2d2d;
  border-color: #2d2d2d;
}

.b-btn-ghost {
  background: #ffffff;
  color: #191919;
  border-color: #d8d8d8;
}

.b-btn-ghost:hover {
  background: #f0f0f0;
  border-color: #c0c0c0;
}

.b-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #0057ff;
  color: #fff;
  border-radius: 100px;
  font-size: 10px;
  font-weight: 700;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
}

/* ── Page ───────────────────────────────────────────── */
.b-page {
  max-width: 1280px;
  margin: 0 auto;
  padding: 40px 24px 80px;
}

/* ── Header ─────────────────────────────────────────── */
.b-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 32px;
  padding-bottom: 32px;
  border-bottom: 1px solid #e8e8e8;
  flex-wrap: wrap;
}

.b-eyebrow {
  display: block;
  font-size: 11px;
  font-weight: 700;
  color: #0057ff;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 10px;
}

.b-title {
  font-size: 40px;
  font-weight: 900;
  letter-spacing: -0.03em;
  color: #191919;
  line-height: 1;
  margin-bottom: 10px;
}

.b-subtitle {
  font-size: 14px;
  color: #909090;
  font-weight: 400;
  max-width: 440px;
  line-height: 1.5;
}

.b-header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  flex-wrap: wrap;
}

/* ── Toolbar ─────────────────────────────────────────── */
.b-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.b-filters {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.b-filters-label {
  font-size: 12px;
  font-weight: 600;
  color: #909090;
  margin-right: 4px;
  white-space: nowrap;
}

.b-chip {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 2px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.1s;
  border: 1px solid #d8d8d8;
  background: #ffffff;
  color: #909090;
  font-family: inherit;
}

.b-chip:hover {
  border-color: #191919;
  color: #191919;
}

.b-chip.active {
  background: #191919;
  border-color: #191919;
  color: #ffffff;
}

.b-view-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.b-meta-text {
  font-size: 12px;
  color: #909090;
  font-weight: 500;
  white-space: nowrap;
}

.b-progress-bar {
  width: 120px;
  height: 3px;
  background: #e8e8e8;
  border-radius: 2px;
  overflow: hidden;
}

.b-progress-fill {
  height: 100%;
  background: #0057ff;
  border-radius: 2px;
  transition: width 0.4s ease;
}

/* ── Grid ────────────────────────────────────────────── */
.b-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
  gap: 1px;
  background: #e8e8e8;
  border: 1px solid #e8e8e8;
}

/* ── Card ────────────────────────────────────────────── */
.b-card {
  background: #ffffff;
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.15s;
  position: relative;
}

.b-card:hover {
  z-index: 2;
  box-shadow: 0 5px 20px rgba(0,0,0,0.13);
}

.b-card.locked {
  background: #fafbff;
}

/* ── Card image ──────────────────────────────────────── */
.b-card-img-wrap {
  position: relative;
  overflow: hidden;
  aspect-ratio: 4/3;
  background: #f0f0f0;
}

.b-card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.4s ease;
}

.b-card:hover .b-card-img {
  transform: scale(1.04);
}

.b-card-img-empty {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #c0c0c0;
  font-size: 13px;
  background: #f5f5f5;
}

/* ── Overlays ────────────────────────────────────────── */
.b-card-overlays {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 12px;
}

.b-day-badge {
  background: #191919;
  color: #ffffff;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.08em;
  padding: 3px 8px;
  border-radius: 2px;
}

.b-card-controls {
  display: flex;
  gap: 4px;
  opacity: 0;
  transition: opacity 0.15s;
}

.b-card:hover .b-card-controls {
  opacity: 1;
}

.b-ctrl-btn {
  width: 28px;
  height: 28px;
  border-radius: 2px;
  border: none;
  background: rgba(255,255,255,0.9);
  color: #191919;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.1s;
  backdrop-filter: blur(4px);
}

.b-ctrl-btn:hover:not(:disabled) {
  background: #ffffff;
}

.b-ctrl-btn.active {
  background: #0057ff;
  color: #ffffff;
}

.b-ctrl-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.b-locked-tag {
  position: absolute;
  bottom: 10px;
  right: 10px;
  display: flex;
  align-items: center;
  gap: 4px;
  background: #0057ff;
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 2px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

/* ── Card body ───────────────────────────────────────── */
.b-card-body {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
  border-top: 1px solid #f0f0f0;
}

.b-card-meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.b-day-date {
  font-size: 11px;
  color: #909090;
  font-weight: 500;
}

.b-source-tag {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 2px 7px;
  border-radius: 2px;
}

.src-ica    { background: #fff0f0; color: #cc0000; }
.src-coop   { background: #fff8e1; color: #c67c00; }
.src-mathem { background: #f0f4ff; color: #3a5bcd; }
.src-arla   { background: #f0f8ff; color: #0066cc; }
.src-koket  { background: #fdf4ff; color: #8b22b5; }
.src-custom { background: #f0fdf4; color: #166534; }

.b-recipe-name {
  font-size: 14px;
  font-weight: 700;
  color: #191919;
  line-height: 1.3;
  letter-spacing: -0.01em;
}

.b-recipe-stats {
  display: flex;
  gap: 14px;
}

.b-stat {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11.5px;
  color: #909090;
  font-weight: 500;
}

.b-view-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 700;
  color: #0057ff;
  text-decoration: none;
  margin-top: 2px;
  width: fit-content;
  transition: color 0.1s;
  letter-spacing: 0;
}

.b-view-link:hover {
  color: #003ecb;
}

/* ── Pick button ─────────────────────────────────────── */
.b-pick-btn {
  padding: 6px 16px;
  border-radius: 4px;
  border: 1px solid #0057ff;
  background: transparent;
  color: #0057ff;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.1s;
  font-family: inherit;
}

.b-pick-btn:hover {
  background: #0057ff;
  color: #ffffff;
}
</style>
