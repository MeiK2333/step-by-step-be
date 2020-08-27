import 'reflect-metadata';
require('dotenv').config();
import { createConnection } from 'typeorm';
import * as TypeORM from 'typeorm';
import { ApolloServer, AuthenticationError } from 'apollo-server';
import { buildSchema } from 'type-graphql';
import jwt from 'jsonwebtoken';
import { Container } from 'typedi';
import { UserResolver } from './resolvers/user';
import { OjResolver } from './resolvers/oj';
import { sdutProblemSpider, vjudgeProblemSpider } from './cron';
import { ojs } from './ojs';
import { Source } from './entities/source';
import { SDUTSpider } from './spider/sdut';

export interface Context {
  user?: { id: number }
}

TypeORM.useContainer(Container);

async function bootstrap() {
  const connection = await createConnection();
  for (const oj of ojs) {
    const o = await connection.getRepository(Source).findOne({name: oj});
    if (!o) {
      const o = new Source();
      o.name = oj;
      await connection.manager.save(o);
    }
  }
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
        user = jwt.verify(token, process.env.JWT_SECRET || '') as { id: number };
      } catch (e) {
        throw new AuthenticationError('authorization token error');
      }
      return { user };
    }
  });
  await server.listen(4000);
}

bootstrap();

sdutProblemSpider.start();
vjudgeProblemSpider.start();