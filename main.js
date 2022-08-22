const pinoElastic = require("pino-elasticsearch");
const pinoMultiStream = require("pino-multi-stream").multistream;
const pino = require("pino");

require("dotenv").config();

const streamToElastic = pinoElastic({
  index: "test-worker",
  consistency: "one",
  node: "http://localhost:9200",
  auth: {
    username: "elastic",
    password: process.env.ELASTIC_PASSWORD,
  },
  "es-version": 8,
  "flush-bytes": 1000,
});

const pinoOptions = {};

const logger = pino(
  pinoOptions,
  pinoMultiStream([{ stream: process.stdout }, { stream: streamToElastic }])
);

logger.info("I'm starting");
logger.warn("Be careful");

for (let i = 0; i < 1000; i++) {
  logger.info({ messageId: i }, "Processing message");
}
