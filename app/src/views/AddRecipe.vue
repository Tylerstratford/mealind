<template>
  <div class="page">
    <div class="mb-5 flex items-start justify-between gap-4">
      <div>
        <h1 class="page-title">{{ isEditing ? '✏️ Edit Recipe' : '➕ Add Recipe' }}</h1>
        <p class="page-sub">{{ isEditing ? 'Update your custom recipe.' : 'Add your own recipe to the meal planner.' }}</p>
      </div>
      <Button variant="outline" @click="$router.back()">← Back</Button>
    </div>

    <!-- URL Import -->
    <Card v-if="!isEditing" class="mb-5 max-w-[760px] p-5">
      <div class="flex flex-col gap-2.5">
        <div class="flex flex-col gap-0.5">
          <span class="text-[15px] font-bold">🔗 Import from URL</span>
          <span class="text-[13px] text-muted-foreground">Paste a recipe URL and we'll fill in the form automatically</span>
        </div>
        <div class="flex gap-2.5">
          <Input v-model="fetchUrl" placeholder="https://www.ica.se/recept/…" class="flex-1"
            @keydown.enter.prevent="fetchFromUrl" />
          <Button @click="fetchFromUrl" :disabled="fetching">
            <span v-if="fetching">⏳ Fetching…</span>
            <span v-else>↓ Import</span>
          </Button>
        </div>
        <div v-if="fetchError" class="rounded-lg bg-destructive/10 px-3 py-2 text-[13px] text-destructive">
          ⚠ {{ fetchError }}
        </div>
        <div v-if="fetchPartial" class="rounded-lg bg-yellow-50 px-3 py-2 text-[13px] text-yellow-800">
          ⚠ Some fields couldn't be extracted automatically — please review and fill in what's missing.
        </div>
        <p class="text-[12px] text-muted-foreground">
          Requires the local scraper server: <code class="rounded bg-[#1e1e2e] px-2 py-0.5 text-[11px] text-[#cdd6f4]">cd scraper && python3 server.py</code>
        </p>
      </div>
    </Card>

    <form @submit.prevent="save" class="flex max-w-[760px] flex-col gap-5" novalidate>

      <!-- Basic Info -->
      <Card class="p-6">
        <h2 class="mb-4 text-base font-bold">Basic Info</h2>
        <div class="flex flex-col gap-4">
          <div class="flex flex-col gap-1.5">
            <Label>Recipe name *</Label>
            <Input v-model="form.name" placeholder="e.g. Mormors köttbullar"
              :class="errors.name ? 'border-destructive ring-1 ring-destructive' : ''"
              @input="errors.name = ''" />
            <span v-if="errors.name" class="text-[12px] text-destructive">{{ errors.name }}</span>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="flex flex-col gap-1.5">
              <Label>Source / website</Label>
              <Input v-model="form.url" placeholder="https://… (optional)" />
            </div>
            <div class="flex flex-col gap-1.5">
              <Label>Label</Label>
              <Select v-model="form.source">
                <option value="custom">My recipe</option>
                <option value="ica">ICA</option>
                <option value="coop">Coop</option>
                <option value="mathem">Mathem</option>
                <option value="other">Other</option>
              </Select>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="flex flex-col gap-1.5">
              <Label>Cook time</Label>
              <Input v-model="form.time" placeholder="e.g. 30 min" />
            </div>
            <div class="flex flex-col gap-1.5">
              <Label>Servings</Label>
              <Input v-model="form.servings" placeholder="e.g. 4" />
            </div>
          </div>

          <!-- Image -->
          <div class="flex flex-col gap-1.5">
            <Label>Image</Label>
            <div class="flex flex-col gap-3">
              <div class="cursor-pointer overflow-hidden rounded-lg border-2 border-dashed border-border transition-colors hover:border-primary hover:bg-secondary/30"
                @click="triggerFileInput" @dragover.prevent @drop.prevent="onDrop">
                <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onFileSelected" />
                <div v-if="!form.image" class="flex flex-col items-center gap-1.5 p-8 text-center">
                  <span class="text-3xl">📷</span>
                  <span class="text-sm font-semibold">Click to upload or take photo</span>
                  <span class="text-[12px] text-muted-foreground">or drag & drop an image here</span>
                </div>
                <div v-else class="relative">
                  <img :src="form.image" alt="Preview" class="max-h-48 w-full object-cover"
                    @error="imageError = true" @load="imageError = false" />
                  <button type="button"
                    class="absolute right-2 top-2 rounded-md bg-black/60 px-2.5 py-1 text-[12px] text-white hover:bg-destructive"
                    @click.stop="form.image = ''">✕ Remove</button>
                  <span v-if="imageError" class="block p-2 text-[12px] text-destructive">⚠ Could not load image</span>
                </div>
              </div>
              <div class="flex flex-col gap-1">
                <span class="text-[12px] font-medium text-muted-foreground">or paste image URL</span>
                <Input v-model="imageUrlInput" placeholder="https://…" @change="applyImageUrl" @keydown.enter.prevent="applyImageUrl" />
              </div>
            </div>
          </div>

          <div class="flex flex-col gap-1.5">
            <Label>Description</Label>
            <Textarea v-model="form.description" :rows="3" placeholder="Short description of the recipe…" />
          </div>

          <div class="flex flex-col gap-1.5">
            <Label>Tags <span class="text-[12px] font-normal text-muted-foreground">(comma-separated, e.g. pasta, vegetarisk, snabb)</span></Label>
            <Input v-model="tagsInput" placeholder="pasta, vegetarisk, snabb" />
          </div>
        </div>
      </Card>

      <!-- Ingredients -->
      <Card :class="['p-6', errors.ingredients ? 'border-destructive' : '']">
        <div class="mb-4 flex items-center justify-between">
          <div>
            <h2 class="text-base font-bold">Ingredients *</h2>
            <span v-if="errors.ingredients" class="text-[12px] text-destructive">{{ errors.ingredients }}</span>
          </div>
          <Button type="button" variant="secondary" size="sm" @click="addIngredient">+ Add row</Button>
        </div>

        <div class="mb-2 grid gap-2 px-1 text-[12px] font-semibold uppercase tracking-wide text-muted-foreground"
          style="grid-template-columns: 80px 80px 1fr 32px">
          <span>Amount</span><span>Unit</span><span>Ingredient name</span><span></span>
        </div>

        <div v-for="(ing, i) in form.ingredients" :key="i"
          class="mb-2 grid items-center gap-2" style="grid-template-columns: 80px 80px 1fr 32px">
          <Input v-model="ing.quantity" placeholder="2" />
          <Input v-model="ing.unit" placeholder="msk" />
          <Input v-model="ing.name" placeholder="Vitlök" @input="errors.ingredients = ''" />
          <Button type="button" variant="ghost" size="icon"
            class="h-9 w-9 text-muted-foreground hover:bg-destructive/10 hover:text-destructive"
            @click="removeIngredient(i)" title="Remove">✕</Button>
        </div>

        <p v-if="form.ingredients.length === 0" class="py-4 text-center text-[13px] text-muted-foreground">
          No ingredients yet — click "+ Add row" to start.
        </p>
        <Button type="button" variant="outline" size="sm" class="mt-2" @click="addIngredient">+ Add ingredient</Button>
      </Card>

      <!-- Actions -->
      <div class="flex justify-end gap-3">
        <Button type="button" variant="outline" @click="$router.back()">Cancel</Button>
        <Button type="submit">{{ isEditing ? '💾 Save changes' : '✅ Add recipe' }}</Button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useRecipeStore } from '@/stores/recipes'
import { useToast } from '@/composables/useToast'
import Button from '@/components/ui/button.vue'
import Card from '@/components/ui/card.vue'
import Input from '@/components/ui/input.vue'
import Textarea from '@/components/ui/textarea.vue'
import Select from '@/components/ui/select.vue'
import Label from '@/components/ui/label.vue'

const router = useRouter()
const route = useRoute()
const recipeStore = useRecipeStore()
const toast = useToast()

const isEditing = computed(() => !!route.params.id)
const imageError = ref(false)
const tagsInput = ref('')
const imageUrlInput = ref('')
const fileInput = ref(null)

const errors = ref({ name: '', ingredients: '' })
const fetchUrl = ref('')
const fetching = ref(false)
const fetchError = ref('')
const fetchPartial = ref(false)

async function fetchFromUrl() {
  if (!fetchUrl.value.trim()) return
  fetching.value = true
  fetchError.value = ''
  fetchPartial.value = false

  try {
    const res = await fetch('http://localhost:8742/scrape', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: fetchUrl.value.trim() })
    })
    if (!res.ok) { const err = await res.json(); throw new Error(err.detail || 'Failed to fetch recipe') }
    const { recipe, partial } = await res.json()
    form.value = { ...form.value, ...recipe, ingredients: recipe.ingredients?.length ? recipe.ingredients.map(i => ({ ...i })) : [{ name: '', quantity: '', unit: '' }] }
    tagsInput.value = (recipe.tags || []).join(', ')
    imageUrlInput.value = recipe.image || ''
    fetchPartial.value = !!partial
    toast.success(partial ? 'Recipe imported — some fields need review.' : 'Recipe imported successfully!')
  } catch (e) {
    fetchError.value = e.message.includes('fetch')
      ? "Could not reach the scraper server. Make sure it's running: python3 server.py"
      : e.message
    toast.error(fetchError.value)
  } finally { fetching.value = false }
}

function triggerFileInput() { fileInput.value?.click() }
function onFileSelected(e) { const file = e.target.files?.[0]; if (file) loadImageFile(file) }
function onDrop(e) { const file = e.dataTransfer.files?.[0]; if (file && file.type.startsWith('image/')) loadImageFile(file) }

function loadImageFile(file) {
  const reader = new FileReader()
  reader.onload = (e) => { form.value.image = e.target.result; imageUrlInput.value = ''; imageError.value = false }
  reader.readAsDataURL(file)
}

function applyImageUrl() {
  if (imageUrlInput.value.trim()) { form.value.image = imageUrlInput.value.trim(); imageError.value = false }
}

const emptyForm = () => ({ name: '', url: '', source: 'custom', image: '', time: '', servings: '', description: '', ingredients: [{ name: '', quantity: '', unit: '' }], tags: [] })
const form = ref(emptyForm())

onMounted(async () => {
  await recipeStore.loadRecipes()
  if (isEditing.value) {
    const existing = recipeStore.getById(route.params.id)
    if (existing) {
      form.value = { ...existing, ingredients: existing.ingredients.map(i => ({ ...i })) }
      tagsInput.value = (existing.tags || []).join(', ')
      imageUrlInput.value = existing.image || ''
    }
  }
})

function addIngredient() { form.value.ingredients.push({ name: '', quantity: '', unit: '' }) }
function removeIngredient(i) { form.value.ingredients.splice(i, 1) }

function validate() {
  errors.value = { name: '', ingredients: '' }
  let valid = true
  if (!form.value.name.trim()) { errors.value.name = 'Recipe name is required.'; valid = false }
  if (form.value.ingredients.filter(i => i.name.trim()).length === 0) { errors.value.ingredients = 'Add at least one ingredient.'; valid = false }
  return valid
}

function save() {
  if (!validate()) { toast.error('Please fix the errors before saving.'); return }
  const tags = tagsInput.value.split(',').map(t => t.trim()).filter(Boolean)
  const recipe = { ...form.value, id: isEditing.value ? form.value.id : crypto.randomUUID(), tags, ingredients: form.value.ingredients.filter(i => i.name.trim()) }
  recipeStore.saveCustom(recipe)
  toast.success(isEditing.value ? 'Recipe updated!' : 'Recipe added!')
  router.push('/recipes')
}
</script>
