import type { Logger } from '../utils/logger.js';

export interface ServiceConfig {
  name: string;
  enabled: boolean;
}

export abstract class BaseService {
  protected readonly logger: Logger;
  protected readonly config: ServiceConfig;
  private _initialized = false;

  constructor(logger: Logger, config: ServiceConfig) {
    this.logger = logger;
    this.config = config;
  }

  get name(): string {
    return this.config.name;
  }

  get isInitialized(): boolean {
    return this._initialized;
  }

  async initialize(): Promise<void> {
    if (this._initialized) {
      this.logger.warn(`Service ${this.config.name} already initialized`);
      return;
    }
    if (!this.config.enabled) {
      this.logger.info(`Service ${this.config.name} is disabled, skipping`);
      return;
    }
    await this.onInitialize();
    this._initialized = true;
    this.logger.info(`Service ${this.config.name} initialized`);
  }

  async shutdown(): Promise<void> {
    if (!this._initialized) return;
    await this.onShutdown();
    this._initialized = false;
    this.logger.info(`Service ${this.config.name} shut down`);
  }

  protected abstract onInitialize(): Promise<void>;
  protected abstract onShutdown(): Promise<void>;
}
