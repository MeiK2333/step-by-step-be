import { CronJob } from 'cron';
import { SDUTSpider } from './spider/sdut';
import { VjudgeSpider } from './spider/vjudge';
import { PojSpider } from './spider/poj';

// 每周更新 VJ 题目数据
export const sdutProblemSpider = new CronJob('0 0 * * 1', async function () {
  const spider = new SDUTSpider();
  await spider.fetchProblems();
}, null, true, 'Asia/Shanghai');

// 每周更新 VJ 题目数据
export const vjudgeProblemSpider = new CronJob('0 0 * * 1', async function () {
  const spider = new VjudgeSpider();
  await spider.fetchProblems();
}, null, true, 'Asia/Shanghai');

// 每周更新 POJ 题目数据
export const pojProblemSpider = new CronJob('0 0 * * 1', async function () {
  const spider = new PojSpider();
  await spider.fetchProblems();
}, null, true, 'Asia/Shanghai');
