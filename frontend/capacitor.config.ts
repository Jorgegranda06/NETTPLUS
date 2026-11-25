import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'ec.edu.utpl.nettplus',
  appName: 'NETTPLUS',
  webDir: 'dist/nettplus-dashboard/browser',
  server: {
    androidScheme: 'http',
    cleartext: true
  }
};

export default config;
