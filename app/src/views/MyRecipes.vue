<template>
  <div class="page">
    <div class="mb-7 flex flex-wrap items-start justify-between gap-4">
      <div>
        <h1 class="page-title">My Recipes</h1>
        <p class="page-sub">{{ recipeStore.custom.length }} custom recipe{{ recipeStore.custom.length !== 1 ? 's' : '' }} saved.</p>
      </div>
      <router-link to="/add-recipe">
        <Button><AppIcon name="plus" :size="15" /> Add Recipe</Button>
      </router-link>
    </div>

    <div v-if="recipeStore.custom.length === 0" class="flex flex-col items-center gap-3 py-16 text-center text-muted-foreground">
      <AppIcon name="book" :size="48" color="#d1d5db" :stroke-width="1" />
      <h3 class="text-lg font-semibold text-foreground">No custom recipes yet</h3>
      <p>Add your own recipes or import them from a URL.</p>
      <router-link to="/add-recipe"><Button>Add your first recipe</Button></router-link>
    </div>

    <div v-else class="flex flex-col gap-4">
      <Card v-for="recipe in recipeStore.custom" :key="recipe.id" class="flex overflow-hidden">
        <div class="shrink-0">
          <img v-if="recipe.image" :src="recipe.image" :alt="recipe.name"
            class="h-36 w-44 object-cover bg-muted block max-sm:w-full max-sm:h-40" />
          <div v-else class="flex h-36 w-44 items-center justify-center bg-muted max-sm:w-full max-sm:h-40">
            <AppIcon name="image" :size="36" color="#d1d5db" :stroke-width="1" />
          </div>
        </div>
        <div class="flex flex-1 min-w-0 flex-col gap-2 p-4">
          <div class="flex items-center justify-between">
            <Badge variant="outline" class="badge-custom">custom</Badge>
            <div class="flex gap-1">
              <Button as-child variant="ghost" size="icon" class="h-8 w-8 text-muted-foreground">
                <router-link :to="`/edit-recipe/${recipe.id}`" title="Edit">
                  <AppIcon name="edit" :size="15" />
                </router-link>
              </Button>
              <Button variant="ghost" size="icon" class="h-8 w-8 hover:bg-destructive/10 hover:text-destructive"
                title="Delete" @click="deleteRecipe(recipe.id)">
                <AppIcon name="trash" :size="15" />
              </Button>
            </div>
          </div>
          <h3 class="text-[17px] font-bold leading-snug">{{ recipe.name }}</h3>
          <div class="flex flex-wrap gap-3 text-[12px] text-muted-foreground">
            <span v-if="recipe.time" class="flex items-center gap-1"><AppIcon name="clock" :size="12" /> {{ recipe.time }}</span>
            <span v-if="recipe.servings" class="flex items-center gap-1"><AppIcon name="user" :size="12" /> {{ recipe.servings }}</span>
            <span v-if="recipe.ingredients?.length" class="flex items-center gap-1">
              <AppIcon name="clipboard" :size="12" /> {{ recipe.ingredients.length }} ingredients
            </span>
          </div>
          <p v-if="recipe.description" class="line-clamp-2 text-[13px] leading-relaxed text-muted-foreground">
            {{ recipe.description }}
          </p>
          <div v-if="recipe.tags?.length" class="flex flex-wrap gap-1.5">
            <Badge v-for="tag in recipe.tags" :key="tag" variant="secondary" class="text-[11px]">{{ tag }}</Badge>
          </div>
          <div class="mt-auto flex items-center gap-2.5 pt-1">
            <a v-if="recipe.url" :href="recipe.url" target="_blank"
              class="flex items-center gap-1 text-[12px] font-medium text-primary hover:underline">
              View source <AppIcon name="externallink" :size="11" />
            </a>
            <Button variant="outline" size="sm" @click="addToPlanner(recipe)">
              <AppIcon name="calendar" :size="13" /> Add to planner
            </Button>
          </div>
        </div>
      </Card>
    </div>

    <!-- Day picker modal -->
    <Teleport to="body">
      <div v-if="pickingRecipe" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
        @click.self="pickingRecipe = null">
        <Card class="flex w-[90%] max-w-sm flex-col gap-3.5 p-6">
          <h3 class="text-[17px] font-bold">Add to Meal Planner</h3>
          <p class="text-[13px] text-muted-foreground">Choose a day for "{{ pickingRecipe.name }}"</p>
          <div class="flex flex-col gap-1">
            <button v-for="day in mealPlan.DAYS" :key="day"
              class="rounded-lg border border-border px-3.5 py-2 text-left text-sm text-foreground transition-colors hover:border-primary hover:bg-secondary hover:text-secondary-foreground"
              @click="confirmAddToDay(day)">{{ day }}</button>
          </div>
          <div class="flex justify-end">
            <Button variant="outline" @click="pickingRecipe = null">Cancel</Button>
          </div>
        </Card>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRecipeStore } from '@/stores/recipes'
import { useMealPlanStore } from '@/stores/mealplan'
import { useToast } from '@/composables/useToast'
import AppIcon from '@/components/AppIcon.vue'
import Button from '@/components/ui/button.vue'
import Card from '@/components/ui/card.vue'
import Badge from '@/components/ui/badge.vue'

const recipeStore = useRecipeStore()
const mealPlan = useMealPlanStore()
const toast = useToast()
const pickingRecipe = ref(null)

onMounted(() => recipeStore.loadRecipes())

function deleteRecipe(id) {
  if (confirm('Delete this recipe?')) {
    recipeStore.deleteCustom(id)
    toast.success('Recipe deleted.')
  }
}

function addToPlanner(recipe) { pickingRecipe.value = recipe }

function confirmAddToDay(day) {
  mealPlan.setDay(day, pickingRecipe.value.id)
  toast.success(`"${pickingRecipe.value.name}" added to ${day}.`)
  pickingRecipe.value = null
}
</script>
