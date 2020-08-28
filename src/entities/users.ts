import { Bind } from './bind';
import { OneToMany, PrimaryGeneratedColumn, Entity, Column, Index } from 'typeorm';
import { Field, ID, ObjectType } from 'type-graphql';
import { Lazy } from './lazy';

@Entity()
@ObjectType()
export class User {
  @Field(type => ID)
  @PrimaryGeneratedColumn()
  id: number

  @Field()
  @Index({ unique: true })
  @Column()
  username: string

  @Field()
  @Column()
  nickname: string

  @Field(type => [Bind])
  @OneToMany(type => Bind, bind => bind.user, { lazy: true })
  binds: Lazy<Bind[]>
}