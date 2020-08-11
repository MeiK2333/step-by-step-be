import { Bind } from './bind';
import { OneToMany, PrimaryGeneratedColumn, Entity, Column, Index } from 'typeorm';
import { Field, ID, ObjectType } from 'type-graphql';

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

  @Column()
  password: string

  @Field(type => [Bind])
  @OneToMany(type => Bind, bind => bind.user)
  bind: Bind[]
}