import { Telegraf, Scenes, session } from "telegraf";
import { signInScene, signUpScene } from "./src/scenes";
import * as dotenv from "dotenv";
dotenv.config();

if (!process.env.BOT_TOKEN) throw new Error("Bot token is required!");

const bot = new Telegraf<Scenes.WizardContext>(process.env.BOT_TOKEN);
// @ts-ignore
const stage = new Scenes.Stage<Scenes.WizardContext>([signInScene, signUpScene])

bot.use(session())
bot.use(stage.middleware());
bot.command("signIn", (ctx) => {
    ctx.scene.enter("signIn")
});
bot.command("signUp", (ctx) => {
    ctx.scene.enter("signUp")
});
bot.command("leave", (ctx) => {
    ctx.scene.leave();
});

bot.launch();
