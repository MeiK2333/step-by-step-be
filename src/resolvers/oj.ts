import { Resolver, Query, Arg } from "type-graphql";
import { Problem } from "../entities/problem";
import { InjectRepository } from "typeorm-typedi-extensions";
import { Repository, MoreThanOrEqual } from "typeorm";
import { Source } from "../entities/source";
import { ProblemInput } from "./types/problem-input";

@Resolver()
export class OjResolver {
  constructor(
    @InjectRepository(Source) private readonly sourceRepository: Repository<Source>,
    @InjectRepository(Problem) private readonly problemRepository: Repository<Problem>
  ) { }

  @Query(returns => [Source])
  async ojs() {
    return await this.sourceRepository.find();
  }

  @Query(returns => [Problem])
  async problems(@Arg('query') query: ProblemInput) {
    const s = await this.sourceRepository.findOne(query.sourceId);
    if (query.limit && query.limit > 1000) {
      query.limit = 1000;
    }
    const problems = await this.problemRepository.find({
      where: {
        source: s,
        id: MoreThanOrEqual(query.start || 0)
      },
      take: query.limit
    });
    return problems;
  }
}
