import type { ErrorCodes } from '../utils/error-codes.js';
import { Logger } from '../utils/logger.js';

export interface AppError {
  code: ErrorCodes;
  message: string;
  statusCode: number;
  cause?: unknown;
  timestamp: Date;
}

export function createAppError(
  code: ErrorCodes,
  message: string,
  statusCode: number = 500,
  cause?: unknown,
): AppError {
  return {
    code,
    message,
    statusCode,
    cause,
    timestamp: new Date(),
  };
}

export function handleError(error: unknown, logger: Logger): AppError {
  if (isAppError(error)) {
    logger.error(`[${error.code}] ${error.message}`, error.cause);
    return error;
  }

  if (error instanceof Error) {
    logger.error(`[UNHANDLED] ${error.message}`, error);
    return createAppError('INTERNAL_ERROR', 'An unexpected error occurred', 500, error);
  }

  logger.error('[UNKNOWN] Non-error thrown', error);
  return createAppError('INTERNAL_ERROR', 'An unexpected error occurred', 500);
}

function isAppError(error: unknown): error is AppError {
  return (
    typeof error === 'object' &&
    error !== null &&
    'code' in error &&
    'message' in error &&
    'statusCode' in error
  );
}
