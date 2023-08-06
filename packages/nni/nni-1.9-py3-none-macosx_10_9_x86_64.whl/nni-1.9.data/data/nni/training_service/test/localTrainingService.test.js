'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const chai = require("chai");
const chaiAsPromised = require("chai-as-promised");
const fs = require("fs");
const path = require("path");
const tmp = require("tmp");
const component = require("../../common/component");
const utils_1 = require("../../common/utils");
const trialConfigMetadataKey_1 = require("../common/trialConfigMetadataKey");
const localTrainingService_1 = require("../local/localTrainingService");
const localCodeDir = tmp.dirSync().name.split('\\').join('\\\\');
const mockedTrialPath = './training_service/test/mockedTrial.py';
fs.copyFileSync(mockedTrialPath, localCodeDir + '/mockedTrial.py');
describe('Unit Test for LocalTrainingService', () => {
    let trialConfig = `{"command":"sleep 1h && echo hello","codeDir":"${localCodeDir}","gpuNum":1}`;
    let localTrainingService;
    before(() => {
        chai.should();
        chai.use(chaiAsPromised);
        utils_1.prepareUnitTest();
    });
    after(() => {
        utils_1.cleanupUnitTest();
    });
    beforeEach(() => {
        localTrainingService = component.get(localTrainingService_1.LocalTrainingService);
        localTrainingService.run();
    });
    afterEach(() => {
        localTrainingService.cleanUp();
    });
    it('List empty trial jobs', async () => {
        chai.expect(await localTrainingService.listTrialJobs()).to.be.empty;
    });
    it('setClusterMetadata and getClusterMetadata', async () => {
        await localTrainingService.setClusterMetadata(trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG, trialConfig);
        localTrainingService.getClusterMetadata(trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG).then((data) => {
            chai.expect(data).to.be.equals(trialConfig);
        });
    });
    it('Submit job and Cancel job', async () => {
        await localTrainingService.setClusterMetadata(trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG, trialConfig);
        const form = {
            sequenceId: 0,
            hyperParameters: {
                value: 'mock hyperparameters',
                index: 0
            }
        };
        const jobDetail = await localTrainingService.submitTrialJob(form);
        chai.expect(jobDetail.status).to.be.equals('WAITING');
        await localTrainingService.cancelTrialJob(jobDetail.id);
        chai.expect(jobDetail.status).to.be.equals('USER_CANCELED');
    }).timeout(20000);
    it('Get trial log', async () => {
        await localTrainingService.setClusterMetadata(trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG, trialConfig);
        const form = {
            sequenceId: 0,
            hyperParameters: {
                value: 'mock hyperparameters',
                index: 0
            }
        };
        const jobDetail = await localTrainingService.submitTrialJob(form);
        const rootDir = utils_1.getExperimentRootDir();
        fs.mkdirSync(path.join(rootDir, 'trials'));
        fs.mkdirSync(jobDetail.workingDirectory);
        fs.writeFileSync(path.join(jobDetail.workingDirectory, 'trial.log'), 'trial log');
        fs.writeFileSync(path.join(jobDetail.workingDirectory, 'stderr'), 'trial stderr');
        chai.expect(await localTrainingService.getTrialLog(jobDetail.id, 'TRIAL_LOG')).to.be.equals('trial log');
        chai.expect(await localTrainingService.getTrialLog(jobDetail.id, 'TRIAL_ERROR')).to.be.equals('trial stderr');
        fs.unlinkSync(path.join(jobDetail.workingDirectory, 'trial.log'));
        fs.unlinkSync(path.join(jobDetail.workingDirectory, 'stderr'));
        fs.rmdirSync(jobDetail.workingDirectory);
        fs.rmdirSync(path.join(rootDir, 'trials'));
        await localTrainingService.cancelTrialJob(jobDetail.id);
    }).timeout(20000);
    it('Read metrics, Add listener, and remove listener', async () => {
        const trialConfig = `{\"command\":\"python3 mockedTrial.py\", \"codeDir\":\"${localCodeDir}\",\"gpuNum\":0}`;
        await localTrainingService.setClusterMetadata(trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG, trialConfig);
        const form = {
            sequenceId: 0,
            hyperParameters: {
                value: 'mock hyperparameters',
                index: 0
            }
        };
        const jobDetail = await localTrainingService.submitTrialJob(form);
        chai.expect(jobDetail.status).to.be.equals('WAITING');
        localTrainingService.listTrialJobs().then((jobList) => {
            chai.expect(jobList.length).to.be.equals(1);
        });
        const listener1 = function f1(metric) {
            chai.expect(metric.id).to.be.equals(jobDetail.id);
        };
        localTrainingService.addTrialJobMetricListener(listener1);
        await utils_1.delay(1000);
        await localTrainingService.cancelTrialJob(jobDetail.id);
        localTrainingService.removeTrialJobMetricListener(listener1);
    }).timeout(20000);
    it('Test multiphaseSupported', () => {
        chai.expect(localTrainingService.isMultiPhaseJobSupported).to.be.equals(true);
    });
});
