type Level = 'debug' | 'info' | 'warn' | 'error';

const prefix = '[TYNE CITY]';

function log(level: Level, message: string, ...detail: unknown[]): void {
  // eslint-disable-next-line no-console
  console[level](`${prefix} ${message}`, ...detail);
}

export const Logger = {
  debug: (m: string, ...d: unknown[]) => { if (import.meta.env.DEV) log('debug', m, ...d); },
  info: (m: string, ...d: unknown[]) => log('info', m, ...d),
  warn: (m: string, ...d: unknown[]) => log('warn', m, ...d),
  error: (m: string, ...d: unknown[]) => log('error', m, ...d),
};

/** Logs uncaught errors and rejections, and forwards them to an optional UI handler. */
export function installGlobalErrorHandlers(onFatal: (message: string) => void): () => void {
  const onError = (e: ErrorEvent) => {
    Logger.error('Uncaught error', e.error ?? e.message);
    onFatal(String(e.message));
  };
  const onRejection = (e: PromiseRejectionEvent) => {
    Logger.error('Unhandled promise rejection', e.reason);
    onFatal(e.reason instanceof Error ? e.reason.message : String(e.reason));
  };
  window.addEventListener('error', onError);
  window.addEventListener('unhandledrejection', onRejection);
  return () => {
    window.removeEventListener('error', onError);
    window.removeEventListener('unhandledrejection', onRejection);
  };
}
