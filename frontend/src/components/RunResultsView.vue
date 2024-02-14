<template>
  <div>
    <div>
      <period-chart v-if="runResults" :results="runResults" height="600px" />
    </div>
    <q-table
      :rows="runResults"
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
            <div class="text-left">
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
                      height="600px"
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
                      height="600px"
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
                      height="600px"
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
                      :src="`${baseUrl}/files/${
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
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { toMaxDecimals } from 'src/utils/numbers';
export default defineComponent({
  name: 'RunResultsView',
});
</script>
<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { withDefaults, onMounted, ref, watch } from 'vue';
import { baseUrl } from 'src/boot/axios';
import { useRunResultsStore } from 'src/stores/run_results';
import {
  Experiment,
  RunResult,
  RunResultFileNodes,
} from 'src/components/models';
import FileNodeChart from './FileNodeChart.vue';
import PeriodChart from './PeriodChart.vue';

const { t } = useI18n({ useScope: 'global' });

export interface RunResultsViewProps {
  experiment: Experiment;
}
const props = withDefaults(defineProps<RunResultsViewProps>(), {
  experiment: undefined,
});

const runResultsStore = useRunResultsStore();
const runResults = ref();
const displayed = ref<string[]>([]);

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
        : toMaxDecimals(val as number, 3),
    sortable: true,
  };
});

const visibleColummns = computed(() => {
  return columns.filter(
    (col) =>
      runResults.value?.filter((run: RunResult) => run[col.name] !== null)
        .length > 0
  );
});

watch(() => props.experiment, updateRunResults);

onMounted(updateRunResults);

function updateRunResults() {
  if (props.experiment) {
    runResultsStore
      .fetchRunResults(props.experiment.id)
      .then((res: RunResult[]) => {
        runResults.value = res.filter(
          (run) => !['Initial', 'Final'].includes(run.run_id)
        );
      });
  }
}

function loadRunFiles(run_id: number) {
  if (!displayed.value.includes(run_id.toString())) {
    displayed.value.push(run_id.toString());
  }
}

function hasFiles() {
  return props.experiment.files;
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
  if (props.experiment.files && props.experiment.files.children) {
    props.experiment.files.children.forEach((element) => {
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
</script>

<style scoped>
.q-table td.q-pa-none {
  padding: 0;
}
</style>
