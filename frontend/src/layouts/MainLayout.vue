<template>
  <q-layout view="hHh Lpr lFf">
    <q-header bordered class="bg-white text-grey-10">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          :disable="!isBuildings"
          @click="toggleLeftDrawer"
        />

        <span class="text-h6 q-ml-md q-mr-xl">
          Masonry Shake-Table Database
        </span>
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
        <q-space />
        <q-btn flat :label="$t('contact_us')" no-caps @click="onShowContact" />
        <q-btn
          flat
          round
          icon="info"
          :title="$t('introduction')"
          @click="onShowIntro"
          class="on-left"
        ></q-btn>
        <a href="https://epfl.ch" target="_blank" class="q-mr-lg q-mt-sm">
          <img src="/EPFL.svg" style="width: 80px" />
        </a>
        <a
          href="https://www.epfl.ch/labs/eesd/"
          target="_blank"
          class="q-mt-sm"
        >
          <img src="/EESD.svg" style="width: 88px" class="float-right" />
        </a>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" :show-if-above="isBuildings" bordered>
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
        <q-card-section class="q-ml-md q-mr-md">
          <div class="text-subtitle1 text-grey-8">
            <q-markdown :src="OverViewMd" no-line-numbers />
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat :label="$t('close')" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="showContact">
      <q-card>
        <q-card-section class="q-ml-md q-mr-md">
          <div class="q-pa-md">
            <p>{{ $t('contact_us_intro') }}</p>

            <div class="q-mt-md">
              <q-btn
                color="red"
                no-caps
                label="Katrin Beyer"
                @click="openPeoplePage('katrin.beyer')"
              />
              <q-btn
                class="on-right"
                color="red"
                no-caps
                label="Mathias Haindl"
                @click="openPeoplePage('mathias.haindl')"
              />
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
const showContact = ref(false);

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
    leftDrawerOpen.value = isBuildings.value;
  }
);

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}
function toggleRightDrawer() {
  rightDrawerOpen.value = !rightDrawerOpen.value;
}

function onShowIntro() {
  showIntro.value = true;
}

function onShowContact() {
  showContact.value = true;
}

function openPeoplePage(username: string) {
  window.open(`https://people.epfl.ch/${username}?lang=en`);
}
</script>
