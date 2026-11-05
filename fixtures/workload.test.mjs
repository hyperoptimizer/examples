import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { configuration, rosenbrock } from './workload.mjs';

test('Rosenbrock has its known optimum and validates finite bounded inputs', () => {
  assert.equal(rosenbrock(1, 1), 0);
  assert.equal(rosenbrock(0, 0), 1);
  for (const argument of [
    '--hpo-x=NaN',
    '--hpo-duration-seconds=301',
    '--hpo-max-bytes=999999999',
    '--hpo-bytes-per-second=999999999',
  ])
    assert.throws(() => configuration([argument]));
});
test('normal and flood fixtures emit valid metrics; flood stays within its byte budget', () => {
  for (const mode of ['normal', 'flood']) {
    const child = spawnSync(
      process.execPath,
      [
        fileURLToPath(new URL('workload.mjs', import.meta.url)),
        '--hpo-x=1',
        '--hpo-y=1',
        '--hpo-duration-seconds=0.2',
        '--hpo-max-bytes=8192',
      ],
      { env: { ...process.env, ABUSE_FIXTURE_MODE: mode }, encoding: 'utf8', timeout: 5000 },
    );
    assert.equal(child.status, 0, child.stderr);
    assert.match(child.stdout, /hpo.metrics.loss=0/);
    assert.ok(Buffer.byteLength(child.stdout) < 9000);
    assert.equal(child.stdout.includes('ABUSE_TEST_ONLY'), mode === 'flood');
    assert.match(child.stderr, /fixture_complete/);
  }
});
