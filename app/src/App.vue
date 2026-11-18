<template>
  <div id="mealmind">
    <nav class="sticky top-0 z-50 border-b border-border bg-card shadow-sm">
      <div class="mx-auto flex h-14 max-w-[1100px] items-center gap-10 px-5">
        <div class="flex items-center gap-2 text-lg font-bold text-primary whitespace-nowrap">
          <AppIcon name="logo" :size="22" />
          MealMind
        </div>
        <div class="flex gap-1">
          <router-link
            v-for="link in navLinks"
            :key="link.to"
            :to="link.to"
            class="flex items-center gap-1.5 rounded-md px-3 py-1.5 text-sm font-medium text-muted-foreground transition-colors hover:bg-secondary hover:text-secondary-foreground"
            :class="{ 'bg-secondary text-secondary-foreground': $route.path === link.to }"
          >
            <AppIcon :name="link.icon" :size="15" />
            {{ link.label }}
          </router-link>
        </div>
      </div>
    </nav>
    <main>
      <router-view />
    </main>
    <ToastContainer />
  </div>
</template>

<script setup>
import ToastContainer from '@/components/ToastContainer.vue'
import AppIcon from '@/components/AppIcon.vue'

const navLinks = [
  { to: '/planner',    icon: 'calendar', label: 'Meal Planner'   },
  { to: '/shopping',   icon: 'cart',     label: 'Shopping List'  },
  { to: '/recipes',    icon: 'book',     label: 'Recipes'        },
  { to: '/my-recipes', icon: 'edit',     label: 'My Recipes'     },
  { to: '/add-recipe', icon: 'plus',     label: 'Add Recipe'     },
]
</script>
