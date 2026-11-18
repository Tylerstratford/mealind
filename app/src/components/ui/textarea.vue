<script setup>
import { cn } from '@/lib/utils'
defineProps({
  class:       { type: String, default: '' },
  placeholder: { type: String, default: '' },
  modelValue:  { default: '' },
  rows:        { type: Number, default: 3 },
  disabled:    { type: Boolean, default: false },
})
defineEmits(['update:modelValue'])
</script>

<template>
  <textarea
    v-bind="$attrs"
    :placeholder="placeholder"
    :value="modelValue"
    :rows="rows"
    :disabled="disabled"
    :class="cn(
      'flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground shadow-sm transition-colors resize-vertical',
      'placeholder:text-muted-foreground/60 placeholder:italic placeholder:font-normal',
      'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
      'disabled:cursor-not-allowed disabled:opacity-50',
      $props.class
    )"
    @input="$emit('update:modelValue', $event.target.value)"
  />
</template>
