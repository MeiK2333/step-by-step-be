import 'reflect-metadata';
import * as TypeORM from 'typeorm';
import { ApolloServer, AuthenticationError } from 'apollo-server-express';
import express from 'express';
import { buildSchema } from 'type-graphql';
import jwt from 'jsonwebtoken';
import { Container } from 'typedi';
import { UserResolver } from './resolvers/user';
import { OjResolver } from './resolvers/oj';
import { sdutProblemSpider, vjudgeProblemSpider, pojProblemSpider, vjudgeSolutionSpider, pojSolutionSpider, sdutSolutionSpider } from './cron';
import { init } from './init';
import Axios from 'axios';
import { User } from './entities/users';

export interface Context {
  user?: { id: number }
}

TypeORM.useContainer(Container);

async function bootstrap() {
  await init();
  const schema = await buildSchema({
    resolvers: [UserResolver, OjResolver],
    container: Container,
    validate: false
  });
  const server = new ApolloServer({
    schema,
    subscriptions: false,
    debug: process.env.DEBUG == 'true',
    context: ({ req }): Context => {
      const token = req.headers.authorization || '';
      let user = null;
      if (!token) {
        return {};
      }
      try {
        user = jwt.verify(token, process.env.JWT_SECRET || 'random_str') as { id: number };
      } catch (e) {
        throw new AuthenticationError('authorization token error');
      }
      return { user };
    }
  });
  const app = express();

  // 通过 GitHub OAUTH 登录
  app.get('/login', async (req, resp) => {
    const code = req.query.code;
    const { data } = await Axios.post('https://github.com/login/oauth/access_token', {
      client_id: process.env.client_id,
      client_secret: process.env.client_secret,
      code
    });
    const reg = /access_token=(.*?)&/g.exec(data);
    if (!reg) {
      resp.status(403).json({ code: 403, msg: '登录失败' });
      return;
    }
    const access_token = reg[1];
    const user_resp = await Axios.get('https://api.github.com/user', {
      headers: {
        Authorization: `token ${access_token}`
      }
    });
    const connection = TypeORM.getConnection();
    let user = await connection.getRepository(User).findOne({ username: user_resp.data.login });
    if (!user) {
      // 如果没有这个用户，则创建
      user = connection.getRepository(User).create({
        username: user_resp.data.login,
        nickname: user_resp.data.name,
      });
      await connection.manager.save(user);
    }
    resp.json({
      authorization: jwt.sign(
        { id: user.id },
        process.env.JWT_SECRET || 'random_str',
        { expiresIn: '365d' }
      )
    });
  })

  server.applyMiddleware({ app });
  app.listen(4000);
}

bootstrap();

sdutProblemSpider.start();
sdutSolutionSpider.start()
vjudgeProblemSpider.start();
vjudgeSolutionSpider.start();
pojProblemSpider.start();
pojSolutionSpider.start();
