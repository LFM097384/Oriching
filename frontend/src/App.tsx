import ModernDivinationWorkbench from './components/ModernDivinationWorkbench';
import { I18nProvider } from './i18n/useI18n';

function App() {
  return (
    <I18nProvider>
      <ModernDivinationWorkbench />
    </I18nProvider>
  );
}

export default App;
