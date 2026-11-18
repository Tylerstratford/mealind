<template>
  <div class="page">
    <div class="mb-7 flex flex-wrap items-start justify-between gap-4">
      <div>
        <h1 class="page-title">🛒 Shopping List</h1>
        <p class="page-sub">Check off items you already have. Add anything extra.</p>
      </div>
      <div class="flex flex-wrap gap-2 pt-2">
        <Button variant="secondary" @click="exportList">📋 Export List</Button>
        <Button variant="outline" class="border-orange-300 bg-orange-50 text-orange-700 hover:bg-orange-100"
          :disabled="allIngredients.length === 0 || normalizing" @click="startNormalize"
          title="Use Claude AI to merge duplicates and fix spelling">
          <span v-if="normalizing">Normalizing…</span>
          <span v-else>✨ Normalize with AI</span>
        </Button>
        <Button @click="copyForWillys">📦 Copy for Willys</Button>
      </div>
    </div>

    <div class="grid gap-5 items-start" style="grid-template-columns: 1fr 300px">
      <!-- Ingredient list -->
      <Card class="p-5">
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-base font-semibold">
            Ingredients <span class="ml-2 text-[13px] font-normal text-muted-foreground">{{ remaining }} items remaining</span>
          </h2>
          <Button variant="outline" size="sm" @click="uncheckAll">Uncheck all</Button>
        </div>

        <div class="mb-5 flex gap-2">
          <Input v-model="newItem" placeholder="Add extra item (e.g. yoghurt, milk…)" @keydown.enter="addExtra" />
          <Button variant="secondary" @click="addExtra">+ Add</Button>
        </div>

        <div v-for="(group, category) in groupedIngredients" :key="category" class="mb-2">
          <h3 class="mb-2 mt-4 text-[11px] font-semibold uppercase tracking-wide text-muted-foreground">{{ category }}</h3>
          <label v-for="item in group" :key="item.name"
            :class="['flex cursor-pointer items-center gap-2.5 rounded-lg px-2.5 py-2 text-sm transition-colors hover:bg-muted/50',
              item.checked ? 'opacity-45' : '']">
            <input type="checkbox" v-model="item.checked" class="h-4 w-4 rounded accent-primary" />
            <span :class="['flex-1', item.checked ? 'line-through' : '']">{{ item.name }}</span>
            <span v-if="item.quantity" class="text-[13px] text-muted-foreground">
              {{ item.quantity }}{{ item.unit ? ' ' + item.unit : '' }}
            </span>
            <Badge v-if="item.extra" variant="outline" class="badge-mathem text-[10px]">extra</Badge>
            <button v-if="item.extra" class="rounded px-1 py-0.5 text-[12px] text-muted-foreground hover:bg-destructive/10 hover:text-destructive"
              @click.prevent="removeExtra(item.name)">✕</button>
          </label>
        </div>

        <div v-if="allIngredients.length === 0" class="flex flex-col items-center gap-3.5 py-8 text-center text-sm text-muted-foreground">
          <p>No ingredients yet — generate a meal plan first.</p>
          <router-link to="/planner"><Button variant="secondary" size="sm">Go to Planner</Button></router-link>
        </div>
      </Card>

      <!-- Sidebar -->
      <div class="flex flex-col gap-4">
        <Card class="p-4">
          <h3 class="mb-3.5 text-[15px] font-semibold">This week's meals</h3>
          <div v-for="{ day, recipe } in mealPlan.plannedRecipes" :key="day"
            class="flex gap-2.5 border-b border-border py-1.5 text-[13px] last:border-b-0">
            <span class="min-w-[32px] font-semibold text-muted-foreground">{{ day.slice(0,3) }}</span>
            <span class="flex-1">{{ recipe?.name ?? '—' }}</span>
          </div>
        </Card>

        <Card class="p-4">
          <div class="mb-3 flex items-center justify-between">
            <h3 class="text-[15px] font-semibold">Staples</h3>
            <div class="flex gap-1.5">
              <Button v-if="!editingStaples && staples.length > 0" variant="secondary" size="sm" @click="addAllStaples">
                Add all
              </Button>
              <Button variant="outline" size="sm" @click="editingStaples = !editingStaples">
                {{ editingStaples ? 'Done' : 'Edit' }}
              </Button>
            </div>
          </div>

          <div v-if="editingStaples" class="mb-2.5 flex gap-2">
            <Input v-model="newStaple" placeholder="Add staple item…" @keydown.enter="addStaple" />
            <Button variant="secondary" size="sm" @click="addStaple">Add</Button>
          </div>

          <div v-if="staples.length === 0 && !editingStaples" class="flex flex-col items-center gap-2.5 py-4 text-center text-[13px] text-muted-foreground">
            <p>No staples yet.</p>
            <Button variant="outline" size="sm" @click="editingStaples = true">+ Add items</Button>
          </div>

          <div class="flex flex-col gap-0.5">
            <div v-for="item in staples" :key="item"
              class="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm hover:bg-muted/50">
              <span class="flex-1">{{ item }}</span>
              <button v-if="editingStaples"
                class="rounded px-1 text-[12px] text-muted-foreground hover:bg-destructive/10 hover:text-destructive"
                @click="removeStaple(item)">✕</button>
              <button v-else
                class="flex h-6 w-6 shrink-0 items-center justify-center rounded border border-border text-sm text-primary hover:border-primary hover:bg-secondary"
                title="Add to list" @click="addStapleToList(item)">+</button>
            </div>
          </div>
        </Card>
      </div>
    </div>

    <!-- API key modal -->
    <Teleport to="body">
      <div v-if="showKeyModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
        @click.self="showKeyModal = false">
        <Card class="flex w-[90%] max-w-lg flex-col gap-3.5 p-6">
          <h3 class="text-[17px] font-bold">Anthropic API Key</h3>
          <p class="text-[13px] text-muted-foreground">
            Enter your Anthropic API key to use Claude for normalization. It's stored only in your browser (localStorage) and sent directly to your local server — never to any third party.
          </p>
          <Input v-model="apiKeyInput" type="password" placeholder="sk-ant-…" @keydown.enter="saveApiKey" />
          <p class="text-[13px] text-muted-foreground">Get a key at <strong>console.anthropic.com</strong></p>
          <div class="flex flex-wrap gap-2">
            <Button @click="saveApiKey" :disabled="!apiKeyInput.trim()">Save & Continue</Button>
            <Button variant="outline" @click="showKeyModal = false">Cancel</Button>
            <Button v-if="anthropicKey" variant="destructive" @click="clearApiKey">Remove key</Button>
          </div>
        </Card>
      </div>
    </Teleport>

    <!-- Normalize review modal -->
    <Teleport to="body">
      <div v-if="normalizeResult" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
        @click.self="normalizeResult = null">
        <Card class="flex w-[90%] max-w-sm flex-col gap-3.5 p-6">
          <h3 class="text-[17px] font-bold">Normalized Shopping List</h3>
          <p class="text-[13px] text-muted-foreground">Claude merged duplicates and fixed spelling. Review and apply.</p>
          <div class="max-h-72 overflow-y-auto rounded-lg border border-border p-1">
            <div v-for="item in normalizeResult" :key="item.name"
              class="flex items-center gap-2.5 rounded-md px-2.5 py-1.5 text-sm hover:bg-muted/50">
              <span class="flex-1">{{ item.name }}</span>
              <span v-if="item.quantity" class="text-[13px] text-muted-foreground">
                {{ item.quantity }}{{ item.unit ? ' ' + item.unit : '' }}
              </span>
            </div>
          </div>
          <div class="flex gap-2">
            <Button @click="applyNormalized">Apply to list</Button>
            <Button variant="outline" @click="normalizeResult = null">Discard</Button>
          </div>
        </Card>
      </div>
    </Teleport>

    <!-- Export modal -->
    <Teleport to="body">
      <div v-if="showExport" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
        @click.self="showExport = false">
        <Card class="flex w-[90%] max-w-lg flex-col gap-3.5 p-6">
          <h3 class="text-[17px] font-bold">📋 Exported Shopping List</h3>
          <p class="text-[13px] text-muted-foreground">Copy this and paste into any notes app or use with a Willys skill.</p>
          <textarea readonly :value="exportText"
            class="h-52 w-full resize-y rounded-lg border border-border bg-muted/30 p-3 font-mono text-[13px]" />
          <div class="flex flex-wrap gap-2">
            <Button @click="copyToClipboard">Copy to clipboard</Button>
            <Button variant="outline" @click="showExport = false">Close</Button>
          </div>
        </Card>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, reactive, watch } from 'vue'
import { useMealPlanStore } from '@/stores/mealplan'
import { useToast } from '@/composables/useToast'
import Button from '@/components/ui/button.vue'
import Card from '@/components/ui/card.vue'
import Badge from '@/components/ui/badge.vue'
import Input from '@/components/ui/input.vue'

const mealPlan = useMealPlanStore()
const toast = useToast()
const newItem = ref('')
const extraItems = reactive([])
const showExport = ref(false)

const anthropicKey = ref(localStorage.getItem('mealmind-anthropic-key') || '')
const showKeyModal = ref(false)
const apiKeyInput = ref('')
const normalizing = ref(false)
const normalizeResult = ref(null)

function startNormalize() {
  if (!anthropicKey.value) { apiKeyInput.value = ''; showKeyModal.value = true; return }
  runNormalize()
}

function saveApiKey() {
  const key = apiKeyInput.value.trim()
  if (!key) return
  anthropicKey.value = key
  localStorage.setItem('mealmind-anthropic-key', key)
  showKeyModal.value = false
  runNormalize()
}

function clearApiKey() {
  anthropicKey.value = ''
  localStorage.removeItem('mealmind-anthropic-key')
  showKeyModal.value = false
  toast.success('API key removed.')
}

async function runNormalize() {
  normalizing.value = true
  try {
    const res = await fetch('http://localhost:8742/normalize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Api-Key': anthropicKey.value },
      body: JSON.stringify({ ingredients: allIngredients.value.map(i => ({ name: i.name, quantity: String(i.quantity || ''), unit: i.unit || '' })) })
    })
    const data = await res.json()
    if (!res.ok) {
      if (res.status === 401) { anthropicKey.value = ''; localStorage.removeItem('mealmind-anthropic-key'); apiKeyInput.value = ''; showKeyModal.value = true; toast.success('Invalid API key — please re-enter it.') }
      else toast.success(`Error: ${data.detail || 'Normalization failed.'}`)
      return
    }
    normalizeResult.value = data.normalized
  } catch { toast.success('Could not reach the local server. Is it running? (cd scraper && python3 server.py)') }
  finally { normalizing.value = false }
}

function applyNormalized() {
  const checkedNames = new Set(allIngredients.value.filter(i => i.checked).map(i => i.name.toLowerCase()))
  extraItems.splice(0, extraItems.length)
  for (const item of normalizeResult.value) {
    extraItems.push(reactive({ name: item.name, quantity: item.quantity || '', unit: item.unit || '', checked: checkedNames.has(item.name.toLowerCase()), extra: true, normalized: true }))
  }
  normalizeResult.value = null
  toast.success('Normalized list applied.')
}

const staples = ref(JSON.parse(localStorage.getItem('mealmind-staples') || '[]'))
const editingStaples = ref(false)
const newStaple = ref('')

watch(staples, val => localStorage.setItem('mealmind-staples', JSON.stringify(val)), { deep: true })

function addStaple() {
  const name = newStaple.value.trim()
  if (!name || staples.value.includes(name)) return
  staples.value.push(name); newStaple.value = ''
}

function removeStaple(name) { staples.value = staples.value.filter(s => s !== name) }

function addStapleToList(name) {
  if (extraItems.find(i => i.name.toLowerCase() === name.toLowerCase())) { toast.success(`"${name}" is already on the list.`); return }
  extraItems.push(reactive({ name, quantity: '', unit: '', checked: false, extra: true }))
  toast.success(`"${name}" added to list.`)
}

function addAllStaples() {
  let added = 0
  for (const name of staples.value) {
    if (!extraItems.find(i => i.name.toLowerCase() === name.toLowerCase())) { extraItems.push(reactive({ name, quantity: '', unit: '', checked: false, extra: true })); added++ }
  }
  if (added > 0) toast.success(`${added} staple${added > 1 ? 's' : ''} added to list.`)
  else toast.success('All staples are already on the list.')
}

const allIngredients = computed(() => [...mealPlan.shoppingIngredients.map(i => reactive({ ...i })), ...extraItems])

const groupedIngredients = computed(() => {
  const groups = { 'From recipes': [], 'Extra items': [] }
  for (const item of allIngredients.value) { if (item.extra) groups['Extra items'].push(item); else groups['From recipes'].push(item) }
  if (groups['Extra items'].length === 0) delete groups['Extra items']
  return groups
})

const remaining = computed(() => allIngredients.value.filter(i => !i.checked).length)

function addExtra() {
  const name = newItem.value.trim()
  if (!name) return
  extraItems.push(reactive({ name, quantity: '', unit: '', checked: false, extra: true }))
  newItem.value = ''
}

function removeExtra(name) { const idx = extraItems.findIndex(i => i.name === name); if (idx !== -1) extraItems.splice(idx, 1) }
function uncheckAll() { for (const item of allIngredients.value) item.checked = false }

const exportText = computed(() => {
  const unchecked = allIngredients.value.filter(i => !i.checked)
  return unchecked.map(i => { let line = i.name; if (i.quantity) line += ` — ${i.quantity}${i.unit ? ' ' + i.unit : ''}`; return line }).join('\n')
})

function exportList() { showExport.value = true }
function copyForWillys() { navigator.clipboard.writeText(exportText.value).then(() => { showExport.value = false; toast.success('Shopping list copied! Ready to use with the Willys skill.') }) }
function copyToClipboard() { navigator.clipboard.writeText(exportText.value).then(() => { toast.success('Copied to clipboard!') }) }
</script>
