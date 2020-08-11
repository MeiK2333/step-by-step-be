import { User } from "./users";
import { Source } from "./source";
import { ManyToOne, PrimaryGeneratedColumn, OneToMany, Column, Entity } from "typeorm";
import { Field, ID, ObjectType } from "type-graphql";
import { Solution } from "./solution";
import { Lazy } from "./lazy";

@Entity()
@ObjectType()
export class Bind {
  @Field(type => ID)
  @PrimaryGeneratedColumn()
  id: number

  @Field(type => User)
  @ManyToOne(type => User, user => user.bind, { lazy: true })
  user: Lazy<User>

  @Field(type => Source)
  @ManyToOne(type => Source, source => source.bind, { lazy: true })
  source: Lazy<Source>

  @Field(type => [Solution])
  @OneToMany(type => Solution, solution => solution.bind, { lazy: true, cascade: ['insert'] })
  solution: Lazy<Solution[]>

  @Field(type => String)
  @Column()
  username: string
}
