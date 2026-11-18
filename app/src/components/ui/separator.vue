<script setup>
import { cn } from '@/lib/utils'
defineProps({
  class:       { type: String, default: '' },
  orientation: { type: String, default: 'horizontal' },
})
</script>
<template>
  <div
    role="separator"
    :class="cn(
      'shrink-0 bg-border',
      orientation === 'horizontal' ? 'h-px w-full' : 'h-full w-px',
      $props.class
    )"
  />
</template>
