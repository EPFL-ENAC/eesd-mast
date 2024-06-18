<template>
  <q-dialog v-model="showDialog" maximized @hide="onHide">
    <q-card>
      <q-card-section>
        <div class="row">
          <q-space />
          <q-btn flat icon="close" size="lg" v-close-popup />
        </div>
      </q-card-section>

      <q-card-section class="text-center">
        <img :src="props.src" style="max-width: 100%" />
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'ImageDialog',
});
</script>
<script setup lang="ts">
interface DialogProps {
  modelValue: boolean;
  src: string;
}

const props = defineProps<DialogProps>();
const emit = defineEmits(['update:modelValue']);

const showDialog = ref(props.modelValue);

watch(
  () => props.modelValue,
  (value) => {
    showDialog.value = value;
  }
);

function onHide() {
  emit('update:modelValue', false);
}
</script>
