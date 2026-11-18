<template>
  <div class="page" @click="closePicker">
    <h1 class="page-title">📖 Recipe Database</h1>
    <p class="page-sub">{{ recipeStore.recipes.length }} recipes loaded. Filter or browse below.</p>

    <!-- Filters -->
    <div class="mb-6 flex flex-col gap-3">
      <Input v-model="search" type="search" placeholder="Search recipes…" class="max-w-sm" />
      <div class="flex flex-wrap gap-2">
        <Badge v-for="src in sources" :key="src" variant="outline"
          :class="['badge-' + src, 'cursor-pointer select-none px-3 py-1 transition-all',
            activeSource === src ? 'ring-2 ring-primary ring-offset-1' : '']"
          @click="activeSource = activeSource === src ? null : src">
          {{ src }}
        </Badge>
        <Badge variant="outline"
          :class="['cursor-pointer select-none px-3 py-1 transition-all',
            activeSource === null ? 'ring-2 ring-primary ring-offset-1' : '']"
          @click="activeSource = null">
          All
        </Badge>
      </div>
    </div>

    <!-- Grid -->
    <div class="grid gap-4" style="grid-template-columns: repeat(auto-fill, minmax(220px, 1fr))">
      <Card v-for="recipe in filtered" :key="recipe.id" class="flex flex-col overflow-hidden transition-shadow hover:shadow-md">
        <a :href="recipe.url || '#'" :target="recipe.url ? '_blank' : '_self'" class="block overflow-hidden">
          <img v-if="recipe.image" :src="recipe.image" :alt="recipe.name" class="h-36 w-full object-cover bg-muted" />
          <div v-else class="flex h-36 items-center justify-center bg-muted text-4xl">🍽️</div>
        </a>
        <div class="flex flex-1 flex-col gap-1.5 p-3">
          <div class="flex items-center justify-between">
            <Badge variant="outline" :class="'badge-' + recipe.source">{{ recipe.source }}</Badge>
            <div class="flex items-center gap-0.5" @click.stop>
              <div class="relative">
                <Button variant="ghost" size="icon" class="h-7 w-7 text-muted-foreground"
                  title="Add to meal planner" @click="togglePicker(recipe.id)">
                  <AppIcon name="calendar" :size="14" />
                </Button>
                <div v-if="activePicker === recipe.id"
                  class="absolute right-0 top-[calc(100%+4px)] z-50 flex min-w-[120px] flex-col gap-0.5 rounded-lg border border-border bg-card p-1 shadow-md">
                  <button v-for="day in mealPlan.DAYS" :key="day"
                    class="rounded-md px-3 py-1.5 text-left text-sm text-foreground transition-colors hover:bg-accent"
                    @click="addToDay(recipe.id, day)">{{ day }}</button>
                </div>
              </div>
              <template v-if="isCustom(recipe.id)">
                <Button as-child variant="ghost" size="icon" class="h-7 w-7 text-muted-foreground">
                  <router-link :to="`/edit-recipe/${recipe.id}`" title="Edit">✏️</router-link>
                </Button>
                <Button variant="ghost" size="icon" class="h-7 w-7 hover:bg-destructive/10 hover:text-destructive"
                  title="Delete" @click="deleteRecipe(recipe.id)">🗑️</Button>
              </template>
            </div>
          </div>
          <h3 class="text-[14px] font-semibold leading-snug">{{ recipe.name }}</h3>
          <div class="flex gap-2.5 text-[12px] text-muted-foreground">
            <span v-if="recipe.time" class="flex items-center gap-1"><AppIcon name="clock" :size="12" /> {{ recipe.time }}</span>
            <span v-if="recipe.servings" class="flex items-center gap-1"><AppIcon name="user" :size="12" /> {{ recipe.servings }}</span>
          </div>
        </div>
      </Card>
    </div>

    <div v-if="filtered.length === 0 && recipeStore.recipes.length > 0"
      class="py-16 text-center text-muted-foreground">No recipes match your filter.</div>
    <div v-if="recipeStore.recipes.length === 0"
      class="flex flex-col items-center gap-3 py-16 text-center text-muted-foreground">
      <div class="text-5xl">🌿</div>
      <h3 class="text-lg font-semibold text-foreground">Database is empty</h3>
      <p>Run the scraper first:</p>
      <code class="rounded-lg bg-[#1e1e2e] px-5 py-3 text-[13px] text-[#cdd6f4]">cd scraper && python scrape_all.py</code>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRecipeStore } from '@/stores/recipes'
import { useMealPlanStore } from '@/stores/mealplan'
import { useToast } from '@/composables/useToast'
import AppIcon from '@/components/AppIcon.vue'
import Button from '@/components/ui/button.vue'
import Card from '@/components/ui/card.vue'
import Badge from '@/components/ui/badge.vue'
import Input from '@/components/ui/input.vue'

const recipeStore = useRecipeStore()
const mealPlan = useMealPlanStore()
const toast = useToast()
const search = ref('')
const activeSource = ref(null)
const activePicker = ref(null)

onMounted(() => recipeStore.loadRecipes())

const SOURCE_ORDER = ['ica', 'coop', 'mathem', 'arla', 'koket']
const sources = computed(() => {
  const present = new Set(recipeStore.recipes.map(r => r.source))
  return SOURCE_ORDER.filter(s => present.has(s)).concat([...present].filter(s => !SOURCE_ORDER.includes(s)))
})

const filtered = computed(() => recipeStore.recipes.filter(r => {
  const matchSearch = !search.value || r.name.toLowerCase().includes(search.value.toLowerCase())
  const matchSource = !activeSource.value || r.source === activeSource.value
  return matchSearch && matchSource
}))

const customIds = computed(() => new Set(recipeStore.custom.map(r => r.id)))
function isCustom(id) { return customIds.value.has(id) }
function togglePicker(id) { activePicker.value = activePicker.value === id ? null : id }
function closePicker() { activePicker.value = null }

function addToDay(recipeId, day) {
  mealPlan.setDay(day, recipeId)
  activePicker.value = null
  const recipe = recipeStore.recipes.find(r => r.id === recipeId)
  toast.success(`"${recipe?.name}" added to ${day}.`)
}

function deleteRecipe(id) {
  if (confirm('Delete this recipe?')) {
    recipeStore.deleteCustom(id)
    toast.success('Recipe deleted.')
  }
}
</script>
