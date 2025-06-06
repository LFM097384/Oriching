import DivinationWorkbench from './components/DivinationWorkbench';
import { I18nProvider } from './i18n/useI18n';
import { ToastProvider } from './components/ui/toast';

function App() {
  return (
    <I18nProvider>
      <ToastProvider>
        <DivinationWorkbench />
      </ToastProvider>
    </I18nProvider>
  );
}

export default App;
