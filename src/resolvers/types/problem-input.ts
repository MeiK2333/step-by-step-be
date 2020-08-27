import { InputType, Field } from 'type-graphql';
import { User } from '../../entities/users';
@InputType()
export class ProblemInput {
  @Field()
  sourceId: number

  @Field({ defaultValue: 0 })
  start?: number

  @Field({ defaultValue: 100 })
  limit?: number
}
