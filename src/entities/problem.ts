import { Source } from "./source"
import { Entity, PrimaryGeneratedColumn, Column, ManyToOne, OneToMany } from "typeorm"
import { ObjectType, Field, ID } from "type-graphql"
import { Lazy } from "./lazy"
import { Solution } from "./solution"

@Entity()
@ObjectType()
export class Problem {
  @Field(type => ID)
  @PrimaryGeneratedColumn()
  id: number

  @Field(type => String)
  @Column()
  problemId: string

  @Field(type => String)
  @Column()
  title: string

  @Field(type => Source)
  @ManyToOne(type => Source, source => source.problems, { lazy: true })
  source: Lazy<Source>

  @Field(type => String)
  @Column()
  link: String

  @Field(type => [Solution])
  @OneToMany(type => Solution, solution => solution.problem, { lazy: true })
  solutions: Solution[]

  @Field(type => Date)
  @Column()
  updatedAt: Date
}
