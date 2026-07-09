import { describe, it, expect } from 'vitest';
import { createLogger } from '../src/utils/logger.js';

describe('Logger', () => {
  it('should create a logger without throwing', () => {
    const logger = createLogger('test');
    expect(logger).toBeDefined();
    expect(typeof logger.info).toBe('function');
  });

  it('should create a child logger', () => {
    const logger = createLogger('parent');
    const child = logger.child({ component: 'test' });
    expect(child).toBeDefined();
  });
});

describe('Error Codes', () => {
  it('should map INTERNAL_ERROR to 500', async () => {
    const { HTTP_STATUS } = await import('../src/utils/error-codes.js');
    expect(HTTP_STATUS.INTERNAL_ERROR).toBe(500);
  });
});
