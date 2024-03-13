<template>
  <div>
    <q-card flat square class="bg-grey-9 text-white">
      <q-card-section>
        <div class="row">
          <div class="col text-center">
            <div class="text-h3">
              {{ analysis.metrics.experiments_count }}
            </div>
            <div class="text-subtitle1">
              {{ $t('buildings_metrics_label') }}
            </div>
          </div>
          <div class="col text-center">
            <div class="text-h3">
              {{ analysis.metrics.references_count }}
            </div>
            <div class="text-subtitle1">
              {{ $t('references_metrics_label') }}
            </div>
          </div>
          <div class="col text-center">
            <div class="text-h3">
              {{ analysis.metrics.run_results_count }}
            </div>
            <div class="text-subtitle1">
              {{ $t('run_results_metrics_label') }}
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'MetricsBanner',
});
</script>
<script setup lang="ts">
import { Metrics } from 'src/components/models';
import { useAnalysisStore } from 'src/stores/analysis';

const analysis = useAnalysisStore();

onMounted(() => {
  analysis.loadMetrics();
});
</script>
