import { User } from '../entities/users';
import { InjectRepository } from 'typeorm-typedi-extensions';
import { Resolver, Mutation, Query, Arg, Ctx } from 'type-graphql';
import { Repository } from 'typeorm';
import { UserInput } from './types/user-input';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { AuthenticationError, ValidationError } from 'apollo-server';
import { Context } from '..';

@Resolver(of => User)
export class UserResolver {
  constructor(
    @InjectRepository(User) private readonly userRepository: Repository<User>
  ) { }

  @Mutation(returns => User)
  async register(@Arg('user') u: UserInput) {
    if (await this.userRepository.findOne({ username: u.username })) {
      throw new ValidationError(`user '${u.username}' was exists`);
    }
    const user = this.userRepository.create({
      username: u.username,
      password: await bcrypt.hash(u.password, 10),
      bind: [],
    });
    await this.userRepository.save(user);
    return user;
  }

  @Mutation(returns => String)
  async login(@Arg('user') u: UserInput) {
    const user = await this.userRepository.findOne({ username: u.username });
    if (!user) {
      throw new AuthenticationError(`user '${u.username}' is not found`);
    }
    const valid = await bcrypt.compare(u.password, user.password);
    if (!valid) {
      throw new AuthenticationError('username or password error');
    }
    return jwt.sign(
      { id: user.id },
      process.env.JWT_SECRET || ''
    )
  }

  @Query(returns => User)
  async me(@Ctx() { user }: Context) {
    if (!user) {
      throw new AuthenticationError('not logged in');
    }
    const u = await this.userRepository.findOne(user.id);
    if (u && !u.bind) {
      u.bind = [];
    }
    return u;
  }
}