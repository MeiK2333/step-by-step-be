import { createConnection } from "typeorm";
import { ojs } from "./ojs";
import { Source } from "./entities/source";
import { User } from "./entities/users";
import { Bind } from "./entities/bind";
import { Problem } from "./entities/problem";
import { VjudgeSpider } from "./spider/vjudge";
import { SDUTSpider } from "./spider/sdut";
import { PojSpider } from "./spider/poj";

export async function init() {
  const connection = await createConnection();
  for (const oj of ojs) {
    const o = await connection.getRepository(Source).findOne({ name: oj });
    if (!o) {
      const o = new Source();
      o.name = oj;
      await connection.manager.save(o);
    }
  }
  const user = await connection.getRepository(User).findOne({ username: 'MeiK2333' });
  if (!user) {
    const user = new User();
    user.username = 'MeiK2333';
    user.nickname = 'MeiK';
    await connection.manager.save(user);
    {
      const source = await connection.getRepository(Source).findOne({ name: 'sdutoj' });
      const bind = new Bind();
      bind.username = 'MeiK';
      bind.user = user;
      if (source) {
        bind.source = source;
      }
      await connection.manager.save(bind);
    }
    {
      const source = await connection.getRepository(Source).findOne({ name: 'poj' });
      const bind = new Bind();
      bind.username = 'MeiK';
      bind.user = user;
      if (source) {
        bind.source = source;
      }
      await connection.manager.save(bind);
    }
    {
      const source = await connection.getRepository(Source).findOne({ name: 'vjudge' });
      const bind = new Bind();
      bind.username = 'MeiK';
      bind.user = user;
      if (source) {
        bind.source = source;
      }
      await connection.manager.save(bind);
    }
  }
  {
    const source = await connection.getRepository(Source).findOne({ name: 'sdutoj' });
    const count = await connection.getRepository(Problem).count({ source });
    if (count == 0) {
      console.log('初始化 sdutoj 题目');
      const spider = new SDUTSpider();
      await spider.fetchProblems();
      console.log('sdutoj 题目初始化完成');
    }
  }
  {
    const source = await connection.getRepository(Source).findOne({ name: 'poj' });
    const count = await connection.getRepository(Problem).count({ source });
    if (count == 0) {
      console.log('初始化 poj 题目');
      const spider = new PojSpider();
      await spider.fetchProblems();
      console.log('poj 题目初始化完成');
    }
  }
  {
    const source = await connection.getRepository(Source).findOne({ name: 'vjudge' });
    const count = await connection.getRepository(Problem).count({ source });
    if (count == 0) {
      console.log('初始化 vjudge 题目');
      const spider = new VjudgeSpider();
      await spider.fetchProblems();
      console.log('vjudge 题目初始化完成');
    }
  }
}
