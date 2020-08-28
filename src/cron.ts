import { CronJob } from 'cron';
import { SDUTSpider } from './spider/sdut';
import { VjudgeSpider } from './spider/vjudge';
import { PojSpider } from './spider/poj';
import { getConnection, createConnection } from 'typeorm';
import { Bind } from './entities/bind';
import { Source } from './entities/source';
import { T, R } from 'task-runner';


// 每周更新 SDUT 题目数据
export const sdutProblemSpider = new CronJob('0 0 * * 1', async function () {
  const spider = new SDUTSpider();
  await spider.fetchProblems();
}, null, true, 'Asia/Shanghai');

// 每周更新 VJ 题目数据
export const vjudgeProblemSpider = new CronJob('0 2 * * 1', async function () {
  const spider = new VjudgeSpider();
  await spider.fetchProblems();
}, null, true, 'Asia/Shanghai');

// 每周更新 POJ 题目数据
export const pojProblemSpider = new CronJob('0 4 * * 1', async function () {
  const spider = new PojSpider();
  await spider.fetchProblems();
}, null, true, 'Asia/Shanghai');

// 每小时更新 POJ 提交数据
export const pojSolutionSpider = new CronJob('0 * * * *', async function () {
  const spider = new PojSpider();
  const connection = getConnection();
  const source = await connection.getRepository(Source).findOne({ name: 'poj' });
  const binds = await connection.getRepository(Bind).find({ source: source });
  const tasks = [];
  for (const bind of binds) {
    tasks.push(T(async () => {
      await spider.fetchSolutions(bind);
    }, { retry: 3 }));
  }
  await R(tasks, { maxRunning: 3 });
}, null, true, 'Asia/Shanghai');


// 每小时更新 VJ 提交数据
export const vjudgeSolutionSpider = new CronJob('10 * * * *', async function () {
  const spider = new VjudgeSpider();
  const connection = getConnection();
  const source = await connection.getRepository(Source).findOne({ name: 'vjudge' });
  const binds = await connection.getRepository(Bind).find({ source: source });
  const tasks = [];
  for (const bind of binds) {
    tasks.push(T(async () => {
      await spider.fetchSolutions(bind);
    }, { retry: 3 }));
  }
  await R(tasks, { maxRunning: 3 });
}, null, true, 'Asia/Shanghai');


// 每小时更新 SDUT 提交数据
export const sdutSolutionSpider = new CronJob('20 * * * *', async function () {
  const spider = new SDUTSpider();
  const connection = getConnection();
  const source = await connection.getRepository(Source).findOne({ name: 'sdutoj' });
  const binds = await connection.getRepository(Bind).find({ source: source });
  const tasks = [];
  for (const bind of binds) {
    tasks.push(T(async () => {
      await spider.fetchSolutions(bind);
    }, { retry: 3 }));
  }
  await R(tasks, { maxRunning: 3 });
}, null, true, 'Asia/Shanghai');
