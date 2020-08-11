import { InputType, Field } from 'type-graphql';

@InputType()
export class BindInput {
  @Field()
  username: string

  @Field()
  source: string
}
