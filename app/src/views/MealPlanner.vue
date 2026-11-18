<template>
  <div class="page" @click="showSavePanel = false">
    <!-- Header -->
    <div class="mb-7 flex flex-wrap items-start justify-between gap-4">
      <div>
        <h1 class="page-title">Meal Planner</h1>
        <p class="page-sub">Generate a 7-day plan. Lock meals you like, then regenerate the rest.</p>
      </div>
      <div class="flex flex-wrap items-center gap-2 pt-2">
        <Button variant="secondary" @click="generatePlan">
          <AppIcon name="shuffle" :size="15" /> Generate Plan
        </Button>
        <div class="relative">
          <Button variant="outline" @click.stop="toggleSavePanel">
            <AppIcon name="save" :size="15" /> Saved Plans
            <span v-if="mealPlan.savedPlans.length"
              class="ml-1 rounded-full bg-primary px-1.5 py-0.5 text-[11px] font-semibold text-primary-foreground leading-none">
              {{ mealPlan.savedPlans.length }}
            </span>
          </Button>
          <div v-if="showSavePanel"
            class="absolute right-0 top-[calc(100%+8px)] z-50 w-80 rounded-lg border border-border bg-card p-4 shadow-lg flex flex-col gap-3"
            @click.stop>
            <div class="flex items-center justify-between">
              <h4 class="text-[15px] font-semibold">Saved Plans</h4>
              <Button variant="ghost" size="icon" class="h-7 w-7" @click="showSavePanel = false">
                <AppIcon name="x" :size="15" />
              </Button>
            </div>
            <div class="flex flex-col gap-2">
              <Input v-model="saveName" placeholder="Plan name…" @keydown.enter="saveCurrentPlan" />
              <div class="flex items-center gap-2">
                <span class="text-xs text-muted-foreground whitespace-nowrap">Week of</span>
                <input v-model="saveWeek" type="date"
                  class="flex h-9 flex-1 rounded-md border border-input bg-background px-3 py-1 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring" />
              </div>
              <Button variant="secondary" size="sm" class="self-end" @click="saveCurrentPlan">Save current plan</Button>
            </div>
            <p v-if="mealPlan.savedPlans.length === 0" class="text-center text-[13px] text-muted-foreground py-2">No saved plans yet.</p>
            <div class="flex max-h-64 flex-col gap-1.5 overflow-y-auto">
              <div v-for="p in mealPlan.savedPlans" :key="p.id"
                class="flex items-center justify-between gap-2 rounded-lg border border-border px-2.5 py-2">
                <div class="flex min-w-0 flex-1 flex-col gap-0.5">
                  <span class="truncate text-sm font-medium">{{ p.name }}</span>
                  <span class="text-[12px] text-muted-foreground">{{ weekRangeLabel(p.weekStart) }}</span>
                </div>
                <div class="flex shrink-0 items-center gap-1">
                  <Button variant="outline" size="sm" class="h-7 text-xs" @click="viewingPlan = p; showSavePanel = false">
                    <AppIcon name="calendar" :size="12" /> View
                  </Button>
                  <Button variant="secondary" size="sm" class="h-7 text-xs" @click="loadSavedPlan(p)">Load</Button>
                  <Button variant="ghost" size="icon" class="h-7 w-7 hover:bg-destructive/10 hover:text-destructive"
                    @click="mealPlan.deleteSavedPlan(p.id)">
                    <AppIcon name="trash" :size="13" />
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <Button @click="goToShopping" :disabled="!hasFullPlan">
          <AppIcon name="cart" :size="15" /> Build Shopping List
        </Button>
      </div>
    </div>

    <!-- Source filters -->
    <div v-if="availableSources.length > 1" class="mb-5 flex flex-wrap items-center gap-2">
      <span class="text-[13px] font-medium text-muted-foreground">Sources:</span>
      <Badge v-for="src in availableSources" :key="src" variant="outline"
        :class="['badge-' + src, 'cursor-pointer select-none px-3 py-1 transition-all',
          mealPlan.activeSources.includes(src) ? 'ring-2 ring-primary ring-offset-1' : '']"
        @click="mealPlan.toggleSource(src)">
        {{ src }}
      </Badge>
      <span v-if="mealPlan.activeSources.length" class="text-[12px] italic text-muted-foreground">
        Only selected sources will be used when generating
      </span>
    </div>

    <div v-if="recipeStore.loading" class="flex flex-col items-center gap-3 py-16 text-muted-foreground">Loading recipes…</div>

    <div v-else-if="recipeStore.recipes.length === 0" class="flex flex-col items-center gap-3 py-16 text-center text-muted-foreground">
      <AppIcon name="book" :size="48" color="#d1d5db" :stroke-width="1" />
      <h3 class="text-lg font-semibold text-foreground">No recipes yet</h3>
      <p>Run the scraper to populate your recipe database, then come back here.</p>
      <code class="rounded-lg bg-[#1e1e2e] px-5 py-3 text-[13px] text-[#cdd6f4]">cd scraper && python3 scrape_all.py</code>
    </div>

    <div v-else class="grid gap-4" style="grid-template-columns: repeat(auto-fill, minmax(280px, 1fr))">
      <Card v-for="{ day, locked, recipe } in mealPlan.plannedRecipes" :key="day"
        :class="['p-4 transition-shadow', locked ? 'border-primary bg-secondary' : '']">
        <div class="mb-3 flex items-center justify-between">
          <span class="text-[15px] font-bold">{{ day }}</span>
          <div class="flex gap-0.5">
            <Button variant="ghost" size="icon" class="h-8 w-8"
              :class="locked ? 'text-primary' : 'text-muted-foreground'"
              :title="locked ? 'Unlock' : 'Lock this meal'"
              @click="mealPlan.toggleLock(day)">
              <AppIcon :name="locked ? 'lock' : 'unlock'" :size="15" />
            </Button>
            <Button variant="ghost" size="icon" class="h-8 w-8 text-muted-foreground"
              title="Swap for a different recipe" @click="mealPlan.swapDay(day)" :disabled="locked">
              <AppIcon name="swap" :size="15" />
            </Button>
          </div>
        </div>
        <div v-if="recipe" class="flex flex-col gap-2.5">
          <img v-if="recipe.image" :src="recipe.image" :alt="recipe.name" class="h-36 w-full rounded-lg object-cover bg-muted" />
          <div v-else class="flex h-36 items-center justify-center rounded-lg bg-muted">
            <AppIcon name="image" :size="36" color="#d1d5db" :stroke-width="1" />
          </div>
          <div class="flex flex-col gap-1.5">
            <Badge variant="outline" :class="['badge-' + recipe.source, 'self-start']">{{ recipe.source }}</Badge>
            <h3 class="text-[15px] font-semibold leading-snug">{{ recipe.name }}</h3>
            <div class="flex flex-wrap gap-2.5 text-[12px] text-muted-foreground">
              <span v-if="recipe.time" class="flex items-center gap-1"><AppIcon name="clock" :size="12" /> {{ recipe.time }}</span>
              <span v-if="recipe.servings" class="flex items-center gap-1"><AppIcon name="user" :size="12" /> {{ recipe.servings }}</span>
              <span v-if="recipe.tags?.length" class="flex items-center gap-1"><AppIcon name="tag" :size="12" /> {{ recipe.tags.slice(0,2).join(', ') }}</span>
            </div>
            <a v-if="recipe.url" :href="recipe.url" target="_blank"
              class="flex w-fit items-center gap-1 text-[12px] font-medium text-primary hover:underline">
              View recipe <AppIcon name="externallink" :size="11" />
            </a>
          </div>
        </div>
        <div v-else class="flex flex-col items-center gap-2.5 py-6 text-sm text-muted-foreground">
          <span>No recipe selected</span>
          <Button variant="outline" size="sm" @click="mealPlan.swapDay(day)">Pick one</Button>
        </div>
      </Card>
    </div>
  </div>

  <!-- Weekly view modal -->
  <Teleport to="body">
    <div v-if="viewingPlan" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-5"
      @click.self="viewingPlan = null">
      <Card class="flex w-full max-w-[1060px] max-h-[90vh] flex-col gap-5 overflow-y-auto p-6">
        <div class="flex items-start justify-between gap-4">
          <div class="flex flex-col gap-1">
            <h2 class="text-xl font-bold">{{ viewingPlan.name }}</h2>
            <span class="text-sm text-muted-foreground">{{ weekRangeLabel(viewingPlan.weekStart) }}</span>
          </div>
          <div class="flex shrink-0 items-center gap-2">
            <Button size="sm" @click="loadSavedPlan(viewingPlan)">
              <AppIcon name="download" :size="14" /> Load plan
            </Button>
            <Button variant="ghost" size="icon" class="h-8 w-8" @click="viewingPlan = null">
              <AppIcon name="x" :size="16" />
            </Button>
          </div>
        </div>
        <div class="grid gap-2.5 overflow-x-auto" style="grid-template-columns: repeat(7, minmax(120px, 1fr))">
          <div v-for="(dayData, idx) in mealPlan.DAYS" :key="dayData" class="flex min-w-[120px] flex-col gap-2">
            <div class="flex flex-col gap-0.5 border-b-2 border-border pb-2">
              <span class="text-[15px] font-bold">{{ dayData.slice(0,3) }}</span>
              <span class="text-[12px] text-muted-foreground">{{ dayDateLabel(viewingPlan.weekStart, idx) }}</span>
            </div>
            <template v-if="planRecipe(viewingPlan, dayData)">
              <div class="overflow-hidden rounded-lg">
                <img v-if="planRecipe(viewingPlan, dayData).image"
                  :src="planRecipe(viewingPlan, dayData).image"
                  :alt="planRecipe(viewingPlan, dayData).name"
                  class="aspect-[4/3] w-full object-cover bg-muted block" />
                <div v-else class="flex aspect-[4/3] items-center justify-center bg-muted">
                  <AppIcon name="image" :size="28" color="#d1d5db" :stroke-width="1" />
                </div>
              </div>
              <div class="flex flex-col gap-1">
                <Badge variant="outline" :class="['badge-' + planRecipe(viewingPlan, dayData).source, 'self-start']">
                  {{ planRecipe(viewingPlan, dayData).source }}
                </Badge>
                <p class="text-[13px] font-semibold leading-snug">{{ planRecipe(viewingPlan, dayData).name }}</p>
                <div class="flex flex-wrap gap-1.5 text-[11px] text-muted-foreground">
                  <span v-if="planRecipe(viewingPlan, dayData).time" class="flex items-center gap-0.5">
                    <AppIcon name="clock" :size="11" /> {{ planRecipe(viewingPlan, dayData).time }}
                  </span>
                  <span v-if="planRecipe(viewingPlan, dayData).servings" class="flex items-center gap-0.5">
                    <AppIcon name="user" :size="11" /> {{ planRecipe(viewingPlan, dayData).servings }}
                  </span>
                </div>
              </div>
            </template>
            <div v-else class="py-4 text-center text-[13px] text-muted-foreground">No meal</div>
          </div>
        </div>
      </Card>
    </div>
  </Teleport>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useRecipeStore } from '@/stores/recipes'
import { useMealPlanStore } from '@/stores/mealplan'
import { useToast } from '@/composables/useToast'
import AppIcon from '@/components/AppIcon.vue'
import Button from '@/components/ui/button.vue'
import Card from '@/components/ui/card.vue'
import Badge from '@/components/ui/badge.vue'
import Input from '@/components/ui/input.vue'

const router = useRouter()
const recipeStore = useRecipeStore()
const mealPlan = useMealPlanStore()
const toast = useToast()

const showSavePanel = ref(false)
const saveName = ref('')
const saveWeek = ref(mealPlan.getMondayOfCurrentWeek())
const viewingPlan = ref(null)

onMounted(async () => { await recipeStore.loadRecipes() })

const hasFullPlan = computed(() => mealPlan.plannedRecipes.every(({ recipe }) => recipe != null))

const SOURCE_ORDER = ['ica', 'coop', 'mathem', 'arla', 'koket']
const availableSources = computed(() => {
  const present = new Set(recipeStore.recipes.map(r => r.source))
  return SOURCE_ORDER.filter(s => present.has(s)).concat([...present].filter(s => !SOURCE_ORDER.includes(s)))
})

function generatePlan() { if (recipeStore.recipes.length === 0) return; mealPlan.generate() }
function goToShopping() { router.push('/shopping') }
function toggleSavePanel() { showSavePanel.value = !showSavePanel.value }

function saveCurrentPlan() {
  const name = saveName.value.trim() || `Plan ${new Date().toLocaleDateString('sv-SE')}`
  mealPlan.savePlan(name, saveWeek.value)
  saveName.value = ''
  saveWeek.value = mealPlan.getMondayOfCurrentWeek()
  toast.success(`"${name}" saved.`)
}

function loadSavedPlan(p) {
  mealPlan.loadPlan(p)
  showSavePanel.value = false
  viewingPlan.value = null
  toast.success(`"${p.name}" loaded.`)
}

function weekRangeLabel(weekStart) {
  if (!weekStart) return ''
  const start = new Date(weekStart + 'T00:00:00')
  const end = new Date(start)
  end.setDate(end.getDate() + 6)
  const fmt = (d) => d.toLocaleDateString('en', { month: 'short', day: 'numeric' })
  return `${fmt(start)} – ${fmt(end)}, ${end.getFullYear()}`
}

function dayDateLabel(weekStart, idx) {
  if (!weekStart) return ''
  const date = new Date(weekStart + 'T00:00:00')
  date.setDate(date.getDate() + idx)
  return date.toLocaleDateString('en', { month: 'short', day: 'numeric' })
}

function planRecipe(plan, day) {
  const id = plan.days[day]?.recipeId
  return id ? recipeStore.getById(id) : null
}
</script>
