<template>
  <div v-if="selected">
    <div class="q-mb-md">
      <span class="text-subtitle1 on-left">{{
        selected.reference.reference
      }}</span>
      <q-chip
        v-if="selected.reference.link_to_experimental_paper"
        icon="article"
        color="accent"
        text-color="white"
        class="on-left"
      >
        <a
          :href="selected.reference.link_to_experimental_paper"
          target="_blank"
          style="text-decoration: none; color: white"
        >
          {{ $t('paper') }}
        </a>
      </q-chip>
      <q-chip
        v-if="selected.reference.link_to_request_data"
        icon="grid_on"
        color="grey-7"
        text-color="white"
        class="on-left"
      >
        <a
          :href="selected.reference.link_to_request_data"
          target="_blank"
          style="text-decoration: none; color: white"
        >
          {{ $t('data') }}
        </a>
      </q-chip>
    </div>
    <div v-if="reference_experiments.length > 1" class="q-mb-md">
      <span class="text-caption on-left">
        {{ $t('other_experiments_of_reference') }}
      </span>
      <span>
        <q-btn
          v-for="exp in reference_experiments"
          :key="exp.id"
          no-caps
          rounded
          :label="exp.experiment_id || exp.id"
          :title="exp.description"
          :disable="exp.id === selected.id"
          class="on-left"
          :class="exp.id === selected.id ? 'bg-grey-8 text-white' : ''"
          :to="`/test/${exp.id}`"
        />
      </span>
    </div>
    <div v-if="selected.experimental_campaign_motivation">
      <div class="text-caption">
        {{ $t('test_motivation') }}
      </div>
      <div class="text-subtitle1 text-grey-8">
        {{ selected.experimental_campaign_motivation }}
      </div>
    </div>
    <div class="row q-gutter-md q-mt-md q-mb-md">
      <div class="col-12 col-md-auto">
        <div v-if="selected.scheme">
          <div>
            <q-img
              :src="schemeUrl"
              :alt="`${selected.description} [${selected.reference}]`"
              spinner-color="grey-6"
              width="250px"
            />
          </div>
          <div class="text-center">
            <q-btn
              dense
              flat
              no-caps
              icon="zoom_in"
              class="text-caption text-primary full-width"
              :label="$t('zoom_image')"
              @click="onShowImage(schemeUrl)"
            />
          </div>
        </div>
        <div v-for="img in planImages" :key="img.id" class="q-mt-md">
          <q-img
            :src="getImageUrlAlt(img)"
            :alt="img.name"
            spinner-color="grey-6"
            width="250px"
            style="border: 1px solid #e0e0e0"
          />
          <div class="text-center">
            <q-btn
              dense
              flat
              no-caps
              icon="zoom_in"
              class="text-caption text-primary full-width"
              :label="$t('zoom_image')"
              @click="onShowImage(getImageUrl(img))"
            />
          </div>
        </div>
      </div>
      <div class="col-12 col-md">
        <div
          v-if="!hasPgaX && !hasPgaY"
          class="q-pt-xl q-pb-xl q-pl-lg q-pr-lg bg-grey-2 text-center text-caption text-grey-8"
        >
          {{ $t('no_period_evolution') }}
        </div>
        <pga-chart
          :experiment="selected"
          direction="x"
          :height="300"
          @loaded="(v) => (hasPgaX = v)"
        />
        <pga-chart
          :experiment="selected"
          direction="y"
          :height="300"
          @loaded="(v) => (hasPgaY = v)"
        />
      </div>
      <div class="col-12 col-md">
        <dg-chart :experiment="selected" :height="300" />
      </div>
    </div>

    <div class="q-ma-md"></div>
    <div class="q-ma-md"></div>
    <q-tabs
      v-model="tab"
      dense
      class="text-grey"
      active-color="secondary"
      indicator-color="secondary"
      align="justify"
    >
      <q-tab name="details" :label="$t('details')" />
      <q-tab name="run_results" :label="$t('run_results')" />
      <q-tab name="files" :label="$t('test_files')" />
      <q-tab name="reference" :label="$t('reference')" />
    </q-tabs>

    <q-separator />

    <q-tab-panels v-model="tab" animated>
      <q-tab-panel name="details">
        <experiment-fields :experiment="selected" />
      </q-tab-panel>

      <q-tab-panel name="run_results">
        <run-results-view :experiment="selected" />
      </q-tab-panel>

      <q-tab-panel name="files">
        <experiment-files-view :experiment="selected" type="test" />
      </q-tab-panel>

      <q-tab-panel name="reference">
        <reference-view :experiment="selected" />
      </q-tab-panel>
    </q-tab-panels>

    <image-dialog v-model="showImage" :src="imageSrc" />
  </div>
</template>

<script lang="ts">
export default defineComponent({
  name: 'ExperimentTestView',
});
</script>
<script setup lang="ts">
import { withDefaults, ref, onMounted } from 'vue';
import { cdnUrl } from 'src/boot/axios';
import ReferenceView from './ReferenceView.vue';
import RunResultsView from './RunResultsView.vue';
import ExperimentFilesView from './ExperimentFilesView.vue';
import ExperimentFields from './ExperimentFields.vue';
import PgaChart from './charts/PgaChart.vue';
import DgChart from './charts/DgChart.vue';
import ImageDialog from './ImageDialog.vue';
import { Experiment, FileNode } from 'src/components/models';
import { useReferencesStore } from 'src/stores/references';

const referencesStore = useReferencesStore();

interface ExperimentViewProps {
  experiment: Experiment;
}
const props = withDefaults(defineProps<ExperimentViewProps>(), {
  experiment: undefined,
});

const tab = ref('details');
const selected = ref();
const reference_experiments = ref<Experiment[]>([]);
const hasPgaX = ref(true);
const hasPgaY = ref(true);
const showImage = ref(false);
const imageSrc = ref('');

const schemeUrl = computed(() => {
  if (selected.value && selected.value.scheme) {
    return `${cdnUrl}${selected.value.scheme.path}`;
  }
  return '';
});

const planImages = computed(() => {
  let imagesFolder = selected.value.plan_files;
  if (imagesFolder && imagesFolder.children) {
    return imagesFolder.children.filter(
      (f: FileNode) => f.name.endsWith('.png') || f.name.endsWith('.webp')
    );
  }
  return [];
});

function getImageUrlAlt(file: FileNode) {
  return `${cdnUrl}${file.alt_path ? file.alt_path : file.path}`;
}

function getImageUrl(file: FileNode) {
  return `${cdnUrl}${file.path}`;
}

watch(() => props.experiment, updateExperiment);

onMounted(updateExperiment);

function updateExperiment() {
  if (props.experiment) {
    referencesStore
      .fetchExperiments(props.experiment.reference_id)
      .then((res) => {
        res.sort((a, b) => {
          const labelA = a.experiment_id || a.id + '';
          const labelB = b.experiment_id || b.id + '';
          return labelA.localeCompare(labelB);
        });
        reference_experiments.value = res;
      });
    selected.value = props.experiment;
  }
}

function onShowImage(src: string) {
  imageSrc.value = src;
  showImage.value = true;
}
</script>
