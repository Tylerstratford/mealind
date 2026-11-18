<template>
  <div class="r-root">

    <!-- Background blobs -->
    <div class="r-blob r-blob-1"></div>
    <div class="r-blob r-blob-2"></div>
    <div class="r-blob r-blob-3"></div>

    <!-- Nav -->
    <nav class="r-nav">
      <div class="r-nav-inner">
        <div class="r-logo">
          <div class="r-logo-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>
            </svg>
          </div>
          MealMind
        </div>

        <div class="r-nav-center">
          <a v-for="link in navLinks" :key="link.label" href="#"
            :class="['r-nav-link', link.active ? 'active' : '']"
            @click.prevent="setActive(link)">
            {{ link.label }}
          </a>
        </div>

        <div class="r-nav-right">
          <button class="r-btn r-btn-outline r-btn-sm">Log in</button>
          <button class="r-btn r-btn-gradient r-btn-sm">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            Add Recipe
          </button>
        </div>
      </div>
    </nav>

    <div class="r-page">

      <!-- Header -->
      <div class="r-header">
        <div class="r-header-text">
          <div class="r-week-pill">
            <span class="r-week-dot"></span>
            Week of Mar 17 – 23, 2026
          </div>
          <h1 class="r-title">Your <span class="r-title-gradient">Weekly</span><br>Meal Plan</h1>
          <p class="r-subtitle">Lock meals you love, swap the rest, and build your shopping list in one click.</p>
        </div>

        <div class="r-header-cards">
          <div class="r-stat-card">
            <span class="r-stat-num">{{ days.filter(d => d.recipe).length }}<span class="r-stat-denom">/7</span></span>
            <span class="r-stat-label">Meals Planned</span>
            <div class="r-stat-bar">
              <div class="r-stat-fill" :style="{ width: (days.filter(d => d.recipe).length / 7 * 100) + '%' }"></div>
            </div>
          </div>
          <div class="r-stat-card accent">
            <span class="r-stat-num">{{ days.filter(d => d.locked).length }}</span>
            <span class="r-stat-label">Locked</span>
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="r-stat-icon"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
          </div>
          <div class="r-stat-card">
            <span class="r-stat-num">{{ uniqueSources }}</span>
            <span class="r-stat-label">Sources</span>
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="r-stat-icon"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/></svg>
          </div>
        </div>

        <div class="r-header-actions">
          <button class="r-btn r-btn-glass">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v14a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
            Saved Plans
            <span class="r-chip-count">3</span>
          </button>
          <button class="r-btn r-btn-glass" @click="generatePlan">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="4" y1="4" x2="9" y2="9"/></svg>
            Generate Plan
          </button>
          <button class="r-btn r-btn-gradient">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
            Build Shopping List
          </button>
        </div>
      </div>

      <!-- Filter bar -->
      <div class="r-filter-row">
        <div class="r-filters">
          <span class="r-filter-label">Sources</span>
          <button v-for="src in sources" :key="src.name"
            :class="['r-filter-chip', src.active ? 'active' : '']"
            @click="toggleSource(src)">
            {{ src.name }}
          </button>
        </div>
        <div class="r-view-toggle">
          <button :class="['r-toggle-btn', viewMode === 'week' ? 'active' : '']" @click="viewMode = 'week'">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
            Grid
          </button>
          <button :class="['r-toggle-btn', viewMode === 'list' ? 'active' : '']" @click="viewMode = 'list'">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
            List
          </button>
        </div>
      </div>

      <!-- Week strip -->
      <div class="r-week-strip">
        <div v-for="(day, idx) in days" :key="day.label"
          :class="['r-day-card', day.locked ? 'locked' : '', !day.recipe ? 'empty' : '', activeDay === idx ? 'featured' : '']"
          @click="activeDay = idx">

          <!-- Image -->
          <div class="r-day-img-wrap">
            <img v-if="day.recipe?.image" :src="day.recipe.image" class="r-day-img" :alt="day.recipe.name" />
            <div v-else class="r-day-img-empty">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><rect x="3" y="3" width="18" height="18" rx="1"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
            </div>

            <!-- Day badge -->
            <div :class="['r-day-label', day.locked ? 'locked' : '']">
              {{ day.label.slice(0,3).toUpperCase() }}
            </div>

            <!-- Action buttons (always visible, subtle) -->
            <div class="r-day-controls">
              <button :class="['r-ctrl', day.locked ? 'locked' : '']"
                @click.stop="day.locked = !day.locked" :title="day.locked ? 'Unlock' : 'Lock'">
                <svg v-if="day.locked" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                <svg v-else width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg>
              </button>
              <button class="r-ctrl" :disabled="day.locked" @click.stop title="Swap">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>
              </button>
            </div>

            <!-- Gradient overlay for text legibility -->
            <div class="r-day-overlay"></div>
          </div>

          <!-- Card body -->
          <div class="r-day-body">
            <div class="r-day-date">{{ day.date }}</div>
            <template v-if="day.recipe">
              <span :class="['r-src-badge', 's-' + day.recipe.source]">{{ day.recipe.source }}</span>
              <h3 class="r-recipe-title">{{ day.recipe.name }}</h3>
              <div class="r-recipe-meta">
                <span v-if="day.recipe.time" class="r-meta">
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  {{ day.recipe.time }}
                </span>
                <span v-if="day.recipe.servings" class="r-meta">
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>
                  {{ day.recipe.servings }}
                </span>
              </div>
              <a href="#" class="r-recipe-link" @click.prevent>
                View <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
              </a>
            </template>
            <template v-else>
              <p class="r-empty-label">No meal yet</p>
              <button class="r-pick-btn">+ Pick recipe</button>
            </template>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const navLinks = ref([
  { label: 'Planner', active: true },
  { label: 'Shopping', active: false },
  { label: 'Recipes', active: false },
  { label: 'My Recipes', active: false },
])

function setActive(link) {
  navLinks.value.forEach(l => l.active = false)
  link.active = true
}

const viewMode = ref('week')
const activeDay = ref(0)

const sources = ref([
  { name: 'ICA', active: true },
  { name: 'Coop', active: false },
  { name: 'Mathem', active: true },
  { name: 'Arla', active: false },
  { name: 'Koket', active: false },
])

function toggleSource(src) { src.active = !src.active }

function generatePlan() { activeDay.value = Math.floor(Math.random() * 7) }

const days = ref([
  { label: 'Monday',    date: 'Mar 17', locked: true,  recipe: { name: 'Pasta Carbonara with Crispy Pancetta', source: 'ica',    time: '25 min', servings: '4', image: 'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=600&q=80' } },
  { label: 'Tuesday',   date: 'Mar 18', locked: false, recipe: { name: 'Thai Green Curry with Jasmine Rice',   source: 'mathem', time: '35 min', servings: '4', image: 'https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?w=600&q=80' } },
  { label: 'Wednesday', date: 'Mar 19', locked: false, recipe: null },
  { label: 'Thursday',  date: 'Mar 20', locked: false, recipe: { name: 'Salmon with Roasted Vegetables',       source: 'coop',   time: '40 min', servings: '2', image: 'https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=600&q=80' } },
  { label: 'Friday',    date: 'Mar 21', locked: true,  recipe: { name: 'Homemade Beef Tacos with Fresh Salsa', source: 'koket',  time: '30 min', servings: '4', image: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=600&q=80' } },
  { label: 'Saturday',  date: 'Mar 22', locked: false, recipe: { name: 'Margherita Pizza',                     source: 'ica',    time: '45 min', servings: '2', image: 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=600&q=80' } },
  { label: 'Sunday',    date: 'Mar 23', locked: false, recipe: { name: 'Swedish Meatballs & Lingonberry',      source: 'arla',   time: '50 min', servings: '6', image: 'https://images.unsplash.com/photo-1529042410759-befb1204b468?w=600&q=80' } },
])

const uniqueSources = computed(() => new Set(days.value.filter(d => d.recipe).map(d => d.recipe.source)).size)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Tokens ──────────────────────────────────────── */
:root {
  --grad: linear-gradient(135deg, #e63950 0%, #ff7849 100%);
  --grad-text: linear-gradient(135deg, #e63950, #ff9a3c);
  --coral: #e63950;
  --amber: #ff7849;
  --bg: #fffaf7;
  --surface: #ffffff;
  --border: #f0e8e5;
  --border-2: #e8ddd8;
  --text: #1a0505;
  --text-2: #7a5c5c;
  --text-3: #b8a8a5;
  --locked-glow: rgba(230, 57, 80, 0.3);
  --radius: 18px;
}

/* ── Base ────────────────────────────────────────── */
.r-root {
  font-family: 'Inter', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

/* ── Background blobs ────────────────────────────── */
.r-blob {
  position: fixed;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
  z-index: 0;
  opacity: 0.12;
}

.r-blob-1 {
  width: 600px; height: 600px;
  background: #e63950;
  top: -200px; right: -200px;
  animation: blobFloat 12s ease-in-out infinite;
}

.r-blob-2 {
  width: 400px; height: 400px;
  background: #ff7849;
  bottom: 100px; left: -150px;
  animation: blobFloat 16s ease-in-out infinite reverse;
}

.r-blob-3 {
  width: 300px; height: 300px;
  background: #ff4d6d;
  top: 40%; left: 40%;
  animation: blobFloat 10s ease-in-out infinite 3s;
}

@keyframes blobFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33%       { transform: translate(30px, -30px) scale(1.05); }
  66%       { transform: translate(-20px, 20px) scale(0.97); }
}

/* ── Nav ─────────────────────────────────────────── */
.r-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 250, 247, 0.85);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border-bottom: 1px solid var(--border);
}

.r-nav-inner {
  max-width: 1300px;
  margin: 0 auto;
  padding: 0 28px;
  height: 62px;
  display: flex;
  align-items: center;
  gap: 0;
  position: relative;
  z-index: 1;
}

.r-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 700;
  color: var(--text);
  font-family: 'Playfair Display', serif;
  letter-spacing: -0.01em;
  margin-right: auto;
}

.r-logo-icon {
  width: 34px; height: 34px;
  background: var(--grad);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.r-nav-center {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 2px;
}

.r-nav-link {
  padding: 6px 16px;
  font-size: 13.5px;
  font-weight: 500;
  color: var(--text-2);
  text-decoration: none;
  border-radius: 100px;
  transition: all 0.15s ease;
  cursor: pointer;
  border: none;
  background: none;
}

.r-nav-link:hover {
  color: var(--text);
  background: rgba(230, 57, 80, 0.06);
}

.r-nav-link.active {
  color: var(--coral);
  background: rgba(230, 57, 80, 0.1);
  font-weight: 600;
}

.r-nav-right {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}

/* ── Buttons ─────────────────────────────────────── */
.r-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 0 20px;
  height: 40px;
  border-radius: 100px;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  white-space: nowrap;
  font-family: 'Inter', sans-serif;
  letter-spacing: -0.01em;
}

.r-btn-sm { height: 34px; padding: 0 16px; font-size: 13px; }

.r-btn-gradient {
  background: var(--grad);
  color: #ffffff;
  position: relative;
  overflow: hidden;
}

.r-btn-gradient::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, transparent 50%);
  opacity: 0;
  transition: opacity 0.2s;
}

.r-btn-gradient:hover::after { opacity: 1; }
.r-btn-gradient:hover { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(230, 57, 80, 0.35); }

.r-btn-outline {
  background: transparent;
  color: var(--text-2);
  border: 1px solid var(--border-2);
}

.r-btn-outline:hover {
  border-color: var(--coral);
  color: var(--coral);
  background: rgba(230, 57, 80, 0.04);
}

.r-btn-glass {
  background: rgba(255,255,255,0.8);
  color: var(--text);
  border: 1px solid var(--border);
  backdrop-filter: blur(8px);
}

.r-btn-glass:hover {
  background: #ffffff;
  border-color: var(--border-2);
  box-shadow: 0 4px 16px rgba(26,5,5,0.08);
}

.r-chip-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--grad);
  color: #fff;
  border-radius: 100px;
  font-size: 10px;
  font-weight: 700;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
}

/* ── Page ────────────────────────────────────────── */
.r-page {
  max-width: 1300px;
  margin: 0 auto;
  padding: 48px 28px 80px;
  position: relative;
  z-index: 1;
}

/* ── Header ──────────────────────────────────────── */
.r-header {
  display: grid;
  grid-template-columns: 1fr auto;
  grid-template-rows: auto auto;
  gap: 24px 40px;
  margin-bottom: 40px;
  align-items: start;
}

.r-header-text { grid-column: 1; grid-row: 1; }
.r-header-cards { grid-column: 2; grid-row: 1; display: flex; gap: 12px; }
.r-header-actions { grid-column: 1 / -1; grid-row: 2; display: flex; gap: 10px; flex-wrap: wrap; }

.r-week-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(230, 57, 80, 0.08);
  color: var(--coral);
  font-size: 12px;
  font-weight: 700;
  padding: 5px 14px;
  border-radius: 100px;
  margin-bottom: 16px;
  letter-spacing: 0.02em;
}

.r-week-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--coral);
  display: inline-block;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.5; transform: scale(0.8); }
}

.r-title {
  font-family: 'Playfair Display', serif;
  font-size: 52px;
  font-weight: 900;
  color: var(--text);
  line-height: 1.05;
  letter-spacing: -0.03em;
  margin-bottom: 14px;
}

.r-title-gradient {
  background: var(--grad-text);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.r-subtitle {
  font-size: 15px;
  color: var(--text-2);
  line-height: 1.6;
  max-width: 420px;
  font-weight: 400;
}

/* ── Stat cards ──────────────────────────────────── */
.r-stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px 24px;
  min-width: 130px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(26,5,5,0.05);
  transition: box-shadow 0.2s, transform 0.2s;
}

.r-stat-card:hover {
  box-shadow: 0 8px 32px rgba(26,5,5,0.1);
  transform: translateY(-2px);
}

.r-stat-card.accent {
  background: var(--grad);
  border-color: transparent;
  color: white;
}

.r-stat-num {
  font-size: 36px;
  font-weight: 800;
  font-family: 'Playfair Display', serif;
  line-height: 1;
  letter-spacing: -0.03em;
  color: inherit;
}

.r-stat-card:not(.accent) .r-stat-num { color: var(--text); }

.r-stat-denom {
  font-size: 18px;
  opacity: 0.4;
  font-weight: 700;
}

.r-stat-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-2);
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

.r-stat-card.accent .r-stat-label { color: rgba(255,255,255,0.75); }

.r-stat-bar {
  height: 3px;
  background: rgba(230,57,80,0.15);
  border-radius: 2px;
  margin-top: 8px;
  overflow: hidden;
}

.r-stat-fill {
  height: 100%;
  background: var(--grad);
  border-radius: 2px;
  transition: width 0.6s cubic-bezier(0.4,0,0.2,1);
}

.r-stat-icon {
  position: absolute;
  bottom: 16px;
  right: 16px;
  opacity: 0.12;
  color: var(--text);
}

.r-stat-card.accent .r-stat-icon {
  color: white;
  opacity: 0.2;
}

/* ── Filter row ──────────────────────────────────── */
.r-filter-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  gap: 16px;
  flex-wrap: wrap;
}

.r-filters {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.r-filter-label {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-right: 4px;
}

.r-filter-chip {
  padding: 5px 14px;
  border-radius: 100px;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
  border: 1px solid var(--border-2);
  background: var(--surface);
  color: var(--text-2);
  font-family: 'Inter', sans-serif;
}

.r-filter-chip:hover {
  border-color: var(--coral);
  color: var(--coral);
}

.r-filter-chip.active {
  background: var(--grad);
  border-color: transparent;
  color: white;
}

.r-view-toggle {
  display: flex;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 100px;
  padding: 3px;
  gap: 2px;
}

.r-toggle-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 12px;
  border-radius: 100px;
  border: none;
  background: none;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-3);
  cursor: pointer;
  transition: all 0.15s;
  font-family: 'Inter', sans-serif;
}

.r-toggle-btn.active {
  background: var(--grad);
  color: white;
}

/* ── Week strip ──────────────────────────────────── */
.r-week-strip {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 12px;
}

/* ── Day card ────────────────────────────────────── */
.r-day-card {
  background: var(--surface);
  border-radius: var(--radius);
  overflow: hidden;
  border: 1.5px solid var(--border);
  display: flex;
  flex-direction: column;
  cursor: pointer;
  transition: transform 0.25s cubic-bezier(0.4,0,0.2,1), box-shadow 0.25s ease, border-color 0.2s;
}

.r-day-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 50px rgba(26,5,5,0.12);
  border-color: var(--border-2);
}

.r-day-card.featured {
  border-color: var(--coral);
  box-shadow: 0 0 0 3px rgba(230,57,80,0.12), 0 20px 50px rgba(230,57,80,0.2);
  transform: translateY(-6px);
}

.r-day-card.locked {
  border-color: rgba(230,57,80,0.4);
  animation: lockedGlow 3s ease-in-out infinite;
}

@keyframes lockedGlow {
  0%, 100% { box-shadow: 0 0 0 0 rgba(230,57,80,0); }
  50%       { box-shadow: 0 0 0 4px rgba(230,57,80,0.15), 0 8px 24px rgba(230,57,80,0.12); }
}

/* ── Day image ───────────────────────────────────── */
.r-day-img-wrap {
  position: relative;
  aspect-ratio: 3/4;
  overflow: hidden;
  background: #f5ede8;
}

.r-day-img {
  width: 100%; height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.5s cubic-bezier(0.4,0,0.2,1);
}

.r-day-card:hover .r-day-img { transform: scale(1.07); }

.r-day-img-empty {
  width: 100%; height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-3);
  background: linear-gradient(135deg, #fdf0ee 0%, #ffeee8 100%);
}

.r-day-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(26,5,5,0.5) 0%, transparent 55%);
  pointer-events: none;
}

/* ── Day badge ───────────────────────────────────── */
.r-day-label {
  position: absolute;
  top: 12px;
  left: 12px;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.1em;
  color: white;
  background: rgba(26,5,5,0.55);
  backdrop-filter: blur(6px);
  padding: 4px 9px;
  border-radius: 100px;
  z-index: 2;
}

.r-day-label.locked {
  background: var(--grad);
}

/* ── Controls ────────────────────────────────────── */
.r-day-controls {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  z-index: 2;
  opacity: 0;
  transform: translateX(6px);
  transition: opacity 0.2s, transform 0.2s;
}

.r-day-card:hover .r-day-controls {
  opacity: 1;
  transform: translateX(0);
}

.r-ctrl {
  width: 26px; height: 26px;
  border-radius: 50%;
  border: none;
  background: rgba(255,255,255,0.92);
  color: var(--text);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s;
  backdrop-filter: blur(6px);
}

.r-ctrl:hover:not(:disabled) {
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  transform: scale(1.1);
}

.r-ctrl.locked {
  background: var(--coral);
  color: white;
}

.r-ctrl:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

/* ── Day body ────────────────────────────────────── */
.r-day-body {
  padding: 14px 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  flex: 1;
}

.r-day-date {
  font-size: 10.5px;
  font-weight: 600;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.r-src-badge {
  font-size: 9.5px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 2px 8px;
  border-radius: 100px;
  align-self: flex-start;
}

.s-ica    { background: #fff0f0; color: #cc0000; }
.s-coop   { background: #fff8e1; color: #c67c00; }
.s-mathem { background: #f0f4ff; color: #3a5bcd; }
.s-arla   { background: #f0f8ff; color: #0066cc; }
.s-koket  { background: #fdf4ff; color: #8b22b5; }
.s-custom { background: #f0fdf4; color: #166534; }

.r-recipe-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--text);
  line-height: 1.3;
  letter-spacing: -0.01em;
  font-family: 'Playfair Display', serif;
}

.r-recipe-meta {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.r-meta {
  display: flex;
  align-items: center;
  gap: 3px;
  font-size: 10.5px;
  color: var(--text-3);
  font-weight: 500;
}

.r-recipe-link {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 11px;
  font-weight: 700;
  color: var(--coral);
  text-decoration: none;
  transition: gap 0.15s;
  margin-top: 2px;
  width: fit-content;
}

.r-recipe-link:hover { gap: 6px; }

/* ── Empty day ───────────────────────────────────── */
.r-empty-label {
  font-size: 12px;
  color: var(--text-3);
  font-style: italic;
}

.r-pick-btn {
  padding: 6px 12px;
  border-radius: 100px;
  border: 1.5px dashed rgba(230,57,80,0.4);
  background: rgba(230,57,80,0.04);
  color: var(--coral);
  font-size: 11.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  font-family: 'Inter', sans-serif;
  align-self: flex-start;
  margin-top: 4px;
}

.r-pick-btn:hover {
  background: rgba(230,57,80,0.1);
  border-style: solid;
  transform: scale(1.02);
}

/* ── Responsive ──────────────────────────────────── */
@media (max-width: 1100px) {
  .r-week-strip { grid-template-columns: repeat(4, 1fr); }
  .r-header { grid-template-columns: 1fr; }
  .r-header-cards { grid-column: 1; }
}

@media (max-width: 700px) {
  .r-week-strip { grid-template-columns: repeat(2, 1fr); }
  .r-title { font-size: 36px; }
  .r-nav-center { display: none; }
}
</style>
