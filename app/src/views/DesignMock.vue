<template>
  <div class="mock-root">

    <!-- Nav -->
    <nav class="mock-nav">
      <div class="mock-nav-inner">
        <div class="mock-logo">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>
          </svg>
          MealMind
        </div>
        <div class="mock-nav-links">
          <a v-for="link in navLinks" :key="link.label" href="#"
            :class="['mock-nav-link', link.active ? 'active' : '']"
            @click.prevent="setActive(link)">
            {{ link.label }}
          </a>
        </div>
        <div class="mock-nav-right">
          <button class="mock-nav-btn">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>
          </button>
        </div>
      </div>
    </nav>

    <div class="mock-page">

      <!-- Header row: title + stat cards -->
      <div class="mock-header">
        <div class="mock-header-text">
          <h1 class="mock-title">Meal Planner</h1>
          <p class="mock-subtitle">Lock meals you love, regenerate the rest.</p>
        </div>

        <!-- Stat cards -->
        <div class="mock-stats">
          <div class="mock-stat-card">
            <span class="mock-stat-num">{{ visibleDays.filter(d => d.recipe).length }}<span class="mock-stat-denom">/{{ planDays }}</span></span>
            <span class="mock-stat-label">Planned</span>
            <div class="mock-stat-bar">
              <div class="mock-stat-fill" :style="{ width: (visibleDays.filter(d => d.recipe).length / planDays * 100) + '%' }"></div>
            </div>
          </div>
          <div class="mock-stat-card accent">
            <span class="mock-stat-num">{{ visibleDays.filter(d => d.locked).length }}</span>
            <span class="mock-stat-label">Locked</span>
            <svg class="mock-stat-icon" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
          </div>
          <div class="mock-stat-card">
            <span class="mock-stat-num">{{ uniqueSources }}</span>
            <span class="mock-stat-label">Sources</span>
            <svg class="mock-stat-icon" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/></svg>
          </div>
        </div>
      </div>

      <!-- Action buttons -->
      <div class="mock-actions">
        <button class="mock-btn mock-btn-ghost">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v14a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
          Saved Plans
          <span class="mock-badge-count">3</span>
        </button>
        <button class="mock-btn mock-btn-secondary">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="4" y1="4" x2="9" y2="9"/></svg>
          Generate Plan
        </button>
        <button class="mock-btn mock-btn-primary">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
          Build Shopping List
        </button>
      </div>

      <!-- Toolbar: sources + plan length -->
      <div class="mock-toolbar">
        <div class="mock-toolbar-group">
          <span class="mock-toolbar-label">Sources</span>
          <button v-for="src in sources" :key="src.name"
            :class="['mock-chip', src.active ? 'active' : '']"
            @click="toggleSource(src)">
            {{ src.name }}
          </button>
        </div>

        <div class="mock-toolbar-divider"></div>

        <div class="mock-toolbar-group">
          <span class="mock-toolbar-label">Plan length</span>
          <div class="mock-day-selector">
            <button v-for="n in 7" :key="n"
              :class="['mock-day-btn', planDays === n ? 'active' : '']"
              @click="planDays = n">
              {{ n }}d
            </button>
          </div>
        </div>
      </div>

      <!-- Grid -->
      <div class="mock-grid">
        <div v-for="day in visibleDays" :key="day.label"
          :class="['mock-card', day.locked ? 'locked' : '']">

          <!-- Card header -->
          <div class="mock-card-header">
            <div class="mock-day-info">
              <span class="mock-day-name">{{ day.label }}</span>
              <span class="mock-day-date">{{ day.date }}</span>
            </div>
            <div class="mock-card-actions">
              <button :class="['mock-icon-btn', day.locked ? 'locked' : '']"
                @click="day.locked = !day.locked"
                :title="day.locked ? 'Unlock' : 'Lock'">
                <svg v-if="day.locked" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                <svg v-else width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg>
              </button>
              <button class="mock-icon-btn" :disabled="day.locked" title="Swap">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>
              </button>
            </div>
          </div>

          <!-- Recipe -->
          <div v-if="day.recipe" class="mock-recipe">
            <div class="mock-recipe-img-wrap">
              <img v-if="day.recipe.image" :src="day.recipe.image" :alt="day.recipe.name" class="mock-recipe-img" />
              <div v-else class="mock-recipe-img-placeholder">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" opacity="0.3"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
              </div>
              <div v-if="day.locked" class="mock-locked-overlay">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                Locked
              </div>
            </div>
            <div class="mock-recipe-body">
              <span :class="['mock-source-badge', 'badge-' + day.recipe.source]">{{ day.recipe.source }}</span>
              <h3 class="mock-recipe-name">{{ day.recipe.name }}</h3>
              <div class="mock-recipe-meta">
                <span v-if="day.recipe.time" class="mock-meta-item">
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  {{ day.recipe.time }}
                </span>
                <span v-if="day.recipe.servings" class="mock-meta-item">
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>
                  {{ day.recipe.servings }}
                </span>
              </div>
              <a href="#" class="mock-recipe-link" @click.prevent>
                View recipe
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
              </a>
            </div>
          </div>

          <!-- Empty -->
          <div v-else class="mock-empty-day">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" opacity="0.25"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/></svg>
            <span>No meal selected</span>
            <button class="mock-pick-btn">Pick one</button>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const navLinks = ref([
  { label: 'Meal Planner', active: true },
  { label: 'Shopping List', active: false },
  { label: 'Recipes', active: false },
  { label: 'My Recipes', active: false },
  { label: 'Add Recipe', active: false },
])

function setActive(link) {
  navLinks.value.forEach(l => l.active = false)
  link.active = true
}

const planDays = ref(7)

const sources = ref([
  { name: 'ICA', active: true },
  { name: 'Coop', active: false },
  { name: 'Mathem', active: true },
  { name: 'Arla', active: false },
  { name: 'Koket', active: false },
])

function toggleSource(src) { src.active = !src.active }

const allDays = ref([
  { label: 'Monday',    date: 'Mar 17', locked: true,  recipe: { name: 'Pasta Carbonara with Crispy Pancetta', source: 'ica',    time: '25 min', servings: '4', image: 'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=400&q=80' } },
  { label: 'Tuesday',   date: 'Mar 18', locked: false, recipe: { name: 'Thai Green Curry with Jasmine Rice',   source: 'mathem', time: '35 min', servings: '4', image: 'https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?w=400&q=80' } },
  { label: 'Wednesday', date: 'Mar 19', locked: false, recipe: null },
  { label: 'Thursday',  date: 'Mar 20', locked: false, recipe: { name: 'Salmon with Roasted Vegetables',       source: 'coop',   time: '40 min', servings: '2', image: 'https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400&q=80' } },
  { label: 'Friday',    date: 'Mar 21', locked: true,  recipe: { name: 'Homemade Beef Tacos with Salsa',       source: 'koket',  time: '30 min', servings: '4', image: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400&q=80' } },
  { label: 'Saturday',  date: 'Mar 22', locked: false, recipe: { name: 'Margherita Pizza',                     source: 'ica',    time: '45 min', servings: '2', image: 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400&q=80' } },
  { label: 'Sunday',    date: 'Mar 23', locked: false, recipe: { name: 'Swedish Meatballs with Lingonberry',   source: 'arla',   time: '50 min', servings: '6', image: 'https://images.unsplash.com/photo-1529042410759-befb1204b468?w=400&q=80' } },
])

const visibleDays = computed(() => allDays.value.slice(0, planDays.value))
const uniqueSources = computed(() => new Set(visibleDays.value.filter(d => d.recipe).map(d => d.recipe.source)).size)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Root ──────────────────────────────────────────── */
.mock-root {
  font-family: 'Inter', system-ui, sans-serif;
  background: #f5f4f7;
  color: #19171c;
  min-height: 100vh;
}

/* ── Nav ───────────────────────────────────────────── */
.mock-nav {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid #e5e4e7;
}

.mock-nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  height: 60px;
  display: flex;
  align-items: center;
  gap: 40px;
}

.mock-logo {
  display: flex;
  align-items: center;
  gap: 9px;
  font-size: 16px;
  font-weight: 700;
  color: #19171c;
  letter-spacing: -0.02em;
  white-space: nowrap;
}

.mock-nav-links {
  display: flex;
  align-items: center;
  gap: 2px;
  flex: 1;
}

.mock-nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 100px;
  font-size: 13.5px;
  font-weight: 500;
  color: #6e6e73;
  text-decoration: none;
  transition: all 0.15s ease;
  cursor: pointer;
  border: none;
  background: none;
}

.mock-nav-link:hover { color: #19171c; background: #f0eef4; }
.mock-nav-link.active { color: #7a40ed; background: #ede8fb; font-weight: 600; }

.mock-nav-right { display: flex; align-items: center; gap: 8px; }

.mock-nav-btn {
  width: 34px; height: 34px;
  border-radius: 50%;
  border: 1px solid #e5e4e7;
  background: #fff;
  color: #6e6e73;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  transition: all 0.15s ease;
}

.mock-nav-btn:hover { background: #f0eef4; color: #19171c; border-color: #d0cdd8; }

/* ── Page ──────────────────────────────────────────── */
.mock-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 24px 80px;
}

/* ── Header ────────────────────────────────────────── */
.mock-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.mock-title {
  font-size: 32px;
  font-weight: 800;
  letter-spacing: -0.04em;
  color: #19171c;
  margin-bottom: 6px;
  line-height: 1.1;
}

.mock-subtitle {
  font-size: 14px;
  color: #97979b;
  font-weight: 400;
  letter-spacing: -0.01em;
}

/* ── Stat cards ────────────────────────────────────── */
.mock-stats {
  display: flex;
  gap: 10px;
  flex-shrink: 0;
  flex-wrap: wrap;
}

.mock-stat-card {
  background: #ffffff;
  border: 1px solid #e5e4e7;
  border-radius: 16px;
  padding: 16px 20px;
  min-width: 110px;
  display: flex;
  flex-direction: column;
  gap: 3px;
  position: relative;
  overflow: hidden;
  transition: box-shadow 0.2s, transform 0.2s;
  box-shadow: 0 1px 4px rgba(25,23,28,0.04);
}

.mock-stat-card:hover {
  box-shadow: 0 6px 24px rgba(25,23,28,0.08);
  transform: translateY(-2px);
}

.mock-stat-card.accent {
  background: #7a40ed;
  border-color: transparent;
}

.mock-stat-num {
  font-size: 30px;
  font-weight: 800;
  letter-spacing: -0.04em;
  line-height: 1;
  color: #19171c;
}

.mock-stat-card.accent .mock-stat-num { color: #ffffff; }

.mock-stat-denom {
  font-size: 16px;
  font-weight: 600;
  opacity: 0.35;
}

.mock-stat-label {
  font-size: 11px;
  font-weight: 600;
  color: #97979b;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.mock-stat-card.accent .mock-stat-label { color: rgba(255,255,255,0.65); }

.mock-stat-bar {
  height: 3px;
  background: #ede8fb;
  border-radius: 2px;
  margin-top: 8px;
  overflow: hidden;
}

.mock-stat-fill {
  height: 100%;
  background: #7a40ed;
  border-radius: 2px;
  transition: width 0.5s cubic-bezier(0.4,0,0.2,1);
}

.mock-stat-icon {
  position: absolute;
  bottom: 12px;
  right: 14px;
  opacity: 0.08;
  color: #19171c;
}

.mock-stat-card.accent .mock-stat-icon { color: #fff; opacity: 0.2; }

/* ── Actions ───────────────────────────────────────── */
.mock-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 24px;
}

/* ── Buttons ───────────────────────────────────────── */
.mock-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 0 18px;
  height: 38px;
  border-radius: 100px;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  white-space: nowrap;
  font-family: inherit;
  letter-spacing: -0.01em;
}

.mock-btn-primary { background: #7a40ed; color: #ffffff; }
.mock-btn-primary:hover { background: #6b32de; box-shadow: 0 4px 16px rgba(122,64,237,0.3); transform: translateY(-1px); }

.mock-btn-secondary { background: #ede8fb; color: #7a40ed; border: 1px solid #d9d0f7; }
.mock-btn-secondary:hover { background: #e3dbf9; border-color: #c8baf3; }

.mock-btn-ghost { background: #ffffff; color: #6e6e73; border: 1px solid #e5e4e7; }
.mock-btn-ghost:hover { background: #f5f4f7; color: #19171c; border-color: #d0cdd8; }

.mock-badge-count {
  display: inline-flex; align-items: center; justify-content: center;
  background: #7a40ed; color: #fff;
  border-radius: 100px; font-size: 10px; font-weight: 700;
  min-width: 18px; height: 18px; padding: 0 5px;
}

/* ── Toolbar ───────────────────────────────────────── */
.mock-toolbar {
  display: flex;
  align-items: center;
  gap: 0;
  margin-bottom: 24px;
  background: #ffffff;
  border: 1px solid #e5e4e7;
  border-radius: 100px;
  padding: 6px 16px;
  flex-wrap: wrap;
  row-gap: 8px;
}

.mock-toolbar-group {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.mock-toolbar-divider {
  width: 1px;
  height: 20px;
  background: #e5e4e7;
  margin: 0 16px;
  flex-shrink: 0;
}

.mock-toolbar-label {
  font-size: 11.5px;
  font-weight: 700;
  color: #97979b;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  white-space: nowrap;
  margin-right: 2px;
}

.mock-chip {
  display: inline-flex;
  align-items: center;
  padding: 4px 13px;
  border-radius: 100px;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
  border: 1px solid #e5e4e7;
  background: transparent;
  color: #6e6e73;
  font-family: inherit;
}

.mock-chip:hover { border-color: #d0cdd8; color: #19171c; background: #f5f4f7; }
.mock-chip.active { background: #ede8fb; border-color: #c8baf3; color: #7a40ed; }

/* ── Days selector ─────────────────────────────────── */
.mock-day-selector {
  display: flex;
  background: #f5f4f7;
  border-radius: 100px;
  padding: 3px;
  gap: 2px;
}

.mock-day-btn {
  padding: 3px 11px;
  border-radius: 100px;
  border: none;
  background: transparent;
  font-size: 12px;
  font-weight: 600;
  color: #97979b;
  cursor: pointer;
  transition: all 0.15s ease;
  font-family: inherit;
  white-space: nowrap;
}

.mock-day-btn:hover { color: #19171c; }
.mock-day-btn.active { background: #7a40ed; color: #ffffff; box-shadow: 0 2px 8px rgba(122,64,237,0.25); }

/* ── Grid ──────────────────────────────────────────── */
.mock-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

/* ── Card ──────────────────────────────────────────── */
.mock-card {
  background: #ffffff;
  border: 1px solid #e5e4e7;
  border-radius: 20px;
  overflow: hidden;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  flex-direction: column;
}

.mock-card:hover { border-color: #d0cdd8; box-shadow: 0 8px 32px rgba(25,23,28,0.08); }
.mock-card.locked { border-color: #c8baf3; background: #faf8ff; }

/* ── Card header ───────────────────────────────────── */
.mock-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px 12px;
  border-bottom: 1px solid #f0eef4;
}

.mock-day-info { display: flex; flex-direction: column; gap: 1px; }
.mock-day-name { font-size: 14px; font-weight: 700; color: #19171c; letter-spacing: -0.02em; }
.mock-day-date { font-size: 11px; color: #97979b; font-weight: 500; }
.mock-card-actions { display: flex; gap: 4px; }

.mock-icon-btn {
  width: 30px; height: 30px;
  border-radius: 50%;
  border: 1px solid #e5e4e7;
  background: #ffffff;
  color: #c3c3c6;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  transition: all 0.15s ease;
}

.mock-icon-btn:hover:not(:disabled) { background: #f5f4f7; color: #6e6e73; border-color: #d0cdd8; }
.mock-icon-btn.locked { background: #ede8fb; border-color: #c8baf3; color: #7a40ed; }
.mock-icon-btn:disabled { opacity: 0.35; cursor: not-allowed; }

/* ── Recipe ────────────────────────────────────────── */
.mock-recipe { display: flex; flex-direction: column; flex: 1; }
.mock-recipe-img-wrap { position: relative; overflow: hidden; }

.mock-recipe-img {
  width: 100%; height: 160px;
  object-fit: cover; display: block;
  transition: transform 0.3s ease;
}

.mock-card:hover .mock-recipe-img { transform: scale(1.03); }

.mock-recipe-img-placeholder {
  width: 100%; height: 160px;
  background: #f5f4f7;
  display: flex; align-items: center; justify-content: center;
}

.mock-locked-overlay {
  position: absolute; top: 10px; right: 10px;
  display: flex; align-items: center; gap: 5px;
  background: #7a40ed; color: #fff;
  font-size: 11px; font-weight: 700;
  padding: 4px 10px; border-radius: 100px;
  letter-spacing: 0.02em;
}

.mock-recipe-body {
  padding: 14px 16px 16px;
  display: flex; flex-direction: column; gap: 6px; flex: 1;
}

.mock-source-badge {
  display: inline-flex; align-items: center;
  padding: 2px 10px; border-radius: 100px;
  font-size: 10.5px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.04em;
  align-self: flex-start; border: 1px solid transparent;
}

.badge-ica    { background: #fff0f0; color: #cc0000; border-color: #fecaca; }
.badge-coop   { background: #fff8e1; color: #c67c00; border-color: #fde68a; }
.badge-mathem { background: #f0f4ff; color: #3a5bcd; border-color: #c7d2fe; }
.badge-arla   { background: #f0f8ff; color: #0066cc; border-color: #bae6fd; }
.badge-koket  { background: #fdf4ff; color: #8b22b5; border-color: #e9d5ff; }
.badge-custom { background: #f0fdf4; color: #166534; border-color: #bbf7d0; }

.mock-recipe-name { font-size: 14.5px; font-weight: 650; color: #19171c; line-height: 1.35; letter-spacing: -0.01em; }
.mock-recipe-meta { display: flex; gap: 12px; flex-wrap: wrap; }
.mock-meta-item { display: flex; align-items: center; gap: 4px; font-size: 11.5px; color: #97979b; font-weight: 500; }

.mock-recipe-link {
  display: inline-flex; align-items: center; gap: 4px;
  font-size: 12px; font-weight: 600; color: #7a40ed;
  text-decoration: none; margin-top: 4px; width: fit-content;
  transition: color 0.15s ease;
}

.mock-recipe-link:hover { color: #6b32de; }

/* ── Empty ─────────────────────────────────────────── */
.mock-empty-day {
  flex: 1; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 10px; padding: 36px 16px;
  color: #c3c3c6; font-size: 13px;
}

.mock-pick-btn {
  padding: 6px 18px; border-radius: 100px;
  border: 1px solid #d9d0f7; background: #ede8fb; color: #7a40ed;
  font-size: 12.5px; font-weight: 600; cursor: pointer;
  transition: all 0.15s ease; font-family: inherit;
}

.mock-pick-btn:hover { background: #e3dbf9; border-color: #c8baf3; }
</style>
