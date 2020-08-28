import { Problem } from "../entities/problem";
import axios from 'axios';
import { getConnection, createConnection } from "typeorm";
import { Source } from "../entities/source";
import { parse } from 'node-html-parser';
import { Bind } from "../entities/bind";
import { Solution, Result, Language } from "../entities/solution";

function resultEnum(result: string) {
  switch (result.trim()) {
    case 'Accepted': return Result.Accepted;
    case 'Wrong Answer': return Result.WrongAnswer;
    case 'Compile Error': return Result.CompileError;
    case 'Time Limit Exceeded': return Result.TimeLimitExceeded;
    case 'Presentation Error': return Result.PresentationError;
    case 'Memory Limit Exceeded': return Result.MemoryLimitExceeded;
    case 'Runtime Error': return Result.RuntimeError;
    case 'Output Limit Exceeded': return Result.OutputLimitExceeded;
  }
  return Result.SystemError;
}

function languageEnum(language: string) {
  switch (language.trim()) {
    case 'G++':
    case 'C++':
      return Language.Cpp;
    case 'GCC':
    case 'C':
      return Language.C;
    case 'Java':
      return Language.Java;
    case 'Pascal':
      return Language.Pascal;
    case 'Fortran':
      return Language.Fortran;
  }
  return Language.Unknown;
}

export class PojSpider {
  constructor() { }
  async fetchSolutions(user: Bind) {
    console.log(user.username);
    const connection = getConnection();
    const problemRepository = connection.getRepository(Problem);
    const solutionRepository = connection.getRepository(Solution);
    const source = await connection.getRepository(Source).findOne({ name: 'poj' });
    if (!source) {
      return;
    }
    const last = await connection.getRepository(Solution).findOne({ where: { bind: user, source }, order: { submittedAt: 'DESC' } });
    // 从上次的位置开始爬取
    let bottom = last ? Number(last.runId) : 0;
    while (1) {
      const url = `http://poj.org/status?user_id=${user.username}&bottom=${bottom}`;
      console.log(url);
      const { data } = await axios.get(url);
      const root = parse(data, { lowerCaseTagName: true });
      const trs = root.querySelectorAll('table')[3].querySelectorAll('tr');
      for (let i = 1; i < trs.length; i++) {
        const tr = trs[i];
        const tds = tr.querySelectorAll('td');
        const runId = tds[0].rawText;
        const nickname = tds[1].rawText;
        const pid = tds[2].rawText;
        const result = resultEnum(tds[3].rawText);
        const memory = Number(tds[4].rawText.replace('K', '') || 0);
        const time = Number(tds[5].rawText.replace('MS', '') || 0);
        const language = languageEnum(tds[6].rawText);
        const len = Number(tds[7].rawText.replace('B', '') || 0);
        const subTime = new Date(tds[8].rawText);

        const problem = await problemRepository.findOne({ source, problemId: pid });
        if (!problem) {
          continue;
        }
        const solution = await solutionRepository.findOne({ bind: user, runId }) || new Solution();
        solution.bind = user;
        solution.problem = problem;
        solution.runId = runId;
        solution.nickname = nickname;
        solution.result = result;
        solution.memoryUsed = memory;
        solution.timeUsed = time;
        solution.language = language;
        solution.codeLength = len;
        solution.submittedAt = subTime;
        await connection.manager.save(solution);
        bottom = bottom > Number(runId) ? bottom : Number(runId);
      }
      // 当条数不足时，说明爬完了
      if (trs.length <= 20) {
        break;
      }
    }
  }
  async fetchProblems() {
    const connection = getConnection();
    const problemRepository = connection.getRepository(Problem);
    const source = await connection.getRepository(Source).findOne({ name: 'poj' });
    if (!source) {
      return;
    }
    const { data } = await axios.get('http://poj.org/problemlist');
    const root = parse(data);
    const as = root.querySelector('center').querySelectorAll('a');
    const urls = [];
    for (const a of as) {
      urls.push('http://poj.org/' + a.getAttribute('href'));
    }
    for (const url of urls) {
      console.log(url);
      const { data } = await axios.get(url);
      const root = parse(data, { lowerCaseTagName: true });
      const trs = root.querySelectorAll('table')[3].querySelectorAll('tr');
      for (let i = 1; i < trs.length; i++) {
        const tr = trs[i];
        const tds = tr.querySelectorAll('td');
        const pid = tds[0].rawText;
        const title = tds[1].rawText;

        let problem = await problemRepository.findOne({ source, problemId: pid });
        if (problem) {
          problem.title = title;
          problem.updatedAt = new Date();
        } else {
          problem = new Problem();
          problem.source = source;
          problem.title = title;
          problem.problemId = pid;
          problem.link = `http://poj.org/problem?id=${pid}`;
          problem.updatedAt = new Date();
        }
        await connection.manager.save(problem);
      }
    }
  }
}
