<template>
  <div v-if="selected">
    <div class="q-mt-md">
      <span class="text-subtitle1 on-left">{{
        selected.reference.reference
      }}</span>
      <q-chip
        v-if="selected.reference.link_to_experimental_paper"
        icon="article"
        color="secondary"
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
    <div class="text-caption text-grey-8">
      {{ selected.reference.full_reference }}
    </div>
    <div v-if="reference_experiments.length > 1" class="q-mt-md">
      <span class="text-caption on-left">
        {{ $t('other_experiments_of_reference') }}
      </span>
      <span>
        <q-chip
          v-for="exp in reference_experiments"
          :key="exp.id"
          :label="exp.experiment_id || exp.id"
          :title="exp.description"
          :clickable="exp.id !== selected.id"
          :class="exp.id === selected.id ? 'bg-grey-8 text-white' : ''"
          @click="onExperiment(exp)"
        />
      </span>
    </div>
    <div v-if="selected.experimental_campaign_motivation" class="q-mt-md">
      <div class="text-caption">
        {{ $t('test_motivation') }}
      </div>
      <div class="text-grey-8">
        {{ selected.experimental_campaign_motivation }}
      </div>
    </div>
    <q-card flat class="q-mt-md">
      <q-card-section v-if="selected.scheme">
        <div class="row justify-center q-gutter-xl">
          <div class="column">
            <div class="col-auto text-center">
              <q-btn
                :label="$t('view_test')"
                no-caps
                icon="analytics"
                color="accent"
                :to="`/test/${selected.id}`"
                class="full-width q-mb-md"
              />
            </div>
            <div class="col">
              <q-img
                :src="schemeUrl"
                :alt="`${selected.description} [${selected.reference}]`"
                spinner-color="grey-6"
                width="250px"
              />
            </div>
          </div>
          <div v-if="hasModels" class="column">
            <div class="col-auto text-center">
              <q-btn
                :label="$t('view_model')"
                no-caps
                icon="house_siding"
                color="secondary"
                :to="`/model/${selected.id}`"
                class="full-width q-mb-md"
              />
            </div>
            <div class="col">
              <q-img
                v-if="hasModels"
                :src="modelsSchemeUrl"
                :alt="`${selected.description} [${selected.reference}]`"
                spinner-color="grey-6"
                width="250px"
              />
            </div>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'ExperimentSummary',
});
</script>
<script setup lang="ts">
import { withDefaults, ref, onMounted } from 'vue';
import { cdnUrl } from 'src/boot/axios';
import { FileNode, Experiment } from 'src/components/models';
import { useReferencesStore } from 'src/stores/references';

const referencesStore = useReferencesStore();

interface ExperimentViewProps {
  experiment: Experiment;
}
const props = withDefaults(defineProps<ExperimentViewProps>(), {
  experiment: undefined,
});

const selected = ref();
const reference_experiments = ref<Experiment[]>([]);

const modelsSchemeUrl = computed(() => {
  if (selected.value) {
    const schemeInfo = selected.value.model_files.children.find(
      (child: FileNode) => child.name.startsWith('scheme')
    );
    return schemeInfo
      ? `${cdnUrl}${
          schemeInfo.alt_path ? schemeInfo.alt_path : schemeInfo.path
        }`
      : '';
  }
  return '';
});

const schemeUrl = computed(() => {
  if (selected.value) {
    return `${cdnUrl}${selected.value.scheme.path}`;
  }
  return '';
});

const hasModels = computed(() => selected.value?.model_files);

const onExperiment = (exp: Experiment) => {
  selected.value = exp;
};

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
</script>
