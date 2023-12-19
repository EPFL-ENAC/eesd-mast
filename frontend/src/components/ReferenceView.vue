<template>
  <div>
    <fields-list :items="items" :dbobject="reference" />
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
export default defineComponent({
  components: { FieldsList },
  name: 'ReferenceView',
});
</script>
<script setup lang="ts">
import { defineProps, withDefaults, onMounted, ref, watch } from 'vue';
import { useReferencesStore } from 'src/stores/references';
import { Experiment } from 'src/components/models';
import FieldsList from './FieldsList.vue';

export interface ReferenceViewProps {
  experiment: Experiment;
}
const props = withDefaults(defineProps<ReferenceViewProps>(), {
  experiment: undefined,
});

const referencesStore = useReferencesStore();
const reference = ref();

const items = [
  {
    field: 'reference',
  },
  {
    field: 'full_reference',
  },
  {
    field: 'publication_year',
  },
  {
    field: 'link_to_experimental_paper',
    html: (val: any) =>
      val.link_to_experimental_paper
        ? `<a href="${val.link_to_experimental_paper}" target="_blank">${val.link_to_experimental_paper}</a>`
        : '-',
  },
  {
    field: 'corresponding_author_name',
  },
  {
    field: 'corresponding_author_email',
    html: (val: any) =>
      val.corresponding_author_email
        ? `<a href="mailto:${val.corresponding_author_email}" target="_blank">${val.corresponding_author_email}</a>`
        : '-',
  },
  {
    field: 'request_data_available',
  },
  {
    field: 'link_to_request_data',
    html: (val: any) =>
      val.link_to_request_data
        ? `<a href="${val.link_to_request_data}" target="_blank">${val.link_to_request_data}</a>`
        : '-',
  },
];

watch(() => props.experiment, updateReference);

onMounted(updateReference);

function updateReference() {
  if (props.experiment) {
    referencesStore
      .fetchReference(props.experiment.reference_id)
      .then((res) => {
        reference.value = res;
      });
  }
}
</script>
