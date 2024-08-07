<template>
  <div v-if="selected">
    <div class="q-mb-md">
      <span class="text-subtitle1 on-left">{{
        $t('model_of', { ref: selected.reference.reference })
      }}</span>
    </div>
    <div class="row q-gutter-md q-mt-md">
      <div v-if="selected.scheme">
        <div>
          <q-img
            :src="modelsSchemeUrlAlt"
            :alt="`${selected.description} [${selected.reference}]`"
            spinner-color="grey-6"
            width="300px"
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
          width="300px"
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
      <div v-if="threeDModelFiles.length > 0">
        <div v-for="file in threeDModelFiles" :key="file.path">
          <vtk-viewer
            :file="file"
            :download="false"
            :with-representation="false"
            width="400px"
          />
        </div>
      </div>
    </div>

    <div v-if="threeDModelFiles.length > 0">
      <div class="text-grey-6 q-mt-md">
        <q-icon name="info"></q-icon>
        {{ $t('vtk_notice') }}
      </div>
      <q-tooltip
        v-model="showVtkTip"
        anchor="top middle"
        self="top middle"
        no-parent-event
        class="bg-grey-7 text-white"
      >
        <div
          class="q-pt-md q-pl-md q-pr-md"
          style="width: 400px; font-size: medium"
        >
          <q-markdown :src="$t('vtk_help')" />
        </div>
      </q-tooltip>
    </div>

    <q-tabs
      v-model="tab"
      dense
      class="text-grey q-mt-xl"
      active-color="secondary"
      active-bg-color="light-blue-1"
      indicator-color="secondary"
      align="justify"
    >
      <q-tab name="details" :label="$t('modeling_assumptions')" />
      <q-tab name="files" :label="$t('model_files')" />
    </q-tabs>

    <q-separator />

    <q-tab-panels v-model="tab" animated>
      <q-tab-panel name="details">
        <numerical-model-fields
          :numerical_model="numericalModelsStore.numerical_model"
        />
      </q-tab-panel>

      <q-tab-panel name="files">
        <experiment-files-view :experiment="selected" type="model" />
      </q-tab-panel>
    </q-tab-panels>

    <image-dialog v-model="showImage" :src="imageSrc" />
  </div>
</template>

<script lang="ts">
export default defineComponent({
  name: 'ExperimentModelView',
});
</script>
<script setup lang="ts">
import { withDefaults, ref, onMounted } from 'vue';
import { cdnUrl } from 'src/boot/axios';
import VtkViewer from './VtkViewer.vue';
import ExperimentFilesView from './ExperimentFilesView.vue';
import NumericalModelFields from './NumericalModelFields.vue';
import ImageDialog from './ImageDialog.vue';
import { Experiment, FileNode } from 'src/components/models';
import { useReferencesStore } from 'src/stores/references';
import { useNumericalModelsStore } from 'src/stores/numerical_models';
import { Settings } from 'src/stores/settings';

const referencesStore = useReferencesStore();
const numericalModelsStore = useNumericalModelsStore();
const settingsStore = useSettingsStore();

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
const showVtkTip = ref(false);

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
    numericalModelsStore.fetchNumericalModel(props.experiment.id);
    if (settingsStore.settings?.intro_shown) {
      triggerVtkTips();
    }
  }
}

watch(
  () => settingsStore.settings,
  () => {
    if (settingsStore.settings?.intro_shown) {
      triggerVtkTips();
    }
  }
);

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

function triggerVtkTips() {
  if (!showVtkTip.value && !settingsStore.settings?.vtk_tips) {
    showVtkTip.value = true;
    setTimeout(() => {
      showVtkTip.value = false;
      const settings = { ...settingsStore.settings } as Settings;
      settings.vtk_tips = true;
      settingsStore.saveSettings(settings);
    }, 5000);
  }
}
</script>
