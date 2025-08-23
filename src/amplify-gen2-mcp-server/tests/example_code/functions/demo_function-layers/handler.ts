import { Logger } from "@aws-lambda-powertools/logger";
import type { Handler } from "aws-lambda";

const logger = new Logger({ serviceName: "serverlessAirline" });

export const handler: Handler = async (event, context) => {
  logger.info("Hello World");
};