# MealMind Design System

Use this as the authoritative reference when building or modifying any frontend UI in this project. Always follow these conventions exactly — do not introduce new patterns without checking here first.

---

## Stack

- **Vue 3** (Composition API + `<script setup>`)
- **Tailwind CSS v4** with `@theme` — configured via CSS variables, not `tailwind.config.js` values
- **Radix Vue** — for accessible component primitives
- **class-variance-authority (cva)** + **clsx** + **tailwind-merge** → `cn()` utility in `src/lib/utils.js`
- **Lucide Vue Next** + custom `AppIcon.vue` SVG system

---

## Color Tokens (HSL CSS Variables)

Defined in `src/style.css` under `:root`. Always use these via Tailwind utilities (`bg-primary`, `text-foreground`, etc.) — never hardcode hex.

| Token | HSL Value | Usage |
|-------|-----------|-------|
| `--primary` | 142 48% 33% | Forest green — primary actions, active states |
| `--primary-foreground` | 0 0% 100% | White text on primary |
| `--secondary` | 142 48% 93% | Light green — secondary buttons, active nav |
| `--secondary-foreground` | 142 48% 25% | Dark green text on secondary |
| `--background` | 0 0% 97% | Page background (off-white) |
| `--foreground` | 0 0% 10% | Near-black body text |
| `--card` | 0 0% 100% | Pure white card surfaces |
| `--card-foreground` | 0 0% 10% | Card body text |
| `--muted` | 210 17% 95% | Subtle backgrounds |
| `--muted-foreground` | 215 14% 43% | Secondary/helper text |
| `--accent` | 142 48% 93% | Same as secondary |
| `--border` | 220 13% 91% | Borders and dividers |
| `--input` | 220 13% 91% | Input borders |
| `--ring` | 142 48% 33% | Focus rings (matches primary) |
| `--destructive` | 0 72% 51% | Error/delete red |
| `--destructive-foreground` | 0 0% 100% | White on destructive |
| `--radius` | 0.6rem | Base border radius |

### Source Badge Colors (hardcoded in CSS, recipe-specific)

| Source | Text | Background |
|--------|------|------------|
| ICA | `#cc0000` | `#fff0f0` |
| Coop | `#c67c00` | `#fff8e1` |
| Mathem | `#3a5bcd` | `#f0f4ff` |
| Arla | `#0066cc` | `#f0f8ff` |
| Koket | `#8b22b5` | `#fdf4ff` |
| Custom | `#166534` | `#f0fdf4` |

---

## Typography

- **Font**: `'Segoe UI', system-ui, sans-serif`
- **Page title**: `font-size: 24px; font-weight: 700; margin-bottom: 6px` → class `.page-title`
- **Page subtitle**: `color: muted-foreground; font-size: 14px; margin-bottom: 24px` → class `.page-sub`
- Use Tailwind text utilities (`text-sm`, `text-xs`, `font-semibold`, etc.) elsewhere

---

## Layout Utilities (from `style.css`)

```css
.page          /* max-width: 1100px, centered, padding: 24px 20px */
.page-title    /* 24px bold heading */
.page-sub      /* 14px muted subtitle */
```

Container: `max-width: 1400px`, `padding: 0 2rem`

---

## Border Radius

| Tailwind class | Value |
|---------------|-------|
| `rounded-lg` | 0.6rem (`--radius`) |
| `rounded-md` | 0.4rem (`calc(--radius - 2px)`) |
| `rounded-sm` | 0.2rem (`calc(--radius - 4px)`) |
| `rounded-full` | Used for badges/pills |

---

## Base UI Components (`src/components/ui/`)

Always import from here. Do not reimplement these patterns.

### `Button` (`button.vue`)

**Variants**: `default` (green fill), `secondary` (light green), `destructive` (red), `outline` (border only), `ghost` (hover only), `link`

**Sizes**: `default`, `sm`, `lg`, `icon`

Base classes: `inline-flex items-center gap-1.5 rounded-md text-sm font-medium focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50 disabled:pointer-events-none`

### `Badge` (`badge.vue`)

Shape: `rounded-full border px-2.5 py-0.5 text-xs font-semibold`

**Variants**: `default` (green fill), `secondary` (light green), `outline` (border only), `destructive` (red)

### `Card` (`card.vue`)

`rounded-lg border border-border bg-card shadow-sm`

Use for all content containers. Common padding: `p-3`, `p-4`, `p-5`, `p-6`.

### `Input` (`input.vue`)

`h-9 border border-input rounded-md focus:ring-2 focus:ring-ring placeholder:italic placeholder:text-muted-foreground/60`

### `Textarea` (`textarea.vue`)

Same focus/border treatment as Input. Default `rows="3"`, resizable vertically.

### `Label` (`label.vue`)

`text-sm font-semibold` — includes peer-disabled states.

### `Select` (`select.vue`)

`h-9` — matches Input styling.

### `Separator` (`separator.vue`)

Horizontal (`h-px bg-border`) or vertical (`w-px bg-border`).

---

## AppIcon Component (`src/components/AppIcon.vue`)

```vue
<AppIcon name="..." :size="18" color="currentColor" :strokeWidth="1.75" />
```

**Available icons**: `calendar`, `cart`, `book`, `plus`, `logo`, `shuffle`, `refresh`, `lock`, `unlock`, `swap`, `link`, `clipboard`, `check`, `uncheck`, `copy`, `edit`, `trash`, `search`, `externallink`, `camera`, `image`, `upload`, `x`, `arrowleft`, `save`, `user`, `clock`, `tag`, `download`

Use `AppIcon` for app-specific icons; use Lucide for anything else.

---

## Toast Notifications (`src/composables/useToast.js`)

```js
import { useToast } from '@/composables/useToast'
const { showToast } = useToast()

showToast('Message', 'success')  // green
showToast('Message', 'error')    // red
showToast('Message', 'info')     // blue
```

`ToastContainer.vue` is mounted in `App.vue` and renders via Teleport to `body`.

---

## Common Patterns

### Page Layout

```vue
<div class="page">
  <h1 class="page-title">Page Title</h1>
  <p class="page-sub">Subtitle text</p>
  <!-- content -->
</div>
```

### Recipe Card Grid

```css
display: grid;
grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
gap: 1rem;
```

### Form Field

```vue
<div class="flex flex-col gap-1.5">
  <Label for="field">Label</Label>
  <Input id="field" v-model="value" placeholder="..." />
</div>
```

### Two-Column Layout (content + sidebar)

```vue
<div class="grid grid-cols-[1fr_320px] gap-6">
  <main>...</main>
  <aside>...</aside>
</div>
```

### Navigation Active State

Active nav links: `bg-secondary text-secondary-foreground`

Nav bar: `sticky top-0 z-50 h-14 bg-card border-b shadow-sm`

---

## State Management

- **Pinia** stores in `src/stores/`
  - `mealplan.js` — meal plan + shopping list state
  - `recipes.js` — recipe database
- Use `storeToRefs()` for reactive destructuring

---

## Do's and Don'ts

**Do:**
- Use `cn()` for conditional class merging
- Use HSL CSS variable tokens via Tailwind utilities
- Reuse base UI components from `src/components/ui/`
- Follow existing Composition API patterns (`<script setup>`, `ref`, `computed`)
- Keep page max-width at 1100px with `.page` class

**Don't:**
- Hardcode colors (use CSS variable tokens)
- Create new UI primitives when existing ones in `ui/` suffice
- Use Options API — all code uses Composition API
- Add inline `style` tags with raw hex/rgb values for theme colors
- Override Tailwind defaults; extend via CSS variables instead
