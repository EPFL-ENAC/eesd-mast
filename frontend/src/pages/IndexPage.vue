<template>
  <q-page>
    <div>
      <app-header url="/Website_Background_Title_Option1_blue.webp" />
      <metrics-banner />
      <experiment-aggregations />
      <q-card class="q-ma-xl">
        <q-card-section>
          <div class="text-h6">{{ $t('how_to_cite') }}</div>
        </q-card-section>
        <q-card-section>
          <q-markdown :src="CiteMd" class="app-md" />
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import AppHeader from 'src/components/AppHeader.vue';
import MetricsBanner from 'src/components/MetricsBanner.vue';
import ExperimentAggregations from 'src/components/ExperimentAggregations.vue';
import CiteMd from 'src/assets/cite.md';
</script>
