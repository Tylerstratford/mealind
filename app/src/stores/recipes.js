import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const CUSTOM_KEY = 'mealmind_custom_recipes'

export const useRecipeStore = defineStore('recipes', () => {
  const scraped = ref([])   // from recipes.json
  const custom = ref([])    // from localStorage
  const loading = ref(false)

  // All recipes merged, custom ones first so they appear at the top
  const recipes = computed(() => [...custom.value, ...scraped.value])

  async function loadRecipes() {
    loading.value = true
    try {
      const res = await fetch('/data/recipes.json')
      scraped.value = await res.json()
    } catch (e) {
      console.warn('No recipes.json found, using empty list.')
      scraped.value = []
    }
    // Load custom recipes from localStorage
    try {
      const stored = localStorage.getItem(CUSTOM_KEY)
      custom.value = stored ? JSON.parse(stored) : []
    } catch (e) {
      custom.value = []
    }
    loading.value = false
  }

  function saveCustom(recipe) {
    const existing = custom.value.findIndex(r => r.id === recipe.id)
    if (existing >= 0) {
      custom.value[existing] = recipe  // edit
    } else {
      custom.value.unshift(recipe)     // add new at top
    }
    localStorage.setItem(CUSTOM_KEY, JSON.stringify(custom.value))
  }

  function deleteCustom(id) {
    custom.value = custom.value.filter(r => r.id !== id)
    localStorage.setItem(CUSTOM_KEY, JSON.stringify(custom.value))
  }

  const bySource = computed(() => {
    const map = {}
    for (const r of recipes.value) {
      if (!map[r.source]) map[r.source] = []
      map[r.source].push(r)
    }
    return map
  })

  function getById(id) {
    return recipes.value.find(r => r.id === id)
  }

  function getRandom(count = 7, exclude = [], sources = []) {
    let pool = recipes.value.filter(r => !exclude.includes(r.id))
    if (sources.length) pool = pool.filter(r => sources.includes(r.source))
    const shuffled = [...pool].sort(() => Math.random() - 0.5)
    return shuffled.slice(0, count)
  }

  return { recipes, custom, loading, loadRecipes, saveCustom, deleteCustom, bySource, getById, getRandom }
})
