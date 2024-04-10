<template>
  <vue-plotly :data="chartData" :layout="layout" />
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  components: { VuePlotly },
  name: 'ExperimentsParallelChart',
});
</script>
<script setup lang="ts">
import { ExperimentParallelCount } from '../models';
import VuePlotly from './VuePlotly.vue';
import { testScaleLabel } from 'src/utils/numbers';
import { isStone } from 'src/utils/criteria';

const { t } = useI18n({ useScope: 'global' });
const analysis = useAnalysisStore();

const layout = {};

const chartData = computed(() => {
  const parCatsData = {
    type: 'parcats',
    dimensions: [] as { label: string; values: string[] }[],
    counts: [] as number[],
    line: {
      //color: 'gray',
      shape: 'hspline',
    },
  };
  if (analysis.experimentsParallelCounts !== null) {
    // merge all stones into one category
    const digestedCounts: ExperimentParallelCount[] = [];
    analysis.experimentsParallelCounts.forEach((line) => {
      if (isStone(line.masonry_unit_material)) {
        const newline = { ...line };
        newline.masonry_unit_material = 'Stone';
        digestedCounts.push(newline);
      } else {
        digestedCounts.push(line);
      }
    });

    parCatsData.counts = digestedCounts.map((line) => line.count);
    [
      'masonry_unit_material',
      'diaphragm_material',
      'storeys_nb',
      'test_scale',
    ].forEach((field: string) => {
      parCatsData.dimensions.push({
        label: t(field),
        values: digestedCounts.map((line) => {
          if (field === 'test_scale') {
            return testScaleLabel(line[field]);
          }
          const val = line[field as keyof typeof line];
          return val === null ? 'N/A' : val.toString();
        }),
      });
    });
  }
  return [parCatsData];
});
</script>
