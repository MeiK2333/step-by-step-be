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

export interface Context {
  user?: { id: number }
}

TypeORM.useContainer(Container);

async function bootstrap() {
  const connection = await createConnection();
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