type LogLevel = 'debug' | 'info' | 'warn' | 'error';

export interface Logger {
  debug(msg: string, ...args: unknown[]): void;
  info(msg: string, ...args: unknown[]): void;
  warn(msg: string, ...args: unknown[]): void;
  error(msg: string, ...args: unknown[]): void;
  child(meta: Record<string, unknown>): Logger;
}

export function createLogger(name: string, level: LogLevel = 'info'): Logger {
  const levels: Record<LogLevel, number> = { debug: 0, info: 1, warn: 2, error: 3 };
  const currentLevel = levels[level];

  function shouldLog(lvl: LogLevel): boolean {
    return levels[lvl] >= currentLevel;
  }

  function formatMessage(lvl: LogLevel, msg: string, args: unknown[]): string {
    const timestamp = new Date().toISOString();
    const extra = args.length > 0 ? ` ${JSON.stringify(args)}` : '';
    return `[${timestamp}] [${lvl.toUpperCase()}] [${name}] ${msg}${extra}`;
  }

  const logger: Logger = {
    debug(msg, ...args) {
      if (shouldLog('debug')) console.debug(formatMessage('debug', msg, args));
    },
    info(msg, ...args) {
      if (shouldLog('info')) console.info(formatMessage('info', msg, args));
    },
    warn(msg, ...args) {
      if (shouldLog('warn')) console.warn(formatMessage('warn', msg, args));
    },
    error(msg, ...args) {
      if (shouldLog('error')) console.error(formatMessage('error', msg, args));
    },
    child(meta) {
      return createLogger(`${name}:${JSON.stringify(meta)}`, level);
    },
  };

  return logger;
}
