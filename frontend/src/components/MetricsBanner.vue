<template>
  <div>
    <q-card flat square class="bg-grey-9 text-white">
      <q-card-section>
        <div class="row">
          <div class="col-12 col-md-3 col-sm-12 text-center">
            <div class="text-h4">
              {{ analysis.counts.experiments_count }}
            </div>
            <div class="text-subtitle1">
              {{ $t('buildings_counts_label') }}
            </div>
          </div>
          <div class="col-12 col-md-3 col-sm-12 text-center">
            <div class="text-h4">
              {{ analysis.counts.models_count }}
            </div>
            <div class="text-subtitle1">
              {{ $t('numerical_models_label') }}
            </div>
          </div>
          <div class="col-12 col-md-3 col-sm-12 text-center">
            <div class="text-h4">100+</div>
            <div class="text-subtitle1">
              {{ $t('references_counts_label') }}
            </div>
          </div>
          <div class="col-12 col-md-3 col-sm-12 text-center">
            <div class="text-h4">
              {{ $t('downloadable') }}
            </div>
            <div class="text-subtitle1">
              {{ $t('run_results_counts_label') }}
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script lang="ts">
export default defineComponent({
  name: 'MetricsBanner',
});
</script>
<script setup lang="ts">
import { useAnalysisStore } from 'src/stores/analysis';

const analysis = useAnalysisStore();

onMounted(() => {
  analysis.loadCounts();
});
</script>
