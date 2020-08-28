import { User } from '../entities/users';
import { InjectRepository } from 'typeorm-typedi-extensions';
import { Resolver, Mutation, Query, Arg, Ctx } from 'type-graphql';
import { Repository } from 'typeorm';
import { UserInput } from './types/user-input';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { AuthenticationError, ValidationError } from 'apollo-server';
import { Context } from '..';
import { Bind } from '../entities/bind';
import { BindInput } from './types/bind-input';
import { ojs } from '../ojs';
import { Source } from '../entities/source';

@Resolver(of => User)
export class UserResolver {
  constructor(
    @InjectRepository(User) private readonly userRepository: Repository<User>,
    @InjectRepository(Bind) private readonly bindRepository: Repository<Bind>,
    @InjectRepository(Source) private readonly sourceRepository: Repository<Source>
  ) { }

  @Mutation(returns => Bind)
  async bindSource(@Arg('account') account: BindInput, @Ctx() ctx: Context) {
    let source = await this.sourceRepository.findOne(account.sourceId);
    // TODO: 验证账号所有权 or 管理员可绑定
    const b = await this.bindRepository.findOne({ username: account.username, source });
    if (b) {
      return b;
    }
    const user = await this.me(ctx);
    // 如果多次绑定，则前面的自动解绑，仅最后一个用户可以绑定
    let bind = await this.bindRepository.findOne({ source, username: account.username });
    if (bind) {
      bind.user = user;
    } else {
      bind = this.bindRepository.create({
        user,
        source,
        username: account.username,
        solutions: [],
      });
    }
    await this.bindRepository.save(bind);
    return bind;
  }

  @Query(returns => User)
  async me(@Ctx() { user }: Context) {
    if (!user) {
      throw new AuthenticationError('not logged in');
    }
    const u = await this.userRepository.findOne(user.id);
    if (!u) {
      throw new AuthenticationError(`user not found`);
    }
    return u;
  }
}