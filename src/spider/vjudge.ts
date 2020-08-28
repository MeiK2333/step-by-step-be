import { Problem } from "../entities/problem";
import axios from 'axios';
import { getConnection, createConnection } from "typeorm";
import { Source } from "../entities/source";
import { Result, Solution, Language } from "../entities/solution";
import { Bind } from "../entities/bind";

export class VjudgeSpider {
  constructor() { }
  async fetchSolutions(user: Bind) {
    console.log(user.username);
    const connection = getConnection();
    const problemRepository = connection.getRepository(Problem);
    const solutionRepository = connection.getRepository(Solution);
    const source = await connection.getRepository(Source).findOne({ name: 'vjudge' });
    if (!source) {
      return;
    }
    const url = `https://vjudge.net/user/solveDetail/${user.username}`;
    const { data } = await axios.get(url);
    // 通过接口获取的 VJ 数据没有提交时间，方便起见全部设置为统一的时间
    for (const key of Object.keys(data.acRecords)) {
      for (const value of data.acRecords[key]) {
        const pid = `${key}-${value}`;
        const problem = await problemRepository.findOne({ source, problemId: pid });
        if (!problem) {
          continue;
        }
        // VJ 数据每个题目仅保留一份数据
        const solution = await solutionRepository.findOne({ source, problem: problem }) || new Solution();
        solution.problem = problem;
        // 仅保存 AC 的数据，因为没有 AC 的数据也无法获取具体信息
        solution.result = Result.Accepted;
        solution.bind = user;
        solution.submittedAt = new Date('1970-01-01 00:00:00');
        solution.timeUsed = 0;
        solution.memoryUsed = 0;
        solution.runId = '';
        solution.codeLength = 0;
        solution.language = Language.Unknown;
        solution.nickname = user.username;
        solution.source = source;
        await connection.manager.save(solution);
      }
    }
  }
  async fetchProblems() {
    const connection = getConnection();
    const problemRepository = connection.getRepository(Problem);
    const source = await connection.getRepository(Source).findOne({ name: 'vjudge' });
    if (!source) {
      return;
    }
    let start = 0;
    while (start < 333333) {
      const url = `https://vjudge.net/problem/data?draw=1&start=${start}&length=100&sortDir=asc&sortCol=3&OJId=All&probNum=&title=&source=&category=all`;
      console.log(url);
      const { data: { data } } = await axios.get(url);
      if (data.length < 100) {
        // 数量不够说明已经爬完了
        break;
      }
      for (const p of data) {
        const pid = `${p.originOJ}-${p.originProb}`;
        let problem = await problemRepository.findOne({ source, problemId: pid });
        if (problem) {
          problem.title = p.title;
          problem.updatedAt = new Date();
        } else {
          problem = problemRepository.create({
            source,
            title: p.title,
            problemId: pid,
            link: `https://vjudge.net/problem/${pid}`,
            updatedAt: new Date()
          });
        }
        await problemRepository.save(problem);
      }
      start += 100;
    }
  }
}
