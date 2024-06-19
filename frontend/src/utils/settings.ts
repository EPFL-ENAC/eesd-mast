import { LocalStorage } from 'quasar';

const APP_COOKIE_NAME = 'mast_settings';

export type Settings = {
  intro_shown: boolean;
  experiments_view: string;
  vulnerabilities_tips: boolean;
  run_results_tips: boolean;
};

export function getSettings(): Settings {
  let settings: Settings = {
    intro_shown: false,
    experiments_view: 'grid',
    vulnerabilities_tips: false,
    run_results_tips: false,
  };
  const settingsSaved = LocalStorage.getItem(APP_COOKIE_NAME);
  // cookies.get() declares to return a string but apparently it automatically parses the JSON string to an object
  if (settingsSaved !== null) {
    if (typeof settingsSaved === 'string') {
      settings = JSON.parse(settingsSaved);
    } else if (typeof settingsSaved === 'object') {
      settings = settingsSaved as Settings;
    }
  }
  return settings;
}

export function saveSettings(settings: Settings) {
  LocalStorage.set(APP_COOKIE_NAME, JSON.stringify(settings));
}
