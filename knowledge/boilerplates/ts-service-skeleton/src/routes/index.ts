import { handleError } from '../middleware/error-handler.js';
import type { BaseService } from '../services/base.js';
import type { Logger } from '../utils/logger.js';

export interface RouteContext {
  logger: Logger;
  services: Record<string, BaseService>;
}

export type RouteHandler<TReq, TRes> = (
  ctx: RouteContext,
  req: TReq,
) => Promise<TRes>;

export function wrapHandler<TReq, TRes>(
  handler: RouteHandler<TReq, TRes>,
): RouteHandler<TReq, TRes> {
  return async (ctx: RouteContext, req: TReq): Promise<TRes> => {
    try {
      return await handler(ctx, req);
    } catch (error) {
      const appError = handleError(error, ctx.logger);
      throw appError;
    }
  };
}

export function createRouter(ctx: RouteContext) {
  return {
    health: wrapHandler(async (_ctx, _req: void) => {
      return { status: 'ok', timestamp: new Date().toISOString() };
    }),

    // Example: echo route
    echo: wrapHandler(async (_ctx, req: { message: string }) => {
      return { echoed: req.message, length: req.message.length };
    }),
  };
}
