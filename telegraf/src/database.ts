import * as mysql from "mysql2";
import * as dotenv from "dotenv";
import { createHash } from "crypto";
dotenv.config();

const connection = mysql.createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    database: process.env.DB_NAME,
    password: process.env.DB_PASSWORD,
});

export async function signIn(username: string | undefined, password: string | undefined): Promise<boolean> {
    return new Promise<boolean>((resolve, reject) => {        
        connection.query("SELECT password FROM users WHERE username = SHA1(?)",
        [username], 
        (err, results) => {
            if (err) {
                console.log(err);
                reject(err)
            };

            // @ts-ignore
            if (results.length > 0) {
                // @ts-ignore
                const hashedPasswordDB = results[0].password.toString("utf8");
                const hashedPasswordInput = createHash("sha1").update(password ?? "", "utf8").digest("hex");
                resolve(hashedPasswordDB === hashedPasswordInput);
            } else {
                resolve(false);
            }
        });
    })
};

export async function signUp(username: string | undefined, password: string | undefined): Promise<boolean> {
    return new Promise<boolean>((resolve, reject) => {

        connection.query("INSERT INTO users (username, password) VALUES (SHA1(?), SHA1(?))",
        [username, password],
        (err, result) => {
            if (err) {
                console.log(err);
                reject(err);
            };
            // @ts-ignore
            if (result.serverStatus === 1) resolve(true);
        })
    })
};