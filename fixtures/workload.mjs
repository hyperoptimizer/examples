import { once } from 'node:events';
import { setTimeout as sleep } from 'node:timers/promises';
import { pathToFileURL } from 'node:url';

export function configuration(args, mode = process.env.ABUSE_FIXTURE_MODE ?? 'normal') {
  if (!['normal', 'flood'].includes(mode)) throw new Error('Unknown fixture mode');
  const options = {
    x: 0,
    y: 0,
    'duration-seconds': 120,
    'bytes-per-second': 131072,
    'max-bytes': 33554432,
  };
  for (const argument of args) {
    const match = /^--hpo-([a-z-]+)=(.+)$/.exec(argument);
    if (!match || !Object.hasOwn(options, match[1]))
      throw new Error(`Unknown argument: ${argument}`);
    options[match[1]] = Number(match[2]);
  }
  for (const [name, value] of Object.entries(options))
    if (!Number.isFinite(value)) throw new Error(`Invalid ${name}`);
  if (Math.abs(options.x) > 10 || Math.abs(options.y) > 10)
    throw new Error('x and y must be within [-10, 10]');
  if (options['duration-seconds'] < 0.1 || options['duration-seconds'] > 300)
    throw new Error('Duration must be 0.1–300 seconds');
  if (options['bytes-per-second'] < 1024 || options['bytes-per-second'] > 262144)
    throw new Error('Rate must be 1–256 KiB/s');
  if (options['max-bytes'] < 1024 || options['max-bytes'] > 33554432)
    throw new Error('Flood budget must be 1 KiB–32 MiB');
  return { ...options, mode };
}

export function rosenbrock(x, y) {
  return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2;
}

export async function run(config) {
  const started = performance.now();
  const deadline = started + config['duration-seconds'] * 1000;
  const loss = rosenbrock(config.x, config.y);
  const metric = () => process.stdout.write(`hpo.metrics.loss=${loss}\n`);
  metric();
  let bytes = 0;
  let nextMetric = started + 1000;
  const line = `ABUSE_TEST_ONLY ${'x'.repeat(1007)}\n`; // Exactly 1024 ASCII bytes.
  while (performance.now() < deadline) {
    if (config.mode === 'flood') {
      const target = Math.min(
        config['max-bytes'],
        Math.floor(((performance.now() - started) / 1000) * config['bytes-per-second']),
      );
      while (bytes + line.length <= target) {
        bytes += line.length;
        if (!process.stdout.write(line)) await once(process.stdout, 'drain');
      }
      if (bytes + line.length > config['max-bytes']) break;
    }
    if (performance.now() >= nextMetric) {
      metric();
      nextMetric = performance.now() + 1000;
    }
    await sleep(Math.min(50, Math.max(0, deadline - performance.now())));
  }
  metric();
  process.stderr.write(`fixture_complete mode=${config.mode} flood_bytes=${bytes}\n`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  run(configuration(process.argv.slice(2))).catch((error) => {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  });
}
