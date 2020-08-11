import { Entity, Column, PrimaryGeneratedColumn, ManyToOne } from "typeorm";
import { Field, ID, ObjectType, registerEnumType } from "type-graphql";
import { Source } from "./source";
import { Bind } from "./bind";
import { Lazy } from "./lazy";
import { Problem } from "./problem";

export enum Result {
  Accepted = 0,
  WrongAnswer = 1,
  TimeLimitExceeded = 2,
  MemoryLimitExceeded = 3,
  RuntimeError = 4,
  OutputLimitExceeded = 5,
  CompileError = 6,
  PresentationError = 7,
  SystemError = 8,
}

registerEnumType(Result, {
  name: 'Result',
  description: 'result'
});

@Entity()
@ObjectType()
export class Solution {
  @Field(type => ID)
  @PrimaryGeneratedColumn()
  id: number;

  @Field(type => Source)
  @ManyToOne(type => Source, source => source.solutions, { lazy: true })
  source: Lazy<Source>

  @Field(type => Bind)
  @ManyToOne(type => Bind, bind => bind.solutions, { lazy: true })
  bind: Lazy<Bind>

  @Field(type => Result)
  @Column()
  result: Result

  @Field(type => Problem)
  @ManyToOne(type => Problem, problem => problem.solutions, { lazy: true })
  problem: Lazy<Problem>

  @Field(type => String)
  @Column()
  runId: string

  @Field(type => String)
  @Column()
  nickname: string

  @Field(type => Number)
  @Column()
  timeUsed: number

  @Field(type => Number)
  @Column()
  memoryUsed: number

  @Field(type => Number)
  @Column()
  codeLength: number

  @Field(type => String)
  @Column()
  language: string

  @Field(type => Date)
  @Column()
  submittedAt: Date
}
