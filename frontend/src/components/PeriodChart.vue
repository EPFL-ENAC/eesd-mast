<template>
  <div v-if="option.series" :style="`height: ${height + 200}px;`">
    <e-charts
      ref="chart"
      autoresize
      :init-options="initOptions"
      :option="option"
      :update-options="updateOptions"
      class="q-ma-md"
      :loading="loading"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'PeriodChart',
});
</script>
<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import ECharts from 'vue-echarts';
import type { EChartsOption } from 'echarts';
import { use } from 'echarts/core';
import { LineChart } from 'echarts/charts';
import { SVGRenderer } from 'echarts/renderers';
import { initOptions, updateOptions } from './charts';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DataZoomComponent,
  LegendComponent,
} from 'echarts/components';
import { Experiment, RunResult } from 'src/components/models';
import { useRunResultsStore } from 'src/stores/run_results';

use([
  SVGRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DataZoomComponent,
  LegendComponent,
]);

export interface PeriodChartProps {
  experiment: Experiment;
  height?: number;
}
const props = withDefaults(defineProps<PeriodChartProps>(), {
  experiment: undefined,
  height: 300,
});

const { t } = useI18n({ useScope: 'global' });
const runResultsStore = useRunResultsStore();

const runResults = ref<RunResult[]>([]);
const chart = shallowRef(null);
const option = ref<EChartsOption>({});
const loading = ref(false);

watch(
  () => props.experiment,
  () => {
    initChartOptions();
  }
);

onMounted(() => {
  initChartOptions();
});

function initChartOptions() {
  option.value = {};
  if (!props.experiment) {
    return;
  }
  runResultsStore
    .fetchRunResults(props.experiment.id)
    .then((res: RunResult[]) => {
      runResults.value = res.filter(
        (run) => !['Initial', 'Final'].includes(run.run_id)
      );
      buildOptions();
    });
}

function buildOptions() {
  loading.value = true;
  const visibleColumns = [
    'nominal_pga_x',
    'nominal_pga_y',
    'actual_pga_x',
    'actual_pga_y',
    'dg_reported',
    'dg_derived',
    'reported_t1_x',
    'reported_t1_y',
  ].filter(
    (col) =>
      runResults.value.filter((run: RunResult) => run[col] !== null).length > 0
  );
  let pgaColumn = visibleColumns.includes('actual_pga_x')
    ? 'actual_pga_x'
    : 'actual_pga_y';
  if (!visibleColumns.includes(pgaColumn)) {
    pgaColumn = visibleColumns.includes('nominal_pga_x')
      ? 'nominal_pga_x'
      : 'nominal_pga_y';
  }
  const dgColumn = visibleColumns.includes('dg_reported')
    ? 'dg_reported'
    : 'dg_derived';
  const periodColumn = visibleColumns.includes('reported_t1_x')
    ? 'reported_t1_x'
    : 'reported_t1_y';
  if (!visibleColumns.includes(periodColumn)) {
    loading.value = false;
    return;
  }

  const datasetPGA = runResults.value
    .filter(
      (result) => result[pgaColumn] !== null && result[periodColumn] !== null
    )
    .map((result) => {
      return [result[pgaColumn], result[periodColumn]];
    });
  const datasetDG = runResults.value
    .filter(
      (result) => result[dgColumn] !== null && result[periodColumn] !== null
    )
    .map((result) => {
      return [result[dgColumn], result[periodColumn]];
    });

  const newOption: EChartsOption = {
    title: {
      text: `${t(periodColumn)} vs. ${t(pgaColumn)} / ${t(dgColumn)}`,
    },
    height: props.height,
    grid: {
      left: 60,
      top: 120,
      right: 60,
      bottom: 100,
    },
    tooltip: {
      trigger: 'axis',
    },
    legend: {
      orient: 'horizontal',
      right: 'center',
      top: 40,
      data: [t(pgaColumn), t(dgColumn)],
    },
    xAxis: [
      {
        type: 'value',
        name: `${t(pgaColumn)} (g)`,
        nameLocation: 'middle',
        nameTextStyle: {
          fontWeight: 'bold',
          fontSize: 16,
          padding: [10, 0, 0, 0],
        },
      },
      {
        type: 'value',
        name: `${t(dgColumn)} (g)`,
        nameLocation: 'middle',
        nameTextStyle: {
          fontWeight: 'bold',
          fontSize: 16,
          padding: [0, 0, 10, 0],
        },
      },
    ],
    yAxis: {
      type: 'value',
      name: `${t(periodColumn)} (s)`,
      nameLocation: 'middle',
      nameTextStyle: {
        fontWeight: 'bold',
        fontSize: 16,
        padding: [0, 0, 30, 0],
      },
    },
    series: [
      {
        name: t(pgaColumn),
        data: datasetPGA,
        xAxisIndex: 0,
        type: 'line',
        symbolSize: 5,
      },
      {
        name: t(dgColumn),
        data: datasetDG,
        xAxisIndex: 1,
        type: 'line',
        symbolSize: 5,
      },
    ],
  };
  option.value = newOption;
  loading.value = false;
}
</script>
