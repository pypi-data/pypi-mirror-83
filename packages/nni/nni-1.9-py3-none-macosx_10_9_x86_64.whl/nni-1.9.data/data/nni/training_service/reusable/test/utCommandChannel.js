"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const ipcInterface_1 = require("../../../core/ipcInterface");
const commandChannel_1 = require("../commandChannel");
class UtRunnerConnection extends commandChannel_1.RunnerConnection {
}
class UtCommandChannel extends commandChannel_1.CommandChannel {
    constructor() {
        super(...arguments);
        this.receivedCommands = [];
    }
    get channelName() {
        return "ut";
    }
    async testSendCommandToTrialDispatcher(environment, commandType, commandData) {
        const content = ipcInterface_1.encodeCommand(commandType, JSON.stringify(commandData));
        this.log.debug(`UtCommandChannel: env ${environment.id} send test command ${content}`);
        this.handleCommand(environment, content.toString("utf8"));
    }
    async testReceiveCommandFromTrialDispatcher() {
        return this.receivedCommands.shift();
    }
    async config(_key, value) {
    }
    async start() {
    }
    async stop() {
    }
    async run() {
    }
    async sendCommandInternal(environment, message) {
        const parsedCommands = this.parseCommands(message);
        for (const parsedCommand of parsedCommands) {
            const command = new commandChannel_1.Command(environment, parsedCommand[0], parsedCommand[1]);
            this.receivedCommands.push(command);
        }
    }
    createRunnerConnection(environment) {
        return new UtRunnerConnection(environment);
    }
}
exports.UtCommandChannel = UtCommandChannel;
