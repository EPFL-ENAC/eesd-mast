import { defineStore } from 'pinia';
import { LocalStorage } from 'quasar';

const APP_COOKIE_NAME = 'mast_settings';

export type Settings = {
  intro_shown: boolean | undefined;
  experiments_view: string | undefined;
  frequencies_tips: boolean | undefined;
  vulnerabilities_tips: boolean | undefined;
  filter_tips: boolean | undefined;
  run_results_tips: boolean | undefined;
  vtk_tips: boolean | undefined;
};

export const useSettingsStore = defineStore('settings', () => {
  const settings = ref<Settings>();

  function initSettings(): Settings {
    if (settings.value != undefined) return settings.value;
    let settingsData: Settings = {
      intro_shown: false,
      experiments_view: 'grid',
      frequencies_tips: false,
      vulnerabilities_tips: false,
      filter_tips: false,
      run_results_tips: false,
      vtk_tips: false,
    };
    const settingsSaved = LocalStorage.getItem(APP_COOKIE_NAME);
    // cookies.get() declares to return a string but apparently it automatically parses the JSON string to an object
    if (settingsSaved !== null) {
      if (typeof settingsSaved === 'string') {
        settingsData = JSON.parse(settingsSaved);
      } else if (typeof settingsSaved === 'object') {
        settingsData = settingsSaved as Settings;
      }
    }
    settings.value = settingsData;
    return settings.value;
  }

  function saveSettings(settingsData: Settings) {
    settings.value = { ...settings.value, ...settingsData };
    LocalStorage.set(APP_COOKIE_NAME, JSON.stringify(settings.value));
  }

  return {
    settings,
    initSettings,
    saveSettings,
  };
});
