import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRecipeStore } from './recipes'

const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

export const useMealPlanStore = defineStore('mealplan', () => {
  const recipeStore = useRecipeStore()

  // plan: { Monday: { locked: false, recipeId: 'xxx' }, ... }
  const plan = ref(Object.fromEntries(DAYS.map(d => [d, { locked: false, recipeId: null }])))

  // Saved plans persisted to localStorage
  const savedPlans = ref(JSON.parse(localStorage.getItem('mealmind-saved-plans') || '[]'))

  function persistSavedPlans() {
    localStorage.setItem('mealmind-saved-plans', JSON.stringify(savedPlans.value))
  }

  function getMondayOfCurrentWeek() {
    const now = new Date()
    const day = now.getDay()
    const diff = day === 0 ? -6 : 1 - day
    const monday = new Date(now)
    monday.setDate(now.getDate() + diff)
    return monday.toISOString().split('T')[0]
  }

  function savePlan(name, weekStart) {
    const snapshot = {
      id: Date.now().toString(),
      name,
      savedAt: new Date().toLocaleDateString('sv-SE'),
      weekStart: weekStart || getMondayOfCurrentWeek(),
      days: Object.fromEntries(
        DAYS.map(d => [d, { recipeId: plan.value[d].recipeId }])
      )
    }
    savedPlans.value.unshift(snapshot)
    persistSavedPlans()
  }

  function loadPlan(savedPlan) {
    DAYS.forEach(d => {
      plan.value[d].recipeId = savedPlan.days[d]?.recipeId ?? null
      plan.value[d].locked = false
    })
  }

  function deleteSavedPlan(id) {
    savedPlans.value = savedPlans.value.filter(p => p.id !== id)
    persistSavedPlans()
  }

  // Source filter for generate/swap (empty = all sources)
  const activeSources = ref([])

  function toggleSource(source) {
    const idx = activeSources.value.indexOf(source)
    if (idx >= 0) activeSources.value.splice(idx, 1)
    else activeSources.value.push(source)
  }

  function generate() {
    const lockedIds = DAYS
      .filter(d => plan.value[d].locked && plan.value[d].recipeId)
      .map(d => plan.value[d].recipeId)

    const unlockedDays = DAYS.filter(d => !plan.value[d].locked)
    const picks = recipeStore.getRandom(unlockedDays.length, lockedIds, activeSources.value)

    unlockedDays.forEach((day, i) => {
      plan.value[day].recipeId = picks[i]?.id ?? null
    })
  }

  function toggleLock(day) {
    plan.value[day].locked = !plan.value[day].locked
  }

  function swapDay(day) {
    const lockedIds = DAYS
      .filter(d => plan.value[d].locked && plan.value[d].recipeId)
      .map(d => plan.value[d].recipeId)
    const currentIds = DAYS.map(d => plan.value[d].recipeId).filter(Boolean)
    const pick = recipeStore.getRandom(1, [...lockedIds, ...currentIds], activeSources.value)
    if (pick[0]) plan.value[day].recipeId = pick[0].id
  }

  function setDay(day, recipeId) {
    plan.value[day].recipeId = recipeId
  }

  const plannedRecipes = computed(() => {
    return DAYS.map(day => ({
      day,
      locked: plan.value[day].locked,
      recipe: recipeStore.getById(plan.value[day].recipeId)
    }))
  })

  // Build aggregated ingredient list from all planned recipes
  const shoppingIngredients = computed(() => {
    const map = {}
    for (const { recipe } of plannedRecipes.value) {
      if (!recipe) continue
      for (const ing of (recipe.ingredients || [])) {
        const key = ing.name.toLowerCase().trim()
        if (map[key]) {
          map[key].recipes.push(recipe.name)
          // Simple quantity aggregation (same unit only)
          if (map[key].unit === ing.unit && ing.quantity) {
            map[key].quantity = (parseFloat(map[key].quantity) || 0) + (parseFloat(ing.quantity) || 0)
          }
        } else {
          map[key] = { ...ing, recipes: [recipe.name], checked: false }
        }
      }
    }
    return Object.values(map)
  })

  return { plan, DAYS, activeSources, toggleSource, generate, toggleLock, swapDay, setDay, plannedRecipes, shoppingIngredients, savedPlans, savePlan, loadPlan, deleteSavedPlan, getMondayOfCurrentWeek }
})
