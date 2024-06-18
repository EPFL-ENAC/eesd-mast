<template>
  <div>
    <fields-list :items="items" :dbobject="reference" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  components: { FieldsList },
  name: 'ReferenceView',
});
</script>
<script setup lang="ts">
import { withDefaults, onMounted, ref, watch } from 'vue';
import { useReferencesStore } from 'src/stores/references';
import { Experiment, Reference } from 'src/components/models';
import FieldsList, { FieldItem } from './FieldsList.vue';

export interface ReferenceViewProps {
  experiment: Experiment;
}
const props = withDefaults(defineProps<ReferenceViewProps>(), {
  experiment: undefined,
});

const referencesStore = useReferencesStore();
const reference = ref();

const items: FieldItem<Reference>[] = [
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
    format: (val: Reference) => '',
    links: (val: Reference) =>
      val.link_to_experimental_paper ? [val.link_to_experimental_paper] : [],
  },
  {
    field: 'corresponding_author',
    html: (val: Reference) =>
      val.corresponding_author_email
        ? `${val.corresponding_author_name} &lt;<a href="mailto:${val.corresponding_author_email}" target="_blank">${val.corresponding_author_email}</a>&gt;`
        : '-',
  },
  {
    field: 'link_to_request_data',
    format: (val: Reference) => '',
    links: (val: Reference) =>
      val.link_to_request_data ? [val.link_to_request_data] : [],
    visible: (val: Reference) => val.link_to_request_data !== null,
  },
];

watch(() => props.experiment, updateReference);

onMounted(updateReference);

function updateReference() {
  if (props.experiment) {
    if (props.experiment.reference) {
      reference.value = props.experiment.reference;
    } else {
      referencesStore
        .fetchReference(props.experiment.reference_id)
        .then((res) => {
          reference.value = res;
        });
    }
  }
}
</script>
