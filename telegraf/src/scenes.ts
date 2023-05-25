import { Scenes } from "telegraf";
import { signIn, signUp } from "./database";

declare module "telegraf" {
    export interface Context {
        wizard: {
            state: {
                username?: string;
                password?: string;
            };
        };
    }
}

export const signInScene = new Scenes.WizardScene(
    "signIn",
    async ctx => {
        await ctx.reply("Введите имя пользователя");
        ctx.wizard.next();
    },
    async ctx => {
        // @ts-ignore
        ctx.wizard.state.username = ctx.message.text;
        await ctx.reply("Теперь введите пароль");
        ctx.wizard.next();
    },
    async ctx => {
        // @ts-ignore
        ctx.wizard.state.password = ctx.message.text;
        if (await signIn(ctx.wizard.state.username, ctx.wizard.state.password)) {
            ctx.reply(`Здравствуйте, ${ctx.wizard.state.username}, Вы успешно вошли в аккаунт`)
        } else {
            ctx.reply("Имя пользователя или пароль неверные, попробуйте еще раз или /leave закройте окно входа");
        };
        ctx.scene.leave();
    }
);

export const signUpScene = new Scenes.WizardScene(
    "signUp",
    async ctx => {
        await ctx.reply("Введите имя пользователя");
        ctx.wizard.next();
    },
    async ctx => {
        // @ts-ignore
        ctx.wizard.state.username = ctx.message.text;
        await ctx.reply("Теперь введите пароль");
        ctx.wizard.next();
    },
    async ctx => {
        // @ts-ignore
        ctx.wizard.state.password = ctx.message.text
        if (await signUp(ctx.wizard.state.username, ctx.wizard.state.password)) {
            ctx.reply(`Здравствуйте, ${ctx.wizard.state.username}, Вы успешно создали аккаунт`)
        } else {
            ctx.reply("Имя пользователя или пароль неверные, попробуйте еще раз или /leave закройте окно регистрации");
            ctx.wizard.selectStep(0);
        };
        ctx.scene.leave();
    }
);