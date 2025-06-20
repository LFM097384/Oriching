<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="2"
    stroke-linecap="round"
    stroke-linejoin="round"
    :class="className"
  >
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
    <circle cx="12" cy="12" r="3"></circle>
  </svg>
</template>

<script>
export default {
  name: 'EyeIcon',
  props: {
    size: {
      type: [String, Number],
      default: 20
    },
    className: {
      type: String,
      default: ''
    }
  }
}
</script>
