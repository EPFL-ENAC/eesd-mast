<template>
  <vue-plotly :data="chartData" :layout="layout" :config="config" />
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
import { getFieldValueColor } from 'src/utils/colors';
import { isStone, isMixedMaterial } from 'src/utils/criteria';

const { t } = useI18n({ useScope: 'global' });
const analysis = useAnalysisStore();

const layout = {
  margin: {
    l: 50, // Left margin
    r: 50, // Right margin
    b: 50, // Bottom margin
    t: 50, // Top margin
  },
};

const config = {
  displayModeBar: false,
  responsive: true,
};

const chartData = computed(() => {
  const parCatsData = {
    type: 'parcats',
    dimensions: [] as { label: string; values: string[] }[],
    counts: [] as number[],
    line: {
      shape: 'hspline',
    },
    labelfont: {
      size: 16,
    },
  };

  if (analysis.experimentsParallelCounts !== null) {
    // merge all stones into one category
    const digestedCounts: ExperimentParallelCount[] = [];
    analysis.experimentsParallelCounts.forEach((line) => {
      const newline = { ...line };
      if (isStone(line.masonry_unit_material)) {
        newline.masonry_unit_material = 'Stone';
      }
      if (isMixedMaterial(line.diaphragm_material)) {
        newline.diaphragm_material = 'Mixed';
      }
      digestedCounts.push(newline);
    });

    parCatsData.counts = digestedCounts.map((line) => line.count);

    // Colors
    if (digestedCounts.filter((line) => line.selected).length === 0) {
      // enforce color when no filter
      parCatsData.line.color = 'lightsteelblue';
    } else {
      const lineColor = digestedCounts.map((line) => {
        return line.selected
          ? getFieldValueColor(
              'masonry_unit_material',
              line.masonry_unit_material
            )
          : 'lightsteelblue';
      });
      parCatsData.line.color = lineColor;
    }

    [
      'masonry_unit_material',
      'masonry_unit_type',
      'diaphragm_material',
      'wall_leaves_nb',
      'storeys_nb',
      'test_scale',
      'simultaneous_excitations_nb',
      'retrofitting_application',
    ].forEach((field: string) => {
      parCatsData.dimensions.push({
        label: t(`${field}_short`),
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
