import { Resolver, Query } from "type-graphql";
import { User } from "../entities/users";
import { ojs as os } from "../ojs";

@Resolver()
export class OjResolver {
  constructor() { }

  @Query(returns => [String])
  async ojs() {
    return os;
  }
}
