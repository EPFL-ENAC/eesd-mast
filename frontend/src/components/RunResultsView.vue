<template>
  <div>
    <q-table
      :rows="runResultsStore.run_results_digest"
      :columns="visibleColummns"
      row-key="run_id"
      hide-pagination
      :rows-per-page-options="[0]"
    >
      <template v-slot:header="props">
        <q-tr :props="props">
          <q-th auto-width v-if="hasFiles()" />
          <q-th v-for="col in props.cols" :key="col.name" :props="props">
            {{ col.label }}
          </q-th>
        </q-tr>
      </template>
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td auto-width v-if="hasFiles()">
            <q-btn
              v-if="hasRunFiles(props.row.run_id)"
              size="xs"
              color="secondary"
              round
              flat
              dense
              @click="props.expand = !props.expand"
              :icon="props.expand ? 'remove' : 'add'"
            />
          </q-td>
          <q-td v-for="col in props.cols" :key="col.name" :props="props">
            {{ col.value }}
          </q-td>
        </q-tr>
        <q-tr v-show="props.expand" :props="props">
          <q-td colspan="100%" class="q-pa-none">
            <div class="justify-left">
              <q-expansion-item
                v-if="getRunFiles(props.row.run_id).top_displacement_histories"
                :label="$t('top_displacement_histories')"
                header-class="bg-grey-3"
                switch-toggle-side
                style="width: calc(100vw - 100px)"
                @show="loadRunFiles(props.row.run_id)"
              >
                <q-card>
                  <q-card-section>
                    <file-node-chart
                      v-if="displayed.includes(props.row.run_id.toString())"
                      :node="
                        getRunFiles(props.row.run_id).top_displacement_histories
                      "
                      :xname="$t('time_sec')"
                      :yname="$t('displacement_mm')"
                    />
                  </q-card-section>
                </q-card>
              </q-expansion-item>
              <q-expansion-item
                v-if="
                  getRunFiles(props.row.run_id).global_force_displacement_curve
                "
                :label="$t('global_force_displacement_curve')"
                header-class="bg-grey-3"
                switch-toggle-side
                style="width: calc(100vw - 100px)"
                @show="loadRunFiles(props.row.run_id)"
              >
                <q-card>
                  <q-card-section>
                    <file-node-chart
                      v-if="displayed.includes(props.row.run_id.toString())"
                      :node="
                        getRunFiles(props.row.run_id)
                          .global_force_displacement_curve
                      "
                      :xname="$t('top_displacement_mm')"
                      :yname="$t('base_shear_kn')"
                    />
                  </q-card-section>
                </q-card>
              </q-expansion-item>
              <q-expansion-item
                v-if="getRunFiles(props.row.run_id).shake_table_accelerations"
                :label="$t('shake_table_accelerations')"
                header-class="bg-grey-3"
                switch-toggle-side
                style="width: calc(100vw - 100px)"
                @show="loadRunFiles(props.row.run_id)"
              >
                <q-card>
                  <q-card-section>
                    <file-node-chart
                      v-if="displayed.includes(props.row.run_id.toString())"
                      :node="
                        getRunFiles(props.row.run_id).shake_table_accelerations
                      "
                      :xname="$t('time_sec')"
                      :yname="$t('acceleration_g')"
                    />
                  </q-card-section>
                </q-card>
              </q-expansion-item>
              <q-expansion-item
                v-if="getRunFiles(props.row.run_id).crack_maps"
                :label="$t('crack_maps')"
                header-class="bg-grey-3"
                switch-toggle-side
                style="width: calc(100vw - 100px)"
              >
                <q-card>
                  <q-card-section>
                    <q-img
                      :src="`${cdnUrl}${
                        getRunFiles(props.row.run_id).crack_maps?.path
                      }`"
                      spinner-color="grey-6"
                      fit="scale-down"
                    />
                  </q-card-section>
                </q-card>
              </q-expansion-item>
            </div>
          </q-td>
        </q-tr>
      </template>
    </q-table>
    <q-tooltip
      v-model="showChartsTip"
      anchor="center middle"
      self="center middle"
      no-parent-event
      class="bg-grey-7 text-white"
    >
      <div
        class="q-pt-md q-pl-md q-pr-md"
        style="width: 400px; font-size: medium"
      >
        <q-markdown :src="$t('echarts_zoom_help')" />
      </div>
    </q-tooltip>
  </div>
</template>

<script lang="ts">
export default defineComponent({
  name: 'RunResultsView',
});
</script>
<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { withDefaults, ref } from 'vue';
import { cdnUrl } from 'src/boot/axios';
import {
  Experiment,
  RunResult,
  RunResultFileNodes,
} from 'src/components/models';
import FileNodeChart from './charts/FileNodeChart.vue';
import { toMaxDecimals, toFixed } from 'src/utils/numbers';
import { Settings } from 'src/stores/settings';

const { t } = useI18n({ useScope: 'global' });
const settingsStore = useSettingsStore();

interface RunResultsViewProps {
  experiment: Experiment;
}
const props = withDefaults(defineProps<RunResultsViewProps>(), {
  experiment: undefined,
});

const runResultsStore = useRunResultsStore();
const displayed = ref<string[]>([]);
const showChartsTip = ref(false);

const columns = [
  'run_id',
  'nominal_pga_x',
  'nominal_pga_y',
  'nominal_pga_z',
  'actual_pga_x',
  'actual_pga_y',
  'actual_pga_z',
  'dg_reported',
  'dg_derived',
  'max_top_drift_x',
  'max_top_drift_y',
  'residual_top_drift_x',
  'residual_top_drift_y',
  'base_shear_coef',
  'reported_t1_x',
  'reported_t1_y',
].map((name) => {
  return {
    name: name,
    required: true,
    label: t(name),
    align: 'left',
    field: name,
    format: (val: unknown) =>
      val === null
        ? '-'
        : typeof val === 'string'
        ? val
        : name.startsWith('dg_')
        ? toMaxDecimals(val as number, 3)
        : toFixed(val as number, 3),
    sortable: true,
  };
});

const visibleColummns = computed(() => {
  return columns.filter(
    (col) =>
      runResultsStore.run_results_digest.filter(
        (run: RunResult) => run[col.name] !== null
      ).length > 0
  );
});

function loadRunFiles(run_id: number) {
  if (!displayed.value.includes(run_id.toString())) {
    displayed.value.push(run_id.toString());
    triggerChartsTip();
  }
}

function hasFiles() {
  return props.experiment.test_files;
}

function hasRunFiles(run_id: number) {
  const nodes = getRunFiles(run_id);
  return (
    nodes.top_displacement_histories ||
    nodes.global_force_displacement_curve ||
    nodes.shake_table_accelerations ||
    nodes.crack_maps
  );
}

function getRunFiles(run_id: number): RunResultFileNodes {
  const nodes: RunResultFileNodes = {
    top_displacement_histories: undefined,
    global_force_displacement_curve: undefined,
    shake_table_accelerations: undefined,
    crack_maps: undefined,
  };
  if (props.experiment.test_files && props.experiment.test_files.children) {
    props.experiment.test_files.children.forEach((element) => {
      if (element.name === 'Top displacement histories') {
        nodes.top_displacement_histories = element.children?.find(
          (child) => child.name === `${run_id}.txt`
        );
      }
      if (element.name === 'Global force-displacement curve') {
        nodes.global_force_displacement_curve = element.children?.find(
          (child) => child.name === `${run_id}.txt`
        );
      }
      if (element.name === 'Shake-table accelerations') {
        nodes.shake_table_accelerations = element.children?.find(
          (child) => child.name === `${run_id}.txt`
        );
      }
      if (element.name === 'Crack maps') {
        nodes.crack_maps = element.children?.find(
          (child) => child.name === `${run_id}.png`
        );
      }
    });
  }

  return nodes;
}

function triggerChartsTip() {
  if (!showChartsTip.value && !settingsStore.settings?.run_results_tips) {
    showChartsTip.value = true;
    setTimeout(() => {
      showChartsTip.value = false;
      settingsStore.saveSettings({ run_results_tips: true } as Settings);
    }, 5000);
  }
}
</script>

<style scoped>
.q-table td.q-pa-none {
  padding: 0;
}
</style>
