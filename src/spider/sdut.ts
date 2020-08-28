import { Problem } from "../entities/problem";
import axios from 'axios';
import { getConnection } from "typeorm";
import { Source } from "../entities/source";
import { Bind } from "../entities/bind";
import { Solution, Result, Language } from "../entities/solution";

function resultEnum(result: number) {
  switch (result) {
    case 1: return Result.Accepted;
    case 4: return Result.WrongAnswer;
    case 7: return Result.CompileError;
    case 2: return Result.TimeLimitExceeded;
    case 8: return Result.PresentationError;
    case 3: return Result.MemoryLimitExceeded;
    case 5: return Result.RuntimeError;
    case 6: return Result.OutputLimitExceeded;
  }
  return Result.SystemError;
}

function languageEnum(language: string) {
  switch (language.trim()) {
    case 'g++':
      return Language.Cpp;
    case 'gcc':
      return Language.C;
    case 'java':
      return Language.Java;
    case 'python2':
    case 'python3':
      return Language.Python;
    case 'c#':
      return Language.CSharp;
  }
  return Language.Unknown;
}

export class SDUTSpider {
  constructor() { }
  async fetchSolutions(user: Bind) {
    console.log(user.username);
    const connection = getConnection();
    const problemRepository = connection.getRepository(Problem);
    const solutionRepository = connection.getRepository(Solution);
    const source = await connection.getRepository(Source).findOne({ name: 'sdutoj' });
    if (!source) {
      return;
    }
    // 获取已经保存的数据条数
    const count = await connection.getRepository(Solution).count({ where: { bind: user, source } });
    // 通过 username 获取 uid
    const { data } = await axios.get(`https://acm.sdut.edu.cn/onlinejudge2/index.php/API_ng/users?username=${user.username}&limit=50&page=1`);
    let userId = -1;
    for (const row of data.data.rows) {
      if (row.username == user.username) {
        userId = row.userId;
        break;
      }
    }
    // 查无此人
    if (userId == -1) {
      return;
    }
    // 获取总数据条数与页数
    const resp = await axios.get('https://acm.sdut.edu.cn/onlinejudge2/index.php/API_ng/solutions?userId=18947&page=1&limit=1&orderDirection=DESC');
    // 如果没有新增数据
    if (resp.data.data.count <= count) {
      return;
    }
    // 获取需要爬取的页数
    const pages = Math.ceil((resp.data.data.count - count) / 100);
    for (let i = pages; i >= 1; i--) {
      const url = `https://acm.sdut.edu.cn/onlinejudge2/index.php/API_ng/solutions?userId=${userId}&page=${i}&limit=100&orderDirection=DESC`;
      console.log(url);
      const { data } = await axios.get(url);
      for (const row of data.data.rows) {
        const problem = await problemRepository.findOne({ source, problemId: String(row.problem.problemId) });
        if (!problem) {
          continue;
        }
        const runId = String(row.solutionId);
        const solution = await solutionRepository.findOne({ source, runId }) || new Solution();
        solution.source = source;
        solution.bind = user;
        solution.problem = problem;
        solution.runId = runId;
        solution.nickname = row.user.nickname;
        solution.result = resultEnum(row.result);
        solution.memoryUsed = row.memory;
        solution.timeUsed = row.time;
        solution.language = languageEnum(row.language);
        solution.codeLength = row.codeLength;
        solution.submittedAt = new Date(row.createdAt * 1000);
        await connection.manager.save(solution);
      }
    }
  }
  async fetchProblems() {
    const connection = getConnection();
    const problemRepository = connection.getRepository(Problem);
    const source = await connection.getRepository(Source).findOne({ name: 'sdutoj' });
    if (!source) {
      return;
    }
    let count = 1;
    let page = 0;
    const pageSize = 100;
    while (page * pageSize < count) {
      page++;
      const url = `https://acm.sdut.edu.cn/onlinejudge2/index.php/API_ng/problems?page=${page}&limit=${pageSize}`;
      console.log(url);
      const { data } = await axios.get(url);
      count = data.data.count;
      for (const row of data.data.rows) {
        let problem = await problemRepository.findOne({ source, problemId: String(row.problemId) });
        if (problem) {
          problem.title = row.title;
          problem.updatedAt = new Date();
        } else {
          problem = problemRepository.create({
            source,
            title: row.title,
            problemId: String(row.problemId),
            link: `https://acm.sdut.edu.cn/onlinejudge3/problems/${row.problemId}`,
            updatedAt: new Date()
          });
        }
        await problemRepository.save(problem);
      }
    }
  }
}
