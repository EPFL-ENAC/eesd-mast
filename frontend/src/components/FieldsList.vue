<template>
  <q-list v-if="dbobject" separator>
    <q-item v-for="item in visibleItems" :key="item.field">
      <q-item-section>
        <q-item-label overline>
          {{ $t(item.field) }}
        </q-item-label>
      </q-item-section>
      <q-item-section>
        <q-item-label>
          <span v-if="item.html" v-html="item.html(dbobject)"></span>
          <div v-else-if="item.links">
            <dt v-if="item.links(dbobject) && item.links(dbobject).length">
              <dl
                v-for="link in item.links(dbobject)"
                :key="link"
                class="q-mt-sm q-mb-sm field-item"
              >
                <a :href="link" target="_blank">
                  {{ truncateString(link, 100) }}
                  <q-icon name="open_in_new" />
                </a>
              </dl>
            </dt>
            <span v-else>-</span>
          </div>
          <span v-else-if="item.format">{{ item.format(dbobject) }}</span>
          <span v-else>
            {{
              dbobject[item.field]
                ? typeof dbobject[item.field] === 'number'
                  ? toMaxDecimals(dbobject[item.field], 3)
                  : dbobject[item.field]
                : '-'
            }}
          </span>
          {{ item.unit }}
          <div
            v-if="item.comment && item.comment(dbobject)"
            class="text-grey-6 q-mt-sm"
          >
            {{ item.comment(dbobject) }}
          </div>
        </q-item-label>
      </q-item-section>
    </q-item>
  </q-list>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { toMaxDecimals } from 'src/utils/numbers';
export default defineComponent({
  name: 'FieldsList',
});
</script>
<script setup lang="ts">
import { withDefaults } from 'vue';
import { DBModel, Experiment, Reference } from 'src/components/models';

export interface FieldItem<T extends DBModel> {
  field: string;
  unit?: string;
  format?: (val: T) => string;
  links?: (val: T) => string[] | null; // href
  html?: (val: T) => string;
  visible?: (val: T) => boolean;
  comment?: (val: T) => string;
}

export interface FieldsListProps {
  dbobject: Experiment | Reference;
  items: FieldItem<Experiment | Reference>[];
}

const props = withDefaults(defineProps<FieldsListProps>(), {
  dbobject: undefined,
  items: undefined,
});

const visibleItems = computed(() => {
  return props.items.filter((item) => {
    if (item.visible) {
      return item.visible(props.dbobject);
    }
    return true;
  });
});

function truncateString(str: string, num: number) {
  if (str.length <= num) {
    return str;
  }
  return str.slice(0, num) + '...';
}
</script>
