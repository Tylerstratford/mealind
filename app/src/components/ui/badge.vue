<script setup>
import { cn } from '@/lib/utils'
defineProps({
  variant: { type: String, default: 'default' },
  class:   { type: String, default: '' },
})

const variants = {
  default:   'border-transparent bg-primary text-primary-foreground',
  secondary: 'border-transparent bg-secondary text-secondary-foreground',
  outline:   'text-foreground',
  destructive: 'border-transparent bg-destructive text-destructive-foreground',
}
</script>

<template>
  <span
    :class="cn(
      'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors',
      variants[variant] ?? variants.default,
      $props.class
    )"
  >
    <slot />
  </span>
</template>
