import { Entity, Column, PrimaryGeneratedColumn, ManyToOne, OneToMany, Unique } from "typeorm";
import { Field, ID, ObjectType } from "type-graphql";
import { Solution } from "./solution";
import { Bind } from "./bind";
import { Lazy } from "./lazy";
import { Problem } from "./problem";

@Entity()
@ObjectType()
export class Source {
  @Field(type => ID)
  @PrimaryGeneratedColumn()
  id: number

  @Field()
  @Column()
  @Unique(['name'])
  name: string

  @Field(type => [Bind])
  @OneToMany(type => Bind, bind => bind.source, { lazy: true })
  binds: Lazy<Bind[]>

  @Field(type => [Problem])
  @OneToMany(type => Problem, problem => problem.source, { lazy: true })
  problems: Lazy<Problem[]>
}