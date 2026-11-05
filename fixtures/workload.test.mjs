import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { configuration, rosenbrock } from './workload.mjs';

test('objective optimum and input bounds', () => {
  assert.equal(rosenbrock(1, 1), 0);
  for (const args of [['--hpo-x=NaN'], ['--hpo-duration-seconds=301'], ['--unknown=1']])
    assert.throws(() => configuration(args));
});

test('normal workload emits only bounded objective metrics', () => {
  const child = spawnSync(process.execPath, [fileURLToPath(new URL('workload.mjs', import.meta.url)), '--hpo-x=1', '--hpo-y=1', '--hpo-duration-seconds=0.2'], { encoding: 'utf8', timeout: 5000 });
  assert.equal(child.status, 0);
  assert.match(child.stdout, /hpo.metrics.loss=0/);
  assert.ok(Buffer.byteLength(child.stdout) < 1000);
  assert.equal(child.stderr, '');
});
