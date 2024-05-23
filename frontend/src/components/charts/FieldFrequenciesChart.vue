<template>
  <div v-if="option.series" :style="`height: ${height - 20}px;`">
    <e-charts
      ref="chart"
      autoresize
      :init-options="initOptions"
      :option="option"
      :update-options="updateOptions"
      class="q-ma-md"
      :loading="loading"
      @click="onClick"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'FieldFrequenciesChart',
});
</script>
<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import ECharts from 'vue-echarts';
import type { EChartsOption } from 'echarts';
import { use } from 'echarts/core';
import { PieChart } from 'echarts/charts';
import { SVGRenderer } from 'echarts/renderers';
import type { CallbackDataParams } from 'echarts/types/dist/shared';
import { initOptions, updateOptions } from '../charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
} from 'echarts/components';
import { testScaleLabel, testScaleValue } from 'src/utils/numbers';
import { getFieldValueColor } from 'src/utils/colors';
import { FieldValue } from 'src/components/models';
import { useAnalysisStore } from 'src/stores/analysis';

const analysis = useAnalysisStore();
use([SVGRenderer, PieChart, TitleComponent, TooltipComponent, LegendComponent]);

interface FieldFrequenciesChartProps {
  field: string;
  height?: number;
}
const props = withDefaults(defineProps<FieldFrequenciesChartProps>(), {
  field: undefined,
  height: 300,
});
const emit = defineEmits<{
  (e: 'change:filter', value?: FieldValue): void;
}>();

const { t } = useI18n({ useScope: 'global' });

const chart = shallowRef(null);
const option = ref<EChartsOption>({});
const loading = ref(false);

const frequencies = computed(() => {
  return analysis.frequencies === null ? {} : analysis.frequencies[props.field];
});

watch(
  () => props.field,
  () => {
    initChartOptions();
  }
);

watch(
  () => frequencies.value,
  () => {
    initChartOptions();
  }
);

onMounted(() => {
  initChartOptions();
});

function onClick(params: CallbackDataParams): void {
  let val: string | number | null = params.name === 'N/A' ? null : params.name;
  if (props.field === 'test_scale') {
    val = testScaleValue(params.name);
  }
  emit('change:filter', {
    field: props.field,
    value: val,
  });
}

function keyLabel(key: string) {
  if (key === 'null' || key === 'None') {
    return 'N/A';
  }
  if (props.field === 'test_scale') {
    return testScaleLabel(key);
  }
  return key;
}

function initChartOptions() {
  option.value = {};
  if (!props.field) {
    return;
  }
  loading.value = true;

  const dataset = Object.entries(frequencies.value)
    .map(([key, value]) => ({
      name: keyLabel(key),
      value,
    }))
    .filter((item) => item.value > 0);

  const colors = dataset.map((item) =>
    getFieldValueColor(props.field, item.name)
  );

  const newOption: EChartsOption = {
    title: {
      text: `${t(props.field)}`,
      left: 'center',
    },
    animation: false,
    height: props.height,
    tooltip: {
      trigger: 'item',
      formatter: '<b>{b}</b>: {c} ({d}%)',
    },
    legend: {
      show: false,
      bottom: '0',
      left: 'center',
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        color: colors,
        avoidLabelOverlap: false,
        // label: {
        //   show: false,
        //   position: 'center',
        // },
        // labelLine: {
        //   show: false,
        // },
        emphasis: {
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold',
          },
        },
        data: dataset,
      },
    ],
  };
  option.value = newOption;
  loading.value = false;
}
</script>
