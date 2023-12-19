<template>
  <q-list v-if="dbobject" separator>
    <q-item clickable v-ripple v-for="item in items" :key="item.field">
      <q-item-section>
        <q-item-label overline>
          {{ $t(item.field) }}
        </q-item-label>
      </q-item-section>
      <q-item-section>
        <q-item-label>
          <span v-if="item.html" v-html="item.html(dbobject)"></span>
          <span v-else-if="item.format">{{ item.format(dbobject) }}</span>
          <span v-else>
            {{ dbobject[item.field] ? dbobject[item.field] : '-' }}
          </span>
          {{ item.unit }}
        </q-item-label>
      </q-item-section>
    </q-item>
  </q-list>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'FieldsList',
});
</script>
<script setup lang="ts">
import { defineProps, withDefaults } from 'vue';

export interface FieldsListProps {
  dbobject: any;
  items: any;
}

withDefaults(defineProps<FieldsListProps>(), {
  dbobject: undefined,
  items: [],
});
</script>
