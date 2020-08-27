import { Problem } from "../entities/problem";
import axios from 'axios';
import { getConnection } from "typeorm";
import { Source } from "../entities/source";

export class SDUTSpider {
  constructor() { }
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
