<template>
  <div v-if="selected">
    <div class="q-mb-md">
      <span class="text-h6 on-left">{{ selected.reference.reference }}</span>
      <q-chip
        v-if="selected.reference.link_to_experimental_paper"
        icon="article"
        color="primary"
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
      <span v-if="reference_experiments.length > 1">
        <q-btn
          v-for="exp in reference_experiments"
          :key="exp.id"
          no-caps
          rounded
          :label="exp.experiment_id || exp.id"
          :title="exp.description"
          :disable="exp.id === selected.id"
          class="on-left"
          :class="exp.id === selected.id ? 'bg-primary text-white' : ''"
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
      <div v-if="selected.scheme">
        <div>
          <q-img
            :src="modelsSchemeUrlAlt"
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
            @click="onShowImage(modelsSchemeUrl)"
          />
        </div>
      </div>
      <div v-for="img in otherImages" :key="img.path">
        <q-img
          :src="getImageUrlAlt(img)"
          :alt="`${selected.description} [${selected.reference}]`"
          spinner-color="grey-6"
          width="250px"
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

    <div class="q-ma-md"></div>
    <div class="q-ma-md"></div>
    <q-tabs
      v-model="tab"
      dense
      class="text-grey"
      active-color="primary"
      indicator-color="primary"
      align="justify"
      narrow-indicator
    >
      <q-tab name="details" :label="$t('details')" />
      <q-tab name="3d_model" :label="$t('3d_model')" />
      <q-tab name="files" :label="$t('files')" />
      <q-tab name="reference" :label="$t('reference')" />
    </q-tabs>

    <q-separator />

    <q-tab-panels v-model="tab" animated>
      <q-tab-panel name="details">
        <experiment-fields :experiment="selected" />
      </q-tab-panel>

      <q-tab-panel name="3d_model">
        <div v-if="threeDModelFiles.length === 0" class="text-grey-6">
          {{ $t('no_3d_model') }}
        </div>
        <div v-else v-for="file in threeDModelFiles" :key="file.path">
          <vtk-viewer :file="file" />
        </div>
      </q-tab-panel>

      <q-tab-panel name="files">
        <experiment-files-view :experiment="selected" type="model" />
      </q-tab-panel>

      <q-tab-panel name="reference">
        <reference-view :experiment="selected" />
      </q-tab-panel>
    </q-tab-panels>

    <image-dialog v-model="showImage" :src="imageSrc" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'ExperimentModelView',
});
</script>
<script setup lang="ts">
import { withDefaults, ref, onMounted } from 'vue';
import { baseUrl } from 'src/boot/axios';
import VtkViewer from './VtkViewer.vue';
import ReferenceView from './ReferenceView.vue';
import ExperimentFilesView from './ExperimentFilesView.vue';
import ExperimentFields from './ExperimentFields.vue';
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
const showImage = ref(false);
const imageSrc = ref('');

const modelsSchemeUrlAlt = computed(() => {
  if (selected.value) {
    const schemeInfo = selected.value.model_files.children.find(
      (child: FileNode) => child.name.startsWith('scheme')
    );
    return getImageUrlAlt(schemeInfo);
  }
  return '';
});

const modelsSchemeUrl = computed(() => {
  if (selected.value) {
    const schemeInfo = selected.value.model_files.children.find(
      (child: FileNode) => child.name.startsWith('scheme')
    );
    return getImageUrl(schemeInfo);
  }
  return '';
});

const otherImages = computed(() => {
  if (selected.value) {
    return selected.value.model_files.children.filter(
      (f: FileNode) =>
        (f.name.endsWith('.png') || f.name.endsWith('.webp')) &&
        !f.name.startsWith('scheme')
    );
  }
  return [];
});

function getImageUrlAlt(file: FileNode) {
  return `${baseUrl}/files/${file.alt_path ? file.alt_path : file.path}`;
}

function getImageUrl(file: FileNode) {
  return `${baseUrl}/files/${file.path}`;
}

watch(() => props.experiment, updateExperiment);

onMounted(updateExperiment);

function updateExperiment() {
  if (props.experiment) {
    referencesStore
      .fetchExperiments(props.experiment.reference_id)
      .then((res) => {
        reference_experiments.value = res;
      });
    selected.value = props.experiment;
  }
}

const threeDModelFiles = computed(() => {
  if (selected.value.model_files && selected.value.model_files.children) {
    return selected.value.model_files.children.filter(
      (f: FileNode) => f.name.endsWith('.vtp') || f.alt_name?.endsWith('.vtp')
    );
  }
  return [];
});

function onShowImage(src: string) {
  imageSrc.value = src;
  showImage.value = true;
}
</script>
