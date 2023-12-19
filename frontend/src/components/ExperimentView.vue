<template>
  <div>
    <div class="text-h5">
      {{ experiment.description }}
      <span v-if="experiment.experiment_id">
        - {{ experiment.experiment_id }}
      </span>
    </div>
    <div class="text-subtitle1 q-mb-md">{{ experiment.reference }}</div>
    <div class="text-subtitle1 text-grey-8">
      {{ experiment.experimental_campaign_motivation }}
    </div>
    <q-card flat class="q-mt-md q-mb-md">
      <q-card-section class="text-center">
        <div>
          <q-img
            v-if="imageDisplay === 'fitted'"
            :src="`${baseUrl}/files/${experiment.scheme.path}`"
            :alt="`${experiment.description} [${experiment.reference}]`"
            spinner-color="grey-6"
            width="250px"
          />
          <img
            v-else
            :src="`${baseUrl}/files/${experiment.scheme.path}`"
            :alt="`${experiment.description} [${experiment.reference}]`"
            spinner-color="grey-6"
          />
        </div>
        <div>
          <span class="text-caption">{{ $t('image_size') }}</span>
          <q-btn
            :disable="imageDisplay === 'fitted'"
            :label="$t('fitted_size')"
            dense
            flat
            no-caps
            size="sm"
            @click="imageDisplay = 'fitted'"
            class="on-left on-right"
          />
          <q-btn
            :disable="imageDisplay !== 'fitted'"
            :label="$t('original_size')"
            dense
            flat
            no-caps
            size="sm"
            @click="imageDisplay = 'full'"
          />
        </div>
      </q-card-section>
    </q-card>
    <q-list separator>
      <q-item clickable v-ripple v-for="item in items" :key="item.field">
        <q-item-section>
          <q-item-label overline>
            {{ $t(item.field) }}
          </q-item-label>
        </q-item-section>
        <q-item-section>
          <q-item-label>
            <span v-if="item.html" v-html="item.html(experiment)"></span>
            <span v-else-if="item.format">{{ item.format(experiment) }}</span>
            <span v-else>
              {{ experiment[item.field] ? experiment[item.field] : '-' }}
            </span>
            {{ item.unit }}
          </q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'ExperimentView',
});
</script>
<script setup lang="ts">
import { defineProps, withDefaults, ref } from 'vue';
import { baseUrl } from 'src/boot/axios';
export interface ExperimentViewProps {
  experiment: any;
}
withDefaults(defineProps<ExperimentViewProps>(), {
  experiment: {},
});

const imageDisplay = ref('fitted');

const items = [
  {
    field: 'storeys_nb',
  },
  {
    field: 'building_height',
    unit: 'm',
  },
  {
    field: 'total_building_height',
    unit: 'm',
  },
  {
    field: 'test_scale',
  },
  {
    field: 'simultaneous_excitations_nb',
  },
  {
    field: 'applied_excitation_directions',
    format: (val: any) =>
      val.applied_excitation_directions
        ? val.applied_excitation_directions.join(' / ')
        : '-',
  },
  {
    field: 'diaphragm_material',
  },
  {
    field: 'roof_material_geometry',
  },
  {
    field: 'masonry_unit_material',
  },
  {
    field: 'masonry_unit_type',
  },
  {
    field: 'mortar_type',
  },
  {
    field: 'masonry_compressive_strength',
    unit: 'MPa',
  },
  {
    field: 'masonry_wall_thickness',
    format: (val: any) =>
      val.masonry_wall_thickness ? val.masonry_wall_thickness.join(' / ') : '-',
    unit: 'mm',
  },
  {
    field: 'wall_leaves_nb',
  },
  {
    field: 'internal_walls',
    format: (val: any) => (val.open_measured_data ? 'Yes' : 'No'),
  },
  {
    field: 'mechanical_connectors',
  },
  {
    field: 'connectors_activation',
  },
  {
    field: 'retrofitted',
    format: (val: any) => (val.open_measured_data ? 'Yes' : 'No'),
  },
  {
    field: 'retrofitting_application',
  },
  {
    field: 'retrofitting_type',
    format: (val: any) =>
      val.retrofitting_type ? val.retrofitting_type.join(' / ') : '-',
  },
  {
    field: 'first_estimated_fundamental_period',
  },
  {
    field: 'last_estimated_fundamental_period',
  },
  {
    field: 'max_horizontal_pga',
  },
  {
    field: 'max_estimated_dg',
  },
  {
    field: 'material_characterizations',
    format: (val: any) =>
      val.material_characterizations
        ? val.material_characterizations.join(' / ')
        : '-',
  },
  {
    field: 'associated_test_types',
    format: (val: any) =>
      val.associated_test_types ? val.associated_test_types.join(' / ') : '-',
  },
  {
    field: 'material_characterization_refs',
    format: (val: any) =>
      val.material_characterization_refs
        ? val.material_characterization_refs.join(' / ')
        : '-',
  },
  {
    field: 'digitalized_data',
    format: (val: any) => (val.open_measured_data ? 'Yes' : 'No'),
  },
  {
    field: 'experimental_results_reported',
    format: (val: any) =>
      val.experimental_results_reported
        ? val.experimental_results_reported.join(' / ')
        : '-',
  },
  {
    field: 'open_measured_data',
    format: (val: any) => (val.open_measured_data ? 'Yes' : 'No'),
  },
  {
    field: 'link_to_open_measured_data',
    html: (val: any) =>
      val.link_to_open_measured_data
        ? `<a href="${val.link_to_open_measured_data}" target="_blank">${val.link_to_open_measured_data}</a>`
        : '-',
  },
  {
    field: 'crack_types_observed',
    format: (val: any) =>
      val.crack_types_observed ? val.crack_types_observed.join(' / ') : '-',
  },
];
</script>
