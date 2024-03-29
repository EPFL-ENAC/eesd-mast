<template>
  <div v-if="option.series" :style="`height: ${height + 150}px;`">
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
  name: 'PgaChart',
});
</script>
<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import ECharts from 'vue-echarts';
import type { EChartsOption } from 'echarts';
import { use } from 'echarts/core';
import { LineChart } from 'echarts/charts';
import { SVGRenderer } from 'echarts/renderers';
import { initOptions, updateOptions } from '../charts';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DataZoomComponent,
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
]);

interface PgaChartProps {
  experiment: Experiment;
  height?: number;
}
const props = withDefaults(defineProps<PgaChartProps>(), {
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

  const newOption: EChartsOption = {
    // title: {
    //   text: `${t(periodColumn)} vs. ${t(pgaColumn)}`,
    // },
    animation: false,
    height: props.height,
    grid: {
      left: 60,
      top: 10,
      right: 60,
      bottom: 0,
    },
    tooltip: {
      trigger: 'item',
      formatter: (params: unknown) => {
        return `${t(pgaColumn)}: ${params.value[0]} g<br />${t(
          periodColumn
        )}: ${params.value[1]} s`;
      },
    },
    xAxis: {
      type: 'value',
      name: `${t(pgaColumn)} (g)`,
      nameLocation: 'middle',
      nameTextStyle: {
        fontWeight: 'bold',
        fontSize: 16,
        padding: [20, 0, 0, 0],
      },
    },
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
        type: 'line',
        symbolSize: 5,
      },
    ],
  };
  option.value = newOption;
  loading.value = false;
}
</script>
