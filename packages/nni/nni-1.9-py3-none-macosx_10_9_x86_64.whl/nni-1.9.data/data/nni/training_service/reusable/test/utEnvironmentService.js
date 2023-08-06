"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const environment_1 = require("../environment");
const utCommandChannel_1 = require("./utCommandChannel");
class UtEnvironmentService extends environment_1.EnvironmentService {
    constructor() {
        super();
        this.allEnvironments = new Map();
        this.hasMoreEnvironmentsInternal = true;
    }
    get hasStorageService() {
        return false;
    }
    get environmentMaintenceLoopInterval() {
        return 1;
    }
    testSetEnvironmentStatus(environment, newStatus) {
        environment.status = newStatus;
    }
    testReset() {
        this.allEnvironments.clear();
    }
    testGetEnvironments() {
        return this.allEnvironments;
    }
    testGetCommandChannel() {
        if (this.commandChannel === undefined) {
            throw new Error(`command channel shouldn't be undefined.`);
        }
        return this.commandChannel;
    }
    testSetNoMoreEnvironment(hasMore) {
        this.hasMoreEnvironmentsInternal = hasMore;
    }
    get hasMoreEnvironments() {
        return this.hasMoreEnvironmentsInternal;
    }
    createCommandChannel(commandEmitter) {
        this.commandChannel = new utCommandChannel_1.UtCommandChannel(commandEmitter);
        return this.commandChannel;
    }
    async config(_key, _value) {
    }
    async refreshEnvironmentsStatus(environments) {
    }
    async startEnvironment(environment) {
        if (!this.allEnvironments.has(environment.id)) {
            this.allEnvironments.set(environment.id, environment);
            environment.status = "WAITING";
        }
    }
    async stopEnvironment(environment) {
        environment.status = "USER_CANCELED";
    }
}
exports.UtEnvironmentService = UtEnvironmentService;
