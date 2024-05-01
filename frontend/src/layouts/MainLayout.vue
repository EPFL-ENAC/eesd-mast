<template>
  <q-layout view="lHh Lpr lFf">
    <q-header bordered class="bg-white text-grey-10">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title class="text-weight-medium">
          Masonry Shake-Table Database
        </q-toolbar-title>
        <div class="row q-col-gutter-md">
          <a href="https://epfl.ch" target="_blank">
            <img src="/EPFL.svg" style="width: 80px" />
          </a>
          <a href="https://www.epfl.ch/labs/eesd/" target="_blank">
            <img src="/EESD.svg" style="width: 88px" class="float-right" />
          </a>
        </div>
      </q-toolbar>
      <q-toolbar inset style="min-height: 20px">
        <q-btn
          flat
          dense
          :label="$t('overview')"
          no-caps
          to="/"
          :class="isHome ? 'bg-grey-3' : ''"
          class="q-pt-sm q-pb-sm q-pr-md q-pl-md"
        />
        <q-btn
          flat
          dense
          :label="$t('buildings')"
          no-caps
          to="/buildings"
          :class="isBuildings ? 'bg-grey-3' : ''"
          class="on-left on-right q-pt-sm q-pb-sm q-pr-md q-pl-md"
        />
        <q-btn
          flat
          dense
          :label="$t('contact_us')"
          no-caps
          to="/submit"
          :class="isSubmit ? 'bg-grey-3' : ''"
          class="q-pt-sm q-pb-sm q-pr-md q-pl-md"
        />
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" :show-if-above="isBuildings" bordered>
      <div v-if="!isBuildings">
        <q-list>
          <q-item-label header class="text-h5">{{
            $t('resources')
          }}</q-item-label>
          <EssentialLink
            v-for="link in essentialLinks"
            :key="link.title"
            v-bind="link"
          />
        </q-list>
      </div>
      <div v-if="isBuildings">
        <q-list>
          <q-item-label header class="text-h5">{{
            $t('filters')
          }}</q-item-label>
        </q-list>
        <experiment-filters></experiment-filters>
      </div>
    </q-drawer>

    <q-drawer side="right" v-model="rightDrawerOpen" bordered>
      <div class="q-pa-md">
        <q-btn
          unelevated
          round
          icon="close"
          @click="toggleRightDrawer"
          class="float-right"
        />
      </div>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-dialog v-model="showIntro">
      <q-card>
        <q-card-section>
          <div class="q-pa-md">
            <div class="text-subtitle1 text-grey-8">
              <q-markdown :src="OverViewMd" no-line-numbers />
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat :label="$t('close')" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-layout>
</template>

<script setup lang="ts">
import { getSettings, saveSettings } from 'src/utils/settings';
import OverViewMd from 'src/assets/overview.md';
import EssentialLink, {
  EssentialLinkProps,
} from 'components/EssentialLink.vue';
import ExperimentFilters from 'src/components/ExperimentFilters.vue';

const route = useRoute();

const showIntro = ref(false);

onMounted(() => {
  const settings = getSettings();
  if (!settings.intro_shown) {
    showIntro.value = true;
    settings.intro_shown = true;
    saveSettings(settings);
  }
});

const isHome = computed(() => route.path === '/');
const isBuildings = computed(() => route.path.startsWith('/buildings'));
const isSubmit = computed(() => route.path.startsWith('/submit'));

const essentialLinks: EssentialLinkProps[] = [
  {
    title: 'EPFL',
    caption: 'epfl.ch',
    icon: 'school',
    link: 'https://epfl.ch',
  },
  {
    title: 'EESD',
    caption: 'epfl.ch/labs/eesd',
    icon: 'record_voice_over',
    link: 'https://www.epfl.ch/labs/eesd/',
  },
  {
    title: 'MAST CLI',
    caption: 'EPFL-ENAC/eesd-mast-cli',
    icon: 'code',
    link: 'https://github.com/EPFL-ENAC/eesd-mast-cli',
  },
];
const leftDrawerOpen = ref(false);
const rightDrawerOpen = ref(false);

watch(
  () => isBuildings.value,
  () => {
    if (isBuildings.value) leftDrawerOpen.value = true;
  }
);

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}
function toggleRightDrawer() {
  rightDrawerOpen.value = !rightDrawerOpen.value;
}
</script>
