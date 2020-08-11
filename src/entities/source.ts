import { Entity, Column, PrimaryGeneratedColumn, ManyToOne, OneToMany } from "typeorm";
import { Field, ID, ObjectType } from "type-graphql";
import { Solution } from "./solution";
import { Bind } from "./bind";

@Entity()
@ObjectType()
export class Source {
  @Field(type => ID)
  @PrimaryGeneratedColumn()
  id: number

  @Field()
  @Column()
  name: string

  @Field(type => [Solution])
  @OneToMany(type => Solution, solution => solution.source)
  solutions: Solution[]

  @Field(type => [Bind])
  @OneToMany(type => Bind, bind => bind.source)
  bind: Bind[]
}