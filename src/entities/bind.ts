import { User } from "./users";
import { Source } from "./source";
import { ManyToOne, PrimaryGeneratedColumn, OneToMany, Column, Entity } from "typeorm";
import { Field, ID, ObjectType } from "type-graphql";
import { Solution } from "./solution";

@Entity()
@ObjectType()
export class Bind {
  @Field(type => ID)
  @PrimaryGeneratedColumn()
  id: number

  @Field(type => User)
  @ManyToOne(type => User, user => user.bind)
  user: User

  @Field(type => Source)
  @ManyToOne(type => Source, source => source.bind)
  source: Source

  @Field(type => [Solution])
  @OneToMany(type => Solution, solution => solution.bind)
  solution: Solution[]
}
