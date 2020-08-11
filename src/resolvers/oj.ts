import { Resolver, Query, Arg } from "type-graphql";
import { User } from "../entities/users";
import { ojs as os } from "../ojs";
import { Problem } from "../entities/problem";

@Resolver()
export class OjResolver {
  constructor() { }

  @Query(returns => [String])
  async ojs() {
    return os;
  }

  @Query(returns => [Problem])
  async problems(@Arg('sourceId') sourceId: number) {
    console.log(sourceId);
  }
}
