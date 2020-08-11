import { Entity, Column, PrimaryGeneratedColumn, ManyToOne } from "typeorm";
import { Field, ID, ObjectType } from "type-graphql";
import { Source } from "./source";
import { Bind } from "./bind";
import { Lazy } from "./lazy";

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
  @ManyToOne(type => Bind, bind => bind.solution, { lazy: true })
  bind: Lazy<Bind>
}
