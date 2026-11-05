import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';

const { values } = parseArgs({
  options: {
    registry: { type: 'string' },
    tag: { type: 'string', default: 'local' },
    platform: { type: 'string' },
    push: { type: 'boolean', default: false },
  },
});
if (!/^[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}$/.test(values.tag)) throw new Error('Invalid image tag');
if (values.registry && !/^[a-z0-9][a-z0-9.:-]*\/[a-z0-9][a-z0-9/_-]*$/.test(values.registry))
  throw new Error('--registry must be a registry host/project path without credentials');
if (values.push && !values.registry)
  throw new Error('--push requires an explicit --registry host/project');
const root = fileURLToPath(new URL('./', import.meta.url));
for (const variant of ['normal']) {
  const tag = `${values.registry ?? 'hpo-examples'}/${variant}:${values.tag}`;
  const result = spawnSync(
    'docker',
    [
      'buildx',
      'build',
      '--file',
      `${root}${variant}/Dockerfile`,
      '--tag',
      tag,
      ...(values.platform ? ['--platform', values.platform] : []),
      values.push ? '--push' : '--load',
      root,
    ],
    { stdio: 'inherit' },
  );
  if (result.error || result.status !== 0)
    throw result.error ?? new Error(`Build failed: ${variant}`);
  process.stdout.write(`${values.push ? 'Pushed' : 'Loaded'} ${tag}\n`);
}
