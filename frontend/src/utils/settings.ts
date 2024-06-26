import { useCookies } from 'vue3-cookies';
const { cookies } = useCookies();

export type Settings = {
  intro_shown: boolean;
  experiments_view: string;
};

export function getSettings(): Settings {
  let settings: Settings = {
    intro_shown: false,
    experiments_view: 'grid',
  };
  const settingsSaved = cookies.get('mast_settings');
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
  cookies.set('mast_settings', JSON.stringify(settings), '1y');
}
