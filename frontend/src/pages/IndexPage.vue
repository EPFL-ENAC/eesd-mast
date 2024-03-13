<template>
  <q-page>
    <div class="q-pa-md">
      <div class="text-subtitle1 text-grey-8">
        <q-markdown :src="OverViewMd" no-line-numbers />
      </div>
    </div>
    <metrics-banner />
  </q-page>
</template>

<script setup lang="ts">
import OverViewMd from 'src/assets/overview.md';
import MetricsBanner from 'src/components/MetricsBanner.vue';
</script>
