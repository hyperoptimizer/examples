import { setTimeout as sleep } from 'node:timers/promises';
import { pathToFileURL } from 'node:url';

export function configuration(args) {
  const options = { x: 0, y: 0, 'duration-seconds': 120 };
  for (const argument of args) {
    const match = /^--hpo-([a-z-]+)=(.+)$/.exec(argument);
    if (!match || !Object.hasOwn(options, match[1])) throw new Error('Unknown argument');
    options[match[1]] = Number(match[2]);
  }
  for (const value of Object.values(options))
    if (!Number.isFinite(value)) throw new Error('Inputs must be finite');
  if (Math.abs(options.x) > 10 || Math.abs(options.y) > 10) throw new Error('Inputs outside range');
  if (options['duration-seconds'] < 0.1 || options['duration-seconds'] > 300)
    throw new Error('Duration outside range');
  return options;
}

export function rosenbrock(x, y) {
  return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2;
}

export async function run(config) {
  const deadline = performance.now() + config['duration-seconds'] * 1000;
  const metric = () => process.stdout.write(`hpo.metrics.loss=${rosenbrock(config.x, config.y)}\n`);
  metric();
  while (performance.now() < deadline) {
    await sleep(Math.min(1000, Math.max(0, deadline - performance.now())));
    metric();
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  run(configuration(process.argv.slice(2))).catch(() => {
    process.stderr.write('Invalid workload configuration.\n');
    process.exitCode = 1;
  });
}
