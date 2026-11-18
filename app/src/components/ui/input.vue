<script setup>
import { cn } from '@/lib/utils'
defineProps({
  class:       { type: String, default: '' },
  type:        { type: String, default: 'text' },
  placeholder: { type: String, default: '' },
  modelValue:  { default: '' },
  disabled:    { type: Boolean, default: false },
})
defineEmits(['update:modelValue'])
</script>

<template>
  <input
    v-bind="$attrs"
    :type="type"
    :placeholder="placeholder"
    :value="modelValue"
    :disabled="disabled"
    :class="cn(
      'flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm text-foreground shadow-sm transition-colors',
      'placeholder:text-muted-foreground/60 placeholder:italic placeholder:font-normal',
      'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
      'disabled:cursor-not-allowed disabled:opacity-50',
      $props.class
    )"
    @input="$emit('update:modelValue', $event.target.value)"
  />
</template>
