<template>
  <q-toolbar>
    <q-btn
      v-if="$q.screen.lt.md && isBuildings"
      flat
      dense
      round
      icon="menu"
      aria-label="Menu"
      :disable="!isBuildings"
    />
    <a href="https://epfl.ch" target="_blank" class="q-mt-sm">
      <img src="/EPFL_logo.png" style="height: 25px" />
    </a>
    <q-tabs shrink stretch active-color="primary" class="q-ml-md">
      <q-route-tab
        no-caps
        to="/"
        :label="$t('overview')"
        exact
        content-class="app-tab"
      />
      <q-route-tab
        no-caps
        :label="$t('buildings')"
        to="/buildings"
        exact
        content-class="app-tab"
      />
    </q-tabs>
    <q-space />
    <q-btn
      flat
      round
      icon="account_circle"
      :title="$t('contact_us')"
      @click="onShowContact"
    />
    <q-btn
      flat
      round
      icon="menu_book"
      :title="$t('resources')"
      @click="onShowResources"
    ></q-btn>
    <q-btn
      flat
      round
      icon="add_box"
      :title="$t('how_to_cite')"
      @click="onShowCite"
    ></q-btn>
    <q-btn
      flat
      round
      icon="info"
      :title="$t('introduction')"
      @click="onShowIntro"
    ></q-btn>
    <q-btn
      flat
      round
      icon="handshake"
      :title="$t('acknowledgements')"
      @click="onShowAcknowledgements"
      class="on-left"
    ></q-btn>
    <a href="https://www.epfl.ch/labs/eesd/" target="_blank" class="q-mt-sm">
      <img
        src="/EESD_logo.png"
        style="height: 25px"
        class="float-right q-mb-xs"
      />
    </a>
  </q-toolbar>

  <simple-dialog
    v-model="showIntro"
    :title="$t('app_title')"
    @update:model-value="onIntroUpdate"
  >
    <div>
      <div class="text-grey-8" style="font-size: larger">
        <q-markdown :src="OverViewMd" />
      </div>
      <q-markdown :src="CiteMd" class="epfl-md" />
    </div>
  </simple-dialog>

  <simple-dialog
    v-model="showCite"
    :title="$t('how_to_cite')"
    :content="CiteMd"
  >
  </simple-dialog>

  <q-dialog v-model="showAcknowledgements">
    <q-card :style="$q.screen.lt.md ? '' : 'width: 500px; max-width: 80vw'">
      <q-card-section class="q-ml-md q-mr-md">
        <div class="text-h6 q-mb-md">
          {{ $t('acknowledgements') }}
        </div>
        <div class="text-subtitle1 text-grey-8">
          <q-markdown :src="AcknowledgementsMd" />
        </div>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat :label="$t('close')" color="primary" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>

  <simple-dialog v-model="showResources" :title="$t('resources')">
    <q-list separator>
      <essential-link
        v-for="link in essentialLinks"
        :key="link.title"
        v-bind="link"
      />
    </q-list>
  </simple-dialog>

  <q-dialog v-model="showContact">
    <q-card :style="$q.screen.lt.md ? '' : 'width: 500px; max-width: 80vw'">
      <q-card-section class="q-ml-md q-mr-md">
        <div class="text-h6 q-mb-sm">
          {{ $t('contact_us') }}
        </div>
        <p>{{ $t('contact_us_intro') }}</p>

        <div class="row q-col-gutter-xl justify-center">
          <div>
            <div>
              <q-img
                src="https://people.epfl.ch/private/common/photos/links/198189.jpg?ts=1718704378"
                style="height: 130px; max-width: 130px"
              />
            </div>
            <div class="text-center">
              <q-btn
                color="red"
                no-caps
                label="Katrin Beyer"
                @click="openPeoplePage('katrin.beyer')"
                class="q-mt-sm"
                style="width: 130px"
              />
            </div>
          </div>
          <div>
            <div>
              <q-img
                src="https://people.epfl.ch/private/common/photos/links/332416.jpg?ts=1718704677"
                style="height: 130px; max-width: 130px"
              />
            </div>
            <div class="text-center">
              <q-btn
                color="red"
                no-caps
                label="Mathias Haindl"
                @click="openPeoplePage('mathias.haindl')"
                class="q-mt-sm"
                style="width: 130px"
              />
            </div>
          </div>
        </div>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat :label="$t('close')" color="primary" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script lang="ts">
export default defineComponent({
  name: 'AppToolbar',
});
</script>
<script setup lang="ts">
import OverViewMd from 'src/assets/overview.md';
import CiteMd from 'src/assets/cite.md';
import AcknowledgementsMd from 'src/assets/acknowledgements.md';
import EssentialLink, {
  EssentialLinkProps,
} from 'components/EssentialLink.vue';
import SimpleDialog from 'src/components/SimpleDialog.vue';
import { Settings } from 'src/stores/settings';

const route = useRoute();
const settingsStore = useSettingsStore();

const showIntro = ref(false);
const showCite = ref(false);
const showResources = ref(false);
const showContact = ref(false);
const showAcknowledgements = ref(false);

const isBuildings = computed(
  () =>
    route.path === '/buildings' ||
    route.path.startsWith('/test') ||
    route.path.startsWith('/model')
);

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
    icon: 'engineering',
    link: 'https://www.epfl.ch/labs/eesd/',
  },
  {
    title: 'ENAC IT4R',
    caption: 'go.epfl.ch/it4r',
    icon: 'construction',
    link: 'https://www.epfl.ch/schools/enac/about/data-at-enac/enac-it4research/',
  },
  {
    title: 'Suggestions and bug reports',
    caption: 'EPFL-ENAC/eesd-mast',
    icon: 'tips_and_updates',
    link: 'https://github.com/EPFL-ENAC/eesd-mast/issues',
  },
  {
    title: 'Python API and command line',
    caption: 'EPFL-ENAC/eesd-mast-cli',
    icon: 'code',
    link: 'https://github.com/EPFL-ENAC/eesd-mast-cli',
  },
];

onMounted(() => {
  if (!settingsStore.settings?.intro_shown) {
    showIntro.value = true;
  }
});

function onShowIntro() {
  showIntro.value = true;
}

function onShowCite() {
  showCite.value = true;
}

function onShowResources() {
  showResources.value = true;
}

function onShowContact() {
  showContact.value = true;
}

function onShowAcknowledgements() {
  showAcknowledgements.value = true;
}

function openPeoplePage(username: string) {
  window.open(`https://people.epfl.ch/${username}?lang=en`);
}

function onIntroUpdate() {
  settingsStore.saveSettings({ intro_shown: !showIntro.value } as Settings);
}
</script>
