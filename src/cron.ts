import { CronJob } from 'cron';
import { SDUTSpider } from './spider/sdut';

export const sdutProblemSpider = new CronJob('0 0 * * *', async function () {
  const spider = new SDUTSpider();
  await spider.fetchProblems();
}, null, true, 'Asia/Shanghai');
